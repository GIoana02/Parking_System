import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Image } from 'react-native';

const MenuScreen = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('Profile')}>
        <Image
          source={require('./images/user.png')} 
          style={styles.image}
        />
        <Text style={styles.buttonText}>My Profile</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('Reservation')}>
        <Image
          source={require('./images/reservation.png')}
          style={styles.image}
        />
        <Text style={styles.buttonText}>Reservation</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#282c34',
  },
  button: {
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#9acd32',
    borderRadius: 10,
    padding: 20,
    margin: 10,
    width: 200,
    height: 200,
    position: 'relative',
  },
  image: {
    width: 120, // Adjust the width of the image as needed
    height: 120, // Adjust the height of the image as needed
    marginBottom: 10,
  },
  buttonText: {
    color: '#ffffff',
    fontSize: 18,
  },
});

export default MenuScreen;
