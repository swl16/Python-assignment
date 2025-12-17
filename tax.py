import tkinter as tk
from tkinter import messagebox

#from google LHDN Malaysia, latest tax rate 
TaxRate = (0.0, 0.01, 0.03, 0.06, 0.11, 0.19, 0.25, 0.26, 0.28, 0.30)
basetax = [5000, 5000, 20000, 35000, 50000, 70000, 100000, 400000, 600000, 2000000]
fixedtax = (0, 0, 150, 600, 1500, 3700, 9400, 84400, 136400, 528400)

# calculate the income tax balance
def taxcalculation(chargeable_income):
   #tax=0 if chargeable income <0
   if chargeable_income<0:
      return 0.0
   taxbalance = 0.0
   if 0 <=chargeable_income<= 5000:
      taxbalance = 0
   elif 5001 <= chargeable_income <= 20000:
      taxbalance = fixedtax[1] + (chargeable_income - basetax[1]) * TaxRate[1]
   elif 20001 <= chargeable_income <= 35000:
      taxbalance = fixedtax[2] + (chargeable_income - basetax[2]) * TaxRate[2]
   elif 35001 <= chargeable_income <= 50000:
      taxbalance = fixedtax[3] + (chargeable_income - basetax[3]) * TaxRate[3]
   elif 50001 <= chargeable_income <= 70000:
      taxbalance = fixedtax[4] + (chargeable_income - basetax[4]) * TaxRate[4]
   elif 70001 <= chargeable_income <= 100000:
      taxbalance = fixedtax[5] + (chargeable_income - basetax[5]) * TaxRate[5]
   elif 100001 <= chargeable_income <= 400000:
      taxbalance = fixedtax[6] + (chargeable_income - basetax[6]) * TaxRate[6]
   elif 400001 <= chargeable_income <= 600000:
      taxbalance = fixedtax[7] + (chargeable_income - basetax[7]) * TaxRate[7]
   elif 600001 <= chargeable_income <= 2000000:
      taxbalance = fixedtax[8] + (chargeable_income - basetax[8]) * TaxRate[8]
   elif chargeable_income > 2000000:
      taxbalance = fixedtax[9] + (chargeable_income - basetax[9]) * TaxRate[9]

#round result to 2 decimal places
   return round(taxbalance,2)
 
#main application window
class taxwindow(tk.Tk):
   def __init__(tax_estimator,username,mainmenu):
    #call parent's class constructor
    super().__init__()
    
    #store username and history file
    tax_estimator.username = username
    tax_estimator.cal_history = f"{tax_estimator.username}_history.txt"

    #hide main menu window
    tax_estimator.mainmenu = mainmenu
    mainmenu.withdraw()

    #window settings
    tax_estimator.title("SIMPLE TAX ESTIMATOR")
    tax_estimator.geometry("750x700")
    tax_estimator.protocol("WM_DELETE_WINDOW", tax_estimator.destroypage)
    tax_estimator.config(background='#f7f2e9')

    #title
    tk.Label(tax_estimator, text="Simple Tax Estimator", font=("Arial",18,"bold"),fg='white', bg='#7e9aed',
          relief='ridge', bd=3, padx=20, pady=15).pack(padx=20, pady=(30,20))
    
    #input fields
    tax_estimator.income = tax_estimator.frame_input("Annual Income (RM)                                                       : ")
    tax_estimator.epf = tax_estimator.frame_input("Enter EPF Contribution (RM)                                         : ")
    tax_estimator.insurance = tax_estimator.frame_input("Enter insurance amount(max RM7000) (RM)                  : ")
    tax_estimator.edufee = tax_estimator.frame_input("Enter self education fees(max RM7000) (RM)                 : ")
    tax_estimator.donate = tax_estimator.frame_input("Enter Donation amount (RM)                                         : ")
    tax_estimator.pcb = tax_estimator.frame_input("Enter the amount of monthly tax deduction(PCB) (RM) : ")
    
    #frame for individual relief info
    frame1 = tk.Frame(tax_estimator,bg='#f7f2e9')
    frame1.pack(fill="x", padx=20, pady=6)

    tk.Label(frame1, text="Individual Relief (RM) : 9000", font=('Arial',13,'bold'),bg='#f7f2e9').pack(side='left')
 
    #output text
    tax_estimator.taxoutput = tk.Text(tax_estimator, width=60, height=8,font=("Arial",12))
    tax_estimator.taxoutput.config(state="disabled")
    tax_estimator.taxoutput.pack(pady=15)

    tax_estimator.taxoutput1 = tk.Text(tax_estimator, width=60, height=4,font=("Arial",12))
    tax_estimator.taxoutput1.config(state="disabled")
    tax_estimator.taxoutput1.pack(pady=15)
    
    #bottom menu frame
    bottom_menu = tk.Frame(tax_estimator, bg='#7e9aed', height=50)
    bottom_menu.pack(side='bottom', fill='x')
    
    #button for calculate tax
    tk.Button(tax_estimator, text="Calculate Tax", width=15, font=("Arial",15,'bold'), fg='white',bg='#7e9aed', relief='ridge', bd=2, 
              command=tax_estimator.runtax).pack(pady=(40,10),anchor='center')
    
    #buttons in bottom menu
    tk.Button(bottom_menu, text="🔙Back", width=10, font=("Arial",15,'bold'), fg='black',bg='#7e9aed', 
           command=tax_estimator.destroypage).pack(side='left', expand=True, fill='both')
    tk.Button(bottom_menu, text="📜Calculation History", width=15, font=("Arial",11,'bold'), fg='black',bg='#7e9aed', 
           command=tax_estimator.loadcalhistory).pack(side='left', expand=True, fill='both')
    tk.Button(bottom_menu, text="⌫Clear all", width=10, font=("Arial",15,'bold'), fg='black',bg="#ff0000", 
           command=tax_estimator.resetinput).pack(side='left', expand=True, fill='both')

    # destroy tax window and return to main menu
   def destroypage(tax_estimator):
        tax_estimator.mainmenu.deiconify()
        tax_estimator.destroy()

   #input frame function
   def frame_input(tax_estimator,result):
      frame = tk.Frame(tax_estimator,bg='#f7f2e9')
      frame.pack(fill="x", padx=20, pady=6)
      tk.Label(frame, text=result, font=("Arial", 13, "bold"),bg='#f7f2e9').pack(side='left')
      entry = tk.Entry(frame, width=30, font=('Arial', 11))
      entry.pack(side='left', padx=10)

      return entry

   #calculation
   def runtax(tax_estimator):
    #check for empty fields
    for entry in [tax_estimator.income, tax_estimator.pcb, tax_estimator.insurance, tax_estimator.edufee, tax_estimator.donate,tax_estimator.pcb]:
       if entry.get().strip() == "":
          messagebox.showerror("Input Error!", "Please fill in ALL fields before calculating.")
          return
    
    #converts input to float and validate
    try:
     income = float(tax_estimator.income.get() or 0)
     epf = float(tax_estimator.epf.get() or 0)
     insurance = float(tax_estimator.insurance.get() or 0) 
     education = float(tax_estimator.edufee.get() or 0)
     donation = float(tax_estimator.donate.get() or 0)
     pcb = float(tax_estimator.pcb.get() or 0)
    except ValueError:
     messagebox.showerror("Error!","Please enter valid numeric values.")
     return
    else:
      #validate maximum relief amounts
      if insurance > 7000:
         messagebox.showerror("Error!", "The Maximum amount for insurance is RM7000. Please try again")
         return
      elif education > 7000:
         messagebox.showerror("Error!", "The Maximum amount for education fee is RM7000. Please try again")
         return
      elif insurance and education > 7000:
         messagebox.showerror("Error!", "The Maximum amount for insurance and education fee is RM7000 each. Please try again")
         return
      elif income < 0 or epf < 0 or insurance < 0 or education < 0 or donation < 0 or pcb < 0:
         messagebox.showerror("Error!","Negative values are not allowed. Please enter valid positive numbers.")
         return
      
    individual = 9000.00
    taxrelief = individual + epf + insurance + education
    chargeable_income = income - taxrelief - donation

    #call function to calculate tax
    tax = taxcalculation(chargeable_income)
    
    #compute rebate
    match True:
       case _ if chargeable_income <= 35000:
           rebate = 400.0
       case _:
          rebate = 0.0

    taxpayable = tax - rebate

    totalpcb = pcb * 12

    tax_estimator.taxoutput.config(state="normal")
    #display results
    tax_estimator.taxoutput.delete("1.0", "end")
    result = (f"Annual Income: RM {income:.2f}\n"
              f"Total Tax Relief (included Individual) : RM {taxrelief:.2f}\n"
              f"Chargeable Income : RM {chargeable_income:.2f}\n"
              f"Estimated Income Tax : RM {tax:.2f}\n"
              f"Eligible Rebate : RM {rebate:.2f}\n"
              f"Estimated Income Tax Payable : RM {taxpayable:.2f}\n"
              f"Total PCB (12 Months) : RM {totalpcb:.2f}\n")
    tax_estimator.taxoutput.insert("end", result)

    tax_estimator.taxoutput1.config(state="normal")
    tax_estimator.taxoutput1.delete("1.0", "end")
    #determine tax payment or refund
    if taxpayable > totalpcb:
      taxpayment = taxpayable - totalpcb
      tax_estimator.taxoutput1.insert("end", "❗Tax payable > PCB. There is insufficient tax payment.\n")
      tax_estimator.taxoutput1.insert("end", f"You need to pay an additional RM {taxpayment:.2f}\n")
    else:
      taxpayment = totalpcb - taxpayable
      tax_estimator.taxoutput1.insert("end", "✔ Tax payable < PCB. There is excess deduction. You get refund.\n")
      tax_estimator.taxoutput1.insert("end", f"You will get a refund of RM {taxpayment:.2f}\n")
      
    tax_estimator.taxoutput.config(state="disabled") #user cannot edit the result
    tax_estimator.taxoutput1.config(state="disabled")
    
    #save result to history file
    tax_estimator.savecalhistory(result)
   
   #save history function
   def savecalhistory(tax_estimator, text):
    with open(tax_estimator.cal_history,"a") as f:
      f.write(text + "\n" + "-" * 50 + "\n")
   
   #load history function
   def loadcalhistory(tax_estimator):
     history_window = tk.Toplevel(tax_estimator)
     history_window.title(f"Calculation History")
     history_window.geometry("500x750")

     # create a scrollbar
     scrollbar = tk.Scrollbar(history_window)
     scrollbar.pack(fill='y', side='right')

     textarea = tk.Text(history_window, width=65, height=35, font=("Arial",13), yscrollcommand=scrollbar.set)
     textarea.pack(padx=10, pady=10)
     
     #update the scrollbar, users can scroll vertically
     scrollbar.config(command=textarea.yview)

     try:
        with open(tax_estimator.cal_history, "r") as f:
           content = f.read()
           if content.strip() == "":
              textarea.insert("end", "No calculation history found")
           else:
              textarea.insert("end", content)
     except FileNotFoundError:
        textarea.insert("end", "No history file found from this user")

     textarea.config(state="disabled")

     def deletehistory():
      confirm = messagebox.askyesno("Delete Calculation History","Confirm delete all calculation history?")
      history_window.withdraw()
     
      with open(tax_estimator.cal_history, "r") as f:
         content = f.read()
         if content.strip() == "":
             messagebox.showinfo("No History", "No calculation history to delete.")
             return
         elif confirm:
             with open(tax_estimator.cal_history,"w"):
              messagebox.showinfo("History Deleted", "Calculation history deleted successfully")

     tk.Button(history_window, text="Delete History", width=10, font=("Arial",11,'bold'), fg='black',bg="#ff0000",relief='ridge', bd=2, 
           padx=10, command=deletehistory).pack(pady=(20,10),anchor='e')
   
   #clear input fields and output
   def resetinput(tax_estimator):
       # Check if there's anything to clear first
       has_input = False
       for entry in [tax_estimator.income, tax_estimator.epf, tax_estimator.insurance,
                     tax_estimator.edufee, tax_estimator.donate, tax_estimator.pcb]:
           if entry.get().strip() != "":
               has_input = True
               break

       # Check if output has content
       if tax_estimator.taxoutput.get("1.0", "end-1c").strip() != "":
           if tax_estimator.taxoutput1.get("1.0", "end-1c").strip() != "":
            has_input = True

       # If nothing to clear, show message and return
       if not has_input:
           messagebox.showinfo("No Input", "No input to clear.")
           return

       # Ask for confirmation
       confirm = messagebox.askyesno("Clear All", "Are you sure you want to clear all input fields and output?")

       if confirm:
           # Clear all input fields
           for entry in [tax_estimator.income, tax_estimator.epf, tax_estimator.insurance,
                         tax_estimator.edufee, tax_estimator.donate, tax_estimator.pcb]:
               entry.delete(0, 'end')
           tax_estimator.taxoutput.config(state="normal")
           tax_estimator.taxoutput1.config(state="normal")
           # Clear output field
           tax_estimator.taxoutput.delete("1.0", "end")
           tax_estimator.taxoutput1.delete("1.0", "end")

           tax_estimator.taxoutput.config(state="disabled")
           tax_estimator.taxoutput1.config(state="disabled")


#run program function
def runprogram(username):
   run = taxwindow(username)
   run.mainloop()

#runprogram("")