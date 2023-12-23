import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

materials = {'whiskey': 23, 'gin': 24,'herbal mix': 25,'lemon': 12,'berry': 16}
for (ingredient, pin) in materials:
    GPIO.setup(pin, GPIO.OUT)

recipe_file = open('recipes.txt', 'r', encoding = 'utf-8')

def pour(ingredient, units): #2 sec. at full power = 1 unit
    GPIO.output(materials[ingredient], GPIO.HIGH)
    time.sleep(units*2)
    GPIO.output(materials[ingredient], GPIO.LOW)