# This code is only for the main code to work with
from tkinter import Tk, messagebox

def show_fake_alert():
    root = Tk()
    root.withdraw()  
    messagebox.showwarning("Security Alert", "Your system has been compromised! Click here for details.")

show_fake_alert()