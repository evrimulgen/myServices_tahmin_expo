import React, { Component } from 'react';
import Panel from '../user/panel';
import { Container, Row, Col } from 'reactstrap';
import './css/header.css'
import PropTypes from 'prop-types'

const propTypes = {
    sendData: PropTypes.func.isRequired
}

class Header extends Component {
    constructor(props) {
        super(props);
        this.state = {
            authed: null
        };
        this.getData = this.getData.bind(this)
    }

    getData(c) {
        this.props.sendData(c)
        this.setState({
            authed: c
        })
    }

    render() {
        return (
            <div className="header-container">
                <Row>
                    <Col lg="3"> <div className="logo"> <a href="/"> home </a> </div> </Col>
                    <Col lg="9" className="header">
                        <Panel sendData={this.getData} />
                    </Col>
                </Row>
            </div>
        );
    }
}
export default Header;
