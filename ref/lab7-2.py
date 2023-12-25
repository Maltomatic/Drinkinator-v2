import time
import traceback
import threading

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

BUZZER_PIN = 24
SERVO_PIN = 23
SERVO_FREQ = 50
LED1_PIN = 18
LED2_PIN = 25
BTN_PIN = 4

is_train = False
degree = 90

GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(LED1_PIN, GPIO.OUT)
GPIO.setup(LED2_PIN, GPIO.OUT)
GPIO.setup(BTN_PIN, GPIO.IN, GPIO.PUD_DOWN)

servo = GPIO.PWM(SERVO_PIN, SERVO_FREQ)

def button_callback(_channel):
    global is_train

    is_train = not is_train
    print(f"{is_train=}")


def degree_worker():
    global degree

    while True:
        if is_train:
            degree = max(0, degree - 5)
        else:
            degree = min(90, degree + 5)

        change_degree(degree)
        time.sleep(0.2)


def led_worker():
    led_mode = 0

    while True:
        if is_train:
            led_mode = 2 | led_mode ^ 0b1
        else:
            led_mode = 2 | led_mode ^ 0b1

            if degree == 90:
                led_mode ^= 2

        set_led(led_mode)
        time.sleep(0.2)


def buzzer_worker():
    buzzer_enable = 0

    while True:
        if is_train:
            buzzer_enable = True
        else:
            if degree == 90:
                buzzer_enable = False

        if buzzer_enable:
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
        else:
            time.sleep(0.1)
            GPIO.output(BUZZER_PIN, GPIO.LOW)

        time.sleep(0.1)


def change_degree(degree):
    cycle = 2 + (degree / 18)
    servo.ChangeDutyCycle(cycle)


def set_led(mode):
    if mode & 2 == 0:
        GPIO.output(LED1_PIN, GPIO.LOW)
        GPIO.output(LED2_PIN, GPIO.LOW)
    elif mode & 1 == 0:
        GPIO.output(LED1_PIN, GPIO.HIGH)
        GPIO.output(LED2_PIN, GPIO.LOW)
    elif mode & 1 == 1:
        GPIO.output(LED2_PIN, GPIO.HIGH)
        GPIO.output(LED1_PIN, GPIO.LOW)


servo.start(0)
change_degree(degree)

GPIO.output(BUZZER_PIN, GPIO.LOW)
GPIO.output(LED1_PIN, GPIO.LOW)
GPIO.output(LED2_PIN, GPIO.LOW)

GPIO.add_event_detect(BTN_PIN, GPIO.RISING, callback=button_callback)

try:
    degree_thread = threading.Thread(target=degree_worker)
    led_thread = threading.Thread(target=led_worker)
    buzzer_thread = threading.Thread(target=buzzer_worker)

    degree_thread.start()
    led_thread.start()
    buzzer_thread.start()

    degree_thread.join()
    led_thread.join()
    buzzer_thread.join()

    # while True:
    #     time.sleep(1)
except:
    traceback.print_exc()
finally:
    GPIO.cleanup()