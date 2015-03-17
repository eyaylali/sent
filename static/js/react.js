/** @jsx React.DOM */

var TicketAccordion = React.createClass({
  render: function() {
    return (
    	<tr className="open-message">
    		<td colSpan="6">
    		<p id= "message-title" className="message-body">Message Body:</p>
    		<p className="message-body">{this.props.ticket.content}</p>

    		</td>
    	</tr>
    	);
  }
});

var Ticket = React.createClass({
  	render: function() {
	  	var zdesk_url = ("https://sent.zendesk.com/agent/tickets/" + this.props.ticket.ticket_id);
	  	var ticketId = "ticket_row_" + this.props.ticket.ticket_id;
	  	var ticketAccordionId = "accordion_row_" + this.props.ticket.ticket_id;
	  	var subjectLength = this.props.ticket.subject.length;
	  	if (subjectLength <= 60) {
	  		var subject = this.props.ticket.subject;
	  	} else {
	  		var subject = this.props.ticket.subject.slice(0,60) + "... ";
	  	};
	  	if (this.props.ticket.today) {
	  		var date = moment(this.props.ticket.date).format("h:mm a")
	  	} else {
	  		var date = moment(this.props.ticket.date).format("M/DD")
	  	};
	  	if (this.props.ticket.sentiment === "upset") {
	  		ticketColor = "danger";
	  	} else {
	  		ticketColor = "active";
	  	};
	  	if (this.props.ticket.source == "twitter" || this.props.ticket.source == "facebook") {
	  		var toExistOrNot = "label label-primary";
	  		var label = "public"
	  	} else {
	  		var toExistOrNot = "";
	  		var label = ""
	  	};
	    return (
	    	<tr className={ticketColor} id={ticketId}>
	  			<td className="centerElement"><input type="checkbox" checked={this.props.selected} onChange={this.props.handleTicketSelection} /></td>
	    		<td className="centerElement">{this.props.ticket.sentiment}</td>
	    		<td>{this.props.ticket.user_name}</td>
	    		<td onClick={this.props.handleAccordions}>{subject} <span className={toExistOrNot}>{label}</span></td>
	    		<td className="centerElement">{date}</td>
	    		<td className="centerElement"><a target="_blank" href= {zdesk_url}><span className="glyphicon glyphicon-send" aria-hidden="true"></span></a></td>
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
  		var displayTotal;
  		if (this.props.sentimentType === "all") {
  			displayTotal = this.props.total_count[0] + this.props.total_count[1] + this.props.total_count[2];
  		} else {
  			displayTotal = this.props.sentimentCount;
  		};
	    return (
	    	<div className="ticket-list" >
		    	<div className="row" id="pagination">
		    		<p className="num-display col-md-2 col-md-offset-7">Viewing {displayStart}-{displayEnd} of {displayTotal}</p>
		    		<div className="pagination-arrows col-md-2">
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
					</div>
				</div>
		        <table id="ticket-table" className="table table-striped table-hover" >
		        	<thead>
		        	<tr className="active">
		        		<th className="centerElement" id="ticket-update">Update?</th>
		        		<th className="centerElement" id="ticket-sentiment">Sentiment</th>
		        		<th id="ticket-name">Customer Name</th>
		        		<th id="ticket-subject">Subject</th>
		        		<th className="centerElement" id="ticket-date">Date</th>
		        		<th className="centerElement" id="ticket-reply">Reply</th>
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
		 if (this.props.sentiment === "positive") {
			var highlightedPositive = " active";
		} else if (this.props.sentiment === "upset") {
			var highlightedUpset = " active";
		} else if (this.props.sentiment === "neutral") {
			var highlightedNeutral = " active";
		} else if (this.props.sentiment === "all") {
			var highlightedAll = " active";
		} else {
			highlighted = ""
		};
		return {
			sentimentType: this.props.sentiment,
			data: [],
			selections: [],
			cursor: 1,
			has_next_page: false,
			total_count: 0,
			accordions: [],
			classListPositive: highlightedPositive,
			classListNeutral: highlightedNeutral,
			classListUpset: highlightedUpset,
			classListAll: highlightedAll
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
        console.dir(this.state);
        $.ajax({
            url: this.props.source + this.state.sentimentType +"?page=" + this.state.cursor,
            dataType: 'json',
            type: 'get',
            success: function(data) {
				var state = {
					data: data.items, 
					cursor: data.cursor, 
					has_next_page: data.next_page, 
					total_count: data.total_count, 
					sentimentCount: data.sentiment_count,
				};
                this.setState(state);
            }.bind(this),
            error: function(xhr, status, err) {
        		console.error(this.props.source, status, err.toString());
      		}.bind(this)
        });
    },
	handleSentimentStateChange: function (newSentimentType) {
		var state = {
				sentimentType: newSentimentType,
    			cursor: 1
    		};
		if (newSentimentType === "positive") {
			state.classListPositive = " active";
			state.classListUpset = "";
			state.classListNeutral = "";
			state.classListAll = "";
		} else if (newSentimentType === "upset") {
			state.classListPositive = "";
			state.classListUpset = " active";
			state.classListNeutral = "";
			state.classListAll = "";
		} else if (newSentimentType === "neutral") {
			state.classListPositive = "";
			state.classListUpset = "";
			state.classListNeutral = " active";
			state.classListAll = "";
		} else if (newSentimentType === "all") {
			state.classListPositive = "";
			state.classListUpset = "";
			state.classListNeutral = "";
			state.classListAll = " active";
		};
		return function () {
    		this.setState(state)
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
    handleSentimentChange: function(newSentiment) {
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
  		var grandTotal = this.state.total_count[0] + this.state.total_count[1] + this.state.total_count[2];
  		var allClass = this.state.classListAll + " list-group-item";
  		var upsetClass = this.state.classListUpset + " list-group-item";
  		var positiveClass = this.state.classListPositive + " list-group-item";
  		var neutralClass = this.state.classListNeutral + " list-group-item";
    return (
    	<div className= "container">
    		<div className = "row">
    		
			    <ul className="list-group" className="col-md-3 inbox-nav">
			    	<li onClick={this.handleSentimentStateChange("all")} href="#" className={allClass}>
				    	<span className="badge">{grandTotal}</span>
				    All
				  	</li>
				  	<li href="#" onClick={this.handleSentimentStateChange("upset")} className={upsetClass}>
				    	<span className="badge">{this.state.total_count[0]}</span>
				    Upset
				  	</li>
				  	<li href="#" onClick={this.handleSentimentStateChange("neutral")} className={neutralClass}>
				    	<span className="badge">{this.state.total_count[1]}</span>
				    Neutral
				  	</li>
				  	<li href="#" onClick={this.handleSentimentStateChange("positive")} className={positiveClass}>
				    	<span className="badge">{this.state.total_count[2]}</span>
				    Positive
				  	</li>
				</ul>
				<div className="col-md-9 messages">
					<div className = "controller">
					    <div className="btn-group">
					      <a className="btn btn-default btn-sm">Update</a>
					      <a href="#" className="btn btn-default dropdown-toggle btn-sm" data-toggle="dropdown" aria-expanded="false"><span className="caret"></span></a>
					      <ul className="dropdown-menu">
					        <li><a href="#" onClick= {this.handleSentimentChange.bind(this, 'upset')}>Upset</a></li>
					          <li><a href="#" onClick= {this.handleSentimentChange.bind(this, 'neutral')}>Neutral</a></li>
					        <li><a href="#" onClick= {this.handleSentimentChange.bind(this, 'positive')}>Positive</a></li>
					      </ul>
					    </div>
					</div>	
				    <TicketList getHandleAccordions= {this.getHandleAccordions} getHandleTicketSelection= {this.getHandleTicketSelection} handlePaginationNext={this.handlePaginationNext} handlePaginationPrevious={this.handlePaginationPrevious} 
				    	{...this.state} />
			    </div>	
		    </div>
    	</div>
    	);
  }
});

var sentiment = $("#ticket-list").attr("data-sentiment");
React.render(
  <InboxPage sentiment = {sentiment} source = '/sent/api/tickets/' />,
  document.getElementById('ticket-list')
);