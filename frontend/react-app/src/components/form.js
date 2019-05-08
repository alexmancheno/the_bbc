import React, { Component } from 'react'
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import green from '@material-ui/core/colors/green';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import CheckBoxOutlineBlankIcon from '@material-ui/icons/CheckBoxOutlineBlank';
import CheckBoxIcon from '@material-ui/icons/CheckBox';
import Favorite from '@material-ui/icons/Favorite';
import FavoriteBorder from '@material-ui/icons/FavoriteBorder';
import Axios from 'axios';

const styles = {
  root: {
    color: green[600],
    '&$checked': {
      color: green[500],
    },
  },
  checked: {},
	};

class Form extends React.Component {
    constructor(props) {
			super(props);
      this.state = {
					vars: null,
					choosen: null
			};
      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }
		
    handleChange = index => event => {
			let choosen = this.state.choosen
			choosen[index].value = event.target.checked
			this.setState({choosen : choosen});
		};

  
    handleSubmit(event) {
			event.preventDefault();
			let vars = ''
			for(let i = 0; i<this.state.choosen.length; i++){
				if(this.state.choosen[i].value === true)
					vars += this.state.choosen[i].key + ','
			}
			this.props.onSubmit(vars.substring(0, vars.length-1))
		}

		componentDidMount() {
			Axios.get('http://localhost:8080/vars')
				.then(response => {
					this.setState({vars: response.data});
					let choosen = []
					for(let i = 0; i<this.state.vars.length;i++){
						choosen.push({key: this.state.vars[i], value: false})
					}
					this.setState({choosen: choosen});
				})
		}


		createCheckBox = () =>{
			if(this.state.vars === null || this.state.choosen == null){
				return;
			}
			let checkBox = []
			for(let i = 0; i<this.state.vars.length;i++){
				checkBox.push(<FormControlLabel key={`${i}`} control={ <Checkbox checked={this.state.choosen[i].value} onChange={this.handleChange(i)} value={`${i}`}/>} label={`${this.state.vars[i]}`}/>)
			}

			return checkBox;
		}

    render() {
			const { classes } = this.props;
      return (
        <form onSubmit={this.handleSubmit}>
					<FormGroup row>
						{this.createCheckBox()}
					</FormGroup>
					<input type="submit" value="Submit" />
				</form>
      );
    }
  }

  Form.propTypes = {
		classes: PropTypes.object.isRequired,
	};
	
	export default withStyles(styles)(Form);