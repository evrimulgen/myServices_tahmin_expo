import React, { Component } from 'react';
import { View, Text, ScrollView, Image, TouchableOpacity, StyleSheet, Button } from 'react-native';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Actions } from 'react-native-router-flux';
import { 
  userGetMe,
  logoutUser,
  userDeleteMe,
  onCityChanged,
  onMenuStateChanged,
} from '../redux/actions';
import axios from "axios";

const uri = 'https://pickaface.net/gallery/avatar/Opi51c74d0125fd4.png';

class Menu extends Component {
  constructor(props) {
      super(props);
      this.state = {
         items: [],
         error: null,
         city: "unknown"
      }
    }

  // console.log(onItemSelected)
  // isOpen = useSelector(state => state.navigateReducer.isOpen)
  // city = useSelector(state => state.navigateReducer.city)
  // dispatch = useDispatch()  
  // CITY_CHANGE = 'CITY_CHANGE'
  
  sideBar(foo) {
    var promise1 = new Promise((resolve, reject) => {
      resolve(this.props.onMenuStateChanged(!this.props.menu_state))
      console.log("worked")
    });
    promise1.then( () => {
      console.log("worked2")
      foo()
    })
  }

  myLoc() {
    navigator.geolocation.getCurrentPosition(
      (position) => 
      this.convertCoords(
        position.coords.latitude,
        position.coords.longitude
      ),
      // let loc = `latitude: ${position.coords.latitude}, longitude: ${position.coords.longitude}`,//convertCoords(position),
      (error) => console.log(error),//this.setState({ error: error.message }),
      { enableHighAccuracy: true, timeout: 20000, maximumAge: 1000},
    )
  }

  convertCoords(latitude, longitude) {
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
      this.props.onCityChanged(text);
      // dispatch({ 
      //     type: CITY_CHANGE, 
      //     payload: text
      // })
    }, (err) => {
      console.log("error happened; you need to catch it...", err);
    });
  };

  render() {
    return (
      <ScrollView scrollsToTop={false} style={styles.menu}>
        <View style={styles.avatarContainer}>
          <Image
            style={styles.avatar}
            source={{ uri }}
          />
          <Text style={styles.name}>{this.props.username}</Text>
          <Button
            title="Home"
            onPress={() => this.sideBar(Actions.Home)}
          />
          <Button
            title="Services"
            onPress={() => this.sideBar(Actions.Services)}
          />
          <Button
            title="Notifications"
            onPress={() => this.sideBar(Actions.Links)}
          />
          <Button
            title="Profile"
            onPress={() => this.sideBar(Actions.Login) }
          />
          <Button
            title="Settings"
            onPress={() => this.sideBar(Actions.UserPage)}
          />
        </View>
        <TouchableOpacity onPress={() => this.myLoc() }>
          <Text>city:{this.props.city}</Text>
        </TouchableOpacity>
      </ScrollView>
    );
  }
  
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
});

const mapStateTopProps = state => {
  console.log(state)
  return {
    user: state.UserReducer.user,
    username: state.UserReducer.username,
    token: state.UserReducer.token,
    loading: state.UserReducer.loading,
    error: state.UserReducer.error,
    city: state.CityReducer.city,
    menu_state: state.CityReducer.menu_state,
  };
};

export default connect(mapStateTopProps, { 
  userGetMe, logoutUser, userDeleteMe, onCityChanged, onMenuStateChanged
})(Menu);