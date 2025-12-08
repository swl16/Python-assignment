import tkinter as tk
from tkinter import messagebox
from tax import *

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
   register.geometry("450x400")

   tk.Label(register, text = "Register New Account", font=("Arial",18,"bold"), fg='white', bg='#7e9aed',
                        relief='ridge', bd=3, padx=20, pady=15).pack(fill='x', padx=20, pady=(20,30))
   
   tk.Label(register, text="Username:", font=('Arial', 15, 'bold')).pack()
   username_entry = tk.Entry(register, width=30,font=("Arial", 11))
   username_entry.pack()

   tk.Label(register, text="Password:", font=('Arial', 15, 'bold')).pack()
   password_entry = tk.Entry(register,width=30,font=("Arial", 11))
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

   tk.Button(register, text="Register", width=15,font=("Arial",15,'bold'), fg='white',bg='#7e9aed',relief='ridge', bd=2, padx=10, 
             command=registeruser).pack(pady=(40,10),anchor='center')

def mainmenu(username):
  menu = tk.Toplevel()
  menu.title("MAIN MENU")
  menu.geometry("500x650")

  tk.Label(menu, text=f"Welcome,{username}!", font=("Arial",18,"bold")).pack(pady=20)

  def createbutton(text,command):
    tk.Button(menu, text=text, width=25, height=2, font=("Arial",16), command=command).pack(pady=10)

  createbutton("Expense Tracker",lambda:taxwindow(username))
  createbutton("Savings Goal Tracker",lambda:taxwindow(username))
  createbutton("Simple Tax Estimator", lambda:taxwindow(username))
  
  tk.Button(menu, text="Logout", font=("Arial",16), width=20, height=2, command=menu.destroy).pack(pady=10)

def loginwindow():
  login = tk.Tk()
  login.title("LOGIN")
  login.geometry("450x400")

  tk.Label(login, text="Login", font=("Arial",18,"bold"), fg='white', bg='#7e9aed',
                        relief='ridge', bd=2, padx=10, pady=10).pack(fill='x', padx=10, pady=(10,20))
  
  tk.Label(login, text="Username: ", font=('Arial', 15, 'bold')).pack()
  username_entry = tk.Entry(login, width=30,font=("Arial", 11))
  username_entry.pack()

  tk.Label(login, text="Password: ", font=('Arial', 15, 'bold')).pack()
  password_entry = tk.Entry(login,width=30,font=("Arial", 11))
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
  
  tk.Button(login, text="Login", width=15, font=("Arial",15,'bold'), fg='white',bg='#7e9aed',relief='ridge', bd=2, padx=10, 
            command=loginuser).pack(pady=(40,10),anchor='center')
  tk.Button(login, text="Register", width =15, font=("Arial",15,'bold'), fg='white',bg='#7e9aed',relief='ridge', bd=2, padx=10, 
            command=registerwindow).pack(pady=(0,50),anchor='center')

  login.mainloop()

loginwindow()
