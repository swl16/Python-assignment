import tkinter as tk
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

# register 
def registerwindow():
   register = tk.Toplevel()
   register.title("REGISTER")
   register.geometry("350x300")

   tk.Label(register, text = "Register New Account", font=("Arial",16,"bold")).pack(pady=10)

   tk.Label(register, text="Username:").pack()
   username_entry = tk.Entry(register, width=30)
   username_entry.pack()

   tk.Label(register, text="Password:").pack()
   password_entry = tk.Entry(register,width=30)
   password_entry.pack()

   def registeruser():
       username = username_entry.get().strip()
       password = password_entry.get().strip()

       users = loadusers()

       if username in users:
        messagebox.showerror("Error","Username already exists! Please change another username.")
        return
       elif username == "" or password == "":
        messagebox.showerror("Error","Username or password cannot be empty!")
        return
       else:
        users[username] = password
        saveuser(username,password)
        messagebox.showinfo("Success","Registration successful!")

       register.destroy()

   tk.Button(register, text="Register", width=25, command=registeruser).pack(pady=20)

def mainmenu(username):
  menu = tk.Toplevel()
  menu.title("MAIN MENU")
  menu.geometry("500x650")

  tk.Label(menu, text=f"Welcome,{username}!", font=("Arial",18,"bold")).pack(pady=20)

  def createbutton(text,command):
    tk.Button(menu, text=text, width=25, height=2, font=("Arial",16), command=command).pack(pady=10)

  createbutton("Expense Tracker")
  createbutton("Savings Goal Tracker")
  createbutton("Simple Tax Estimator")
  
  tk.Button(menu, text="Logout", font=("Arial",16), width=20, height=2, command=menu.destroy).pack(pady=10)

def loginwindow():
  login = tk.Tk()
  login.title("LOGIN")
  login.geometry("350x300")

  tk.Label(login, text="Login", font=("Arial",18,"bold")).pack(pady=20)

  tk.Label(login, text="Username:").pack()
  username_entry = tk.Entry(login, width=30)
  username_entry.pack()

  tk.Label(login, text="Password:").pack()
  password_entry = tk.Entry(login, width=30)
  password_entry.pack()

  def loginuser():
     username = username_entry.get().strip()
     password = password_entry.get().strip()

     users = loadusers()

     if username in users and users[username] == password:
      messagebox.showinfo("Success","Login successful!")
      mainmenu(username)
     else:
      messagebox.showerror("Error","Invalid username or password! Please try again.")
      return
     
  tk.Button(login, text="Login", width=25, command=loginuser).pack(pady=10)
  tk.Button(login, text="Register", width =25, command=registerwindow).pack()

  login.mainloop()

loginwindow()
