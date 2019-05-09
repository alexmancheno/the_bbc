import React, { Component } from 'react'
import ReactDOM from 'react-dom'
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import PropTypes from 'prop-types';
import Typography from '@material-ui/core/Typography';
import SimpleLineChart from './simpleline';
import Form from './form';
import SimpleTable from './simpletable';

const styles = theme => ({
    chartContainer: {
      marginLeft: -22,
    },
    tableContainer: {
      height: 320,
    },
  });

class Custom extends Component {
    constructor(props){
      super(props)
    }
  
    render() {
      const { classes } = this.props;
      return (
        <div>
            <Typography variant="h4" gutterBottom component="h2">
                Custom
            </Typography>
            <Typography component="div" className={classes.chartContainer}>
                <SimpleLineChart prop={this.props.prop}/>
            </Typography>
            <Typography component="div" className={classes.chartContainer}>
                <Form onSubmit={this.props.onSubmit}></Form>
            </Typography>
            <Typography component="div" className={classes.chartContainer}>
                <SimpleTable prop = {this.props.prop}/>
            </Typography>
        </div>
      );
    }
  }
  
  Custom.propTypes = {
    classes: PropTypes.object.isRequired,
  };
  

  export default withStyles(styles)(Custom);