import React from 'react';
import { SafeAreaView, Text, StyleSheet, Button, View } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import LoginScreen from './LoginScreen';
import RegisterScreen from './RegisterScreen';
import ProfilePage from "./ProfilePage";
import MenuScreen from './MenuScreen';
import Reservation from "./Reservation";


const Stack = createStackNavigator();

const WelcomeScreen = ({ navigation }) => {
  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Welcome to My Private Parking App</Text>
      <View style={styles.buttonContainer}>
        <Button
          title="Login"
          onPress={() => navigation.navigate('Login')}
          color="#9acd32"
          style={styles.button}
        />
        <View style={styles.buttonSpace} />
        <Button
          title="Register"
          onPress={() => navigation.navigate('Register')}
          color="#9acd32"
          style={styles.button}
        />
      </View>
    </SafeAreaView>
  );
};

const App = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Welcome">
        <Stack.Screen name="Welcome" component={WelcomeScreen} />
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Register" component={RegisterScreen} />
        <Stack.Screen name="Profile" component={ProfilePage} />
        <Stack.Screen name="Menu" component={MenuScreen} />
        <Stack.Screen name="Reservation" component={Reservation} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#282c34',
  },
  title: {
    fontSize: 30,
    textAlign: 'center',
    margin: 10,
    color: 'white',
  },
  buttonContainer: {
    flexDirection: 'row',
    marginTop: 30,
  },
  button: {
    marginHorizontal: 20,
    paddingVertical: 25,
    paddingHorizontal: 50,
  },
  buttonSpace: {
    width: 20,
  },
});

export default App;
