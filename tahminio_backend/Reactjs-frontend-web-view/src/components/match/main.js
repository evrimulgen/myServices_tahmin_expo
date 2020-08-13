import React, { Component } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types'
import Game from './game';
import MessageList from './messagelist';
import PredictionList from './predictionlist';
import Match from './match';
import './css/main.css'
import { Row, Col } from 'reactstrap';
import Feed from '../main/feed'
import Sidebar from '../main/sidebar'
import Header from '../main/header'

const propTypes = {
}


class Main extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: null,
            showMatch: false,
            authed: null,
        };
        this.handle = this.handle.bind(this);
        this.getData = this.getData.bind(this)
        this.toggle = this.toggle.bind(this);
    }


    getData(c) {
        this.setState({
            authed: c
        })
    }

    componentDidMount() {
        this.handle();
    }

    componentDidUpdate(prevProps, prevState) {
    }

    handle(e) {
        let that = this;
        let q = this.props.match.params.id
        if (q) {
            axios.get('http://api.tahmin.io/v1/matches/' + q + '/', {
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

    toggle() {
        this.setState({
            showMatch: !this.state.showMatch
        });
    }


    render() {
        let feed = this.state.authed ? <Feed /> : ''
        console.log('here')
        console.log(this.state.data);
        if (this.state.data) {
            return (
                <div className="main-container">
                    <Header sendData={this.getData} />
                    <Row>
                        <Col lg="3"> <Sidebar /> </Col>
                        <Col lg="6">
                            <div>  <Match match={this.state.data.match} /> </div>
                            <br />
                            <div>  <Game game={this.state.data.games} matchId={this.state.data.match.id} /> </div>
                            <br />
                            <div>  <MessageList messageList={this.state.data.messages} matchId={this.state.data.match.id} /></div>
                            <br />
                            <div> <PredictionList predictionList={this.state.data.predictions} matchId={this.state.data.match.id} /> </div>
                        </Col>
                        <Col lg="3"> <Feed /> </Col>
                    </Row>
                </div>
            )
        }
        else return (null)
    }
}

Main.propTypes = propTypes

export default Main;