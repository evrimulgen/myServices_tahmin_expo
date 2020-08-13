import React, { useState, useEffect } from 'react';
import { View, Text, ScrollView, Image, TouchableOpacity, StyleSheet, Button } from 'react-native';
import PropTypes from 'prop-types';
import { useSelector, useDispatch } from 'react-redux' 
import axios from "axios";

const uri = 'https://pickaface.net/gallery/avatar/Opi51c74d0125fd4.png';

export default function Menu({ onItemSelected }) {

  const navigate = useSelector(state => state.navigateReducer.navigate)
  const city = useSelector(state => state.navigateReducer.city)
  const dispatch = useDispatch()  
  const CITY_CHANGE = 'CITY_CHANGE'
    
  const myLoc = () => {
    // Promise.resolve()
    navigator.geolocation.getCurrentPosition(
      (position) => 
      convertCoords(
        position.coords.latitude,
        position.coords.longitude
      ),
      // let loc = `latitude: ${position.coords.latitude}, longitude: ${position.coords.longitude}`,//convertCoords(position),
      (error) => console.log(error),//this.setState({ error: error.message }),
      { enableHighAccuracy: true, timeout: 20000, maximumAge: 1000},
    )
  }

  const convertCoords = (latitude, longitude) => {
    // latitude = 31.188502; longitude = 16.584834 // Sirte
    // Access to fetch at 'https://maps.googleapis.com/maps/api/geocode/jsonlatlng=29.917184,-90.03008&key=AIzaSyAO7VpyFushhr6-s6Jt1O5ozkDRxq8QAUk' 
    // from origin 'http://localhost:19006' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource. 
    // If an opaque response serves your needs, set the request's mode to 'no-cors' to fetch the resource with CORS disabled.
    let key = "AIzaSyAzjpQAbCDWukrFmf-tZICJs-kZTxIwFeI";
    let url = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=${key}`;
    axios({
        method: 'get',
        url: url,
    })
    .then( r => {
      let address = r.data.plus_code.compound_code;
      address = address.split(",")[0].split(" ")
      let text = ""
      for (let i = 0; i < address.length; i++) {
        if (i>=1) text = text + " " + address[i]
      }
      dispatch({ 
          type: CITY_CHANGE, 
          payload: text
      })
    }, (err) => {
      console.log("error happened; you need to catch it...", err);
    });
  };

  // setTimeout(
  //   () => {
  //     const navigate = useSelector(state => state.navigate)
  //   }, 300
  // )
  return (
    <ScrollView scrollsToTop={false} style={styles.menu}>
      <View style={styles.avatarContainer}>
        <Image
          style={styles.avatar}
          source={{ uri }}
        />
        <Text style={styles.name}>Your name</Text>
        <Button
          title="Home"
          onPress={() => navigate.navigate('Home')}
        />
        <Button
          title="Services"
          onPress={() => navigate.navigate('Services')}
        />
        <Button
          title="Notifications"
          onPress={() => navigate.navigate('Links')}
        />
        <Button
          title="Profile"
          onPress={() => navigate.navigate('Login')}
        />
        <Button
          title="Settings"
          onPress={() => navigate.navigate('Settings')}
        />
      </View>
      <TouchableOpacity onPress={() => myLoc() }>
        <Text>city:{city}</Text>
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

const styles = StyleSheet.create({
    avatarContainer: {
        marginBottom: 20,
        marginTop: 20,
    },
    menu: {
      flex: 1,
      width: window.width,
      height: window.height,
      backgroundColor: 'gray',
      padding: 20,
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
})