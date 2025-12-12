import tkinter as tk
from tkinter import messagebox

#from google LHDN Malaysia, latest tax rate 
TaxRate = (0.0, 0.01, 0.03, 0.06, 0.11, 0.19, 0.25, 0.26, 0.28, 0.30)
basetax = [5000, 5000, 20000, 35000, 50000, 70000, 100000, 400000, 600000, 2000000]
fixedtax = (0, 0, 150, 600, 1500, 3700, 9400, 84400, 136400, 528400)

# calculate the income tax balance
def taxcalculation(chargeable_income):
   if chargeable_income<=0:
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

   return round(taxbalance,2)
 
 
class taxwindow(tk.Tk):
   def __init__(tax_estimator,username):
    super().__init__()
     
    tax_estimator.username = username
    tax_estimator.cal_history = f"{tax_estimator.username}_history.txt"

    tax_estimator.title("SIMPLE TAX ESTIMATOR")
    tax_estimator.geometry("750x700")

    #title
    tk.Label(tax_estimator, text="Simple Tax Estimator", font=("Arial",18,"bold"),fg='white', bg='#7e9aed',
          relief='ridge', bd=3, padx=20, pady=15).pack(padx=20, pady=(30,20))
 
    tax_estimator.income = tax_estimator.frame_input("Annual Income (RM)                                                       : ")
    tax_estimator.epf = tax_estimator.frame_input("Enter EPF Contribution (RM)                                         : ")
    tax_estimator.insurance = tax_estimator.frame_input("Enter insurance amount(max RM7000) (RM)                  : ")
    tax_estimator.edufee = tax_estimator.frame_input("Enter self education fees(max RM7000) (RM)                 : ")
    tax_estimator.donate = tax_estimator.frame_input("Enter Donation amount (RM)                                         : ")
    tax_estimator.pcb = tax_estimator.frame_input("Enter the amount of monthly tax deduction(PCB) (RM) : ")

    frame1 = tk.Frame(tax_estimator)
    frame1.pack(fill="x", padx=20, pady=6)

    tk.Label(frame1, text="Individual Relief (RM) : 9000", font=('Arial',13,'bold')).pack(side='left')
 
    #output text
    tax_estimator.taxoutput = tk.Text(tax_estimator, width=60, height=12,font=("Arial",12))
    tax_estimator.taxoutput.pack(pady=15)

    tk.Button(tax_estimator, text="Calculate Tax", width=15, font=("Arial",15,'bold'), fg='white',bg='#7e9aed',relief='ridge', bd=2, 
           padx=10, command=tax_estimator.runtax).pack(pady=(40,10),anchor='center')
    tk.Button(tax_estimator, text="Calculation History", width=15, font=("Arial",11,'bold'), fg='black',bg='#7e9aed',relief='ridge', bd=2, 
           padx=10, command=tax_estimator.loadcalhistory).pack(pady=(40,10),anchor='center',side='bottom')

   def frame_input(tax_estimator,result):
      frame = tk.Frame(tax_estimator)
      frame.pack(fill="x", padx=20, pady=6)
      tk.Label(frame, text=result, font=("Arial", 13, "bold")).pack(side='left')
      entry = tk.Entry(frame, width=30, font=('Arial', 11))
      entry.pack(side='left', padx=10)

      return entry

   #calculation
   def runtax(tax_estimator):
    
    for entry in [tax_estimator.income, tax_estimator.pcb, tax_estimator.insurance, tax_estimator.edufee, tax_estimator.donate,tax_estimator.pcb]:
       if entry.get().strip() == "":
          messagebox.showerror("Input Error!", "Please fill in ALL fields before calculating.")
          return

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
      if insurance > 7000:
         messagebox.showerror("Error!", "The Maximum amount for insurance is RM7000. Please try again")
         return
      elif education > 7000:
         messagebox.showerror("Error!", "The Maximum amount for education fee is RM7000. Please try again")
         return
        
    individual = 9000.00
    taxrelief = individual + epf + insurance + education
    chargeable_income = income - taxrelief - donation

    tax = taxcalculation(chargeable_income)

    match True:
       case _ if chargeable_income <= 35000:
           rebate = 400.0
       case _:
          rebate = 0.0

    taxpayable = tax - rebate

    totalpcb = pcb * 12

    tax_estimator.taxoutput.delete("1.0", "end")
    result = (f"Annual Income: RM {income:.2f}\n"
              f"Total Tax Relief (included Individual) : RM {taxrelief:.2f}\n"
              f"Chargeable Income : RM {chargeable_income:.2f}\n"
              f"Estimated Income Tax : RM {tax:.2f}\n"
              f"Eligible Rebate : RM {rebate:.2f}\n"
              f"Estimated Income Tax Payable : RM {taxpayable:.2f}\n"
              f"Total PCB (12 Months) : RM {totalpcb:.2f}\n")
    tax_estimator.taxoutput.insert("end", result)
    if taxpayable > totalpcb:
      tax_estimator.taxoutput.insert("end", "❗Tax payable > PCB. There is insufficient tax payment.")
    else:
      tax_estimator.taxoutput.insert("end", "✔ Tax payable < PCB. There is excess deduction. You get refund.")

    tax_estimator.savecalhistory(result)

   def savecalhistory(tax_estimator, text):
    with open(tax_estimator.cal_history,"a") as f:
      f.write(text + "\n" + "-" * 50 + "\n")

   def loadcalhistory(tax_estimator):
     history_window = tk.Toplevel(tax_estimator)
     history_window.title(f"Calculation History")
     history_window.geometry("500x650")

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

     def deletehistory():
      confirm = messagebox.askyesno("Confirm delete all calculation history?")
     
      with open(tax_estimator.cal_history, "r") as f:
         content = f.read()
         if content.strip() == "":
             messagebox.showinfo("No History", "No calculation history to delete.")
             return
         elif confirm:
             with open(tax_estimator.cal_history,"w").close():
              messagebox.showinfo("History Deleted", "Calculation history deleted successfully")

     tk.Button(history_window, text="Delete History", width=15, font=("Arial",11,'bold'), fg='black',bg="#ff0000",relief='ridge', bd=2, 
           padx=10, command=deletehistory).pack(pady=(40,10),anchor='center')

   def destroypage(tax_estimator):
    tax_estimator.destroy()

    tk.Button(tax_estimator, text="Back", width=10, font=("Arial",15,'bold'), fg='black',bg='#7e9aed',relief='ridge', bd=2, 
           padx=10, command=tax_estimator.destroypage).pack(pady=(40,10),anchor='w',side='left')


def runwindow(username = "User"):
   run = taxwindow(username)
   run.mainloop()

runwindow("TestUser")