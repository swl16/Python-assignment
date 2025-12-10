import tkinter as tk
from tkinter import messagebox
from tax import *
from ExpensesTracker import *

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
   register.config(background='#f7f2e9')

   frameregister = tk.Frame(register,bg='#f7f2e9')
   frameregister.pack(fill="x", padx=40, pady=6)

   tk.Label(frameregister, text = "Register New Account", font=("Arial",18,"bold"), fg='white', bg='#7e9aed',
                        relief='ridge', bd=3, padx=20, pady=20).pack(fill='x', pady=(20,30))
   
   tk.Label(frameregister, text="Username :", font=('Arial', 15, 'bold'),bg='#f7f2e9').pack(side="left",padx=10)
   username_entry = tk.Entry(frameregister, width=28,font=("Arial", 11))
   username_entry.pack(side='left')

   frameregister_password = tk.Frame(register,bg='#f7f2e9')
   frameregister_password.pack(fill="x", padx=40, pady=(20,50))

   tk.Label(frameregister_password, text="Password :", font=('Arial', 15, 'bold'),bg='#f7f2e9').pack(side="left", padx=10)
   password_entry = tk.Entry(frameregister_password,width=28,font=("Arial", 11))
   password_entry.pack(side='left')

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
             command=registeruser).pack(anchor='center')

def mainmenu(username):
  menu = tk.Toplevel()
  menu.title("MAIN MENU")
  menu.geometry("500x650")

  tk.Label(menu, text=f"Welcome,{username}!", font=("Arial",18,"bold")).pack(pady=20)

  def createbutton(text,command):
    tk.Button(menu, text=text, width=25, height=2, font=("Arial",16), command=command).pack(pady=10)

  createbutton("Expense Tracker",lambda:ExpensesTracker(username))
  createbutton("Savings Goal Tracker",lambda:taxwindow(username))
  createbutton("Simple Tax Estimator", lambda:taxwindow(username))
  
  tk.Button(menu, text="Logout", font=("Arial",16), width=10, height=1, fg='black', bg="#ff0000",command=menu.destroy).pack(pady=10, side='bottom', anchor='center')

def loginwindow():
  login = tk.Tk()
  login.title("LOGIN")
  login.geometry("450x400")

  framelogin = tk.Frame(login)
  framelogin.pack(fill="x", padx=20, pady=6)

  tk.Label(framelogin, text="Login", font=("Arial",18,"bold"), fg='white', bg='#7e9aed',
                        relief='ridge', bd=2, padx=10, pady=10).pack(fill='x', padx=10, pady=(10,20))
  
  tk.Label(framelogin, text="Username: ", font=('Arial', 15, 'bold')).pack(side="left")
  username_entry = tk.Entry(framelogin, width=30,font=("Arial", 11))
  username_entry.pack(side="left", padx=10)

  framelogin1 = tk.Frame(login)
  framelogin1.pack(fill="x", padx=20, pady=6)

  tk.Label(framelogin1, text="Password: ", font=('Arial', 15, 'bold')).pack(side="left")
  password_entry = tk.Entry(framelogin1,width=30,font=("Arial", 11))
  password_entry.pack(side="left", padx=10)

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
