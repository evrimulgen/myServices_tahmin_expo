import { View, Text, TouchableOpacity, Image, ScrollView, Dimensions } from 'react-native';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { 
	userGetMe,
	logoutUser,
	userDeleteMe,
} from '../redux/actions';

const Actions = 'react-native-router-flux';
import { Input } from 'react-native-elements';
import { Button } from 'react-native-elements';

const HEIGHT = Dimensions.get('window').height;

class UserPage extends Component {
	state = { count: 0 }

	onLogoutUser() {
	  const { token } = this.props;
		this.props.logoutUser({ token });
  }

  onUserDeleteMe() {
  	// TODO
  	// make an alert function that ask if you want to delete your account
  	// demand the owner's password
  	const { token } = this.props;
		this.props.userDeleteMe({ token });
  }

  renderForgot() {
    if (this.props.error !== '') {
      return(
        <View>
          <Text style={{ fontSize: 15, textAlign: 'center' }}>Forgot your password or username?</Text>
        </View>
      );
    }
  }

	renderPage() {
	  const { user } = this.props;
	  if (user === null) {
			return (
		    <View>
		        <TouchableOpacity onPress={() => Actions.ForgotInfo()}>

            {this.renderForgot()}
		          
		        </TouchableOpacity>

          <View style={{ flexDirection: "row", flex: 1, alignItems: 'center', marginLeft: 40, marginRight: 40, marginTop: 10, }}>
            <View style={{ flex: 2,borderBottomColor: 'black', borderBottomWidth: 1 }}>
            </View>

            <View style={{ flex: 1, }}>
		          <Text style={{ fontSize: 30, textAlign: 'center' }}>OR</Text>
		        </View>

            <View style={{ flex: 2, borderBottomColor: 'black', borderBottomWidth: 1, }}>
            </View>
          </View>

            <Button block style={{ marginLeft: 40, marginRight: 40, flex: 1, marginTop: 10, }}onPress={() => Actions.SignUp()}>
              <Text style={{ textAlign: 'center', fontSize: 20, }}>Sign Up</Text>
            </Button>
		  	</View>
		  );
	  }

	  return (
      <ScrollView>

        <View style={{ flex: 1, flexDirection: 'column', margin: 25, alignItems: 'center',}}>
          <View>
            <Image 
              source={{ uri: 
                  user.profile_photo !== null
                  ? user.profile_photo
                  : 'https://upload.wikimedia.org/wikipedia/commons/9/97/Anonim.png'
              }}
              style={styles.profilePhoto}
            />
          </View>
          <View>
            <Text>{user.first_name}</Text>
          </View>
          <View>
            <Text>{user.email}</Text>
          </View>
          <View>
            <Text>{user.last_name}</Text>
          </View>
          <View>
            <Text>{user.username}</Text>
          </View>
          <View>
            <Text>{user.bio}</Text>
          </View>
          <View>
            <Text>{user.token}</Text>
          </View>
        </View>

        <Button 
          type="outline" 
          onPress={() => Actions.UpdateMe()}
          title="Update Me"
        />

        <Button 
          type="outline" 
          onPress={this.onLogoutUser.bind(this)}
          title="Log Out"
        />

        <Button 
          type="outline" 
          onPress={this.onUserDeleteMe.bind(this)}
          title="Delete Yourself"
        />

      </ScrollView>
    );
	}

	render() {
		return (
      <View style={{height: HEIGHT}}>
				{this.renderPage()}
      </View>
		);
	}
};

const { width, height } = Dimensions.get("window");
const styles = {
  errorTextStyle: {
    fontSize: 20,
    alignSelf: 'center',
    color: 'red'
  },
  profilePhoto: {
    height: width / 5,
    width: width / 5,
    borderRadius: 64,
    borderWidth: 1,
    borderColor: 'black',
  }
};

const mapStateTopProps = state => {
  return {
    user: state.UserReducer.user,
    token: state.UserReducer.token,
    loading: state.UserReducer.loading,
    error: state.UserReducer.error,
  };
};

export default connect(mapStateTopProps, { 
  userGetMe, logoutUser, userDeleteMe, 
})(UserPage);


       
        	// { !user.is_verified
         //    ? <Button block style={{ flex: 1 }} onPress={this.onUserVerify.bind(this)}>
         //        <Text>Verify your account</Text>
         //      </Button>
        	// 	: null
        	// }