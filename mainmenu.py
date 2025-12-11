import tkinter as tk
from tkinter import messagebox
from tax import taxwindow
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
def registerwindow(login_window):
   register = tk.Toplevel()
   register.title("REGISTER")
   register.geometry("450x400")
   register.config(background='#f7f2e9')
   login_window.withdraw()

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

   def Back_login_page():
       register.destroy()
       login_window.deiconify()

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

        Back_login_page()

   Button_frame = Frame(register, bg='#fcf7ed')
   Button_frame.pack(anchor='center')

   tk.Button(Button_frame, text="Register",font=("Arial",15,'bold'), fg='white',bg='#7e9aed',relief='ridge', bd=2, padx=12, pady=5, command=registeruser).pack(side='left',padx=10)
   tk.Button(Button_frame, text = "Cancel",font=("Arial",15,'bold'), fg='white',bg='#7e9aed',relief='ridge', bd=2, padx=12, pady=5, command=Back_login_page).pack(side='left',padx=10)

def mainmenu(username,login_window):
  menu = tk.Tk()
  menu.title("MAIN MENU")
  menu.geometry("500x650")
  menu.config(background='#f7f2e9')
  login_window.destroy()

  tk.Label(menu, text=f"Welcome,{username}!", font=("Arial",18,"bold"),bg='#f7f2e9').pack(pady=20)

  def createbutton(text,command):
    tk.Button(menu, text=text, width=25, height=2, font=("Arial",16), command=command).pack(pady=10)

  createbutton("Expense Tracker",lambda:ExpensesTracker(username,menu))
  createbutton("Savings Goal Tracker",lambda:taxwindow(username))
  createbutton("Simple Tax Estimator", lambda:taxwindow())

  def Log_out():
      menu.destroy()
      loginwindow()
  
  tk.Button(menu, text="Logout", font=("Arial",16), width=10, height=1, fg='black', bg="#ff0000",command=Log_out).pack(pady=10, side='bottom', anchor='center')

  menu.mainloop()

def loginwindow():
  login = tk.Tk()
  login.title("LOGIN")
  login.geometry("450x400")
  login.config(background='#f7f2e9')

  try:
      icon = PhotoImage(file='coin.png')
      login.iconphoto(True, icon)
  except:
      pass

  framelogin = tk.Frame(login,bg='#f7f2e9')
  framelogin.pack(fill="x", padx=40, pady=6)

  tk.Label(framelogin, text="Login", font=("Arial",18,"bold"), fg='white', bg='#7e9aed',
                        relief='ridge', bd=2, padx=20, pady=20).pack(fill='x', pady=(20,30))
  
  tk.Label(framelogin, text="Username : ", font=('Arial', 15, 'bold'),bg='#f7f2e9').pack(side="left",padx=10)
  username_entry = tk.Entry(framelogin, width=28,font=("Arial", 11))
  username_entry.pack(side="left")

  framelogin_pass = tk.Frame(login,bg='#f7f2e9')
  framelogin_pass.pack(fill="x", padx=40, pady=(20,50))

  tk.Label(framelogin_pass, text="Password : ", font=('Arial', 15, 'bold'),bg='#f7f2e9').pack(side="left",padx=10)
  password_entry = tk.Entry(framelogin_pass,width=28,font=("Arial", 11))
  password_entry.pack(side="left")

  def loginuser():
     username = username_entry.get().strip()
     password = password_entry.get().strip()

     users = loadusers()

     if username in users and users[username] == password:
      messagebox.showinfo("Success","Login successful!")
      mainmenu(username,login)
     else:
      messagebox.showerror("Error","Invalid username or password! Please try again.")
      return
  
  tk.Button(login, text="Login", width=15, font=("Arial",15,'bold'), fg='white',bg='#7e9aed',relief='ridge', bd=2, padx=10,
            command=loginuser).pack(pady=(0,10),anchor='center')

  register_frame = tk.Frame(login,bg='#f7f2e9')
  register_frame.pack(anchor='center')

  tk.Label(register_frame,text="Don't have account?",font=("Arial",11),bg='#f7f2e9').pack(side="left",padx=(10,5))
  tk.Button(register_frame, text="Register", font=("Arial",11,"underline"), bg='#f7f2e9',fg='#7e9aed', bd=0, relief='flat', command=lambda : registerwindow(login)).pack(side="left")

  login.mainloop()

loginwindow()
