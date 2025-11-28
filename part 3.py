print("Simple Tax Estimator\n")

while True:
 annual = float(input("Annual Income (RM) : "))
 
 print("Individual : RM 9000")
 epf = float(input("\nEnter EPF Contribution (RM) : "))
 insurance = float (input("Enter Insurance amount(limited to RM7000) (RM) : "))
 if insurance >7000:
  print("Exceed RM7000. Please try again.")
  continue
 
 education = float(input("Enter self education fees(limited to 7000) (RM) : "))
 if education >7000:
  print("Exceed RM7000. Please try again.")
  continue

 individual = 9000

 taxrelief = epf + insurance + education + individual

 donation = float(input("Enter Donation amount (RM) : "))

 chargeable = annual - taxrelief - donation

 if chargeable > 0 and chargeable <=5000:
  rate = 0
  tax = 0
  tax2 = 0
 elif chargeable >=5001 and chargeable <=20000:
  rate = 0.01
  tax = 0
  tax2 = (chargeable - 5000) * rate
 elif chargeable >=20001 and chargeable <= 35000:
  rate = 0.03
  tax = 150
  tax2 = (chargeable - 20000) * rate
 elif chargeable >=35001 and chargeable <= 50000:
  rate = 0.08
  tax = 600
  tax2 = (chargeable - 35000) * rate
 elif chargeable >=50001 and chargeable <= 70000:
  rate = 0.14
  tax = 1800
  tax2 = (chargeable - 50000) * rate
 elif chargeable >=70001 and chargeable <= 100000:
  rate = 0.21
  tax = 4600
  tax2 = (chargeable - 70000) * rate
 elif chargeable >=100001 and chargeable <= 250000:
  rate = 0.24
  tax = 10900
  tax2 = (chargeable - 100000) * rate
 elif chargeable >=250001 and chargeable <= 400000:
  rate = 0.245
  tax = 46900
  tax2 = (chargeable - 250000) * rate
 elif chargeable >=400001 and chargeable <= 600000:
  rate = 0.25
  tax = 83650
  tax2 = (chargeable - 400000) * rate
 elif chargeable >=600001 and chargeable <= 1000000:
  rate = 0.26
  tax = 133650
  tax2 = (chargeable - 600000) * rate
 elif chargeable >=1000001 and chargeable <= 2000000:
  rate = 0.28
  tax = 237650
  tax2 = (chargeable - 1000000) * rate
 elif chargeable >2000000:
  rate = 0.30
  tax = 517650
  tax2 = (chargeable - 2000000) * rate

 totaltax = tax + tax2

 if chargeable <= 35000:
  rebate = 400
  print(f"Eligible rebate : RM{rebate}")

 taxpayable = totaltax - rebate

 pcb = float(input("Enter the amount of monthly tax deduction(PCB) (RM) : "))

 totalpcb = pcb * 12

 if taxpayable > totalpcb:
  taxpayment = taxpayable - totalpcb
  print(f"You needed to pay RM{taxpayment:.2f} to IRB because the deducted PCB was incufficient for your income tax.")
  break
 else:
  taxpayment = totalpcb - taxpayable
  print(f"RM{taxpayment:.2f} of excess deduction of PCB will be refunded by IRB to your bank account.")
  break
