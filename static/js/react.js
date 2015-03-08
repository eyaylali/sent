/** @jsx React.DOM */

var TicketAccordion = React.createClass({
  render: function() {
//  	var zdesk_url = ("https://sent.zendesk.com/agent/tickets/" + this.props.ticket.ticket_id);
//  	var date = moment(this.props.date)
    return (
    	<tr className="warning">
    		<td colSpan="5">{this.props.ticket.content}</td>
    	</tr>
    	);
  }
});

var Ticket = React.createClass({
	updateSentiment: function () {

	},
  	render: function() {
	  	var zdesk_url = ("https://sent.zendesk.com/agent/tickets/" + this.props.ticket.ticket_id);
	  	var date = moment(this.props.date)
	  	var ticketId = "ticket_row_" + this.props.ticket.ticket_id;
	  	var ticketAccordionId = "accordion_row_" + this.props.ticket.ticket_id;
	    return (
	    	<tr className="active" id={ticketId} >
	  			<td><input type="checkbox" checked={this.props.selected} onChange={this.props.handleTicketSelection} /></td>
	    		<td>{this.props.ticket.sentiment}</td>
	    		<td>{this.props.ticket.user_name}</td>
	    		<td onClick={this.props.handleAccordions}>{this.props.ticket.subject}</td>
	    		<td>{this.props.ticket.date}</td>
	    	</tr>
	    	);
  }
});

var TicketList = React.createClass({
  	render: function() {
  		var getHandleTicketSelection = this.props.getHandleTicketSelection;
  		var getHandleAccordions = this.props.getHandleAccordions;
  		var selections = this.props.selections;
  		var accordions = this.props.accordions;
  		var tickets = [];
  		i = 1
  		if (this.props.data.length > 0) {
  			this.props.data.forEach(function(t) {
  				var handleTicketSelection = getHandleTicketSelection(t.ticket_id);
  				var handleAccordions = getHandleAccordions(t.ticket_id);
  				var selected = selections.indexOf(t.ticket_id) !== -1;
				tickets.push(
					<Ticket 
						key = {t.ticket_id} 
						ticket={t} 
						selected = {selected} 
						handleAccordions = {handleAccordions} 
						handleTicketSelection = {handleTicketSelection} 
					/>
				);
				if (accordions.indexOf(t.ticket_id) !== -1) {
					tickets.push(
						<TicketAccordion 
							key = {t.ticket_id + "-accordion"} 
							ticket={t} 
						/>
					);
				}
  			});
  		};
  		var displayStart = ((this.props.cursor-1) * 20) + 1;
  		var displayEnd = ((this.props.cursor-1) * 20) + this.props.data.length; 
	    return (
	    	<div className="ticketList">
	        <nav>
				<ul className="pagination">
				    <li onClick={this.props.handlePaginationPrevious}>
				    	<a href="#" aria-label="Previous">
				        	<span aria-hidden="true">&laquo;</span>
				      	</a>
				    </li>
				    <li onClick={this.props.handlePaginationNext}>
				      	<a href="#" aria-label="Next">
				        	<span aria-hidden="true">&raquo;</span>
				      	</a>
				    </li>
				</ul>
			</nav>
			<p>Viewing {displayStart}-{displayEnd} of {this.props.sentimentCount}</p>
	        <table className="table table-bordered table-condensed" >
	        	<thead>
	        	<tr className="active">
	        		<th>Update?</th>
	        		<th>Sentiment</th>
	        		<th>Customer Name</th>
	        		<th>Subject</th>
	        		<th>Date</th>
	        	</tr>
	        	</thead>
	        	<tbody>
	        	{tickets}
	        	</tbody>
	        </table>
	      	</div>
    );
  }
});

var InboxPage = React.createClass({
	getInitialState: function() {
		return {
			sentimentType: this.props.sentiment,
			data: [],
			selections: [],
			cursor: 1,
			has_next_page: false,
			total_count: 0,
			accordions: [],
		};
		
	},
	getHandleAccordions: function(ticketId) {
		return function() {
			var accordions = this.state.accordions;
			var newAccordions;
			if (accordions.indexOf(ticketId) === -1) {
				newAccordions = accordions.concat(ticketId)
			} else {
				newAccordions = accordions.filter(function (entry) {
					return ticketId !== entry
				})
			}
			this.setState({
				accordions: newAccordions
			})
		}.bind(this)
	},
	getHandleTicketSelection: function(ticketId) {
		return function() {
			var selections = this.state.selections;
			var newSelections;
			if (selections.indexOf(ticketId) === -1) {
				newSelections = selections.concat(ticketId)
			} else {
				newSelections = selections.filter(function (entry) {
					return ticketId !== entry
				})
			}
			this.setState({
				selections: newSelections
			})
		}.bind(this)
	},
	loadTicketsFromServer: function() {
        $.ajax({
            url: this.props.source + this.state.sentimentType +"?page=" + this.state.cursor,
            dataType: 'json',
            type: 'get',
            success: function(data) {
                this.setState({data: data.items, cursor: data.cursor, has_next_page: data.next_page, total_count: data.total_count, sentimentCount: data.sentiment_count});
            }.bind(this),
            error: function(xhr, status, err) {
        		console.error(this.props.source, status, err.toString());
      		}.bind(this)
        });
    },
	handleSentimentStateChange: function (newSentimentType) {
		return function () {
    		this.setState({
    			sentimentType: newSentimentType
    		})
    	}.bind(this)
	},
	componentDidMount: function () {
	    this.loadTicketsFromServer()  
	},
	componentDidUpdate: function (prevProps, prevState) {
	    if (this.state.cursor !== prevState.cursor || this.state.sentimentType !== prevState.sentimentType) {
	    	this.loadTicketsFromServer();
	    }
	},
	handlePaginationPrevious: function() {
    	if (this.state.cursor > 1) {
    		this.setState({
    			cursor: this.state.cursor - 1
    		})
    	};
    },
    handlePaginationNext: function() {
    	if (this.state.has_next_page == true) {
    		this.setState({
    			cursor: this.state.cursor + 1
    		})
    	};
    },
    handleSentimentChange: function() {
    	var newSentiment = this.refs.controlSelect.getDOMNode().value;
    	$.ajax({
            url: this.props.source,
            dataType: 'json',
            type: 'post',
            data: {
            	newSentiment: newSentiment,
            	selections: this.state.selections
            },
            success: function() {
                this.loadTicketsFromServer()
            }.bind(this),
            error: function(xhr, status, err) {
        		console.error(this.props.source, status, err.toString());
      		}.bind(this)
        });
    },
  	render: function() {
    return (
    	<div className= "container">
    		<div className = "controller">
    			<select ref = "controlSelect">
    				<option value="upset">Upset</option>
    				<option value="neutral">Neutral</option>
    				<option value="positive">Positive</option>
    			</select>
    			<button onClick= {this.handleSentimentChange}>Update</button>
    		</div>
		    <ul className="list-group" className="col-md-3">
			  <li onClick={this.handleSentimentStateChange("upset")} className="list-group-item">
			    <span className="badge">{this.state.total_count[0]}</span>
			    Upset
			  </li>
			  <li onClick={this.handleSentimentStateChange("neutral")} className="list-group-item">
			    <span className="badge">{this.state.total_count[1]}</span>
			    Neutral
			  </li>
			  <li onClick={this.handleSentimentStateChange("positive")} className="list-group-item">
			    <span className="badge">{this.state.total_count[2]}</span>
			    Positive
			  </li>
			</ul>
		    <TicketList getHandleAccordions= {this.getHandleAccordions} getHandleTicketSelection= {this.getHandleTicketSelection} handlePaginationNext={this.handlePaginationNext} handlePaginationPrevious={this.handlePaginationPrevious} 
		    	{...this.state} />
    	</div>
    	);

  }
});
var sentiment = $("#ticket-list").attr("data-sentiment");
React.render(
  <InboxPage sentiment = {sentiment} source = '/sent/api/tickets/' />,
  document.getElementById('ticket-list')
);