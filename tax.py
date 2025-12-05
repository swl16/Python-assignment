import tkinter as tk
from tkinter import messagebox

TaxRate = (0.0, 0.01, 0.03, 0.06, 0.11, 0.19, 0.25, 0.26, 0.28, 0.30)
basetax = [5000, 5000, 20000, 35000, 50000, 70000, 100000, 400000, 600000, 2000000]
fixedtax = (0, 0, 150, 600, 1500, 3700, 9400, 84400, 136400, 528400)

def taxcalculation(chargeable_income):
   if chargeable_income<=0:
      return 0.0
   remaining_tax = chargeable_income
   taxbalance = 0.0
   if 0 <= remaining_tax <= 5000:
      taxbalance = fixedtax[0] + (remaining_tax - basetax[0]) * TaxRate[0]
   elif 5001 <= remaining_tax <= 20000:
      taxbalance = fixedtax[1] + (remaining_tax - basetax[1]) * TaxRate[1]
   elif 20001 <= remaining_tax <= 35000:
      taxbalance = fixedtax[2] + (remaining_tax - basetax[2]) * TaxRate[2]
   elif 35001 <= remaining_tax <= 50000:
      taxbalance = fixedtax[3] + (remaining_tax - basetax[3]) * TaxRate[4]
   elif 50001 <= remaining_tax <= 70000:
      taxbalance = fixedtax[4] + (remaining_tax - basetax[4]) * TaxRate[1]
   elif 70001 <= remaining_tax <= 100000:
      taxbalance = fixedtax[5] + (remaining_tax - basetax[5]) * TaxRate[1]
   elif 100001 <= remaining_tax <= 400000:
      taxbalance = fixedtax[6] + (remaining_tax - basetax[6]) * TaxRate[1]
   elif 400001 <= remaining_tax <= 600000:
      taxbalance = fixedtax[7] + (remaining_tax - basetax[7]) * TaxRate[1]
   elif 600001 <= remaining_tax <= 2000000:
      taxbalance = fixedtax[8] + (remaining_tax - basetax[8]) * TaxRate[1]
   elif remaining_tax > 2000000:
      taxbalance = fixedtax[9] + (remaining_tax - basetax[9]) * TaxRate[1]

   return round(taxbalance,2)
   

def taxwindow():
 tax_estimator = tk.Toplevel()
 tax_estimator.title("SIMPLE TAX ESTIMATOR")
 tax_estimator.geometry("500x650")

 tk.Label(tax_estimator, text="Simple Tax Estimator", font=("Arial",18,"bold")).pack(pady=20)

 tk.Label(tax_estimator, text="Annual Income (RM): ").pack()
 income_entry = tk.Entry(tax_estimator, width=30)
 income_entry.pack()

 tk.Label(tax_estimator, text="Individual (RM) : 9000", width=30).pack()

 tk.Label(tax_estimator, text="Enter EPF Contribution (RM) : ").pack()
 epf_entry = tk.Entry(tax_estimator, width=30)   
 epf_entry.pack()

 tk.Label(tax_estimator, text="Enter insurance amount(limited to RM7000) (RM) : ").pack()
 insurance_entry = tk.Entry(tax_estimator, width=30)
 insurance_entry.pack()

 tk.Label(tax_estimator, text="Enter self education fees(limited to 7000) (RM) : ").pack()
 edufee_entry = tk.Entry(tax_estimator, width=30)
 edufee_entry.pack()

 tk.Label(tax_estimator, text="Enter Donation amount (RM) : ").pack()
 donate_entry = tk.Entry(tax_estimator, width=30)
 donate_entry.pack()

 tk.Label(tax_estimator, text="Enter the amount of monthly tax deduction(PCB) (RM) : ").pack()
 pcb_entry = tk.Entry(tax_estimator, width=30)
 pcb_entry.pack()

 taxoutput = tk.Text(tax_estimator, width=60, height=12,font=("Arial",12))

 def runtax():
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
      taxoutput.insert("end", "Tax payable > PCB. There is insufficient tax payment")
   else:
      taxoutput.insert("end", "Tax payable < PCB. There is excess deduction.")

 tk.Button(tax_estimator, text="Calculate Tax", width=18, command=runtax).pack(pady=6)
