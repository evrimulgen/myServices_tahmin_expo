import React, { Component } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import './css/search.css'

class Search extends Component {
    constructor(props) {
        super(props);
        this.state = {
            search: null,
            result: null
        };
        this.handleSearch = this.handleSearch.bind(this);
        this.handle = this.handle.bind(this);
    }

    handleSearch(e) {
        this.setState({ search: e.target.value });
    }
    handle(e) {
        let that = this;
        if (this.state.search != null) {
            axios.get('http://api.tahmin.io/v1/users/?query=' + this.state.search, { // change this to search endpoint
                'headers': { 'Authorization': "Token " + localStorage.getItem('tahmin.io-token') }
            })
                .then(function (r) {
                    console.log(r);
                    that.setState({
                        result: r, // fix this data
                    })
                })
                .catch(function (e) { console.log(e); })
        }
    }

    render() {
        let result = this.state.result ? <div> {this.state.result} </div> : null;
        return (
            <div className="search-container">
                    <input type="text" placeholder={'Search...'} defaultValue={this.state.search} onChange={this.handleSearch} />
                    <button onClick={this.handle}> Search </button>
                    {result}
                </div>
        )

    }
}

export default Search;