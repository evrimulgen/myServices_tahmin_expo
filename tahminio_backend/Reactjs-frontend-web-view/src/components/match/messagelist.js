import React, { Component } from 'react';
import PropTypes from 'prop-types'
import User from './user'
import axios from 'axios'
import uuidv4 from 'uuid/v4'

const propTypes = {
    messageList: PropTypes.array,
    matchId: PropTypes.number
}

class MessageList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            messageList: null,
            result: null,
            showUser: false,
            query: null,
            user: null,
            myId: null,
            showEdit: [],
            editMsg: [],
            msg: null
        };
        this.handleClick = this.handleClick.bind(this);
        this.getStatus = this.getStatus.bind(this);
        this.handleFollow = this.handleFollow.bind(this);
        this.handleUnfollow = this.handleUnfollow.bind(this);
        this.handleDelete = this.handleDelete.bind(this);
        this.handleEdit = this.handleEdit.bind(this);
        this.handleEditSubmit = this.handleEditSubmit.bind(this);
        this.handleEditMsg = this.handleEditMsg.bind(this);
        this.handleMsg = this.handleMsg.bind(this);
        this.handleMsgSubmit = this.handleMsgSubmit.bind(this);
        this.getMe = this.getMe.bind(this);
    }

    componentDidMount() {
        this.getMe();
    }


    componentDidUpdate(prevProps, prevState) {
        if (this.props.matchId !== prevProps.matchId) {
            this.setState({
                msg: null
            })
            document.querySelector('#msg-form').value = '';
        }
        if (prevState.query !== this.state.query || prevState.showUser !== this.state.showUser) {
            this.setState({
                user: this.state.showUser ? <User query={this.state.query} status={this.getStatus} /> : '',
            })
        }
    }


    handleEditMsg(e) {
        let id = e.target.getAttribute('id')
        let editMsg = this.state.editMsg;
        editMsg[id] = e.target.value;
        this.setState({
            editMsg: editMsg
        })
    }

    handleMsg(e) {
        this.setState({
            msg: e.target.value
        })
    }

    handleClick(e) {
        console.log('ok')
        this.setState({
            showUser: true,
            query: e.target.getAttribute('value')
        })
    }

    handleFollow(e) {
        let q = e.target.getAttribute('value');
        axios.post('http://api.tahmin.io/v1/users/' + q + '/follow/', {
        }, { 'headers': { 'Authorization': "Token " + localStorage.getItem('tahmin.io-token') } })
            .then(function (r) {
                console.log(r.data);
            })
            .catch(function (e) { console.log(e); })
    }

    handleUnfollow(e) {
        let q = e.target.getAttribute('value');
        axios.post('http://api.tahmin.io/v1/users/' + q + '/unfollow/', {
        }, { 'headers': { 'Authorization': "Token " + localStorage.getItem('tahmin.io-token') } })
            .then(function (r) {
                console.log(r.data);
            })
            .catch(function (e) { console.log(e); })
    }


    handleDelete(e) {
        let q = e.target.getAttribute('value');
        let w = e.target.getAttribute('value2');
        axios.delete('http://api.tahmin.io/v1/matches/' + q + '/messages/' + w + '/', { 'headers': { 'Authorization': "Token " + localStorage.getItem('tahmin.io-token') } })
            .then(function (r) {
                console.log(r.data);
            })
            .catch(function (e) {
                console.log(e);
                console.log(localStorage.getItem('tahmin.io-token'))
            })
    }

    handleEdit(e) {
        let id = e.target.getAttribute('value2')
        let showEdit = this.state.showEdit;
        showEdit[id] = true;
        this.setState({ showEdit: showEdit })
    }


    handleEditSubmit(e) {
        let q = e.target.getAttribute('value');
        let w = e.target.getAttribute('value2');
        let data = this.state.editMsg[w];
        console.log(this.state.editMsg)
        let that = this;
        axios.patch('http://api.tahmin.io/v1/matches/' + q + '/messages/' + w + '/', {
            "text": data
        }, { 'headers': { 'Authorization': "Token " + localStorage.getItem('tahmin.io-token') } })
            .then(function (r) {
                console.log(r.data);
                let showEdit = that.state.showEdit;
                let editMsg = that.state.editMsg;
                showEdit[w] = null;
                editMsg[w] = false;
                that.setState({
                    showEdit: showEdit,
                    editMsg: editMsg
                })
            })
            .catch(function (e) { console.log(e); })
    }

    handleMsgSubmit(e) {
        let q = e.target.getAttribute('value');
        let data = this.state.msg;
        let that = this;
        axios.post('http://api.tahmin.io/v1/matches/' + q + '/messages/', {
            "text": data
        }, { 'headers': { 'Authorization': "Token " + localStorage.getItem('tahmin.io-token') } })
            .then(function (r) {
                console.log(r.data);
                that.setState({
                    msg: null
                })
            })
            .catch(function (e) { console.log(e); })
    }


    getMe(e) {
        let that = this;
        axios.get('http://api.tahmin.io/v1/users/me/', {
            'headers': { 'Authorization': "Token " + localStorage.getItem('tahmin.io-token') }
        })
            .then(function (r) {
                console.log(r);
                that.setState({
                    myId: r.data.id,
                })
            })
            .catch(function (e) { console.log(e); })

    }

    getStatus(s) {
        this.setState({
            showUser: s
        })
    }


    render() {
        let { messageList } = this.props;
        let msgForm = <div>
            <input type="text" id='msg-form' placeholder={'Post a new message...'} defaultValue={this.state.msg} onChange={this.handleMsg} />
            <button value={this.props.matchId} onClick={this.handleMsgSubmit}> Submit </button>
        </div>
        // if user not in follow list else...
        if (messageList) {
            return (
                <div>
                    {messageList.map((val, i) => {
                        let editForm = <div>
                            <input id={val.id} type="text" placeholder={'Edit your message...'} defaultValue={this.state.editMsg[val.id]} onChange={this.handleEditMsg} />
                            <button value={val.match.id} value2={val.id} onClick={this.handleEditSubmit}> Submit </button>
                        </div>
                        let follow = <a value={val.user.id} onClick={this.handleFollow} style={{ cursor: 'pointer' }}>{'Follow'}</a>
                        let unfollow = <a value={val.user.id} onClick={this.handleUnfollow} style={{ cursor: 'pointer' }}>{'Unfollow'}</a>
                        let del = <a value={val.match.id} value2={val.id} onClick={this.handleDelete} style={{ cursor: 'pointer' }}>{'Delete'}</a>
                        let edit = <div> <a value={val.match.id} value2={val.id} onClick={this.handleEdit} style={{ cursor: 'pointer' }}>{'Edit'}</a>
                        </div>
                        return <div key={uuidv4()}>
                            {val.text} {<a value={val.id} onClick={this.handleClick} style={{ cursor: 'pointer' }}>{val.user.username}</a>} {follow} {unfollow}
                            {' '}{val.user.id === this.state.myId ? del : ''} {val.user.id === this.state.myId ? edit : ''}
                            {this.state.showEdit[val.id] ? editForm : ''}
                        </div>
                    })}
                    {msgForm}
                    {this.state.user}
                </div>
            )
        }
        else {
            return (null)
        }

    }
}

MessageList.propTypes = propTypes

export default MessageList;