import React, { Component } from 'react';
import { connect } from 'react-redux';
import { onMenuStateChanged } from './redux/actions';
import { Platform, StatusBar, StyleSheet } from 'react-native';
import BottomTabNavigator from './navigation/BottomTabNavigator';
import LinkingConfiguration from './navigation/LinkingConfiguration';
import SideMenu from 'react-native-side-menu';
import { Router, Scene } from 'react-native-router-flux';
import Menu from './screens/MenuHalfScreen';
import HomeScreen from './screens/HomeScreen';
import LinksScreen from './screens/LinksScreen';
import ServicesScreen from './screens/ServicesScreen';
import Login from './components/LogIn';
import SignUp from './components/SignUp';
import UserPage from './components/UserPage';
import CityReducer from './redux/reducers/CityReducer';
import {
	View,
	TouchableOpacity,
	Image,
	Text,
} from 'react-native';

const menu = <Menu navigator={navigator}/>;
class Main extends Component {
	toggle(state) {
		this.props.onMenuStateChanged(state)
	}

	render() { 
		return ( 
	      <SideMenu 
	      	isOpen={this.props.menu_state} 
	      	menu={menu}
	      	autoClosing={true}
	      	disableGestures={true}
	      	onChange={(isOpen) => this.toggle(isOpen)}
	      	style={styles.container}>
	      	<MenuButton onPress={() => this.toggle(true)}/>
	        {Platform.OS === 'ios' && <StatusBar barStyle="dark-content" />}
	        <Router>
	          <Scene key="root">
	            <Scene key="Home" component={HomeScreen} />
	            <Scene key="Links" component={LinksScreen} />
	            <Scene key="Services" component={ServicesScreen} />
	            <Scene key="Login" component={Login} />
	            <Scene key="SignUp" component={SignUp} />
	            <Scene key="UserPage" component={UserPage} />
	          </Scene>
	        </Router>
	      </SideMenu>
  		)
	}
}

class MenuButton extends Component {

  handlePress(e) {
    if (this.props.onPress) {
      this.props.onPress(e);
    }
  }

  render() {
    return (
      <View style={styles.menuButton} >
        <TouchableOpacity 
          onPress={this.handlePress.bind(this)}
          style={this.props.style}>
          <Text>{this.props.children}</Text>
          <Image
            source={{ uri: 'http://i.imgur.com/vKRaKDX.png', width: 40, height: 40, }} />        
        </TouchableOpacity>      
      </View>
    );
  }
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
});

const mapStateTopProps = state => {
  return {
    menu_state: state.CityReducer.menu_state,
  };
};

export default connect(mapStateTopProps, { 
  onMenuStateChanged
})(Main);
