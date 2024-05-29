import React, { useState } from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import { Picker } from '@react-native-picker/picker';

const Reservation = () => {
  const carPlateIds = ['ABC123', 'XYZ789', 'DEF456']; // Sample car plate IDs
  const timeSlots = ['10:00 AM - 12:00 PM', '12:00 PM - 02:00 PM', '02:00 PM - 04:00 PM']; // Sample time slots

  const [selectedCarPlateId, setSelectedCarPlateId] = useState(carPlateIds[0]);
  const [selectedTimeSlot, setSelectedTimeSlot] = useState(timeSlots[0]);

  const handleReservation = () => {
    console.log('Car Plate ID:', selectedCarPlateId);
    console.log('Time Slot:', selectedTimeSlot);
    // Add logic to save reservation data or navigate to confirmation screen
  };

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Select Car Plate ID:</Text>
      <View style={styles.pickerContainer}>
        <Picker
          selectedValue={selectedCarPlateId}
          onValueChange={(itemValue) => setSelectedCarPlateId(itemValue)}
          style={styles.picker}
        >
          {carPlateIds.map((plateId, index) => (
            <Picker.Item key={index} label={plateId} value={plateId} />
          ))}
        </Picker>
      </View>

      <Text style={styles.label}>Select Time Slot:</Text>
      <View style={styles.pickerContainer}>
        <Picker
          selectedValue={selectedTimeSlot}
          onValueChange={(itemValue) => setSelectedTimeSlot(itemValue)}
          style={styles.picker}
        >
          {timeSlots.map((slot, index) => (
            <Picker.Item key={index} label={slot} value={slot} />
          ))}
        </Picker>
      </View>

      <Button title="Reserve" onPress={handleReservation} color="#9acd32" />
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
  pickerContainer: {
    borderWidth: 1,
    borderColor: 'gray',
    borderRadius: 5,
    marginBottom: 20,
    width: '100%',
    backgroundColor: 'white',
  },
  picker: {
    height: 50,
    width: '100%',
  },
});

export default Reservation;
