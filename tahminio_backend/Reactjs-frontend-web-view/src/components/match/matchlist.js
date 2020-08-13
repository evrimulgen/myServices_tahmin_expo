import React, { Component } from 'react';
import axios from 'axios';
import Main from './main';
import './css/matchlist.css'
import { formatDate } from './auxillary';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faComments, faFutbol } from '@fortawesome/free-regular-svg-icons'
import { Row, Col } from 'reactstrap';
import Date from './date';
import League from './league';
import uuidv4 from 'uuid/v4'

class MatchList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            list: null,
            query: null,
            main: null,
            refreshed: 0,
        };
        this.elements = {};
        this.dates = [];
        this.leagues = [];
        this.getMatches = this.getMatches.bind(this);
        this.handleClick = this.handleClick.bind(this);
        this.getStatus = this.getStatus.bind(this);
        this.liveRefresh = this.liveRefresh.bind(this);
    }

    componentWillMount() {
        this.liveRefresh();
    }

    getMatches() {
        let that = this;
        axios.get('http://api.tahmin.io/v1/matches/', {
        })
            .then(function (r) {
                console.log(r);
                that.setState({
                    list: r.data,
                    refreshed: that.state.refreshed + 1
                })
            })
            .catch(function (e) { console.log(e); })
    }

    liveRefresh() {
        this.getMatches();
        setInterval(() => {
            this.getMatches()
        }, 15000)
    }

    handleClick(e) {
        let id = e.currentTarget.getAttribute('id')
        window.open("/match/" + id, '_blank')
    }

    getStatus(s) {
        console.log('yes')
        console.log(s);
        this.setState({
            showMatch: s
        })
    }

    componentDidUpdate(prevProps, prevState) {
        if (prevState.query !== this.state.query || prevState.showMatch !== this.state.showMatch) {
            this.setState({
                main: this.state.showMatch ? <Main query={this.state.query} status={this.getStatus} /> : '',
            })
        }
    }


    render() {
        let { list } = this.state
        this.elements = {};
        this.dates = [];
        this.leagues = [];
        if (list) {
            return (
                <div className="matchlist-container" ref="matchlist-container">
                    {list.map((val, i) => {
                        let current = val.datetime;
                        let curDate = formatDate(current)[0];
                        let league = val.league.name;
                        console.log(curDate)
                        let firstDate = null;
                        let firstLeague = null;
                        if (!(this.dates.some(ele => { return ele === curDate }))) {
                            firstDate = <Date key={uuidv4()} matchDate={curDate} />
                            this.dates.push(curDate);
                            this.elements[curDate] = [];
                            this.elements[curDate].push(firstDate)
                        }
                        if (!(this.leagues.some(ele => { return ele === league }))) {
                            firstLeague = <League key={uuidv4()} matchLeague={league} />
                            this.leagues.push(league);
                            this.elements[curDate][league] = [];
                            this.elements[curDate][league].push(firstLeague)
                        }
                        let handicap = '(-' + Math.abs(val.handicap) + 'H)'
                        let info = <div key={uuidv4()} className="matchlist-single">
                            {<a id={val.id} onClick={this.handleClick} style={{ cursor: 'pointer' }}>
                                <Row>
                                    <Col lg="2" className="id-league-date"> {val.minute ? val.minute : formatDate(val.datetime)[1]} </Col>
                                    <Col lg="1"> {val.handicap < 0 ? handicap : ''} </Col>
                                    <Col lg="6" className="matchlist-match"> {val.home_team.name} {val.score} {val.away_team.name} </Col>
                                    <Col lg="1"> {val.handicap > 0 ? handicap : ''} </Col>
                                    <Col lg="2" className="predictions-messages"> {val.prediction_count} <FontAwesomeIcon icon={faFutbol} /> {val.message_count} <FontAwesomeIcon icon={faComments} /> </Col>
                                </Row>
                            </a>}
                        </div>
                        this.elements[curDate][league].push(info)
                    })}
                    <div key={uuidv4()}>
                        {console.log(this.elements)}
                        {Object.keys(this.elements).map(date => {
                                return (
                                    Object.keys(this.elements[date]).map(leagues => { return <div key={uuidv4()}> {this.elements[date][leagues]} </div> })
                                )
                            })}
                    </div>
                </div>
            )
        }
        else {
            return ('Loading...')
        }
    }
}

export default MatchList;