import React from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import App from '../main/App'
import Main from '../match/main'

const Routes = () => (
    <Router>
        <div>
            <Route exact path="/" component={App} />
            <Route path="/match/:id" component={Main} />
            </div>
    </Router>
);

export default Routes;