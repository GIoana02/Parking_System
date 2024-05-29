#include <ESP32Servo.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "secrets.h"

Servo myservo;
const int IRPin = 34, trigPin = 33, echoPin = 32, trigPin2 = 21, echoPin2 = 19;
const int trigPin3 = 25, echoPin3 = 26, servoPin = 18;
const int ledPin1 = 22, ledPin2 = 23, ledPin3 = 2, ledPin4 = 4;
int CAR_SPOTS = 2;
const int MAX_CAR_SPOTS = 2;

WiFiClientSecure net;
PubSubClient client(net);

// Global variables to store the state
int lastCarSpots = 2;
bool lastPrivateSpotStatus = false;


void setup() {
  Serial.begin(115200);
  connectWiFiAndMQTT();

  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);
  myservo.setPeriodHertz(50);
  myservo.attach(servoPin, 500, 2400);

  pinMode(IRPin, INPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);
  pinMode(trigPin3, OUTPUT);
  pinMode(echoPin3, INPUT);
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin3, OUTPUT);
  pinMode(ledPin4, OUTPUT);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();
  monitorParkingSystem();
  delay(100);
}

bool isPrivateSpotOccupied = false;

void monitorParkingSystem() {
  // Ultrasonic sensor logic for car entries and exits
  long duration, distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2; // Convert time to distance

  int IRValue = analogRead(IRPin);

  if (distance < 5 && CAR_SPOTS > 0) { // Car is very close and spots are available
    CAR_SPOTS--;
    Serial.print("Car entered, remaining spots: ");
    Serial.println(CAR_SPOTS);
    myservo.write(90); // Open barrier
    delay(1000); // Keep barrier open briefly
    myservo.write(0); // Close barrier
    publishMessage(CAR_SPOTS);
    delay(3000); // Delay to prevent rapid re-triggering
  } else if (distance > 10) { // No car within close proximity
    if (CAR_SPOTS == 0) {
      Serial.println("No spots available, barrier remains closed.");
    } else {
      myservo.write(0); // Ensure the barrier is closed if no car is detected within immediate range
    }
  }

  if (IRValue < 1000 && CAR_SPOTS < MAX_CAR_SPOTS) { // IR sensor detects a car exiting
    CAR_SPOTS++;
    Serial.print("Car exited, available spots: ");
    Serial.println(CAR_SPOTS);
    myservo.write(90); // Open barrier
    delay(1000); // Keep barrier open briefly
    myservo.write(0); // Close barrier
    publishMessage(CAR_SPOTS);
    delay(3000); // Delay to prevent rapid re-triggering
  }

  // Monitor additional parking spots
  monitorParkingSpot(trigPin2, echoPin2, ledPin1, ledPin2, true);
  monitorParkingSpot(trigPin3, echoPin3, ledPin3, ledPin4, false);
}

void monitorParkingSpot(int trigPin, int echoPin, int ledPinRed, int ledPinGreen, bool isPrivate) {
    static unsigned long privateSpotTimer = 0; // Timer for private spot
    static unsigned long nonPrivateSpotTimer = 0;
    static bool privatePreviouslyOccupied = false; // Track previous occupation status for private spot
    static bool nonPrivatePreviouslyOccupied = false; // Track previous occupation status for non-private spot

    long duration, distance;
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    duration = pulseIn(echoPin, HIGH);
    distance = duration * 0.034 / 2; // Convert time to distance

    bool carPresent = distance < 5;

    if (carPresent) {
        if (isPrivate) {
            if (!isPrivateSpotOccupied) {
                isPrivateSpotOccupied = true;
                privateSpotTimer = millis(); // Start timing when car is first detected
            }
            if (!privatePreviouslyOccupied && isPrivateSpotOccupied && (millis() - privateSpotTimer > 5000)) {
                // Check if 20 seconds have passed and the spot was previously unoccupied
                digitalWrite(ledPinRed, LOW);
                digitalWrite(ledPinGreen, HIGH);
                sendPrivateSpotUpdate(true);  // Send true when a car parks
                privatePreviouslyOccupied = true; // Update the state to occupied
            }
        } else {
            if (!nonPrivatePreviouslyOccupied) {
                nonPrivateSpotTimer = millis(); // Start timing when car is first detected for non-private spots
                nonPrivatePreviouslyOccupied = true;
            }
            if (nonPrivatePreviouslyOccupied && (millis() - nonPrivateSpotTimer > 5000)) {
                digitalWrite(ledPinRed, LOW);
                digitalWrite(ledPinGreen, HIGH);
                //sendNonPrivateSpotUpdate(true);  // Send true after 5 seconds of car being present
            }
        }
    } else {
        digitalWrite(ledPinRed, HIGH);
        digitalWrite(ledPinGreen, LOW);
        if (isPrivate && privatePreviouslyOccupied) {
            sendPrivateSpotUpdate(false);  // Send false when a car leaves
            isPrivateSpotOccupied = false;
            privatePreviouslyOccupied = false; // Reset the occupied flag
        } else if (!isPrivate && nonPrivatePreviouslyOccupied) {
            //sendNonPrivateSpotUpdate(false);  // Immediate update for non-private spots
            nonPrivatePreviouslyOccupied = false;
        }
    }
}


void connectWiFiAndMQTT() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.println("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  net.setCACert(AWS_CERT_CA);
  net.setCertificate(AWS_CERT_CRT);
  net.setPrivateKey(AWS_CERT_PRIVATE);
  client.setServer(AWS_IOT_ENDPOINT, 8883);

  while (!client.connect(THINGNAME)) {
    Serial.print(".");
    delay(100);
  }
  Serial.println("Connected to AWS IoT");
  client.subscribe("parkingSystem/slots/slot1/status");
}

void connectWiFi() {
  while (WiFi.status() != WL_CONNECTED) {
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi");
}

void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(THINGNAME)) {
      Serial.println("connected");
      // Resubscribe or publish a connect message if needed
      client.subscribe("parkingSystem/slots/slot1/status");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void publishMessage(int spotsAvailable) {
  StaticJsonDocument<200> doc;
  doc["time"] = millis();
  doc["availableSpots"] = spotsAvailable;
  char jsonBuffer[512];
  serializeJson(doc, jsonBuffer);
  client.publish("parkingSystem/slots/slot1/status", jsonBuffer);
}

void sendPrivateSpotUpdate(bool status) {
    StaticJsonDocument<200> doc;
    doc["time"] = millis();
    doc["occupied"] = status;
    char jsonBuffer[512];
    serializeJson(doc, jsonBuffer);
    client.publish("parkingSystem/slots/slot1/status", jsonBuffer);
}