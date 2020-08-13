import React, { Component } from 'react';
import Panel from '../user/panel';
import MatchList from '../match/matchlist';
import Leaderboard from '../user/leaderboard';
import { Container, Row, Col } from 'reactstrap';
import './css/App.css'
import Feed from './feed'
import Sidebar from './sidebar'
import Header from './header'

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      authed: null
    };
    this.getData = this.getData.bind(this)
  }

  getData(c) {
    this.setState({
      authed: c
    })
  }

  render() {
    let feed = this.state.authed ? <Feed /> : ''
    return (
      <div>
        <Header sendData={this.getData} />
        <Row>
          <Col lg="3"> <Sidebar /> </Col>
          <Col lg="6">
            <MatchList />
          </Col>
          <Col lg="3"> {feed} </Col>
        </Row>
      </div>
    );
  }
}
export default App;
