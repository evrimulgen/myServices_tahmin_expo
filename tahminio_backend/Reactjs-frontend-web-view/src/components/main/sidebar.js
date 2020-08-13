import React, { Component } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import './css/feed.css'

const propTypes = {

}


class Sidebar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: []
        };
    }

    render() {
        if (this.state.data === null) {
        return (
            null
        )
    }
    else {
        return (
            'xd'
        )
    }
    }

}


Sidebar.propTypes = propTypes

export default Sidebar;