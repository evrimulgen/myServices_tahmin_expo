import React, { Component } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import './css/feed.css'

const propTypes = {

}


class Feed extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: null,
        };
        this.getFeed = this.getFeed.bind(this);
    }

    componentDidMount() {
        this.getFeed()
    }

    getFeed() {
        let that = this;
        console.log(localStorage.getItem('tahmin.io-token'))
        axios.get('http://api.tahmin.io/v1/users/feed/', {
            headers: {
                "Authorization": "Token " + localStorage.getItem('tahmin.io-token')
            }
        }).then((res) => {
            console.log(res.data)
            that.setState({
                data: res.data
            })
        }).catch((e) => {
            console.log(e)
        })
    }

    render() {
        if (this.state.data === null) {
            return (
                <div className="feed-container">no</div>
            )
        }
        else {
            return (
                <div className="feed-container">xd</div>
            )
        }
    }

}


Feed.propTypes = propTypes

export default Feed;