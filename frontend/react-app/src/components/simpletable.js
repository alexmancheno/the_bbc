import React, { Component } from 'react'
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
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

class SimpleTable extends Component {
  createTable = () =>{
    let meta = this.props.prop.metadata
    if(meta === null) return;
    let data = []
    let id = 0;
    data.push(
      <TableRow key={id++}>
        <TableCell component="th" scope="row"> R-Square </TableCell>
        <TableCell align="right">{meta["R^2"]}</TableCell>
      </TableRow>
    )
    data.push(
      <TableRow key={id++}>
        <TableCell component="th" scope="row"> Mean-Squared-Error </TableCell>
        <TableCell align="right">{meta.mean_squared_error}</TableCell>
      </TableRow>
    )
    data.push(
      <TableRow key={id++}>
        <TableCell component="th" scope="row"> Mean-Absolute-Error </TableCell>
        <TableCell align="right">{meta.mean_absolute_error}</TableCell>
      </TableRow>
    )

    let coe = meta.coefficients
    for(let i = 0; i<coe.length; i++){
      data.push(
        <TableRow key={id++}>
          <TableCell component="th" scope="row">{coe[i].independent_var + ' Coefficient'} </TableCell>
          <TableCell align="right">{coe[i].coefficient}</TableCell>
        </TableRow>
      )
    }

    data.push(
      <TableRow key={id++}>
        <TableCell component="th" scope="row">Intercept</TableCell>
        <TableCell align="right">{meta.intercept}</TableCell>
      </TableRow>
    )
    
    return data
  }

  render(){
    const { classes } = this.props;
    return (
      <Paper className={classes.root}>
        <Table className={classes.table}>
          <TableBody>
            {this.createTable()}
          </TableBody>
        </Table>
      </Paper>
    );
  }
}

SimpleTable.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(SimpleTable);