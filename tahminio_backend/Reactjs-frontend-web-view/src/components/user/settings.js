import React, { Component } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';

const propTypes = {
    data: PropTypes.object.isRequired,
    sendData: PropTypes.func.isRequired
}

class Settings extends Component {
    constructor(props) {
        super(props);
        this.state = {
            pwd: null,
            pwdConfirm: null,
            oldPwd: null,
            mail: null,
            bio: this.props.data.data.bio
        };
        this.handlePwdChange = this.handlePwdChange.bind(this);
        this.handlePwdCChange = this.handlePwdCChange.bind(this);
        this.handleOldPwdChange = this.handleOldPwdChange.bind(this);
        this.handle = this.handle.bind(this);
        this.handleMailChange = this.handleMailChange.bind(this);
        this.handlePwd = this.handlePwd.bind(this);
    }

    
    handleOldPwdChange(e) {
        this.setState({ oldPwd: e.target.value });
    }
    handlePwdChange(e) {
        this.setState({ pwd: e.target.value });
    }
    handlePwdCChange(e) {
        this.setState({ pwdConfirm: e.target.value });
    }
    handleMailChange(e) {
        this.setState({ mail: e.target.value });
    }
    handleBioChange(e) {
        this.setState({ bio: e.target.value });
    }

    handle(e) {
        let that = this;
        let data = {};
        if (e.target.value === 'e-mail') data.email = this.state.mail
        if (e.target.value ===  'bio') data.bio = this.state.bio
        if (Object.keys(data).length > 0) {
            console.log(data)
            axios.patch('http://api.tahmin.io/v1/users/me/', data, {
                'headers': { 'Authorization': "Token " + localStorage.getItem('tahmin.io-token') }
            }).then(function (r) {
                that.props.sendData([r, true])
                localStorage.setItem('tahmin.io-token', r.data.token);
            })
                .catch(function (e) { console.log(e) })
        }
        else (console.log(this.state.pwd + ' ' + this.state.pwdConfirm + ' ' ));
        e.preventDefault();
    }   

    
    handlePwd(e) {
        let that = this;
        let data = {};
        data.new_password = this.state.pwd;
        data.old_password = this.state.oldPwd;
        if (this.state.pwd === this.state.pwdConfirm && Object.keys(data).length > 0) {
            console.log(data)
            axios.patch('http://api.tahmin.io/v1/users/me/password/', data, {
                'headers': { 'Authorization': "Token " + localStorage.getItem('tahmin.io-token') }
            }).then(function (r) {
                that.props.sendData([r, true])
            })
                .catch(function (e) { console.log(e) })
        }
        else (console.log(this.state.pwd + ' ' + this.state.pwdConfirm + ' ' ));
        e.preventDefault();
    }


    render() {
        return (
            <div>
                <div className='settings-field-1' >
                    <input type="password" placeholder={'Old Password'} defaultValue={this.state.oldPwd} onChange={this.handleOldPwdChange} />
                </div>
                <div className='settings-field-1' >
                    <input type="password" placeholder={'Password'} defaultValue={this.state.pwd} onChange={this.handlePwdChange} />
                </div>
                <div className='settings-field-2' >
                    <input type="password" placeholder={'Confirm'} defaultValue={this.state.pwdConfirm} onChange={this.handlePwdCChange} />
                </div>
                <div className='settings-field-3'>
                    <button  value='pwd' onClick={this.handlePwd}> Update password </button>
                </div>
                <div className='settings-field-4' >
                    <input type="text" placeholder={'E-Mail'} defaultValue={this.state.mail} onChange={this.handleMailChange} />
                </div>
                <div className='settings-field-5'>
                    <button  value='e-mail' onClick={this.handle}> Update e-mail </button>
                </div>
                <div className='settings-field-6' >
                    <input type="text" placeholder={'Bio'} defaultValue={this.state.bio} onChange={this.handleBioChange} />
                </div>
                <div className='settings-field-7'>
                    <button value='bio' onClick={this.handle}> Update bio </button>
                </div>
            </div>
        )
    }
}

Settings.propTypes = propTypes

export default Settings;