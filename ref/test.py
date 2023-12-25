import time
import traceback

import RPi.GPIO as GPIO


GPIO.setwarnings(False)

BUZZER_PIN = 24
SERVO_PIN = 23
SERVO_FREQ = 50
LED1_PIN = 18
LED2_PIN = 25
BTN_PIN = 4

is_train = False
degree = 90
led_mode = 0
buzzer_enable = False

GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(LED1_PIN, GPIO.OUT)
GPIO.setup(LED2_PIN, GPIO.OUT)
GPIO.setup(BTN_PIN, GPIO.IN, GPIO.PUD_DOWN)

servo = GPIO.PWM(SERVO_PIN, SERVO_FREQ)

def change_degree(degree):
    cycle = int(2 + (degree / 18))
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

try:
    while True:
        if GPIO.input(BTN_PIN) == GPIO.HIGH:
            is_train = not is_train
            print(f"{is_train=}")

        if is_train:
            degree = max(0, degree - 10)
            led_mode = 2 | led_mode ^ 0b1

            buzzer_enable = True

        else:
            degree = min(90, degree + 10)
            led_mode = 2 | led_mode ^ 0b1

            if degree == 90:
                led_mode ^= 2
                buzzer_enable = False

        change_degree(degree)
        set_led(led_mode)

        if buzzer_enable:
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(BUZZER_PIN, GPIO.LOW)

        time.sleep(0.5)
except:
    traceback.print_exc()
finally:
    GPIO.cleanup()
