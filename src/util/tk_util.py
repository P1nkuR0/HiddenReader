import tkinter as tk
from tkinter import simpledialog

def get_user_input(prompt):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    user_input = simpledialog.askstring(" ", prompt)
    root.destroy()
    return user_input

if __name__ == "__main__":
    text = get_user_input()
    print("User entered:", text)
