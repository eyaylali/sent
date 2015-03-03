/** @jsx React.DOM */

var Ticket = React.createClass({
  render: function() {
    return (
    	<tr>
    		<td>Sentiment</td>
    		<td>Customer Name</td>
    		<td>Subject</td>
    	</tr>
    	);
  }
});

var TicketList = React.createClass({
	
    loadTicketsFromServer: function() {
        $.ajax({
            url: this.props.source,
            dataType: 'json',
            type: 'get',
            success: function(data) {
                this.setState({data: data});
            }.bind(this),
            error: function(xhr, status, err) {
        		console.error(this.props.source, status, err.toString());
      		}.bind(this)
        });
    },
    getInitialState: function() {
    	return {data: []};
  	},
    componentDidMount: function() {
	    this.loadTicketsFromServer();
	},
  	render: function() {
	    return (
	    	<div className="ticketList">
	        <h1>Tickets</h1>
	        <Ticket data={this.state.data} />
	      	</div>
    );
  }
});


var Page = React.createClass({
  render: function() {
    return (
    	<div>
	    	<div>Hello!</div>
	    	<TicketList />
    	</div>
    	);

  }
});

React.render(
  <Page source = '/sent/api/tickets' />,
  document.getElementById('ticket-list')
);