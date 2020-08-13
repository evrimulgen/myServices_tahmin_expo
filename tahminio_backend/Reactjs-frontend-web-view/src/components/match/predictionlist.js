import React, { Component } from 'react';
import PropTypes from 'prop-types'
import axios from 'axios'
import User from './user'
import uuidv4 from 'uuid/v4'

const propTypes = {
    predictionList: PropTypes.array,
    matchId: PropTypes.number
}

class PredictionList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            predictionList: null,
            result: null,
            query: null,
            myId: null,
            showUser: null,
        };
        this.handleClick = this.handleClick.bind(this);
        this.getStatus = this.getStatus.bind(this);
        this.handleFollow = this.handleFollow.bind(this);
        this.handleUnfollow = this.handleUnfollow.bind(this);
        this.handleUpvote = this.handleUpvote.bind(this);
        this.handleDelete = this.handleDelete.bind(this);
        this.getMe = this.getMe.bind(this);
    }

    componentDidMount() {
        this.getMe();
    }

    componentDidUpdate(prevProps, prevState) {
        if (prevState.query !== this.state.query || prevState.showUser !== this.state.showUser) {
            this.setState({
                user: this.state.showUser ? <User query={this.state.query} status={this.getStatus} /> : '',
            })
        }
    }

    handleClick(e) {
        console.log('ok')
        this.setState({
            showUser: true,
            query: e.target.text
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

    handleUpvote(e) {
        let q = e.target.getAttribute('value');
        let w = e.target.getAttribute('value2')
        console.log(q)
        console.log(w)
        axios.post('http://api.tahmin.io/v1/matches/' + q + '/predictions/' + w + '/upvote/', {
        }, { 'headers': { 'Authorization': "Token " + localStorage.getItem('tahmin.io-token') } })
            .then(function (r) {
                console.log(r.data);
            })
            .catch(function (e) { console.log(e); })
    }

    handleUndoUpvote(e) {
        let q = e.target.getAttribute('value');
        let w = e.target.getAttribute('value2')
        axios.post('http://api.tahmin.io/v1/matches/' + q + '/predictions/' + w + '/undoupvote/', {
        }, { 'headers': { 'Authorization': "Token " + localStorage.getItem('tahmin.io-token') } })
            .then(function (r) {
                console.log(r.data);
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


    handleDelete(e) {
        let q = e.target.getAttribute('value');
        let w = e.target.getAttribute('value2');
        axios.delete('http://api.tahmin.io/v1/matches/' + q + '/predictions/' + w + '/',
            { 'headers': { 'Authorization': "Token " + localStorage.getItem('tahmin.io-token') } })
            .then(function (r) {
                console.log(r.data);
            })
            .catch(function (e) { console.log(e); })
    }


    render() {
        let { predictionList } = this.props;
        // if user not in follow list else...
        if (predictionList) {
            return (
                <div>
                    {predictionList.map((val, i) => {
                        console.log(val.upvoted)
                        console.log(val)
                        let follow = <a value={val.user.id} onClick={this.handleFollow} style={{ cursor: 'pointer' }}>{'Follow'}</a>
                        let unfollow = <a value={val.user.id} onClick={this.handleUnfollow} style={{ cursor: 'pointer' }}>{'Unfollow'}</a>
                        let upvote = <a value={val.match.id} value2={val.id} onClick={this.handleUpvote} style={{ cursor: 'pointer' }}>{'Upvote'}</a>
                        let undoUpvote = <a value={val.match.id} value2={val.id} onClick={this.handleUndoUpvote} style={{ cursor: 'pointer' }}>{'Undo Upvote'}</a>
                        let del = <a value={val.match.id} value2={val.id} onClick={this.handleDelete} style={{ cursor: 'pointer' }}>{'Delete'}</a>
                        console.log(follow.props.value)
                        return <div key={uuidv4()}>
                            {val.game} {val.text} {val.user.username} {follow} {unfollow} {val.upvoted ? undoUpvote : upvote} {val.upvote_count}
                            {' '} {val.user.id === this.state.myId ? del : ''}
                        </div>
                    })}
                    {this.state.user}
                </div>
            )
        }
        else {
            return (null)
        }

    }
}

PredictionList.propTypes = propTypes

export default PredictionList;