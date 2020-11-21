import { 
  CITY_CHANGE,
  MENU_STATE
} from '../actions/types';

const INITIAL_STATE = {
  city: "unknown",
  menu_state: false,
};

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case CITY_CHANGE:
      return { ...state, city: action.payload };
    case MENU_STATE:
      return { ...state, menu_state: action.payload };
    default:
      return state;
  }
};