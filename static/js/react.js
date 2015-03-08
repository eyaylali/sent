/** @jsx React.DOM */

var TicketAccordion = React.createClass({
  render: function() {
//  	var zdesk_url = ("https://sent.zendesk.com/agent/tickets/" + this.props.ticket.ticket_id);
//  	var date = moment(this.props.date)
  	var ticketId = "accordion_row_" + this.props.ticket.ticket_id;
	var divStyle = {
	  color: 'black',
	  display: 'none'
	};
    return (
    	<tr style={divStyle} className="warning" id={ticketId}>
    		<td colSpan="4">{this.props.ticket.content}</td>
    	</tr>
    	);
  }
});

var Ticket = React.createClass({
	showHideAccordion: function () {
		$('#accordion_row_' + this.props.ticket.ticket_id).toggle();
	},
	updateSentiment: function () {

	},
	// $.get('/changeSentiment', funtion(){
	// 	this.props.updateMe();
	// })
  	render: function() {
	  	var zdesk_url = ("https://sent.zendesk.com/agent/tickets/" + this.props.ticket.ticket_id);
	  	var date = moment(this.props.date)
	  	var ticketId = "ticket_row_" + this.props.ticket.ticket_id;
	  	var ticketAccordionId = "accordion_row_" + this.props.ticket.ticket_id;
	    return (
	    	<tr className="active" id={ticketId} onClick={this.showHideAccordion}>
	    		<td>{this.props.ticket.sentiment}</td>
	    		<td>{this.props.ticket.user_name}</td>
	    		<td>{this.props.ticket.subject}</td>
	    		<td>{this.props.ticket.date}</td>
	    	</tr>
	    	);
  }
});

var TicketList = React.createClass({
	getInitialState: function() {
    	return {data: [], cursor: "1"};
  	},
    loadTicketsFromServer: function() {
        $.ajax({
            url: this.props.source + this.props.sentimentType +"?page=" + this.state.cursor,
            dataType: 'json',
            type: 'get',
            success: function(data) {
                this.setState({data: data.items, cursor: data.cursor, next_page: data.next_page, total_count: data.total_count});
            }.bind(this),
            error: function(xhr, status, err) {
        		console.error(this.props.source, status, err.toString());
      		}.bind(this)
        });
    },
    handlePaginationPrevious: function() {
    	if (this.state.cursor > 1) {
    		this.state.cursor--;
    		this.loadTicketsFromServer()};
    },
    handlePaginationNext: function() {
    	if (this.state.next_page == 1) {
    	this.state.cursor++;
    	this.loadTicketsFromServer()};
    },
    componentDidMount: function() {
	    this.loadTicketsFromServer();
  	},
  	componentDidUpdate: function (prevProps, prevState) {
  	     if (prevProps.sentimentType !== this.props.sentimentType) {
			this.loadTicketsFromServer();
		} 
  	},
  	render: function() {
  		var tickets = [];
  		i = 1
  		if (this.state.data.length > 0) {
  			this.state.data.forEach(function(t) {
				tickets.push(<Ticket key = {i++} ticket={t} />);
				tickets.push(<TicketAccordion key = {i++} ticket={t} />);
  			});
  		};
  		var display_start = ((this.state.cursor-1) * 20) + 1;
  		var display_end = ((this.state.cursor-1) * 20) + this.state.data.length;
	    return (
	    	<div className="ticketList">
	        <nav>
				<ul className="pagination">
				    <li onClick={this.handlePaginationPrevious}>
				    	<a href="#" aria-label="Previous">
				        	<span aria-hidden="true">&laquo;</span>
				      	</a>
				    </li>
				    <li onClick={this.handlePaginationNext}>
				      	<a href="#" aria-label="Next">
				        	<span aria-hidden="true">&raquo;</span>
				      	</a>
				    </li>
				</ul>
			</nav>
			<p>Viewing {display_start}-{display_end} of {this.state.total_count}</p>
	        <table className="table table-bordered table-condensed" >
	        	<thead>
	        	<tr className="active">
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
			sentimentType: this.props.sentiment
		};
		
	},
	handleSentimentStateChange: function (newSentiment) {
		this.setState({sentimentType: newSentiment});
	},
  	render: function() {
    return (
    	<div className= "container">
		    <ul className="list-group" className="col-md-3">
			  <li onClick={this.handleSentimentStateChange.bind(null,"upset")} className="list-group-item">
			    <span className="badge">#</span>
			    Upset
			  </li>
			  <li onClick={this.handleSentimentStateChange.bind(null,"neutral")} className="list-group-item">
			    <span className="badge">#</span>
			    Neutral
			  </li>
			  <li onClick={this.handleSentimentStateChange.bind(null,"positive")} className="list-group-item">
			    <span className="badge">#</span>
			    Positive
			  </li>
			</ul>
		    <TicketList sentimentType={this.state.sentimentType} source = {this.props.source}/>
    	</div>
    	);

  }
});
var sentiment = $("#ticket-list").attr("data-sentiment");
React.render(
  <InboxPage sentiment = {sentiment} source = '/sent/api/tickets/' />,
  document.getElementById('ticket-list')
);