import { View, Text, TouchableOpacity} from 'react-native';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { 
  usernameChanged,
  emailChanged,
  passwordChanged,
  firstnameChanged,
  lastnameChanged,
  bioChanged,
  logoutUser,
  userSignUp,
  password_second_changed,
  pageChanged,
} from '../redux/actions';
import { navigateReducer } from '../App.js'
import { Card, CardSection, Spinner } from './common'; // Input
import Icon from 'react-native-vector-icons/FontAwesome';
import { Input } from 'react-native-elements';
import { Button } from 'react-native-elements';
import { Actions } from 'react-native-router-flux';
// import { useSelector, useDispatch } from 'react-redux' 
// const navigate = useSelector(state => state.navigateReducer.navigate)
// const city = useSelector(state => state.navigateReducer.city)

// const navigator_changed = () => {
//   return {
//     increment, decrement
//   };
// };

class SignUp extends Component {
  onUsernameChange(text) {
    this.props.usernameChanged(text);
  }

  onEmailChange(text) {
    this.props.emailChanged(text);
  }
  
  onPasswordChange(text) {
    this.props.passwordChanged(text);
  }

  on_Password_second_change(text) {
    this.props.password_second_changed(text);
  }

  onFirstnameChange(text) {
    this.props.firstnameChanged(text);
  }

  onLastnameChange(text) {
    this.props.lastnameChanged(text);
  }

  onBioChange(text) {
    this.props.bioChanged(text);
  }

  onButtonPress() {
    const { 
      username, 
      email, 
      password,
      password_second,
      first_name,
      last_name,
      bio,
    } = this.props;

    var rets = this.props;
    console.log(rets.user);
    this.props.userSignUp({ username, email, password, password_second, first_name, last_name, bio });
    // if (ret.statusText == "Created") {
      //this.props.navigate.navigate("UserPage")
    Actions.UserPage()
      // this.props.pageChanged('UserPage', {
      //       user: this.props.user,
      //     });
    // }
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
      <View>
      <Button
        title="Sign Up"
        type="outline"
        onPress={this.onButtonPress.bind(this)} 
        //onPress={() => }
      />
      </View>
    );
  }

  render() {
    return (
      <Card>
          <Input 
            label="Username"
            //placeholder="username123"
            onChangeText={this.onUsernameChange.bind(this)}
            value={this.props.username}
          />
          <Input
            label="Email"
            //placeholder="email"
            onChangeText={this.onEmailChange.bind(this)}
            value={this.props.email}
          />

       
          <Input
            secureTextEntry
            label="Password"
            //placeholder="password"
            onChangeText={this.onPasswordChange.bind(this)}
            value={this.props.password}
          />
          
          <Input
            secureTextEntry
            label="retype password"
            //placeholder="password"
            onChangeText={this.on_Password_second_change.bind(this)}
            value={this.props.password_second}
          />        

        {this.renderError()}
        
       
          {this.renderButton()}
        
      </Card>
    );
  }
}

const styles = {
  errorTextStyle: {
    fontSize: 20,
    alignSelf: 'center',
    color: 'red'
  }
};
const mapStateTopProps = state => {
  //console.log(state, state.navigateReducer.navigate)
  return {
    username: state.UserReducer.username,
    email: state.UserReducer.email,
    password: state.UserReducer.password,
    password_second: state.UserReducer.password_second,
    first_name: state.UserReducer.first_name,
    last_name: state.UserReducer.last_name,
    bio: state.UserReducer.bio,
    error: state.UserReducer.error,
    loading: state.UserReducer.loading,
    user: state.UserReducer.user,
    page: state.PageReducer.pageName,
  };
};

export default connect(mapStateTopProps, { 
  usernameChanged, 
  emailChanged, 
  passwordChanged, 
  password_second_changed,
  userSignUp, 
  logoutUser, 
  firstnameChanged, 
  lastnameChanged, 
  bioChanged,
  pageChanged,
})(SignUp);

          // <Input
          //   label="first_name"
          //   placeholder="David"
          //   onChangeText={this.onFirstnameChange.bind(this)}
          //   value={this.props.first_name}
          // />
    
          // <Input
          //   label="last_name"
          //   placeholder="LAST"
          //   onChangeText={this.onLastnameChange.bind(this)}
          //   value={this.props.last_name}
          // />
       
          // <Input
          //   label="Biography"
          //   placeholder="tell me about yourself"
          //   onChangeText={this.onBioChange.bind(this)}
          //   value={this.props.bio}
          // />