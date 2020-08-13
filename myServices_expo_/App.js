import React from 'react';
import { Platform, StatusBar, StyleSheet } from 'react-native';
import useCachedResources from './hooks/useCachedResources';
import BottomTabNavigator from './navigation/BottomTabNavigator';
import LinkingConfiguration from './navigation/LinkingConfiguration';
import SideMenu from 'react-native-side-menu';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import ReduxThunk from 'redux-thunk';
import { createStackNavigator } from '@react-navigation/stack';
import { NavigationContainer } from '@react-navigation/native';
import Menu from './screens/MenuHalfScreen';
import HomeScreen from './screens/HomeScreen';
import LinksScreen from './screens/LinksScreen';
import ServicesScreen from './screens/ServicesScreen';
import Login from './components/LogIn';
import SignUp from './components/SignUp';
import { combineReducers } from 'redux';
import UserReducer from './redux/reducers/UserReducer';
import MatchReducer from './redux/reducers/MatchReducer';
import SearchReducer from './redux/reducers/SearchReducer';
import LeaderboardReducer from './redux/reducers/LeaderboardReducer';
import ForumReducer from './redux/reducers/ForumReducer';

const Stack = createStackNavigator();
// yeni klosore koy bunu
// gereken varyasyona cevir # axios fln
const navigateReducer = (state = { count: 0, city: "undefined", navigate: "LANDING_PAGE" }, action) => {
  switch(action.type) {
    case "PAGE_CHANGE":
      // using to navigate between screens
      return { ...state, navigate: action.payload }
    case 'CITY_CHANGE':
      return { ...state, city: action.payload }
    case 'COUNT_UP':
      return { ...state, count: state.count + 1 }
    case 'COUNT_DOWN': 
      return { ...state, count: state.count - 1 }
    case 'SET_COUNT': 
      return { ...state, count: action.value }
    default:
      return state
  }
}

const combReducers = combineReducers({
  navigateReducer,
  UserReducer,
  MatchReducer,
  SearchReducer,
  LeaderboardReducer,
  ForumReducer,
});

export default function App(props) {
  const isLoadingComplete = useCachedResources();
  const menu = <Menu navigator={navigator}/>;
  const store = createStore(combReducers, {}, applyMiddleware(ReduxThunk));
  console.log(store)
  if (!isLoadingComplete) {
    return null;
  } else {
    return (
      <Provider store={store}>
        <SideMenu menu={menu} style={styles.container}>
          {Platform.OS === 'ios' && <StatusBar barStyle="dark-content" />}
          <NavigationContainer linking={LinkingConfiguration}>
            <Stack.Navigator initialRouteName="Home">
              <Stack.Screen name="Home" component={HomeScreen} />
              <Stack.Screen name="Links" component={LinksScreen} />
              <Stack.Screen name="Services" component={ServicesScreen} />
              <Stack.Screen name="Login" component={Login} />
              <Stack.Screen name="SignUp" component={SignUp} />
            </Stack.Navigator>
          </NavigationContainer>
        </SideMenu>
      </Provider>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
});
