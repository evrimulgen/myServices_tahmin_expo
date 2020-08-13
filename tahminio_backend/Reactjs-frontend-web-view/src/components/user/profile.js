import React, { Component } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';

const propTypes = {
    data: PropTypes.object.isRequired,
}

class Profile extends Component {
    constructor(props) {
        super(props);
        this.state = {
        };
    }

    render() {
        return (
            <div>
                profile stuff
            </div>
        )
    }
}

Profile.propTypes = propTypes

export default Profile;