/** @jsx React.DOM */

var Ticket = React.createClass({
  render: function() {
    return (
    	<tr>
    		<td>Sentiment</td>
    		<td>Customer Name</td>
    		<td>Subject</td>
    	);
  }
});

var TicketList = React.createClass({
  render: function() {
  	rows = [];
  	for (row in this.props.data)
    return (
    	<table><Ticket /></table>
    	);
  }
});

var Page = React.createClass({
  render: function() {
    return (
    	<div>Hello!</div>
    	<TicketList />
    	);

  }
});

React.render(
  <Page url = '/sent/api/tickets' />,
  document.getElementById('ticket-list')
);