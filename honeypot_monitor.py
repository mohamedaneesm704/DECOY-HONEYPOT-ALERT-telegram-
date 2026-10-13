import os
import time
import hashlib
import getpass
import socket
import urllib.request
import urllib.parse

FOLDER = "C:/Users/Jaitha/OneDrive/Documents"
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

def get_hash(filepath):
    try:
        with open(filepath, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return None

def get_all_hashes():
    hashes = {}
    for root, _, files in os.walk(FOLDER):
        for file in files:
            if file.endswith('.py'): continue
            path = os.path.join(root, file)
            hashes[path] = get_hash(path)
    return hashes

def send_alert(filename):
    user, ip = getpass.getuser(), socket.gethostbyname(socket.gethostname())
    msg = f"🚨 ALL-FILE HONEYPOT ALERT!\n\nFile Modified: {filename}\nUser: {user}\nIP: {ip}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = urllib.parse.urlencode({'chat_id': CHAT_ID, 'text': msg}).encode('utf-8')
    try:
        urllib.request.urlopen(url, data=payload)
        print(f"\n[ALERT SENT] File modified: {filename}")
    except Exception as e:
        print(f"\n[ERROR] Telegram send failed: {e}")

known_files = get_all_hashes()
print("--- ALL FILES HONEYPOT ACTIVE ---")

while True:
    current_files = get_all_hashes()
    for path, h in current_files.items():
        if path in known_files and h != known_files[path]:
            send_alert(path)
    known_files = current_files
    print("[INFO] Monitoring all files...", end="\r")
    time.sleep(2)
