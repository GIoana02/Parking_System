import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';

const ProfilePage = () => {
  const [name, setName] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [carPlateIds, setCarPlateIds] = useState([]);

  const handleSave = () => {
    // Implement save profile logic here
    console.log('Name:', name);
    console.log('Phone Number:', phoneNumber);
    console.log('Car Plate IDs:', carPlateIds);
    // Add logic to save profile data or navigate to confirmation screen
  };

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Name:</Text>
      <TextInput
        style={styles.input}
        value={name}
        onChangeText={setName}
        placeholder="Enter your name"
      />

      <Text style={styles.label}>Phone Number:</Text>
      <TextInput
        style={styles.input}
        value={phoneNumber}
        onChangeText={setPhoneNumber}
        placeholder="Enter your phone number"
      />

      <Text style={styles.label}>Car Plate IDs:</Text>
      {carPlateIds.map((plateId, index) => (
        <TextInput
          key={index}
          style={styles.input}
          value={plateId}
          onChangeText={(text) => {
            const updatedCarPlateIds = [...carPlateIds];
            updatedCarPlateIds[index] = text;
            setCarPlateIds(updatedCarPlateIds);
          }}
          placeholder={`Enter car plate ID ${index + 1}`}
        />
      ))}

      <Button title="Add Car Plate ID" onPress={() => setCarPlateIds([...carPlateIds, ''])} />
      <Button title="Save" onPress={handleSave} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
    backgroundColor: '#282c34',
  },
  label: {
    fontSize: 18,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 10,
  },
  input: {
    height: 40,
    width: '100%',
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 20,
    paddingHorizontal: 10,
    backgroundColor: 'white',
  },
});

export default ProfilePage;
