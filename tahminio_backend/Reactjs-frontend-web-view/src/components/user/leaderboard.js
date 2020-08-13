import React, { Component } from 'react';
import axios from 'axios'
import uuidv4 from 'uuid/v4';

const propTypes = {

}

class Leaderboard extends Component {
    constructor(props) {
        super(props);
        this.state = {
            pages: null,
            data: null,
            page: 1,
            pageList: []
        };
        this.getPages = this.getPages.bind(this);
        this.getLeaderboard = this.getLeaderboard.bind(this);
        this.setPage = this.setPage.bind(this);
    }

    componentDidMount() {
        this.getPages()
        this.getLeaderboard();
    }

    componentDidUpdate(prevProps, prevState) {
        if (!(Object.is(prevState, this.state))) {
            if (this.state.page !== prevState.page) {
                this.getLeaderboard()
            }
        }
    }

    getPages() {
        let that = this;
        let pages = [];
        axios.get('http://api.tahmin.io/v1/leaders/total_pages/').then((res) => {
            that.setState({
                pages: res.data.total_pages // ?;
            })
            console.log(res.data.total_pages)
            for (var i = 0; i < this.state.pages; ++i) {
                let pageLink = <a onClick={this.setPage} style={{ cursor: 'pointer' }}>{i}</a>
                pages.push(pageLink)
            }
            this.setState({
                pageList: pages
            })
        })
    }

    setPage(e) {
        this.setState({
            page: e.target.text
        })
    }

    getLeaderboard() {
        let that = this;
        let { page } = this.state;
        axios.get('http://api.tahmin.io/v1/leaders/' + page + '/').then((res) => {
            that.setState({
                data: res.data
            })
        })
    }


    render() {
        if (this.state.pages !== null && this.state.data !== null && this.state.pageList.length > 0) {
            return (
                <div>
                    {this.state.data.map((val) => { let usr = val.username; return <div key={uuidv4()}> {usr} </div> })}
                    {this.state.pageList.map((val) => {
                        return <span key={uuidv4()}> {val} </span>
                    })}
                </div>
            )
        }
        else return null;
    }
}

Leaderboard.propTypes = propTypes

export default Leaderboard;