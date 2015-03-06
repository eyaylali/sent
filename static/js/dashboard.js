/** @jsx React.DOM */


// var SentimentGraph = React.createClass({
//   render: function() {
//     return (
      
//      );
//   }
// });

var SentimentCounter = React.createClass({
  render: function() {
    return (
      <div className= "counter">
      {this.props.count}
      </div>
      );
  }
});

var SentimentCounterList = React.createClass({
  getInitialState: function() {
    return {data: [], cursor: "today"};
  },
  loadCountsFromServer: function() {
      $.ajax({
          url: this.props.source + "?time=" + this.state.cursor,
          dataType: 'json',
          type: 'get',
          success: function(data) {
            console.log(data);
              this.setState({data: data.counts, cursor: data.cursor});
          }.bind(this),
          error: function(xhr, status, err) {
          console.error(this.props.source, status, err.toString());
        }.bind(this)
      });
  },
  componentDidMount: function() {
    this.loadCountsFromServer();
    setInterval(this.loadCountsFromServer, this.props.pollInterval);
  },
  render: function() {
    var counts = [];
    console.log(this.state.data.length)
    if (this.state.data.length > 0) {
      this.state.data.forEach(function(c) {
      counts.push(<SentimentCounter count={c} />);
      });
    };
    return (
      <div className="counterList">
      {counts}
      </div>
    );
  }
});















var Dashboard = React.createClass({
  render: function() {
    return (
      <div className= "container">
      <div className="dropdown">
        <button className="btn btn-default dropdown-toggle" type="button" id="dropdownMenu1" data-toggle="dropdown" aria-expanded="true">
        Date Range <span className="caret"></span>
        </button>
        <ul className="dropdown-menu" role="menu" aria-labelledby="dropdownMenu1">
          <li role="presentation"><a role="menuitem" tabIndex="-1" href="#">Today</a></li>
          <li role="presentation"><a role="menuitem" tabIndex="-1" href="#">This Week</a></li>
          <li role="presentation"><a role="menuitem" tabIndex="-1" href="#">This Month</a></li>
        </ul>
      </div>
      <SentimentCounterList source = {this.props.source}/>
      </div>
    	);
  }
});



React.render(
  <Dashboard source = '/sent/api/tickets/' />,
  document.getElementById('analytics-dashboard')
);

