/** @jsx React.DOM */

// var Ticket = React.createClass({
//   render: function() {
//     return (
//     	<tr>
//     		<td>Sentiment</td>
//     		<td>Customer Name</td>
//     		<td>Subject</td>
//     	</tr>
//     	);
//   }
// });

// var TicketList = React.createClass({
//   render: function() {
//   	rows = [];
//     return (
//     	<table><Ticket /></table>
//     	);
//   }
// });

// var Page = React.createClass({
//   render: function() {
//     return (
//     	<div>
// 	    	<div>Hello!</div>
// 	    	<TicketList />
//     	</div>
//     	);

//   }
// });

// React.render(
//   <Page url = '/sent/api/tickets' />,
//   document.getElementById('ticket-list')
// );

var chart = c3.generate({
    bindto: '#chart',
    data: {
      columns: [
        ['data1', 30, 200, 100, 400, 150, 250],
        ['data2', 50, 20, 10, 40, 15, 25]
      ],
      axes: {
        data2: 'y2' // ADD
      }
    },
    axis: {
      y2: {
        show: true // ADD
      }
    }
});