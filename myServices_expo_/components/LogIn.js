import { View, Text, KeyboardAvoidingView, Animated, Button, TouchableOpacity, Dimensions } from 'react-native';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { 
  usernameChanged,
  passwordChanged,
  userLogin,
  logoutUser,
  pageChanged,
} from '../redux/actions';
import { Card, CardSection, Input, Spinner } from './common';
import styled from 'styled-components/native';
import SignUp from './SignUp';
import { Actions } from 'react-native-router-flux';

const HEIGHT = Dimensions.get('window').height;

var _animate =  new Animated.Value(10) 

class Login extends Component {
  state = { formStatus: 'login'};

  startAnimationAQ() {
    // ONLY SPRING WORKS FOR SOME FUCKING REASON FIND WHY AND FIX AMK SEYINI
    // CANNOT ANIMATE SHIT!!!
    Animated.spring(_animate, {
      toValue: 1000,
      duration: 10,
      useNativeDriver: false, // <-- Add this
    }).start();
  }
        
  onUsernameChange(text) {
    this.props.usernameChanged(text);
  }
  
  onPasswordChange(text) {
    this.props.passwordChanged(text);
  }

  onButtonPress() {
    const { username, password } = this.props;
    //var username = 'mirkan1';
    //var password = 'anadolu123';
    this.props.userLogin({ username, password });
  }

  onLogoutUser() {
    const { token } = this.props.user.data;
    this.props.logoutUser({ token });
  }

  renderError() {
    if (this.props.error) {
      return (
        <View style={{ backgroundColor: 'white' }}>
          <Text style={styles.errorTextStyle}>
            {this.props.error}
          </Text>
        </View>
      );
    }
  }

  renderButton() {
    if (this.props.loading) {
      return <Spinner size="large" />;
    }
    return (

      <View style={{ height: HEIGHT}}>
        {/* <Animated.View style={styles.myStyle} /> */}

        {/* <Button block style={{ marginLeft: 40, marginRight: 40, marginTop: 10, flex: 1 }} onPress={() => this.startAnimationAQ()}>
          <Text> click me </Text>
        </Button> */}

        <TouchableOpacity  
          style={styles.appButtonContainer} 
          onPress={this.onButtonPress.bind(this)} 
        >
          <Text style={styles.appButtonText}>Login</Text>
        </TouchableOpacity>
          <View style={{ display: "flex", alignItems: "center" }}>
            <Text style={{top: "50%",left: "50%"}}>or</Text>
          </View>

          <TouchableOpacity 
            style={styles.appButtonContainer} 
            onPress={() => Actions.SignUp()}>
            <Text style={styles.appButtonText}>Sign Up</Text>
          </TouchableOpacity>
      </View>
    );
  }

  render() {
    return (
      <KeyboardAvoidingView behavior="padding">
        <Card>
          <Text style={{fontSize: 18}}>Username</Text>
          <CardSection>
            <Input 
              style={styles.inputStyle, { borderRadius: "25px" }}
              placeholder="username123"
              onChangeText={this.onUsernameChange.bind(this)}
              value={this.props.username}
              returnKeyType="next"
              autoCorrect={false}
              autoCapitalize="none"
            />
          </CardSection>

          <Text style={{fontSize: 18}}>Password</Text>
          <CardSection>
            <Input
              style={styles.inputStyle, { borderRadius: "25px" }}
              secureTextEntry
              placeholder="password"
              onChangeText={this.onPasswordChange.bind(this)}
              value={this.props.password}
              returnKeyType="go"
              autoCorrect={false}
              autoCapitalize="none"
            />
          </CardSection>
        </Card>
        {this.renderError()}
        
        {this.renderButton()}
      </KeyboardAvoidingView>
    );
  }
};

const Login_button = styled.TouchableOpacity`
  font-size: 180px;
  margin: 50px;
`
const Title = styled.Text`
	font-size: 20px;
	font-weight: 500;
	color: palevioletred;
`;

const styles = {
  appButtonContainer: { backgroundColor: "#3F98FF", borderRadious: 10, paddingVertical: 10, paddingHorizantal: 12, marginLeft: "10%", marginRight: "10%"}, 
  appButtonText: { fontSize: 18, color: "#fff", fontWeight: "bold", alignSelf: "center", textTransform: "uppercase"},
  errorTextStyle: {
    fontSize: 20,
    alignSelf: 'center',
    color: 'red'
  },
  inputStyle: {
    height: 400,
  },
  myStyle: {
    backgroundColor: 'red', width: _animate, height: _animate
  }
};

const mapStateToProps = state => {
  console.log(state)
  return {
    username: state.UserReducer.username,
    password: state.UserReducer.password,
    error: state.UserReducer.error,
    loading: state.UserReducer.loading,
    user: state.UserReducer.user,
    page: state.PageReducer.pageName,
  };
};

export default connect(mapStateToProps, { 
  usernameChanged, passwordChanged, userLogin, logoutUser, pageChanged,
})(Login);