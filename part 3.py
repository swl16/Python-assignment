import tkinter as tk
from tkinter import messagebox

# ==============================
# Malaysia Tax Table (Tuple + List)
# ==============================
TaxRate = (0.00, 0.01, 0.03, 0.06, 0.11, 0.19, 0.25, 0.26, 0.28, 0.30)
BaseTax = [5000, 5000, 20000, 35000, 50000, 70000, 100000, 400000, 600000, 2000000]
FixedTax = (0, 0, 150, 600, 1500, 3700, 9400, 84400, 136400, 528400)


# ==============================
# Calculate Tax (Uses if-else + tuple + list)
# ==============================
def taxcalculation(chargeable_income):

    if chargeable_income <= 0:
        return 0.0

    # Using if-elif (Requirement)
    if 0 <= chargeable_income <= 5000:
        return 0.0
    elif 5001 <= chargeable_income <= 20000:
        return round(FixedTax[1] + (chargeable_income - BaseTax[1]) * TaxRate[1], 2)
    elif 20001 <= chargeable_income <= 35000:
        return round(FixedTax[2] + (chargeable_income - BaseTax[2]) * TaxRate[2], 2)
    elif 35001 <= chargeable_income <= 50000:
        return round(FixedTax[3] + (chargeable_income - BaseTax[3]) * TaxRate[3], 2)
    elif 50001 <= chargeable_income <= 70000:
        return round(FixedTax[4] + (chargeable_income - BaseTax[4]) * TaxRate[4], 2)
    elif 70001 <= chargeable_income <= 100000:
        return round(FixedTax[5] + (chargeable_income - BaseTax[5]) * TaxRate[5], 2)
    elif 100001 <= chargeable_income <= 400000:
        return round(FixedTax[6] + (chargeable_income - BaseTax[6]) * TaxRate[6], 2)
    elif 400001 <= chargeable_income <= 600000:
        return round(FixedTax[7] + (chargeable_income - BaseTax[7]) * TaxRate[7], 2)
    elif 600001 <= chargeable_income <= 2000000:
        return round(FixedTax[8] + (chargeable_income - BaseTax[8]) * TaxRate[8], 2)
    else:
        return round(FixedTax[9] + (chargeable_income - BaseTax[9]) * TaxRate[9], 2)



# ============================================================
# GUI CLASS (Inheritance requirement ✔)
# ============================================================
class TaxEstimatorApp(tk.Tk):
    def __init__(self, username):
        super().__init__()

        # Encapsulation: local variable
        self.username = username
        self.history_file = f"{self.username}_history.txt"

        # GUI Setup
        self.title("SIMPLE TAX ESTIMATOR")
        self.geometry("550x700")

        # Title
        tk.Label(self, text="Simple Tax Estimator", font=("Arial", 18, "bold"),
                 fg="white", bg="#7e9aed", relief="ridge", bd=3,
                 padx=20, pady=15).pack(fill="x", pady=20)

        # Input frames
        self.income = self.create_input("Annual Income (RM):")
        self.epf = self.create_input("EPF Contribution (RM):")
        self.insurance = self.create_input("Insurance (max RM7000):")
        self.education = self.create_input("Self Education Fees (max RM7000):")
        self.donation = self.create_input("Donation (RM):")
        self.pcb = self.create_input("Monthly PCB (RM):")

        tk.Label(self, text="Individual Relief: RM 9000", font=("Arial", 13, "bold")).pack(pady=5)

        # Output textbox
        self.output = tk.Text(self, width=60, height=12, font=("Arial", 12))
        self.output.pack(pady=15)

        # Buttons
        tk.Button(self, text="Calculate Tax", width=15, font=("Arial", 14, "bold"),
                  bg="#7e9aed", command=self.calculate).pack(pady=10)

        tk.Button(self, text="History", width=15, font=("Arial", 11, "bold"),
                  bg="#7e9aed", command=self.load_history).pack()

        tk.Button(self, text="Delete History", width=15,
                  font=("Arial", 11, "bold"), bg="red", fg="white",
                  command=self.delete_history).pack(pady=10)

    # ============= Create reusable input row =================
    def create_input(self, label_text):
        frame = tk.Frame(self)
        frame.pack(fill="x", pady=5)
        tk.Label(frame, text=label_text, font=("Arial", 12, "bold")).pack(side="left")
        entry = tk.Entry(frame, width=30, font=("Arial", 11))
        entry.pack(side='left', padx=10)
        return entry

    # ============================================================
    # Save History Function (File writing ✔)
    # ============================================================
    def save_history(self, text):
        with open(self.history_file, "a") as f:
            f.write(text + "\n" + "-" * 50 + "\n")

    # ============================================================
    # Calculation Logic (If-Else + Match + loops + exception)
    # ============================================================
    def calculate(self):

        # While loop example (keep checking for missing fields)
        for entry in [self.income, self.epf, self.insurance, self.education, self.donation, self.pcb]:
            if entry.get().strip() == "":
                messagebox.showerror("Error", "Please fill all fields.")
                return

        # Exception handling
        try:
            income = float(self.income.get())
            epf = float(self.epf.get())
            insurance = float(self.insurance.get())
            edu = float(self.education.get())
            donate = float(self.donation.get())
            pcb = float(self.pcb.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Numbers only.")
            return

        relief = 9000 + epf + insurance + edu
        chargeable = income - relief - donate
        tax = taxcalculation(chargeable)

        # Match-case requirement ✔
        match True:
            case _ if chargeable <= 35000:
                rebate = 400
            case _:
                rebate = 0

        tax_payable = tax - rebate
        total_pcb = pcb * 12

        # Display
        self.output.delete("1.0", "end")
        result = (
            f"Income: RM {income:.2f}\n"
            f"Total Relief: RM {relief:.2f}\n"
            f"Chargeable Income: RM {chargeable:.2f}\n"
            f"Tax: RM {tax:.2f}\n"
            f"Rebate: RM {rebate:.2f}\n"
            f"Tax Payable: RM {tax_payable:.2f}\n"
            f"Total PCB (12 months): RM {total_pcb:.2f}\n"
        )
        self.output.insert("end", result)

        # Save to file
        self.save_history(result)

    # ============================================================
    # Load History (File read ✔ + Scrollbar)
    # ============================================================
    def load_history(self):
        win = tk.Toplevel(self)
        win.title("History")
        win.geometry("500x500")

        scrollbar = tk.Scrollbar(win)
        scrollbar.pack(side="right", fill="y")

        text = tk.Text(win, width=60, height=25, yscrollcommand=scrollbar.set)
        text.pack()

        scrollbar.config(command=text.yview)

        try:
            with open(self.history_file, "r") as f:
                text.insert("end", f.read())
        except FileNotFoundError:
            text.insert("end", "No history found.")

    # ============================================================
    # Delete History (File overwrite ✔)
    # ============================================================
    def delete_history(self):
        confirm = messagebox.askyesno("Confirm", "Delete ALL history?")
        if confirm:
            open(self.history_file, "w").close()
            messagebox.showinfo("Deleted", "History cleared.")



# ============================
# Run Program
# ============================
def taxwindow(username="User"):
    app = TaxEstimatorApp(username)
    app.mainloop()


taxwindow("TestUser")
