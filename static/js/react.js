/** @jsx React.DOM */

var Ticket = React.createClass({
  render: function() {
    return (
    	<tr>
    		<td>{this.props.ticket.sentiment}</td>
    		<td>{this.props.ticket.date}</td>
    		<td>{this.props.ticket.user_name}</td>
    		<td>{this.props.ticket.subject}</td>
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
	        <table class="table">
	        	<tr>
	        		<th>Sentiment</th>
	        		<th>Date</th>
	        		<th>Customer Name</th>
	        		<th>Subject</th>
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
	    	<div>Hello!</div>
	    	<TicketList source = {this.props.source}/>
    	</div>
    	);

  }
});

React.render(
  <InboxPage source = '/sent/api/tickets' pollInterval={2000}/>,
  document.getElementById('ticket-list')
);