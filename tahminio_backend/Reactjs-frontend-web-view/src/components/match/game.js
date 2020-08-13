import React, { Component } from 'react';
import PropTypes from 'prop-types'
import axios from 'axios'
import uuidv4 from 'uuid/v4'

const propTypes = {
    game: PropTypes.array,
    matchId: PropTypes.number
}

class Game extends Component {
    constructor(props) {
        super(props);
        this.state = {
            game: null,
            result: null,
            prediction: null,
            showMsgBox: false,
            msg: null,
        };
        this.handleClick = this.handleClick.bind(this);
        this.handle = this.handle.bind(this);
        this.handleMsgChange = this.handleMsgChange.bind(this);
        this.handlePrediction = this.handlePrediction.bind(this);
    }

    handleMsgChange(e) {
        this.setState({ msg: e.target.value });
    }

    handleClick(e) {
        this.setState({
            prediction: e.target.text,
            showMsgBox: true,
        })
    }

    handlePrediction(e) {
        this.handle();
    }

    componentDidUpdate(prevProps, prevState) {
        console.log('upd')
        console.log(this.props.matchId)
        console.log(prevProps.matchId)
        if (this.props.matchId !== prevProps.matchId) {
            this.setState({
                msg: null,
                prediction: null,
                showMsgBox: false,
            })
            document.querySelector('#msg-form').value = '';
        }
    }

    handle(e) {
        let that = this;
        let q = this.props.matchId;
        console.log(this.state.msg)
        console.log(this.state.prediction)
        if (this.state.prediction) {
            axios.post('http://api.tahmin.io/v1/matches/' + q + '/predictions/', {
                text: this.state.msg,
                game: this.state.prediction
            }, { 'headers': { 'Authorization': "Token " + localStorage.getItem('tahmin.io-token') } })
                .then(function (r) {
                    console.log(r.data);
                    that.setState({
                        data: r.data,
                        msg: null,
                        showMsgBox: false,
                    })
                })
                .catch(function (e) { console.log(e); })
        }
    }

    render() {
        let { game } = this.props
        let msgBox = this.state.showMsgBox ?
            <div>
                <input id="msg-form" type="text" placeholder={'Message'} defaultValue={this.state.msg} onChange={this.handleMsgChange} />
                <button onClick={this.handlePrediction}> Submit </button>
            </div> : '';
        if (game) {
            return (
                <div>
                    {game.map((val, i) => {
                        return <div key={uuidv4()}> {<a onClick={this.handleClick} style={{ cursor: 'pointer' }}>{val.string}</a>} {val.odd}</div>
                    })}
                    {msgBox}
                </div>
            )
        }
    }
}

Game.propTypes = propTypes

export default Game;