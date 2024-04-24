import React from 'react';
import { View, Button, StyleSheet } from 'react-native';

const MenuScreen = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <Button title="My Profile" onPress={() => navigation.navigate('Profile')} />
      <Button title="Reservation" onPress={() => navigation.navigate('Reservation')} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default MenuScreen;
