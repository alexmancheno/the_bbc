import React, { Component } from 'react';
import Typography from '@material-ui/core/Typography';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableHead from '@material-ui/core/TableHead';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

const styles = {
  root: {
    width: '100%',
    overflowX: 'auto',
  },
  table: {
    minWidth: 700,
  },
};

class Dash extends Component{
		constructor(props) {
			super(props);
		};
		
    render(){
			const { classes } = this.props;
      return(
				<div>
					<Typography variant="h4" gutterBottom component="h2">
					Linear Regression Engine for Mortgage Rates
          </Typography>
					<Paper className={classes.root}>
						<Table className={classes.table}>
							<TableHead>
								<TableRow>
									<TableCell >Symbols</TableCell>
									<TableCell >Independent Variables</TableCell>
								</TableRow>
							</TableHead>
							<TableBody>
								<TableRow key={1}>
									<TableCell component="th" scope="row">CPI</TableCell>
									<TableCell  component="th" scope="row">Consumer Price Index</TableCell>
								</TableRow>
								<TableRow key={2}>
									<TableCell component="th" scope="row">CPIHA</TableCell>
									<TableCell  component="th" scope="row">Consumer Price Index Housing Average</TableCell>
								</TableRow>
								<TableRow key={3}>
									<TableCell component="th" scope="row">DJI</TableCell>
									<TableCell  component="th" scope="row">Dow Jones Index</TableCell>
								</TableRow>
								<TableRow key={4}>
									<TableCell component="th" scope="row">FIR</TableCell>
									<TableCell  component="th" scope="row">Federal Interest Rates</TableCell>
								</TableRow>
								<TableRow key={5}>
									<TableCell component="th" scope="row">GDP</TableCell>
									<TableCell  component="th" scope="row">Gross Domestic Product</TableCell>
								</TableRow>
								<TableRow key={6}>
									<TableCell component="th" scope="row">GSPC</TableCell>
									<TableCell  component="th" scope="row">S&P 500 Index</TableCell>
								</TableRow>
								<TableRow key={7}>
									<TableCell component="th" scope="row">MSB</TableCell>
									<TableCell  component="th" scope="row">Mortgage Backed Securities</TableCell>
								</TableRow>
								<TableRow key={8}>
									<TableCell component="th" scope="row">U</TableCell>
									<TableCell  component="th" scope="row">Unemployment Rate</TableCell>
								</TableRow>
							</TableBody>
						</Table>
					</Paper>
				</div>
    	);
    }
}
Dash.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Dash);