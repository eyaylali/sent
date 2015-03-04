/** @jsx React.DOM */

var Ticket = React.createClass({
  render: function() {
  	var zdesk_url = ("https://sent.zendesk.com/agent/tickets/" + this.props.ticket.ticket_id);
    return (
    	<tr>
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
            url: this.props.source + "?page=" + this.state.cursor,
            dataType: 'json',
            type: 'get',
            success: function(data) {
            	console.log(data);
                this.setState({data: data.items, cursor: data.cursor});

            }.bind(this),
            error: function(xhr, status, err) {
        		console.error(this.props.source, status, err.toString());
      		}.bind(this)
        });
    },
    handlePagination: function() {
    	//FILL IN
    },
    componentDidMount: function() {
	    this.loadTicketsFromServer();
	    setInterval(this.loadCommentsFromServer, this.props.pollInterval);
	},

  	render: function() {
  		var tickets = [];
  		if (this.state.data.length > 0) {
  			this.state.data.forEach(function(t) {
				tickets.push(<Ticket ticket={t} />);
  			});
  		}
 
	    return (
	    	<div className="ticketList">
	        <h1>Tickets</h1>
	        <nav>
				<ul className="pagination">
				    <li onClick={this.handlePagination}>
				    	<a href="#" aria-label="Previous">
				        	<span aria-hidden="true">&laquo;</span>
				      	</a>
				    </li>
				    <li onClick={this.handlePagination}>
				      	<a href="#" aria-label="Next">
				        	<span aria-hidden="true">&raquo;</span>
				      	</a>
				    </li>
				</ul>
			</nav>
			Viewing 1-20 of 252
	        <table className="table">
	        	<tr>
	        		<th>Sentiment</th>
	        		<th>Customer Name</th>
	        		<th>Subject</th>
	        		<th>Date</th>
	        	</tr>
	        	{tickets}
	        </table>
	      	</div>
    );
  }
});

var InboxPage = React.createClass({
  render: function() {
    return (
    	<div className= "container">
	    	<TicketList source = {this.props.source}/>
    	</div>
    	);

  }
});

React.render(
  <InboxPage source = '/sent/api/tickets' pollInterval={2000}/>,
  document.getElementById('ticket-list')
);