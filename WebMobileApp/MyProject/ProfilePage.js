import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, TouchableOpacity } from 'react-native';
import { Picker } from '@react-native-picker/picker';

const ProfilePage = () => {
  const [name, setName] = useState('John Doe'); // Example default value
  const [email, setEmail] = useState('john.doe@example.com'); // Example default value
  const [phoneNumber, setPhoneNumber] = useState('123-456-7890'); // Example default value
  const [carPlateIds, setCarPlateIds] = useState(['ABC123', 'XYZ789']); // Example default values
  const [selectedCarPlateId, setSelectedCarPlateId] = useState('');

  const handleSave = () => {
    // Implement save profile logic here
    console.log('Name:', name);
    console.log('Email:', email);
    console.log('Phone Number:', phoneNumber);
    console.log('Car Plate IDs:', carPlateIds);
    // Add logic to save profile data or navigate to confirmation screen
  };

  const handleAddCarPlateId = () => {
    setCarPlateIds([...carPlateIds, '']);
  };

  const handleUpdateCarPlateId = (text, index) => {
    const updatedCarPlateIds = [...carPlateIds];
    updatedCarPlateIds[index] = text;
    setCarPlateIds(updatedCarPlateIds);
  };

  const handleDeleteCarPlateId = (index) => {
    const updatedCarPlateIds = carPlateIds.filter((_, i) => i !== index);
    setCarPlateIds(updatedCarPlateIds);
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

      <Text style={styles.label}>Email:</Text>
      <TextInput
        style={styles.input}
        value={email}
        onChangeText={setEmail}
        placeholder="Enter your email"
      />

      <Text style={styles.label}>Phone Number:</Text>
      <TextInput
        style={styles.input}
        value={phoneNumber}
        onChangeText={setPhoneNumber}
        placeholder="Enter your phone number"
      />

      <Text style={styles.label}>Select Car Plate ID:</Text>
      <Picker
        selectedValue={selectedCarPlateId}
        style={styles.picker}
        onValueChange={(itemValue) => setSelectedCarPlateId(itemValue)}
      >
        {carPlateIds.map((plateId, index) => (
          <Picker.Item key={index} label={plateId} value={plateId} />
        ))}
      </Picker>

      <Text style={styles.label}>Add or Update Car Plate IDs:</Text>
      {carPlateIds.map((plateId, index) => (
        <View key={index} style={styles.carPlateRow}>
          <TextInput
            style={styles.input}
            value={plateId}
            onChangeText={(text) => handleUpdateCarPlateId(text, index)}
            placeholder={`Enter car plate ID ${index + 1}`}
          />
          <TouchableOpacity
            style={styles.deleteButton}
            onPress={() => handleDeleteCarPlateId(index)}
          >
            <Text style={styles.deleteButtonText}>Delete</Text>
          </TouchableOpacity>
        </View>
      ))}

      <Button title="Add Car Plate ID" onPress={handleAddCarPlateId} color="#9acd32" />
      <View style={styles.buttonSpace} />
      <Button title="Save" onPress={handleSave} color="#9acd32" />
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
  picker: {
    height: 50,
    width: '100%',
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 20,
    backgroundColor: 'white',
  },
  carPlateRow: {
    flexDirection: 'row',
    alignItems: 'center',
    width: '100%',
    marginBottom: 10,
  },
  deleteButton: {
    backgroundColor: '#ff6347',
    padding: 10,
    marginLeft: 10,
    borderRadius: 5,
  },
  deleteButtonText: {
    color: 'white',
  },
  buttonSpace: {
    height: 20,
  },
});

export default ProfilePage;
