import time
import random
import requests
from colorama import init, Fore, Style
from prompt_toolkit import prompt
from openfoodfacts import API, APIVersion, Country, Environment, Flavor
import menu
import ingredients_list
import os

def check_ingredient(target: str, api_result: str) -> bool:
    url = "https://ai.hackclub.com/proxy/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.environ.get("HACKCLUB_API_KEY")}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "google/gemini-2.5-flash-lite-preview-09-2025",
        "messages": [
            {
                "role": "user",
                "content": f"Check if '{target}' or similar variations (plural, singular, related terms like 'water' and 'mineral water') is mentioned in this ingredient list: {api_result}. Reply with only 'yes' or 'no'."
            }
        ]
    }


    response = requests.post(url, headers=headers, json=data)
    
    return "yes" in response.text.lower()

api = API(
    user_agent="tastyBarcodes/v0.1 (boom@thetwoboom.xyz)",
    username=None,
    password=None,
    country=Country.world,
    flavor=Flavor.off,
    version=APIVersion.v2,
    environment=Environment.org,
)

api_key = os.environ.get("HACKCLUB_API_KEY")

if not api_key:
    print("Please set HACKCLUB_API_KEY")
    exit()

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
    
    code = input("Please scan your item: ")

    if time.time() - time_start > clock:
        print("Whoops, your time is already over")
        break

    api_response = api.product.get(code)
    if not api_response:
        print("Not found in database")
        time.sleep(1.5)
        continue

    ingredients = str(api_response.get("ingredients"))

    if check_ingredient(ingredient_en, str(ingredients)):
        print("You got it!")
        points += 1
        
        ingredient_en = random.choice(list(ingredients_list.ingredients_translated.keys()))
        ingredient_other = ingredients_list.ingredients_translated[ingredient_en]
    else:
        print("You didn't get it")

    time.sleep(1.5)


print(f"Timer: 0s left")
print(f"You got {points} in total")
if points > highscore:
    print("Congrats! You've set the new highscore!")
    print(f"Previous Highscore: {highscore}")
    print(f"New Highscore: {points}")