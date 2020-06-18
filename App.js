import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import React, { useState } from 'react';
import { Platform, StatusBar, StyleSheet, View, Text, ScrollView, Image, TouchableOpacity } from 'react-native';
import PropTypes from 'prop-types';
import useCachedResources from './hooks/useCachedResources';
import BottomTabNavigator from './navigation/BottomTabNavigator';
import LinkingConfiguration from './navigation/LinkingConfiguration';
import SideMenu from 'react-native-side-menu';

const convertCoords = (position) => {
  return fetch(`https://maps.googleapis.com/maps/api/geocode/jsonlatlng=${position.coords.latitude},${position.coords.longitude}&key=AIzaSyC_qG7UbdSQ8WHm9KmnQ9hhPQdfK7pZFXY`)
  .then((response) => response.json())
  .then((location) => {
    this.setState({
      address: location.results[0].formatted_address,
      longitude: location.results[0].geometry.location.lng,
      latitude: location.results[0].geometry.location.lat
    })
  })
}


const Stack = createStackNavigator();
const uri = 'https://pickaface.net/gallery/avatar/Opi51c74d0125fd4.png';
function Menu({ onItemSelected }) {
  const [loc, setState] = useState({
    latitude: 'Q',
    longitude: 'Q'
  });
  //console.log(setState())
 

  const myLoc = () => {
    navigator.geolocation.getCurrentPosition(
      (position) => 
      setState({
        latitude: position.coords.latitude,
        longitude: position.coords.longitude
      }),
      //loc = `latitude: ${position.coords.latitude}, longitude: ${position.coords.longitude}`,//convertCoords(position),
      (error) => console.log(error),//this.setState({ error: error.message }),
      { enableHighAccuracy: true, timeout:20000, maximumAge: 1000},
    )
  }
  //myLoc()
  return (
    <ScrollView scrollsToTop={false} style={styles.menu}>
      <View style={styles.avatarContainer}>
        <Image
          style={styles.avatar}
          source={{ uri }}
        />
        <Text style={styles.name}>Your name</Text>
      </View>

      <TouchableOpacity onPress={() => myLoc() }>
        <Text>latitude: {loc.latitude}, longitude: {loc.longitude}</Text>
      </TouchableOpacity>

      <Text
        onPress={() => console.log('About')} // onItemSelected("About")
        style={styles.item}
      >
        About
      </Text>

      <Text
        onPress={() => console.log('Contacts')} // onItemSelected("About")
        style={styles.item}
      >
        Contacts
      </Text>
    </ScrollView>
  );
}

Menu.propTypes = {
  onItemSelected: PropTypes.func.isRequired,
};

export default function App(props) {
  const isLoadingComplete = useCachedResources();
  const menu = <Menu navigator={navigator}/>;

  if (!isLoadingComplete) {
    return null;
  } else {
    return (
      <SideMenu menu={menu} style={styles.container}>
        {Platform.OS === 'ios' && <StatusBar barStyle="dark-content" />}
        <NavigationContainer linking={LinkingConfiguration}>
          <Stack.Navigator>
            <Stack.Screen name="Root" component={BottomTabNavigator} />
          </Stack.Navigator>
        </NavigationContainer>
      </SideMenu>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  menu: {
    flex: 1,
    width: window.width,
    height: window.height,
    backgroundColor: 'gray',
    padding: 20,
  },
  avatarContainer: {
    marginBottom: 20,
    marginTop: 20,
  },
  avatar: {
    width: 48,
    height: 48,
    borderRadius: 24,
    flex: 1,
  },
  name: {
    position: 'absolute',
    left: 70,
    top: 20,
  },
  item: {
    fontSize: 14,
    fontWeight: '300',
    paddingTop: 5,
  },
});
