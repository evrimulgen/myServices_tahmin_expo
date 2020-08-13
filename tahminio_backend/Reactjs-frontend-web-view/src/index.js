import React from 'react';
import ReactDOM from 'react-dom';
import Routes from './components/routes/routes';
import registerServiceWorker from './registerServiceWorker';
import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';

ReactDOM.render(<Routes />, document.getElementById('root'));
registerServiceWorker();
