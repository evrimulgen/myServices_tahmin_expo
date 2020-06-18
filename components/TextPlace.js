import React from 'react'
import { MonoText } from '../components/StyledText';
import { 
  Platform, 
  StyleSheet, 
  Text, 
  View, 
  TouchableOpacity,
  Linking 
} from 'react-native';
import cities_en from '../assets/cities/cities.js';

function pattern_(prop, index) {
  let link = "https://tr.wikipedia.org/wiki/" + prop
  return (
    <TouchableOpacity 
      style={{ width: "100%"}}
      onPress={() => Linking.openURL(link)}
    >
      <Text>
        {prop}, {index}
      </Text>
    </TouchableOpacity>
  )
}

const cities_en_ = cities_en;
const gotTheText = []

for(let i=0; i<cities_en_.length; i++){
  gotTheText.push(cities_en_)
};
export default function TextPlace() {  
    return (
        <View style={styles.tabBarInfoContainer}>
        <View style={styles.tabBarInfoText}>
          {cities_en_.split(",").map((p, index) => (
            pattern_(p.trim(), index)
          ))}
        </View>

        {/* <View style={[styles.codeHighlightContainer, styles.navigationFilename]}>
          <MonoText style={styles.codeHighlightText}>components/TextPlace.js</MonoText>
        </View> */}
      </View>
    )
}

const styles = StyleSheet.create({
    tabBarInfoContainer: {
        position: 'absolute',
        width: '100%',
        height: '100%',
        //bottom: 0,
        //left: 0,
        //right: 0,
        ...Platform.select({
          ios: {
            shadowColor: 'black',
            shadowOffset: { width: 0, height: -3 },
            shadowOpacity: 0.1,
            shadowRadius: 3,
          },
          android: {
            elevation: 20,
          },
        }),
        alignItems: 'center',
        backgroundColor: '#fbfbfb',
        paddingVertical: 20,
      },
    tabBarInfoText: {
      fontSize: 17,
      color: 'rgba(96,100,109, 1)',
      textAlign: 'center',
    },
    codeHighlightText: {
        color: 'rgba(96,100,109, 0.8)',
    },
    codeHighlightContainer: {
        backgroundColor: 'rgba(0,0,0,0.05)',
        borderRadius: 3,
        paddingHorizontal: 4,
    },
})