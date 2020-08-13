import React, { Component } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types'
import './style.css'

const propTypes = {
    sendData: PropTypes.func.isRequired
}


class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {
            usr: null,
            pwd: null,
        };
        this.handleUsrChange = this.handleUsrChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handlePwdChange = this.handlePwdChange.bind(this);

    }

    handleUsrChange(e) {
        this.setState({ usr: e.target.value });
    }

    handlePwdChange(e) {
        this.setState({ pwd: e.target.value });
    }


    handleSubmit(e) {
        let that = this
        axios.post('http://api.tahmin.io/v1/users/login/', {
            "username": this.state.usr,
            "password": this.state.pwd,
        }).then(function (r) {
            localStorage.setItem('tahmin.io-token', r.data.token);
            that.props.sendData([r, true])
        })
            .catch(function (e) { console.log(e) })
        e.preventDefault();
    }

    render() {
        return (
            <div className="login-form">
                <form onSubmit={this.handleSubmit}>
                <div className="login-field">
                <input type="text" placeholder={'Username'} defaultValue={this.state.usr} onChange={this.handleUsrChange} />
                    </div>
                    <div className="login-field-2">
                <input type="password" placeholder={'Password'} defaultValue={this.state.pwd} onChange={this.handlePwdChange} />
                    </div>
                    <div className="login-field-3">
                    <input type="submit" value="Login" />
                    </div>
                </form>
            </div>

        )
    }
}

Login.propTypes = propTypes

export default Login;