import React, { Component } from 'react'
import PropTypes from 'prop-types';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Drawer from '@material-ui/core/Drawer';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import List from '@material-ui/core/List';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import Item from './components/listitem';
import SimpleLineChart from './components/simpleline';
import Fab from '@material-ui/core/Fab';
import NavigationIcon from '@material-ui/icons/Navigation';
import Form from './components/form';
import SimpleTable from './components/simpletable';
import Axios from 'axios';

const drawerWidth = 240;
const fs = require('fs');

const styles = theme => ({
  root: {
    display: 'flex',
  },
  toolbar: {
    paddingRight: 24,
  },
  toolbarIcon: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: '0 8px',
    ...theme.mixins.toolbar,
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarShift: {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  menuButton: {
    marginLeft: 12,
    marginRight: 36,
  },
  menuButtonHidden: {
    display: 'none',
  },
  title: {
    flexGrow: 1,
  },
  drawerPaper: {
    position: 'relative',
    whiteSpace: 'nowrap',
    width: drawerWidth,
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  drawerPaperClose: {
    overflowX: 'hidden',
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    width: theme.spacing.unit * 7,
    [theme.breakpoints.up('sm')]: {
      width: theme.spacing.unit * 9,
    },
  },
  appBarSpacer: theme.mixins.toolbar,
  content: {
    flexGrow: 1,
    padding: theme.spacing.unit * 3,
    height: '100vh',
    overflow: 'auto',
  },
  chartContainer: {
    marginLeft: -22,
  },
  tableContainer: {
    height: 320,
  },
  h5: {
    marginBottom: theme.spacing.unit * 2,
  },
  fab: {
    margin: theme.spacing.unit,
  },
  extendedIcon: {
    marginRight: theme.spacing.unit,
  },
});

class App extends Component {
  constructor(){
    super()
    this.state = {
      open: false,
      data: null,
      kfold: null
    };
  }

  isCache = (s) =>{
    if(fs.existsSync(`cache/${s}.json`))
      return true;
  
    return false;
  }

  getkfolds = () =>{
    if(this.isCache('kfolds.json')){
      this.setState({kfold: fs.createReadStream(`cache/kfold.json`)})
    }
    Axios.get('http://localhost:8080/reglist')
      .then(response => {
        this.setState({kfold: response});
      })
    
  }
  

  fetch = (s) =>{
    console.log(s)
    Axios.get('http://localhost:8080/regression?vars='+s)
      .then(response => {
        console.log(response.data.true_vs_prediction)
        let size = response.data.true_vs_prediction.length
        let data = new Array();
        for(let i = 0; i< size; i++){
          data.push({Date: response.data.true_vs_prediction[i][0], Predicted: response.data.true_vs_prediction[i][1], Actual: response.data.true_vs_prediction[i][2]});
        }
        this.setState({data: data});
      })
  }

  handleDrawerOpen = () => {
    this.setState({ open: true });
  };

  handleDrawerClose = () => {
    this.setState({ open: false });
  };

  render() {
    const { classes } = this.props;
    return (
      <div className={classes.root}>
        <CssBaseline />
        <AppBar position="absolute" className={classNames(classes.appBar, this.state.open && classes.appBarShift)}>
            <Toolbar disableGutters={!this.state.open} className={classes.toolbar}>
                <IconButton color="inherit" aria-label="Open drawer" onClick={this.handleDrawerOpen} className={classNames(
                    classes.menuButton,
                    this.state.open && classes.menuButtonHidden,
                )}>
                    <MenuIcon />
                </IconButton>
                <Typography component="h1" variant="h6" color="inherit" noWrap className={classes.title}>
                    BBC - Big Bank Conglomerate
                </Typography>
            </Toolbar>
        </AppBar>
        <Drawer 
            variant="permanent" 
            classes={{
                paper: classNames(classes.drawerPaper, !this.state.open && classes.drawerPaperClose),
            }} 
            open={this.state.open}>
            <div className={classes.toolbarIcon}>
                <IconButton onClick={this.handleDrawerClose}>
                    <ChevronLeftIcon />
                </IconButton>
            </div>
            <Divider />
                <List><Item /></List>
        </Drawer>
        <main className={classes.content}>
          <div className={classes.appBarSpacer} />
          <Typography variant="h4" gutterBottom component="h2">
            Results
          </Typography>
          <Typography component="div" className={classes.chartContainer}>
            <SimpleLineChart prop={this.state}/>
          </Typography>
          <Form onSubmit={this.fetch}></Form>
        </main>
      </div>
    );
  }
}

App.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(App);