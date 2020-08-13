import React, { Component } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types'
import './style.css'

const propTypes = {
    sendData: PropTypes.func.isRequired
}


class Recovery extends Component {
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
        let key = window.location.href.split('?key=')[1]
        let password = this.state.usr;
        axios.post('http://api.tahmin.io/v1/users/change_password/', {
            key: key,
            password: password,
        }).then(function (r) {
        })
        .catch(function (e) { console.error(e.response) })
        e.preventDefault();
    }

    render() {
        return (
            <div className="login-form">
                <form onSubmit={this.handleSubmit}>
                    <div className="login-field">
                        <input type="password" placeholder={'Password'} defaultValue={this.state.usr} onChange={this.handleUsrChange} />
                    </div>
                    <div className="login-field-3">
                        <input type="submit" value="Confirm" />
                    </div>
                </form>
            </div>

        )
    }
}

Recovery.propTypes = propTypes

export default Recovery;