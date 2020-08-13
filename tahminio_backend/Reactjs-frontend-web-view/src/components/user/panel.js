import React, { Component } from 'react';
import PropTypes from 'prop-types';
import AuthHandler from '../auth/authhandler'
import Search from './search'
import './css/panel.css'
import { Row, Col } from 'reactstrap';


const propTypes = {
sendData: PropTypes.func.isRequired
}

class Panel extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: 'Guest',
        };
        this.getData = this.getData.bind(this);
    }

    getData(c) {
        console.log(c);
        if (c !== null) {
            this.props.sendData(true)
            this.setState({
                username: c.data.username
            })

        }
        else {
            this.props.sendData(false)
            this.setState({
                username: 'Guest'
            })
        }
    }



    render() {
        return (
            <div className="panel-container">
                <Row>
                    <Col lg="8">
                        <Search />
                    </Col>
                    <Col lg="4">
                        <div className="auth-container">
                            <div className="auth"> Welcome {this.state.username} </div>
                            <br/>
                            <div className="auth"><AuthHandler sendData={this.getData} /> </div>
                        </div>
                    </Col>
                </Row>
            </div>
        )
    }
}

Panel.propTypes = propTypes

export default Panel;