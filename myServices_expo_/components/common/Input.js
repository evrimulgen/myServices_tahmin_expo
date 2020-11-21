import React, { Component } from 'react';
import { StyleSheet, View, Text, TextInput } from 'react-native';

const Input = ({ label, value, onChangeText, placeholder, secureTextEntry, returnKeyType, autoCapitalize }) => {
	return (
		<View style={styles.containerStyle}>
			<Text style={styles.labelStyle}>{label}</Text>
			<TextInput
				secureTextEntry={secureTextEntry}
				placeholder={placeholder}
				autoCorrect={false}
				value={value}
				onChangeText={onChangeText}
				style={styles.inputStyle}
				autoCapitalize={autoCapitalize}
				returnKeyType={returnKeyType}
			/>
		</View>
	);
};

const styles = StyleSheet.create({
	inputStyle: {
		color: '#000',
		paddingRight: 5,
		paddingLeft: 5,
		fontSize: 18,
		lineHeight: 23,
		flex: 3,
	},
	labelStyle: {
		fontSize: 18,
		paddingLeft: 20,
		flex: 0,
	},
	containerStyle: {
		height: 40,
		alignItems: 'center',
	},

});


export { Input };

// import Icon from 'react-native-vector-icons/FontAwesome';
// import { Input } from 'react-native-elements';

// <Input
//   placeholder='BASIC INPUT'
// />

// <Input
//   placeholder='INPUT WITH ICON'
//   leftIcon={{ type: 'font-awesome', name: 'chevron-left' }}
// />

// <Input
//   placeholder='INPUT WITH CUSTOM ICON'
//   leftIcon={
//     <Icon
//       name='user'
//       size={24}
//       color='black'
//     />
//   }
// />


//  <Input
//    placeholder="Comment"
//    leftIcon={{ type: 'font-awesome', name: 'comment' }}
//    style={styles}
//    onChangeText={value => this.setState({ comment: value })}
//   />


// <Input
//   placeholder='INPUT WITH ERROR MESSAGE'
//   errorStyle={{ color: 'red' }}
//   errorMessage='ENTER A VALID ERROR HERE'
// />

// <Input placeholder="Password" secureTextEntry={true} />