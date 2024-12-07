from httpx                import Client, get, post
from random               import randint, choices, choice
from string               import ascii_lowercase, digits, ascii_letters
from re                   import search
from time                 import sleep
from rsa                  import PublicKey, encrypt as rsae
from binascii             import hexlify
from urllib.parse         import urlencode, quote
from threading            import Thread, active_count, Lock
from hmac                 import new
from hashlib              import sha1
from time                 import time,sleep,strftime, time
from base64               import b64encode
from colorama             import Fore, init
from secrets              import token_urlsafe
from os                   import system
from sys                  import exit
from yaml                 import safe_load
from multiprocessing      import freeze_support
from requests import Session
import imaplib
import email
import requests
import logging
import json
import pymailtm
import requests
import random
import string
from console import Console

console = Console()
promo_mail = console.input("Enter Mail To Recieve Promos :")
class Sign:
    def __init__(self) -> None:
        self.sign_key = b"gUtPzJFZch4ZyAGviiyH94P99lQ3pFdRTwpJWDlSGFfwgpr6ses5ALOxWHOIT7R1"

    def get_message(self, string, stamp):
        string = string[:min(255, len(string))]
        return string + stamp

    def sign(self, uri):
        mac     = new(self.sign_key, digestmod=sha1)
        stamp   = str(int(time() * 1000))

        mac.update(self.get_message(uri, stamp).encode('utf-8'))

        md      = quote(b64encode(mac.digest()))

        builder = []
        builder.append(uri)
        builder.append('&') if '?' in uri else builder.append('?')

        builder.append("msgpad=" + stamp)
        builder.append("&md="    + md)

        return ''.join(builder)
    
    def chrlen(self, n: str) -> str:
        return chr(len(n))
    
    def encrypt(self, json, mail, pw):
        string  = f"{self.chrlen(json['sessionKey'])}{json['sessionKey']}{self.chrlen(mail)}{mail}{self.chrlen(pw)}{pw}".encode()
        mod     = int(json['nvalue'], 16)
        evl     = int(json['evalue'], 16)
        pbk     = PublicKey(evl, mod)
        out     = rsae(string, pbk)

        return hexlify(out).decode('utf-8')


class Register:
    def __init__(self, mail, thread_id,max_retries=3):
        self.pw = "rjsdadawd"
        self.thread_id= thread_id
        self.mail = mail
        self.max_retries = max_retries
        self.session = Session()
        self.session.headers.update({
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        })
        

    def get_birth(self):
        return {
            "year": "1987",
            "month": str(randint(1, 12)),
            "dayOfMonth": str(randint(1, 28))
        }

    def get_data(self):
        try:
            response = self.session.get("https://www.webtoons.com/member/login/rsa/getKeys", timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Error fetching RSA keys: {e}")
            return None

    def cook(self):
        try:
            self.session.get("https://gak.webtoons.com/v1/web/cookie", timeout=10)
        except Exception as e:
            logging.warning(f"Failed to fetch cookies: {e}")

    def register(self):
        retries = 0
        while retries < self.max_retries:
            try:
                self.cook()
                self.name = "".join(choices(ascii_lowercase, k=18))
                url = "https://www.webtoons.com/member/join/doJoinById"
                json_data = self.get_data()
                if not json_data:
                    logging.error("Failed to get RSA keys, retrying...")
                    retries += 1
                    sleep(2)
                    continue

                data = urlencode({
                    **self.get_birth(),
                    "loginType": "EMAIL",
                    "nickname": self.name,
                    "encnm": json_data["keyName"],
                    "encpw": Sign().encrypt(json_data, self.mail, self.pw),
                    "zoneId": "Europe/Berlin",
                    "emailEventAlarm": "false",
                })

                response = self.session.post(url, data=data, timeout=10)
                #print(response.text)
                console.info(f"Registered Account: {self.name}")
                return self.name
            except Exception as e:
                console.error(f"Registration failed on attempt {retries + 1}: {e}")
                retries += 1
                sleep(2)

        console.error(f"Failed to register after {self.max_retries} attempts.")
        return None
def getcookies():
    return {
        "wtu"                : token_urlsafe(24),
        "locale"             : "en",
        "needGDPR"           : "true",
        "needCCPA"           : "false",
        "needCOPPA"          : "false",
        "countryCode"        : "RO",
        "timezoneOffset"     : "+3",
        "ctZoneId"           : "Europe/Bucharest",
        "wtv"                : "1",
        "wts"                : str(int(time() * 1000)),
        "__cmpconsentx47472" : f"{token_urlsafe(2)}_{token_urlsafe(3)}_{token_urlsafe(25)}",
        "__cmpcccx47472"     : token_urlsafe(18),
        "_fbp"               : "fb.1.1684479996310.2019224647",
        "_scid"              : "858a934e-433c-4e07-b4c3-c1a1b9becc34",
        "_gid"               : "GA1.2.1604983543.1733464036",
        "_tt_enable_cookie"  : "1",
        "_ttp"               : "2dlVmcQxdz_oQTW_6zMA2eNlFy3",
        "_scid_r"            : "858a934e-433c-4e07-b4c3-c1a1b9becc34",
        "_ga"                : "GA1.2.1604983543.1733464036",
        "_ga_ZTE4EZ7DVX"     : "GS1.1.1684486049.2.0.1684486049.60.0.0",
    }
class Claim:
    def __init__(self, email, password, name, thread_id) -> None:
        self.session = Client(headers = {
            "accept-encoding"   : "gzip",
            "connection"        : "Keep-Alive",
            "content-type"      : "application/x-www-form-urlencoded", 
            "host"              : "global.apis.naver.com",
            "user-agent"        : "Android/9 Model/SM-N975F com.naver.linewebtoon/2.12.5(2120500,uid:10059) NeoIdSignInMod/0.1.12",
        },timeout=10)

        self.sign       = Sign().sign
        self.email      = email
        self.password   = password
        self.name       = name
        self.thread_id  = thread_id

    def getData(self) -> dict:
        for _ in range(10):
            try:
                return self.session.get(self.sign("https://global.apis.naver.com/lineWebtoon/webtoon/getRsaKey.json?v=1&platform=APP_ANDROID&language=en&serviceZone=GLOBAL&locale=en")).json()["message"]["result"]     
            except:
                continue #sprint(f"Error", self.thread_id, f"{Fore.RED}Failed To Get Data")

    def read(self):
        for page in range(1, 10):
            self.headers_read = {
                "accept-encoding"   : "gzip",
                "connection"        : "Keep-Alive",
                "host"              : "global.apis.naver.com",
                "user-agent"        : "nApps (Android 9; SM-N975F; linewebtoon; 2.12.5)",
                "cookie"            : f'NEO_SES="{self.ses}"'
            }
            params = urlencode({
                "v"             : "2",
                "webtoonType"   : "WEBTOON",
                "titleNo"       : "2705",
                "episodeNo"     : str(page),
                "platform"      : "APP_ANDROID",
                "language"      : "en",
                "serviceZone"   : "GLOBAL&&",
                "locale"        : "en"
            })
            
            url = f"https://global.apis.naver.com/lineWebtoon/webtoon/eventReadLog.json?{params}"
            for _ in range(3):
                try: # Error Handling Needed
                    page_read = self.session.get(self.sign(url), headers=self.headers_read).json()

                    if page_read['message']['result']["progressType"] != "NONE":
                        self.session.get(page_read['message']['result']["pageUrl"],headers={ 
                                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                                "accept-encoding": "gzip, deflate",
                                "accept-language": "en-US,en;q=0.9",
                                "connection": "keep-ali/ve",
                                "host": "m.webtoons.com",
                                "sec-fetch-dest": "document",
                                "sec-fetch-mode": "navigate",
                                "sec-fetch-site": "none",
                                "sec-fetch-user": "?1",
                               "upgrade-insecure-requests": "1",
                                "user-agent": "Mozilla/5.0 (Linux; Android 9; SM-N975F Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/113.0.5672.131 Mobile Safari/537.36 linewebtoon/2.12.5 (GLOBAL; EAF)",
                                "x-requested-with": "com.naver.linewebtoon"
                            }, cookies=getcookies())
                    break
                except Exception as e:
                    pass

    def claim(self):
        self.session.headers = {
            "accept"            : "application/json, text/plain, */*",
            "accept-encoding"   : "gzip, deflate",
            "accept-language"   : "en-US,en;q=0.9",
            "connection"        : "keep-alive",
            "host"              : "m.webtoons.com",
            "referer"           : "https://m.webtoons.com/app/promotion/read/DiscordPhase2-Reading-December2024_Real_Fixed_NewCodes/progress?platform=APP_ANDROID",
            "sec-fetch-dest"    : "empty",
            "sec-fetch-mode"    : "cors",
            "sec-fetch-site"    : "same-origin",
            "user-agent"        : "Mozilla/5.0 (Linux; Android 9; SM-N975F Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/113.0.5672.131 Mobile Safari/537.36 linewebtoon/2.12.5 (GLOBAL; EAF)",
            "x-requested-with"  : "com.naver.linewebtoon",
        }

        self.session.cookies = getcookies()
        self.session.cookies.set("NEO_SES", self.ses)

        url = "https://m.webtoons.com/app/promotion/saveSubmitPayload"
        data = {
            "eventNo": 5362,
            "email": promo_mail #add ur own mail here
        }
        r = self.session.post(url,json=data, timeout=15)
        #print(r.text)
        if r.status_code == 200:
            console.success(f"Claimed Promo -> {self.email}")
        else:
            console.error(f"Failed to Claim Promo -> {self.email}. Status code: {r.status_code}")

        

    def redeem(self):
        json    = self.getData()
        url     = "https://global.apis.naver.com/lineWebtoon/webtoon/loginById.json"
        data   = urlencode({
            "v"            : "2",
            "encnm"        : json["keyName"],
            "encpw"        : Sign().encrypt(json, self.email, self.password),
            "language"     : "en",
            "loginType"    : "EMAIL",
            "serviceZone"  : "GLOBAL",
        })

        self.ses =  self.session.post(url, data=data).json()["message"]["result"]["ses"]
        
        self.session.cookies.set("NEO_SES", self.ses)
        self.session.headers["user-agent"] = "nApps (Android 7.1.2; G011A; linewebtoon; 2.12.5)"
        console.info(f"Reading The Pages -> {self.email}")
        self.read()
        self.claim()

def main():
    email = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10)) + "@soscandia.org"
    passw = "Payload69"
    EmailNo = requests.post(
        "https://api.mail.tm/accounts" ,
        json={
            "address": email,
            "password": passw
        }
    )
    if EmailNo.status_code == 201:
        emailaccount = pymailtm.Account(id=10 , address=str(email) , password=str(passw))
        (Register(email , 1).register())
        verify = None
        while not verify:
            sleep(1)
            try: verify = emailaccount.get_messages()[0].text.split("[")[-2].split("]")[0]
            except: pass
        #print(verify)
        open("Seprated.txt" , "a+" , encoding = "utf-8").write(f"{email}:{passw}" + '\n')
        req = requests.get(verify , headers={
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Brave\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "sec-ch-ua-full-version-list": "\"Brave\";v=\"131.0.0.0\", \"Chromium\";v=\"131.0.0.0\", \"Not_A Brand\";v=\"24.0.0.0\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": "\"\"",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-ch-ua-platform-version": "\"15.0.0\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "x-requested-with": "XMLHttpRequest",
            "Referer": "https://www.webtoons.com/member/join",
            "Referrer-Policy": "unsafe-url"
        })
        claim_instance = Claim(email, "rjsdadawd", "sdadsadasdcx", thread_id=1)  # Create an instance of the Claim class
        claim_instance.redeem()
        


from concurrent.futures import ThreadPoolExecutor


with ThreadPoolExecutor(max_workers=100) as exe:
    for _ in range(10000):
        exe.submit(main)
