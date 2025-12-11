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
 
 
 # window to insert the tax information and calculate the tax 
def taxwindow(username):
  
  Username = username
  cal_history = f"{Username}_history.txt"

  def savecalhistory(income,taxrelief,chargeable_income,tax,rebate,taxpayable,totalpcb):
   with open(cal_history,"a") as f:
      f.write(f"{Username}'s Calculation History\n")
      f.write(f"Annual Income : RM {income:.2f}\n")
      f.write(f"Total Tax Relief (included Individual) : RM {taxrelief:.2f}\n")
      f.write(f"Chargeable Income : RM {chargeable_income:.2f}\n")
      f.write(f"Estimated Income Tax : RM {tax:.2f}\n")
      f.write(f"Eligible Rebate : RM {rebate:.2f}\n")
      f.write(f"Estimated Income Tax Payable : RM {taxpayable:.2f}\n")
      f.write(f"Total PCB Deducted : RM {totalpcb:.2f}\n")
      f.write("-" * 50 + "\n")

  def loadcalhistory():
     history_window = tk.Toplevel()
     history_window.title(f"{Username}'s Calculation History")
     history_window.geometry("500x650")

     # create a scrollbar
     scrollbar = tk.Scrollbar(history_window)
     scrollbar.pack(fill='y', side='right')

     textarea = tk.Text(history_window, width=65, height=35, font=("Arial",13), yscrollcommand=scrollbar.set)
     textarea.pack(padx=10, pady=10)
     
     #update the scrollbar, users can scroll vertically
     scrollbar.config(command=textarea.yview)

     try:
        with open(cal_history, "r") as f:
           content = f.read()
           if content.strip() == "":
              textarea.insert("end", "No calculation history found")
           else:
              textarea.insert("end", content)
     except FileNotFoundError:
        textarea.insert("end", "No history file found from this user")

     tk.Button(history_window, text="Delete History", width=15, font=("Arial",11,'bold'), fg='black',bg='#7e9aed',relief='ridge', bd=2, 
           padx=10, command=deletehistory).pack(pady=(40,10),anchor='center')

  def deletehistory():
     confirm = messagebox.askyesno("Confirm want to delete all calculation history?")

     if confirm:
        with open(cal_history,"w") as f:
           f.close()
           messagebox.showinfo("History Deleted", "Calculation history deleted successfully")

  tax_estimator = tk.Tk()
  tax_estimator.title("SIMPLE TAX ESTIMATOR")
  tax_estimator.geometry("550x670")

 #do a frame so that two widgets can be on the same line
  frame = tk.Frame(tax_estimator)
  frame.pack(fill="x", padx=20, pady=6)

 #title
  tk.Label(frame, text="Simple Tax Estimator", font=("Arial",18,"bold"),fg='white', bg='#7e9aed',
          relief='ridge', bd=3, padx=20, pady=15).pack(fill='x', padx=20, pady=(30,20))
 
  tk.Label(frame, text="Annual Income (RM)                                                       : ", font=('Arial', 13, 'bold')).pack(side="left")
  income_entry = tk.Entry(frame, width=30, font=('Arial', 11))
  income_entry.pack(side="left", padx=10)

  frame1 = tk.Frame(tax_estimator)
  frame1.pack(fill="x", padx=20, pady=6)

  tk.Label(frame1, text="Enter EPF Contribution (RM)                                         : ", font=('Arial', 13, 'bold')).pack(side="left")
  epf_entry = tk.Entry(frame1, width=30, font=('Arial', 11))
  epf_entry.pack(side="left", padx=10)

  frame2 = tk.Frame(tax_estimator)
  frame2.pack(fill="x", padx=20, pady=6)

  tk.Label(frame2, text="Enter insurance amount(max RM7000) (RM)                  : ", font=('Arial', 13, 'bold')).pack(side="left")
  insurance_entry = tk.Entry(frame2, width=30, font=('Arial', 11))
  insurance_entry.pack(side="left", padx=10)

  frame3 = tk.Frame(tax_estimator)
  frame3.pack(fill="x", padx=20, pady=6)

  tk.Label(frame3, text="Enter self education fees(max RM7000) (RM)                 : ", font=('Arial', 13, 'bold')).pack(side="left")
  edufee_entry = tk.Entry(frame3, width=30, font=('Arial', 11))
  edufee_entry.pack(side="left", padx=10)

  frame4 = tk.Frame(tax_estimator)
  frame4.pack(fill="x", padx=20, pady=6)

  tk.Label(frame4, text="Enter Donation amount (RM)                                         : ", font=('Arial', 13, 'bold')).pack(side="left")
  donate_entry = tk.Entry(frame4, width=30, font=('Arial', 11))
  donate_entry.pack(side="left", padx=10)

  frame5 = tk.Frame(tax_estimator)
  frame5.pack(fill="x", padx=20, pady=6)

  tk.Label(frame5, text="Enter the amount of monthly tax deduction(PCB) (RM) : ", font=('Arial', 13, 'bold')).pack(side="left")
  pcb_entry = tk.Entry(frame5, width=30, font=('Arial', 11))
  pcb_entry.pack(side="left", padx=10)

  frame6 = tk.Frame(tax_estimator)
  frame6.pack(fill="x", padx=20, pady=6)

  tk.Label(frame6, text="Individual Relief (RM) : 9000", font=('Arial',13,'bold')).pack(side='left')
 
  #output text
  taxoutput = tk.Text(tax_estimator, width=60, height=12,font=("Arial",12))
  taxoutput.pack(pady=15)

  #calculation
  def runtax():

   if(income_entry.get().strip() == "" or
      epf_entry.get().strip() == "" or
      insurance_entry.get().strip() == "" or
      edufee_entry.get().strip() == "" or
      donate_entry.get().strip() == "" or
      pcb_entry.get().strip() == ""):

      messagebox.showerror("Input Error!", "Please fill in ALL fields before calculating.")
      return

   try:
     income = float(income_entry.get() or 0)
     epf = float(epf_entry.get() or 0)
     insurance = float(insurance_entry.get() or 0) 
     education = float(edufee_entry.get() or 0)
     donation = float(donate_entry.get() or 0)
     pcb = float(pcb_entry.get() or 0)
   except ValueError:
     messagebox.showerror("Error!","Please enter valid numeric values.")
     return
        
   individual = 9000.00
   taxrelief = individual + epf + insurance + education
   chargeable_income = income - taxrelief - donation

   tax = taxcalculation(chargeable_income)

   rebate = 0.0
   if chargeable_income <= 35000:
      rebate = 400.0

   taxpayable = tax - rebate

   totalpcb = pcb * 12

   taxoutput.delete("1.0", "end")
   taxoutput.insert("end", f"Annual Income : RM {income:.2f}\n")
   taxoutput.insert("end", f"Total Tax Relief (included Individual) : RM {taxrelief:.2f}\n")
   taxoutput.insert("end", f"Chargeable Income : RM {chargeable_income:.2f}\n")
   taxoutput.insert("end", f"Estimated Income Tax : RM {tax:.2f}\n")
   taxoutput.insert("end", f"Eligible Rebate : RM {rebate:.2f}\n")
   taxoutput.insert("end", f"Estimated Income Tax Payable : RM {taxpayable:.2f}\n")
   taxoutput.insert("end", f"Total PCB Deducted : RM {totalpcb:.2f}\n")
   if taxpayable > totalpcb:
      taxoutput.insert("end", "❗Tax payable > PCB. There is insufficient tax payment.")
   else:
      taxoutput.insert("end", "✔ Tax payable < PCB. There is excess deduction. You get refund.")

   savecalhistory(income,taxrelief,chargeable_income,tax,rebate,taxpayable,totalpcb)

  def destroypage():
   tax_estimator.destroy()

  tk.Button(tax_estimator, text="Calculate Tax", width=15, font=("Arial",15,'bold'), fg='white',bg='#7e9aed',relief='ridge', bd=2, 
           padx=10, command=runtax).pack(pady=(40,10),anchor='center')
  tk.Button(tax_estimator, text="Calculation History", width=15, font=("Arial",11,'bold'), fg='black',bg='#7e9aed',relief='ridge', bd=2, 
           padx=10, command=loadcalhistory).pack(pady=(40,10),anchor='center')
  tk.Button(tax_estimator, text="Back", width=10, font=("Arial",15,'bold'), fg='black',bg='#7e9aed',relief='ridge', bd=2, 
           padx=10, command=destroypage).pack(pady=(40,10),anchor='center')
 
  #tax_estimator.mainloop()

#taxwindow()

