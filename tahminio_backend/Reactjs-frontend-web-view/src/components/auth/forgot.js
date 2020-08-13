import React, { Component } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types'
import './style.css'

const propTypes = {
    sendData: PropTypes.func.isRequired
}


class Forgot extends Component {
    constructor(props) {
        super(props);
        this.state = {
            usr: null,
        };
        this.handleUsrChange = this.handleUsrChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    handleUsrChange(e) {
        this.setState({ usr: e.target.value });
    }



    handleSubmit(e) {
        axios.post('http://api.tahmin.io/v1/users/forgot_password/', {
            "user_identifier": this.state.usr,
        }).then(function (r) {
            console.log(r)
        })
            .catch(function (e) { console.log(e) })
        e.preventDefault();
    }

    render() {
        return (
            <div className="login-form">
                <form onSubmit={this.handleSubmit}>
                <div className="login-field">
                <input type="text" placeholder={'Username or E-Mail'} defaultValue={this.state.usr} onChange={this.handleUsrChange} />
                    </div>
                    <div className="login-field-3">
                    <input type="submit" value="Confirm" />
                    </div>
                </form>
            </div>

        )
    }
}

Forgot.propTypes = propTypes

export default Forgot;