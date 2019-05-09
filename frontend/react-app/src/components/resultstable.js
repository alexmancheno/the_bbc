import React, { Component } from 'react'
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import Typography from '@material-ui/core/Typography';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
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

class ResultsTable extends Component {

	fillTable = () =>{
		let data = []
		for(let i = 0; i<10; i++){
			let str = ''
			// for(let i = 0; i<this.props.prop[i].independent_variables.length; i++)
			// 	str += this.props.prop[i].independent_variables[]
			data.push(
				<TableRow key={i}>
					<TableCell component="th" scope="row">{this.props.prop[i].independent_variables.toString()}</TableCell>
					<TableCell align="right" component="th" scope="row">{this.props.prop[i]["r^2"]}</TableCell>
				</TableRow>
			)
		}
		return data
	}
	render(){
		const { classes } = this.props;

		return (
			<div>
				<Typography variant="h4" gutterBottom component="h2">
					Linear Regression/ K Folds Results
				</Typography>
				<Typography component="div" className={classes.chartContainer}>
				<Paper className={classes.root}>
					<Table className={classes.table}>
						<TableHead>
							<TableRow>
								<TableCell >Independent Variables</TableCell>
								<TableCell align="right">R-Squared</TableCell>
							</TableRow>
						</TableHead>
						<TableBody>
							{this.fillTable()}
						</TableBody>
					</Table>
				</Paper>
				</Typography>
			</div>
		);
	}
}

ResultsTable.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(ResultsTable);