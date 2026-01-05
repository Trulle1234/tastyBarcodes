import time
from colorama import init, Fore, Style
from prompt_toolkit import prompt
from openfoodfacts import API, APIVersion, Country, Environment, Flavor
from menu import menu

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

choice = menu(
    title="Main Menu",
    options=["Play", "Set Timer", "Credits", "Exit"],
    cursor_color="green",
    title_color="cyan",
    options_color="white",
)

if choice == "Play":
    pass  # start game

elif choice == "Set Timer":
    clock = int(input("Set timer in seconds: "))

elif choice == "Credits":
    print("Made by _________________")
    input("Press Enter to return")

elif choice == "Exit":
    exit()


# clock = prompt("Set how many seconds the timer should have. just type the number" ).strip()

input("Press Enter to continue...")
while clock > 0:
    print("\n"*100)
    print(f"Timer: {Fore.RED}{str(clock)}{Style.RESET_ALL}s left")
    print("Ingredient Placeholder")
    time.sleep(5)
    clock -= 5

print(f"Timer: 0s left")
print(f"You got {points} in total")
if points > highscore:
    print("Congrats! You've set the new highscore!")
    print(f"Previous Highscore: {highscore}")
    print(f"New Highscore: {points}")