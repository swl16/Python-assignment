userfile = "users1.txt"

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

def register(users):

    while True:
        username = str(input("Enter new username: "))
        password = str(input("Enter new password: "))

        if username in users:
           print("Username already exists! Please change another username.")
        elif username == "" or password == "":
           print("Username or password cannot be empty!")
        else:
           saveuser(username, password)
           print("Registration successful!")
           break

def login(users):
    while True:
      username = str(input("Enter username: "))
      password = str(input("Enter password: "))
      if username in users and users[username] == password:
        print("Login successful!")
        break
      else:
        print("Invalid username or password! Please try again.")

def run():
  print("REGISTER")
  register(users)
  print("LOGIN")
  login(users)

  print("Main Menu")
  print("1. Expense Tracker")
  print("2. Savings Goal Tracker")
  print("3. Simple Tax Estimator")
  print("4. Logout")
  while True:
   choice = int(input("Enter your choice: "))
   match choice:
    case 1:
     print("Option 1 selected.")
     break
    case 2:
     print("Option 2 selected.")
     break
    case 3:
     print("Option 3 selected.")
     break
    case 4:
     print("Logged out successfully.")
     break
    case _:
     print("Invalid choice. Please try again.")
            
users = loadusers()
run()