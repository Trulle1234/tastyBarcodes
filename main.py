import time
import random
import requests
from colorama import init, Fore, Style
from prompt_toolkit import prompt
from openfoodfacts import API, APIVersion, Country, Environment, Flavor
import menu
import ingredients_list
import os, os.path
from sys import exit

def add_score(score, name):
    if not os.path.isfile("leaderboard.txt"):
        with open("leaderboard.txt", "w") as f:
            f.write("")
    with open("leaderboard.txt", "a") as f:
        f.write(f"{name}:{score}\n")

def load_highscore():
    h_score = 0
    if os.path.isfile("leaderboard.txt"):
        with open("leaderboard.txt") as f:
            score_dict = {}
            for line in f:
                line_array = line.rstrip().split(":")
                if h_score < int(line_array[1]):
                    h_score = int(line_array[1])
    return h_score

def show_scores():
    print(f"{Fore.MAGENTA}Leaderboard:{Style.RESET_ALL}")
    if os.path.isfile("leaderboard.txt"):
        with open("leaderboard.txt") as f:
            score_dict = {}
            for line in f:
                line_array = line.rstrip().split(":")
                score_dict[line_array[0]] = int(line_array[1])
            score_dict_sorted = dict(sorted(score_dict.items(), key=lambda kv: kv[1], reverse=True))
            for name in score_dict_sorted:
                print(f"{Fore.LIGHTYELLOW_EX}{name}{Style.RESET_ALL}: {Fore.CYAN}{str(score_dict[name])}{Style.RESET_ALL}")
    else:
        print("Nobody on this PC has played the game yet!")

def check_ingredient(target_en, target_other, name, api_result):
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
                "content": f"I have a product called '{name}' and im trying to find '{target_en}' or '{target_other}' or similar variations (plural, singular, different languages, related terms like 'water' and 'mineral water' or 'spices' and a specific spice) in this ingredient list: {api_result}. Reply with only 'yes' or 'no'."
            }
        ]
    }

    if target_en.lower() in api_result.lower() or target_other.lower() in api_result.lower():
        return True, False

    response = requests.post(url, headers=headers, json=data)

    return "yes" in response.text.lower(), True

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
    input("\nPress Enter to exit")
    exit()

ingredient_array = []
clock = 60
points = 0
highscore = load_highscore()
title = f"""
 ---------------------------------------------------------------------
|  _______                ____                          _             |
| |__   __|              |  _ \\                        | |            |
|    | | __ _ ___ _   _  | |_) | __ _ _ __ ___ ___   __| | ___  ___   |
|    | |/ _` / __| | | | |  _ < / _` | '__/ __/ _ \\ / _` |/ _ \\/ __|  |
|    | | (_| \\__ \\ |_| | | |_) | (_| | | | (_| (_) | (_| |  __/\\__ |  |
|    |_|\\__,_|___/\\__, | |____/ \\__,_|_|  \\___\\___/ \\__,_|\\___||___/  |
|                  __/ |                                              |
|                 |___/                                               |
 ---------------------------------------------------------------------
"""

active = True
while active:
    choice = menu.menu(
        title=title,
        options=["Play\n", "Credits\n", "Leaderboard\n", "Exit\n"],
        cursor_color="green",
        title_color="cyan",
        options_color="white",
    )

    os.system('cls' if os.name == 'nt' else 'clear')
    if choice == "Credits\n":
        print(f"""
{Fore.LIGHTCYAN_EX}Made by:{Style.RESET_ALL}
TheTwoBoom
Flavius
Trulle123
            """)
        input("Press Enter to return")

    elif choice == "Exit\n":
        print("Exiting the program!")
        active = False

    elif choice == "Leaderboard\n":
        show_scores()
        print("\n")
        input("Press Enter to return")

    elif choice == "Play\n":
        clock = int(prompt("Set how many seconds the timer should have: " ).strip())

        ingredient_en = random.choice(list(ingredients_list.ingredients_translated.keys()))
        ingredient_other = ingredients_list.ingredients_translated[ingredient_en]

        time_start = time.time()
        while time.time() - time_start < clock:
            remaining_time = clock - int(time.time() - time_start)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Timer: {Fore.BLUE}{remaining_time}{Style.RESET_ALL}s left\n")

            print(f"Please find something containing: {Fore.LIGHTMAGENTA_EX}{ingredient_en}{Style.RESET_ALL}")

            code = input("Please scan your item (Type \"skip\" to skip the item): ")

            if time.time() - time_start > clock:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Whoops, your time is already over \n")
                break

            if code.lower() == "skip":
                print(f"{Fore.RED}Please hold for 15 seconds{Style.RESET_ALL}")
                time.sleep(15)

                ingredient_en = random.choice(list(ingredients_list.ingredients_translated.keys()))
                ingredient_other = ingredients_list.ingredients_translated[ingredient_en]

                print("Wait time now over!")
            elif code.isdigit():
                api_response = api.product.get(code)
                if not api_response:
                    print(f"{Fore.YELLOW}Not found in database{Style.RESET_ALL}")
                    time.sleep(1.5)

                else:
                    ingredients = str(api_response.get("ingredients"))
                    name = str(api_response.get("product_name"))
                    res, used_ai = check_ingredient(ingredient_en, ingredient_other, name, str(ingredients))

                    if res:
                        print(f"{Fore.GREEN}You got it!{Style.RESET_ALL}")
                        points += 1

                        ingredient_en = random.choice(list(ingredients_list.ingredients_translated.keys()))
                        ingredient_other = ingredients_list.ingredients_translated[ingredient_en]
                    else:
                        print(f"{Fore.RED}You didn't get it{Style.RESET_ALL}")

            else:
                print(f"{Fore.RED}Please enter a valid barcode{Style.RESET_ALL}")
            time.sleep(1.5)

        print(f"Timer: {Fore.BLUE}0{Style.RESET_ALL}s left")
        print(f"You got {points} points in total")
        print("\n")
        show_scores()
        print("\n")
        if points > highscore:
            print(f"{Fore.CYAN}Congrats! You've set the new highscore!{Style.RESET_ALL}")
            print(f"Previous Highscore: {highscore}")
            print(f"New Highscore: {points}")
            print("\n")
            highscore = points
            name = input(f"{Fore.CYAN}Enter a your name: {Style.RESET_ALL}")
            add_score(points, name)

        input("\nPress Enter to return")