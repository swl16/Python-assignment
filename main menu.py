from tkinter import *
from tkinter import messagebox

userfile = "user.txt"
def saveuser(username,password):
    with open(userfile,"a") as f:
        f.write(f"{username},{password}\n")

def loadusers():
  data = {}
  try:
   with open(userfile,"r")as f:
    for line in f:
      username, password = line.strip().split(",")
      data[username] = password
  except FileNotFoundError:
      pass
  return data

def registerwindow():
    def register():
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

    Button(reg_window, text="Register", command=register).grid(row=2, columnspan=2)

def login(username,password):
    username = str(input("Enter username: "))
    password = str(input("Enter password: "))

    if username in users and users[username] == password:
        print("Success", "Login successful!")
    else:
        print("Error", "Invalid username or password!")



    


def run():
    username = str(input("Enter username: "))
    password = str(input("Enter password: "))
    saveuser(username, password)
    print("Username: ", username)
    print("Password: ", password)
    
    print("LOGIN")
    login(username, password)


run()