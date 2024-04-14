import RPi.GPIO as GPIO
import time

from gpiozero import Servo

flag = False

servo_pin = 21
servo = Servo(servo_pin)  # Specify the factory for hardware PWM
servo.min()

TRIG1 = 17
ECHO1 = 27
TRIG2 = 22
ECHO2 = 23
TRIG3 = 20
ECHO3 = 26

RED1 = 9
GREEN1 = 10
BLUE1 = 11
RED2 = 24
GREEN2 = 25
BLUE2 = 8
IR_SENSOR = 16

GPIO.setmode(GPIO.BCM)

GPIO.setup(IR_SENSOR, GPIO.IN)

GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)
GPIO.setup(TRIG3, GPIO.OUT)
GPIO.setup(ECHO3, GPIO.IN)

GPIO.setup(RED1, GPIO.OUT)
GPIO.setup(GREEN1, GPIO.OUT)
GPIO.setup(BLUE1, GPIO.OUT)
GPIO.setup(RED2, GPIO.OUT)
GPIO.setup(GREEN2, GPIO.OUT)
GPIO.setup(BLUE2, GPIO.OUT)

def ir_sensor():
    if GPIO.input(IR_SENSOR) == GPIO.LOW:
        return True
    else:
        return False
        
def get_distance(trig, echo):
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)
    pulse_start = time.time()
    pulse_end = pulse_start 

    while GPIO.input(echo) == 0:
        pulse_start = time.time()

    while GPIO.input(echo) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

def get_distance1():
    GPIO.output(TRIG3, True)
    time.sleep(0.00001)
    GPIO.output(TRIG3, False)

    start_time = sleep_time = 0
    while GPIO.input(ECHO3) == 0:
        start_time = time.time()
    while GPIO.input(ECHO3) == 1:
        sleep_time = time.time()
    time_elapsed = sleep_time - start_time
    distance = (time_elapsed * 34300)/2
    return distance

def degrees_to_val(degrees, max_angle = 180):
    return(degrees / max_angle) * 2 - 1

def set_led_color(red_pin, green_pin, blue_pin, color):
    GPIO.output(red_pin, GPIO.HIGH)
    GPIO.output(green_pin, GPIO.HIGH)
    GPIO.output(blue_pin, GPIO.HIGH)

    if color == 'RED':
        GPIO.output(red_pin, GPIO.LOW)
    elif color == 'GREEN':
        GPIO.output(green_pin, GPIO.LOW)

    print(f"LED connected to pins {red_pin}, {green_pin}, {blue_pin} is now {color}")

def check_parking_space(trig, echo, red_pin, green_pin, blue_pin, spot_number):
    distance = get_distance(trig, echo)
    print(f"Distance measured by sensor {spot_number}: {distance} cm")
    if distance < 8:
        set_led_color(red_pin, green_pin, blue_pin, 'RED')
    else:
        set_led_color(red_pin, green_pin, blue_pin, 'GREEN')

try:
    while True:
        infrared_obstacle = ir_sensor()
        check_parking_space(TRIG1, ECHO1, RED1, GREEN1, BLUE1, 1)
        check_parking_space(TRIG2, ECHO2, RED2, GREEN2, BLUE2, 2)
        time.sleep(1)
        
        distance = get_distance1()
        print("Distance: %.1f cm" % distance)
        
        if (distance < 10 or infrared_obstacle) and flag == False:
            print("Object detected")
            servo.value = degrees_to_val(180)
            flag = True
            print(flag)
        elif distance >= 10 and not infrared_obstacle and flag == True:
            time.sleep(1)
            flag = False
            servo.min()
            print(flag)
        time.sleep(1)
        servo.detach()  # Detach the servo to minimize jitter
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
