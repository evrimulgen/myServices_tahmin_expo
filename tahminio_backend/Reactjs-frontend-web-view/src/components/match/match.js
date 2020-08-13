import React, { Component } from 'react';
import PropTypes from 'prop-types'
import { formatDate } from './auxillary';

const propTypes = {
    match: PropTypes.object
}

class Match extends Component {
    constructor(props) {
        super(props);
        this.state = {
            result: null,
        };
    }
    render() {
        let { match } = this.props
        if (match) {
            let handicap = '(' + Math.abs(match.handicap) + 'H)'
            return (
                <div className="match-container">
                    {match.home_team.name} {match.handicap < 0 ? handicap : ''} {match.score} {match.away_team.name} {match.handicap > 0 ? handicap : ''}
                    <br />
                    {match.minute ? match.minute : formatDate(match.datetime)[1]} {match.league.name}
                </div>
            )
        }
    }
}

Match.propTypes = propTypes

export default Match;