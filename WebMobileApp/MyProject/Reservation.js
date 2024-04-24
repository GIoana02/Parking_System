import React, { useState } from 'react';
import { View, Text, Picker, Button, StyleSheet } from 'react-native';

const Reservation = () => {
  // Sample data for car plate IDs and time slots
  const carPlateIds = ['ABC123', 'XYZ789', 'DEF456']; // Sample car plate IDs
  const timeSlots = ['10:00 AM - 12:00 PM', '12:00 PM - 02:00 PM', '02:00 PM - 04:00 PM']; // Sample time slots

  const [selectedCarPlateId, setSelectedCarPlateId] = useState('');
  const [selectedTimeSlot, setSelectedTimeSlot] = useState('');

  const handleReservation = () => {
    // Implement reservation logic here
    console.log('Car Plate ID:', selectedCarPlateId);
    console.log('Time Slot:', selectedTimeSlot);
    // Add logic to save reservation data or navigate to confirmation screen
  };

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Select Car Plate ID:</Text>
      <Picker
        selectedValue={selectedCarPlateId}
        style={styles.picker}
        onValueChange={(itemValue, itemIndex) => setSelectedCarPlateId(itemValue)}
      >
        {carPlateIds.map((plateId, index) => (
          <Picker.Item key={index} label={plateId} value={plateId} />
        ))}
      </Picker>

      <Text style={styles.label}>Select Time Slot:</Text>
      <Picker
        selectedValue={selectedTimeSlot}
        style={styles.picker}
        onValueChange={(itemValue, itemIndex) => setSelectedTimeSlot(itemValue)}
      >
        {timeSlots.map((slot, index) => (
          <Picker.Item key={index} label={slot} value={slot} />
        ))}
      </Picker>

      <Button title="Reserve" onPress={handleReservation} />
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
  picker: {
    height: 50,
    width: '100%',
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 20,
    backgroundColor: 'white',
  },
});

export default Reservation;
