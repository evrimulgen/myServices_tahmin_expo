import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Login from './login';
import Signup from './signup';
import Forgot from './forgot';
import Recovery from './recovery';
import Settings from '../user/settings';
import Profile from '../user/profile';
import axios from 'axios';

const propTypes = {
    sendData: PropTypes.func.isRequired
}

class AuthHandler extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: null,
            status: false,
            showSettings: false,
            showLogin: false,
            showSignup: false,
            showForgot: false,
            showProfile: false,
        };
        this.logoutHandler = this.logoutHandler.bind(this);
        this.checkLogin = this.checkLogin.bind(this);
        this.getData = this.getData.bind(this);
        this.showSettings = this.showSettings.bind(this);
        this.showSignup = this.showSignup.bind(this);
        this.showLogin = this.showLogin.bind(this);
        this.showForgot = this.showForgot.bind(this);
        this.showProfile = this.showProfile.bind(this);
    }

    getData(c) {
        this.setState({
            data: c[0],
            status: c[1]
        })
    }

    componentDidMount() {
        this.checkLogin()
    }

    componentDidUpdate(prevProps, prevState) {
        if (this.state.status !== prevState.status) {
            this.setState({
                showSettings: false,
                showLogin: false,
                showSignup: false,
                showForgot: false,
                showProfile: false,
            })
        }
        if (!(Object.is(prevState, this.state))) {
            if (this.state.data === null) this.props.sendData(null);
            else this.props.sendData(this.state.data);
        }
    }

    checkLogin() {
        let that = this;
        if (localStorage.getItem('tahmin.io-token') && localStorage.getItem('tahmin.io-token').length > 0) {
            axios.get('http://api.tahmin.io/v1/users/me/', {
                'headers': { 'Authorization': "Token " + localStorage.getItem('tahmin.io-token') }
            })
                .then(function (r) {
                    console.log(r);
                    that.props.sendData(r);
                    that.setState({
                        data: r,
                        status: true
                    })
                })
                .catch(function (e) { console.log(e); })
        }
    }

    logoutHandler() {
        this.setState({
            data: null,
            status: false
        })
        localStorage.setItem('tahmin.io-token', null);
    }

    showSettings() {
        this.setState({ showSettings: true })
    }

    showSignup() {
        this.setState({ showSignup: true })
    }

    showProfile() {
        this.setState({ showProfile: true })
    }

    showLogin() {
        this.setState({ showLogin: true })
    }

    showForgot() {
        this.setState({ showForgot: true })
    }

    render() {
        if (this.state.status) {
            let settings = this.state.showSettings ? <Settings data={this.state.data} sendData={this.getData} /> : null;
            let profile = this.state.showProfile ? <Profile data={this.state.data} /> : null;
            return (
                <div>
                    <br />
                    <button onClick={this.logoutHandler}>Log out</button>
                    <button onClick={this.showSettings}> Settings </button>
                    <button onClick={this.showProfile}> Profile </button>
                    {settings} {profile}
                </div>
            )
        }
        else {
            let signup = this.state.showSignup ? <Signup sendData={this.getData} /> : null;
            let login = this.state.showLogin ? <Login sendData={this.getData} /> : null;
            let forgot = this.state.showForgot ? <Forgot sendData={this.getData} /> : null;
            let pwd = window.location.href.indexOf('key') > -1 ? <Recovery sendData={this.getData} /> : null;
            return (
                <div>
                    <button onClick={this.showSignup}> Sign Up </button>
                    <button onClick={this.showLogin}> Login </button>
                    {/* <button onClick={this.showForgot}> Forgot password? </button> */}
                    {signup} {login} {forgot} {pwd}
                </div>
            )
        }
    }
}

AuthHandler.propTypes = propTypes;

export default AuthHandler;