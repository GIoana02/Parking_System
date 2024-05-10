#include <ESP32Servo.h>
#include "WiFiManager.h"

WiFiManager wifiManager;
Servo myservo;  // Create a servo object

const int IRPin = 34;       // GPIO pin connected to the IR sensor's output
const int trigPin = 33;     // GPIO pin connected to the ultrasonic sensor's trigger
const int echoPin = 32;     // GPIO pin connected to the ultrasonic sensor's echo
const int trigPin2 = 21;    // GPIO pin connected to the second ultrasonic sensor's trigger
const int echoPin2 = 19;    // GPIO pin connected to the second ultrasonic sensor's echo
const int trigPin3 = 25;    // GPIO pin connected to the third ultrasonic sensor's trigger
const int echoPin3 = 26;    // GPIO pin connected to the third ultrasonic sensor's echo
const int servoPin = 18;    // GPIO pin connected to the servo motor's PWM input
const int ledPin1 = 22;     // GPIO pin connected to the first LED
const int ledPin2 = 23;     // GPIO pin connected to the second LED
const int ledPin3 = 2;     // GPIO pin connected to the first LED
const int ledPin4 = 4;


void setup() {
  Serial.begin(115200);


  wifiManager.connect("DIGI-3uAM", "VS427Jez");
  if (wifiManager.isConnected()) {
    Serial.println("Connected to wifi");
  }
  Serial.println("HELLLLLLLLLLLLLLLLLLO");
  
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
  long duration, distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and return)

  long duration2, distance2;
  digitalWrite(trigPin2, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin2, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin2, LOW);

  duration2 = pulseIn(echoPin2, HIGH);
  distance2 = duration2 * 0.034 / 2;


  long duration3, distance3;
  digitalWrite(trigPin3, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin3, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin3, LOW);

  duration3 = pulseIn(echoPin3, HIGH);
  distance3 = duration3 * 0.034 / 2;

  int IRValue = analogRead(IRPin);
  Serial.println(IRValue);
  Serial.println(distance3);

  if (distance < 10 || IRValue < 1000) {
    myservo.write(90);
  } else {
    delay(1000);
    myservo.write(0);
  }

  // Control LEDs based on the distance measured by the second ultrasonic sensor
  if (distance2 < 10) {
    digitalWrite(ledPin1, LOW); // Turn on LED 1
    digitalWrite(ledPin2, HIGH);
  } else {
    digitalWrite(ledPin1, HIGH);
    digitalWrite(ledPin2, LOW);
      // Turn off LED 1
    
  }



  if (distance3 < 10) {
    digitalWrite(ledPin3, LOW); // Turn on LED 1
    digitalWrite(ledPin4, HIGH);
  } else {
    digitalWrite(ledPin3, HIGH);
    digitalWrite(ledPin4, LOW);
      // Turn off LED 1
    
  }

}