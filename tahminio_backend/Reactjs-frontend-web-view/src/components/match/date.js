import React, { Component } from 'react';
import PropTypes from 'prop-types'

const propTypes = {
    matchDate: PropTypes.string.isRequired
}

class Date extends Component {
    constructor(props) {
        super(props);
        this.state = {
        };
    }
    render() {
        let { matchDate } = this.props
        return (
            <div className="date-container">
                {matchDate}
            </div>
        )
    }
}

Date.propTypes = propTypes

export default Date;