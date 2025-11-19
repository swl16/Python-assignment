from tkinter import *
from tkinter import messagebox

userfile = "C:\Users\WEI LI\OneDrive\Desktop\STUDY\SEM 2\Python Assignment\user.txt"
def saveuser(username, password):
    with open(userfile, "a") as f:
        f.write(f"{username},{password}\n")

with open(userfile, "r") as f:
    users = [line.strip().split(",")[0] for line in f.readlines()]

def registerwindow():
    def submit_registration():
        username = entry_username.get()
        password = entry_password.get()

        if username in users:
            messagebox.showerror("Error", "Username already exists!")
            return
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty!")
            return 
        else:
            saveuser(username, password)
            messagebox.showinfo("Success", "Registration successful!")
            reg_window.destroy()

    reg_window = Toplevel()
    reg_window.title("Register")

    Label(reg_window, text="Username:").grid(row=0, column=0)
    entry_username = Entry(reg_window)
    entry_username.grid(row=0, column=1)

    Label(reg_window, text="Password:").grid(row=1, column=0)
    entry_password = Entry(reg_window, show="*")
    entry_password.grid(row=1, column=1)

    Button(reg_window, text="Register", command=submit_registration).grid(row=2, columnspan=2)

