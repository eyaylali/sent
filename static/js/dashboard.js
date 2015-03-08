/** @jsx React.DOM */


var SentimentGraph = React.createClass({
  componentDidMount: function() {
    this.chart = c3.generate({
      bindto: this.refs.myContainer.getDOMNode(),
    data: {
        x: 'x',
        columns: [
            ['x', '2013-01-01', '2013-01-02', '2013-01-03', '2013-01-04', '2013-01-05', '2013-01-06'],
            ['upset', 5, 20, 10, 40, 15, 25],
            ['neutral', 13, 34, 20, 50, 25, 35],
            ['positive', 13, 34, 20, 50, 25, 35]
        ]
    },
    axis: {
        x: {
            type: 'timeseries',
            tick: {
                format: '%Y-%m-%d'
            }
        },
        y: {
        label: {
          text: 'Ticket Count',
          position: 'outer-middle'
        }
      },
    }
});
  },
  updateGraph: function () {
    //ETL putting data in format I need
  },
  componentDidUpdate: function () {
    this.updateGraph()
    //call only if data changes
  },
  render: function() {
    return (
      <div ref="myContainer">
      </div>
     );
  }
});

var SentimentCounter = React.createClass({
  render: function() {
    return (
      <div className= "box" id = "counter">
        <p id="countertext">{this.props.sentimentCount.count}</p>
      </div>
      );
  }
});

var SentimentCounterList = React.createClass({
  getInitialState: function() {
    return {data: [], timePeriod: this.props.timePeriod};
  },
  loadCountsFromServer: function() {
      $.ajax({
          url: this.props.source + "?time=" + this.props.timePeriod,
          dataType: 'json',
          type: 'get',
          success: function(data) {
              this.setState({data: data.counts});
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
      this.loadCountsFromServer();
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
      <div>
      <div className="counterList">
      {counts}
      </div>
      <SentimentGraph />
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
    var timePeriod = this.state.timePeriod;
    return (
      <div className= "container">
      <ul className="nav nav-tabs">
        <li onClick={this.handleTimeChange.bind(null,"today")} role="presentation" 
        className={timePeriod == "today" ? "active" : null}><a href="#">Today</a></li>
        <li onClick={this.handleTimeChange.bind(null,"week")} role="presentation" className={timePeriod == "week" ? "active" : null}><a href="#">Last Week</a></li>
        <li onClick={this.handleTimeChange.bind(null,"month")} role="presentation" className={timePeriod == "month" ? "active" : null}><a href="#">Last Month</a></li>
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

