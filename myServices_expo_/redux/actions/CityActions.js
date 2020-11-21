import axios from 'axios';
import { Actions } from 'react-native-router-flux';
var qs = require('qs');

import { 
  CITY_CHANGE,
  MENU_STATE,
} from './types';

const allowed_host = "http://127.0.0.1:8000";

export const onCityChanged = (text) => {
  return {
    type: CITY_CHANGE,
    payload: text
  };
};

export const onMenuStateChanged = (text) => {
  return {
    type: MENU_STATE,
    payload: text
  };
};