import RPi.GPIO as GPIO
import time, multiprocessing

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

materials = {'whiskey': 23, 'gin': 24,'herb': 25,'lemon': 12,'berry': 16}
for (ingredient, pin) in materials.items():
    GPIO.setup(pin, GPIO.OUT)
cookbook = {'Fruity Whiskey Sour': 17, 'Bramble': 27, 'Last Word riff': 22, 'Final Ward riff': 5, 'Boozed Up': 6, 'Embittered': 26}
for (drink, pin) in cookbook.items():
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

recipe_file = open('recipes.txt', 'r', encoding = 'utf-8')
recipe_list = recipe_file.read().split('\n\n')
recipe_file.close()
recipes = {}
for el in recipe_list:
    el = el.split('\n')
    recipe = {}
    for item in el[1:]:
        (amount, source) = item.split(' ', 1)
        recipe[source.strip()] = float(amount)
    recipes[el[0].strip()] = recipe

def pour(ingredient, units): #2 sec. at full power = 1 unit
    GPIO.output(materials[ingredient], GPIO.HIGH)
    time.sleep(units*2 + 0.15)
    GPIO.output(materials[ingredient], GPIO.LOW)

def mix(recipe):
    pool = []
    for ingredient, units in recipe.items():
        p = multiprocessing.Process(target = pour, args = (ingredient, units))
        pool.append(p)
    for p in pool:
        p.start()
    for p in pool:
        p.join()

while(1):
    for drink, pin in cookbook.items():
        if(GPIO.input(pin) == GPIO.HIGH):
            mix(recipes[drink])
            time.sleep(2)
            break