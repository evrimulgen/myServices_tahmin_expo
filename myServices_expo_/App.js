import React, { Component } from 'react';
import useCachedResources from './hooks/useCachedResources';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import ReduxThunk from 'redux-thunk';
import { combineReducers } from 'redux';
import UserReducer from './redux/reducers/UserReducer';
import SearchReducer from './redux/reducers/SearchReducer';
import CityReducer from './redux/reducers/CityReducer';
import PageReducer from './redux/reducers/PageReducer';
import Main from "./Main";
//const Stack = createStackNavigator();
// yeni klosore koy bunu
// gereken varyasyona cevir # axios fln
// const navigateReducer = (state = { count: 0, city: "undefined", navigate: "LANDING_PAGE", isOpen: true }, action) => {
//   switch(action.type) {
//     case "PAGE_CHANGE":
//       // using to navigate between screens
//       return { ...state, navigate: action.payload }
//     case 'CITY_CHANGE':
//       return { ...state, city: action.payload }
//     case "isOpen":
//       // using to navigate between screens
//       console.log(state.isOpen)
//       return { ...state, isOpen: !state.isOpen }
//     default:
//       return state
//   }
// }


export default function App() {
  const combReducers = combineReducers({
    UserReducer,
    SearchReducer,
    CityReducer,
    PageReducer,
  });

  const isLoadingComplete = useCachedResources();
  const store = createStore(combReducers, {}, applyMiddleware(ReduxThunk));
  

  if (!isLoadingComplete) {
    return null;
  } else {
    return (
      <Provider store={store}>
        <Main/>
      </Provider>
    );
  }
  
}



