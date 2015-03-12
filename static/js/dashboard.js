/** @jsx React.DOM */

var PieGraph = React.createClass({
  componentDidMount: function() {
    this.chart = c3.generate({
      bindto: this.refs.myPie.getDOMNode(),
    data: {
        columns: [],
        type : 'donut',
    },
    donut: {
        title: "Source"
    }
  });
  },
  updatePie: function () {
    this.chart.load({
    columns: this.props.chartData[this.props.sentimentType],
    });
  },
  componentDidUpdate: function (prevProps) {
      if (prevProps.chartData !== this.props.chartData || prevProps.sentimentType !== this.props.sentimentType) {
        this.updatePie()
        console.log("data changed!");
      }
  },
  render: function() {
    return (
      <div ref="myPie"></div>
     );
  }
});

var SentimentGraph = React.createClass({
  getInitialState: function() {
    return {
    sentimentType: "total"
    }
  },
  componentDidMount: function() {
    this.chart = c3.generate({
      bindto: this.refs.myContainer.getDOMNode(),
    data: {
        x: 'x',
        xFormat: "%Y-%m-%d %H:%M:%S",
        columns: this.props.columns,
        onclick: function (d) { this.handleSeriesClick(d.id) }.bind(this),
    },
    axis: {
        x: {
            type: 'timeseries',
            tick: {
                format: this.getFormatDisplay()
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
  handleSeriesClick: function(seriesId) {
    var newSentimentType;
    if (this.state.sentimentType === seriesId) {
      newSentimentType = "total";
    } else {
      newSentimentType = seriesId;
    }
    this.setState({sentimentType:newSentimentType});
  },
  updateGraph: function () {
    this.chart.load({
    columns: this.props.columns,
    format: this.getFormatDisplay()
    });
  },
  getFormatDisplay: function () {
    if (this.props.timePeriod !== "today") {
      var formatDisplay = '%Y-%m-%d';
    } else {
      var formatDisplay = '%H:%M';
    };
  },
  componentDidUpdate: function (prevProps, prevState) {
      if (prevProps.columns !== this.props.columns) {
      this.updateGraph();
    } 
  },
  render: function() {
    return (
      <div>
      <div ref="myContainer"></div>
      <PieGraph chartData={this.props.sourceData} sentimentType = {this.state.sentimentType}/>
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
    return {data: [], timePeriod: this.props.timePeriod, columns: []};
  },
  loadCountsFromServer: function() {
      $.ajax({
          url: this.props.source + "?time=" + this.props.timePeriod,
          dataType: 'json',
          type: 'get',
          success: function(data) {
              this.setState({data: data.counts, timePeriod : data.time_period, columns : data.columns, sourceData : data.source_data, customerData : data.customer_data});
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
      counts.push(<SentimentCounter key={c.label} sentimentCount={c} />);
      });
    };
    return (
      <div>
      <div className="counterList">
      {counts}
      </div>
      <SentimentGraph {...this.state}/>
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
      <SentimentCounterList {...this.state} source = {this.props.source}/>
      </div>
    	);
  }
});


React.render(
  <Dashboard source = '/sent/api/data/'/>,
  document.getElementById('analytics-dashboard')
);

