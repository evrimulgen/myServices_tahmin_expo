import React, { Component } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';

const propTypes = {
    query: PropTypes.string.isRequired,
    status: PropTypes.func.isRequired
}

class User extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: null
        };
        this.handleClose = this.handleClose.bind(this);
        this.handle = this.handle.bind(this);
    }

    componentDidMount() {
        this.handle();
    }

    componentDidUpdate(prevProps, prevState) {
        if (this.props.query !== prevProps.query) {
            this.handle();
        }
    }

    handle(e) {
        let that = this;
        let q = this.props.query;
        if (this.props.query) {
            axios.get('http://api.tahmin.io/v1/users/' + q + '/', {
            })
                .then(function (r) {
                    console.log(r.data);
                    that.setState({
                        data: r.data,
                    })
                })
                .catch(function (e) { console.log(e); })
        }
    }

    handleClose(e) {
        console.log(e);
        this.props.status(false);
    }

    render() {
        if (this.state.data) {
            // map trophies
            return (
                <div>
                    <div> {this.state.data.username} </div>
                    <button onClick={this.handleClose}> close user </button>
                </div>
            )
        }
        else {
            return (null)
        }
    }
}

User.propTypes = propTypes;

export default User;