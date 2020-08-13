import React, { Component } from 'react';
import PropTypes from 'prop-types'

const propTypes = {
    matchLeague: PropTypes.string.isRequired
}

class League extends Component {
    constructor(props) {
        super(props);
        this.state = {
        };
    }
    render() {
        let { matchLeague } = this.props
        return (
            <div className="league-container">
                {matchLeague}
            </div>
        )
    }
}

League.propTypes = propTypes

export default League;