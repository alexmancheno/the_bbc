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
import Button from '@material-ui/core/Button';
import Axios from 'axios';
import CircularProgress from '@material-ui/core/CircularProgress';

const styles = theme=>({
  root: {
    width: '100%',
    overflowX: 'auto',
  },
  table: {
    minWidth: 700,
  },
  progress: {
    margin: theme.spacing.unit * 2,
  },
});

class ResultsTable extends Component {

	constructor(){
		super()
		this.state = {
		  fetchResults: false,
		  reglist: null,
		  loading: false,
		  displayButton: true
		};

		this.fetchResults = this.fetchResults.bind(this);
		this.loading = this.loading.bind(this);
	}

	fillTable = () =>{
		let data = []
		for(let i = 0; i<10; i++){
			let str = ''
			// for(let i = 0; i<this.props.prop[i].independent_variables.length; i++)
			// 	str += this.props.prop[i].independent_variables[]
			if(this.props.prop!=null){
				data.push(
					<TableRow key={i}>
						<TableCell component="th" scope="row">{this.props.prop[i].independent_variables.toString()}</TableCell>
						<TableCell align="right" component="th" scope="row">{this.props.prop[i]["r^2"]}</TableCell>
					</TableRow>
				)
			}
			else {
				data.push(
					<TableRow key={i}>
						<TableCell component="th" scope="row">{this.state.reglist[i].independent_variables.toString()}</TableCell>
						<TableCell align="right" component="th" scope="row">{this.state.reglist[i]["r^2"]}</TableCell>
					</TableRow>
				)
			}
		}
		return data
	}

	loading = () =>{
		this.setState({loading: true, displayButton: false})
	}

	fetchResults = () =>{
		this.loading()
		if(this.state.fetchResults == false){
		  Axios.get('http://97.107.142.134:81/reglist')
		  .then(response => {
			this.setState({reglist : response.data, fetchResults: true, loading:false})
			this.props.onSubmit(this.state.reglist);
		  })
		}
	  }

	switch = () =>{
		const { classes } = this.props;
		if(this.state.fetchResults){
			return<Typography component="div" className={classes.chartContainer}>
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
		}else if(this.state.displayButton){
			return <Button type="submit"  size="small" onClick={this.fetchResults} className={classes.primary}> Run Regression</Button>
		}else if(this.state.loading){
			return <CircularProgress className={classes.progress} />
		}
	}
	render(){
		const { classes } = this.props;

		return (
			<div>
				<Typography variant="h4" gutterBottom component="h2">
					Linear Regression/ K Folds Results
				</Typography>
				{this.switch()}
			</div>
		);
	}
}

ResultsTable.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(ResultsTable);