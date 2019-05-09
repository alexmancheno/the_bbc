import React, { Component } from 'react';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import DashboardIcon from '@material-ui/icons/Dashboard';
import ResultsIcon from '@material-ui/icons/TrendingUp'
import EditIcon from '@material-ui/icons/Edit'
class Item extends Component{
  render(){
    return(
      <div>
        <ListItem button onClick={this.props.onClick(0)}>
          <ListItemIcon>
            <DashboardIcon />
          </ListItemIcon>
          <ListItemText primary="Dashboard" />
        </ListItem>
        <ListItem button onClick={this.props.onClick(1)}>
          <ListItemIcon>
            <ResultsIcon />
          </ListItemIcon>
          <ListItemText primary="Results" />
        </ListItem>
        <ListItem button onClick={this.props.onClick(2)}>
          <ListItemIcon>
            <EditIcon  />
          </ListItemIcon>
          <ListItemText primary="Edit" />
        </ListItem>
      </div>
    );
  }
}
export default Item;