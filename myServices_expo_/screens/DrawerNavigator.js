import React from 'react';
import { Platform, Dimensions } from 'react-native';
//import { createDrawerNavigator, createAppContainer } from 'react-navigation';

import Menu from './MenuHalfScreen';

import {createDrawerNavigator} from 'react-navigation-stack'



const Drawer = createDrawerNavigator();

function MyDrawer() {
  return (
    <Drawer.Navigator>
      <Drawer.Screen name="Feed" component={MenuHalfScreen} />
      <Drawer.Screen name="Article" component={MenuHalfScreen} />
    </Drawer.Navigator>
  );
}


const WIDTH = Dimensions.get('window').width;

const DrawerConfig = {
	drawerWidth: WIDTH*0.83,
}
const DrawerNavigator = createDrawerNavigator({
	Home: {
		screen: MenuHalfScreen
	},
}, DrawerConfig)

export default MyDrawer;