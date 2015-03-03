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
  render: function() {
  	rows = [];
    return (
    	<table><Ticket /></table>
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

// React.render(
//   <Page url = '/sent/api/tickets' />,
//   document.getElementById('ticket-list')
// );