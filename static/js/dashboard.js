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
      <div className= "box" id = "counter">
        <p>{this.props.sentimentCount.count}</p>
      </div>
      );
  }
});

var SentimentCounterList = React.createClass({
  getInitialState: function() {
    return {data: [], cursor: this.props.timePeriod};
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
  },
  componentDidUpdate: function (prevProps, prevState) {
      if (prevProps.timePeriod !== this.props.timePeriod) {
      this.loadTicketsFromServer();
    } 
    },
  render: function() {
    var counts = [];
    if (this.state.data.length > 0) {
      this.state.data.forEach(function(c) {
      counts.push(<SentimentCounter sentimentCount={c} />);
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
  getInitialState: function() {
    return {
      timePeriod: "today"
    };
  },
  handleTimeChange: function (period) {
    this.setState({timePeriod: period});
  },
  render: function() {
    return (
      <div className= "container">
      <ul className="nav nav-tabs">
        <li onClick={this.handleTimeChange.bind(null,"today")} role="presentation" className="active"><a href="#">Today</a></li>
        <li onClick={this.handleTimeChange.bind(null,"week")} role="presentation"><a href="#">Last Week</a></li>
        <li onClick={this.handleTimeChange.bind(null,"month")} role="presentation"><a href="#">Last Month</a></li>
      </ul>
      <SentimentCounterList timePeriod={this.state.timePeriod} source = {this.props.source}/>
      </div>
    	);
  }
});


React.render(
  <Dashboard source = '/sent/api/data/'/>,
  document.getElementById('analytics-dashboard')
);

