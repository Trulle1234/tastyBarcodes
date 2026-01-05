import time
import random
from colorama import init, Fore, Style
from prompt_toolkit import prompt
from openfoodfacts import API, APIVersion, Country, Environment, Flavor
import menu
import ingredients_list
import threading

api = API(
    user_agent="tastyBarcodes/v0.1 (boom@thetwoboom.xyz)",
    username=None,
    password=None,
    country=Country.world,
    flavor=Flavor.off,
    version=APIVersion.v2,
    environment=Environment.org,
)

ingredient_array = []
clock = 60
points = 0
with open("highscore.txt") as f:
    highscore = int(f.readline())

print(f"""
{Fore.CYAN}
 ---------------------------------------------------------------------
| Welcome to                                                          |
|  _______                ____                          _             |
| |__   __|              |  _ \\                        | |            |
|    | | __ _ ___ _   _  | |_) | __ _ _ __ ___ ___   __| | ___  ___   |
|    | |/ _` / __| | | | |  _ < / _` | '__/ __/ _ \\ / _` |/ _ \\/ __|  |
|    | | (_| \\__ \\ |_| | | |_) | (_| | | | (_| (_) | (_| |  __/\\__ |  |
|    |_|\\__,_|___/\\__, | |____/ \\__,_|_|  \\___\\___/ \\__,_|\\___||___/  |
|                  __/ |                                              |
|                 |___/                                               |
 ---------------------------------------------------------------------{Style.RESET_ALL}""")

choice = menu.menu(
    title="Main Menu",
    options=["Play", "Credits", "Exit"],
    cursor_color="green",
    title_color="cyan",
    options_color="white",
)

if choice == "Play":
    pass  # start game

elif choice == "Credits":
    print("Made by _________________")
    input("Press Enter to return")

elif choice == "Exit":
    exit()

clock = int(prompt("Set how many seconds the timer should have: " ).strip())

ingredient_en = random.choice(list(ingredients_list.ingredients_translated.keys()))
ingredient_other = ingredients_list.ingredients_translated[ingredient_en]

time_start = time.time()
while time.time() - time_start < clock:
    remaining_time = clock - int(time.time() - time_start)
    print("\n"*100)
    print(f"Timer: {Fore.RED}{remaining_time}{Style.RESET_ALL}s left")

    print("Please find something containing: " + ingredient_en)
    
    code = [None]
    def get_input():
        code[0] = prompt("Please scan your item: ", default="").strip()
    
    thread = threading.Thread(target=get_input, daemon=True)
    thread.start()
    thread.join(timeout=5.0)
    
    if not code[0]:
        continue

    ingredients = api.product.get(code[0]).get("ingredients")
    if ingredient_other in str(ingredients):
        print("You got it!")
        points += 1
        
        ingredient_en = random.choice(list(ingredients_list.ingredients_translated.keys()))
        ingredient_other = ingredients_list.ingredients_translated[ingredient_en]
    else:
        print("You didn't get it")


print(f"Timer: 0s left")
print(f"You got {points} in total")
if points > highscore:
    print("Congrats! You've set the new highscore!")
    print(f"Previous Highscore: {highscore}")
    print(f"New Highscore: {points}")