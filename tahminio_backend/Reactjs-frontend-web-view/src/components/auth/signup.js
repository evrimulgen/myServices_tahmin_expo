import React, { Component } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types'
import './style.css'

const propTypes = {
    sendData: PropTypes.func.isRequired
}

class Signup extends Component {
    constructor(props) {
        super(props);
        this.state = {
            usr: null,
            pwd: null,
            mail: null,
            fname: null,
            lname: null,
        };
        this.handleUsrChange = this.handleUsrChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handlePwdChange = this.handlePwdChange.bind(this);
        this.handleMailChange = this.handleMailChange.bind(this);
        this.handleFnameChange = this.handleFnameChange.bind(this);
        this.handleLnameChange = this.handleLnameChange.bind(this);

    }

    handleUsrChange(e) {
        this.setState({ usr: e.target.value });
    }

    handlePwdChange(e) {
        this.setState({ pwd: e.target.value });
    }

    handleMailChange(e) {
        this.setState({ mail: e.target.value });
    }

    handleFnameChange(e) {
        this.setState({ fname: e.target.value });
    }

    handleLnameChange(e) {
        this.setState({ lname: e.target.value });
    }

    handleSubmit(e) {
        let that = this;
        axios.post('http://api.tahmin.io/v1/users/signup/', {
            "username": this.state.usr,
            "password": this.state.pwd,
            "email": this.state.mail,
            "first_name": this.state.fname,
            "last_name": this.state.lname,
        }).then(function (r) {
            localStorage.setItem('tahmin.io-token', r.data.token);
            that.props.sendData([r, true])
        })
            .catch(function (e) { console.log(e) })
        e.preventDefault();
    }

    render() {
        return (
            <div className="signup-form">
                <form onSubmit={this.handleSubmit}>
                    <div className='signup-field' >
                        <input type="text" placeholder={'Username'} defaultValue={this.state.usr} onChange={this.handleUsrChange} />
                    </div>
                    <div className='signup-field-2' >
                        <input type="password" placeholder={'Password'} defaultValue={this.state.pwd} onChange={this.handlePwdChange} />
                    </div>
                    <div className='signup-field-3' >
                        <input type="text" placeholder={'E-Mail'} defaultValue={this.state.mail} onChange={this.handleMailChange} />
                    </div>
                    <div className='signup-field-4' >
                        <input type="text" placeholder={'First Name (optional)'} defaultValue={this.state.fname} onChange={this.handleFnameChange} />
                    </div>
                    <div className='signup-field-5' >
                        <input type="text" placeholder={'Last Name (optional)'} defaultValue={this.state.lname} onChange={this.handleLnameChange} />
                    </div>
                    <div className='signup-field-6'>
                        <input type="submit" value="Sign up" />
                    </div>
                </form>
            </div>

        )
    }
}

Signup.propTypes = propTypes

export default Signup;