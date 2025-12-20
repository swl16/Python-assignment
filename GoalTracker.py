import json
import os
import uuid
import datetime
import math
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from time import strftime

# --- Configuration and Constants ---
DATE_FORMAT = "%d-%m-%Y"
MALAYSIA_TIMEZONE_OFFSET = datetime.timezone(datetime.timedelta(hours=8)) # GMT+8
CURRENCY_SYMBOL = "RM" 

# --- Core Logic Functions (Modified to accept filename) ---

def load_goals(filename):
    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_goals(goals, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(goals, f, indent=4)
    except IOError as e:
        messagebox.showerror("File Error", f"Error: Could not save data to file. {e}")

def calculate_pacing_and_status(goal):
    target_date_str = goal.get('target_date')
    saved = goal.get('saved', 0.0)
    target = goal.get('target', 0.0)
    date_created_str = goal.get('date_created')

    if target <= saved:
        return 0.0, 0, "Complete"

    if not target_date_str or not date_created_str:
        return target - saved, 1, "Needs Date"

    try:
        target_date = datetime.datetime.strptime(target_date_str, DATE_FORMAT).date()
        date_created = datetime.datetime.fromisoformat(date_created_str).date() 
    except ValueError:
        return target - saved, 1, "Date Error"

    today = datetime.date.today()
    
    if target_date <= today:
        return max(0, target - saved), 0, "Overdue"

    months_remaining = (target_date.year - today.year) * 12 + (target_date.month - today.month)
    if target_date.day > today.day:
        months_remaining += 1

    months_remaining = max(1, months_remaining)
    amount_remaining = target - saved
    required_monthly = amount_remaining / months_remaining

    total_months = (target_date.year - date_created.year) * 12 + (target_date.month - date_created.month)
    total_months = max(1, total_months)
    months_elapsed = (today.year - date_created.year) * 12 + (today.month - date_created.month)
    
    expected_saved = 0.0
    if months_elapsed > 0 and months_elapsed < total_months:
        expected_saved = (target / total_months) * months_elapsed
    elif months_elapsed >= total_months:
        expected_saved = target

    if saved >= expected_saved:
        current_status = "On Track"
    else:
        current_status = "Falling Behind"

    return required_monthly, months_remaining, current_status

# --- World Clock Class ---

class WorldClock(ttk.Frame):
    def _init_(self, master, style_name, *args, **kwargs):
        super()._init_(master, style=style_name, *args, **kwargs)
        
        self.time_label = ttk.Label(self, 
                                    font=('Arial', 12, 'bold'), 
                                    foreground='#004d40', 
                                    background='#b3e5fc', 
                                    padding=5)
        self.time_label.pack(fill='x', padx=10, pady=5)

        self.timer_id = None
        self.update_time()

    def update_time(self):
        if not self.winfo_exists():
            return

        now_utc = datetime.datetime.now(datetime.timezone.utc)
        malaysia_time = now_utc.astimezone(MALAYSIA_TIMEZONE_OFFSET)
        
        time_str = malaysia_time.strftime('%I:%M:%S %p %Z')
        date_str = malaysia_time.strftime('%A, %d %b %Y')
        
        display_text = f"Malaysia Time (GMT+8)\n{date_str}\n{time_str}"
        self.time_label.config(text=display_text)
        
        self.timer_id = self.after(1000, self.update_time)

    def stop(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None


# --- Tkinter GUI Application Class ---

class GoalTrackerApp:
    def _init_(self, username, mainmenu):

        self.username = username
        self.mainmenu = mainmenu
        self.mainmenu.withdraw()

        # --- SET UNIQUE USER FILENAME ---
        self.filename = f"savings_goals_{self.username}.json"

        self.master = tk.Tk()
        self.master.protocol("WM_DELETE_WINDOW", self.back_menu)
        self.master.title(f"Savings Goal Tracker - {self.username} ({CURRENCY_SYMBOL})")
        
        # Load specific user goals
        self.goals = load_goals(self.filename)
        
        # Storing inside self.current_vars to prevent memory scope issues
        self.current_vars = {}
        
        style = ttk.Style()
        style.theme_use('clam')
        
        PRIMARY_BLUE = '#f7f2e9'
        SECONDARY_BLUE = '#b3e5fc' 
        ACCENT_BLUE = '#7e9aed'   
        
        style.configure('TFrame', background=PRIMARY_BLUE)
        style.configure('TLabel', background=PRIMARY_BLUE, font=('Arial', 10))
        style.configure('Clock.TFrame', background=SECONDARY_BLUE, relief='raised', borderwidth=1)

        style.configure('TButton', 
                        background=ACCENT_BLUE, 
                        foreground='white', 
                        font=('Arial', 10, 'bold'), 
                        padding=6, 
                        relief='flat')
        style.map('TButton', 
                 background=[('active', '#03a9f4'), ('pressed', '#0288d1')])
        
        style.configure('Treeview', 
                        background='white', 
                        foreground='#333333',
                        rowheight=25,
                        fieldbackground='white')
        style.configure('Treeview.Heading', 
                        background=SECONDARY_BLUE, 
                        foreground='#000000', 
                        font=('Arial', 10, 'bold'))
        style.map('Treeview.Heading', 
                  background=[('active', ACCENT_BLUE)])

        self.main_frame = ttk.Frame(self.master, padding="15 15 15 15", relief='raised', borderwidth=2)
        self.main_frame.pack(fill='both', expand=True)

        self.back_frame = ttk.Frame(self.main_frame, style='TFrame')
        self.back_frame.pack(fill='x',padx=20,pady=(10,0))

        back_button = ttk.Button(self.back_frame,text = "< Back",command=self.back_menu)
        back_button.pack(side="left")

        self.top_panel = ttk.Frame(self.main_frame, style='TFrame')
        self.top_panel.pack(fill='x', pady=(0, 20))
        
        title_label = ttk.Label(self.top_panel, text="Financial Goals Dashboard", 
                                font=('Arial', 16, 'bold'), 
                                background=PRIMARY_BLUE, 
                                foreground='#004d40')
        title_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.clock = WorldClock(self.top_panel, style_name='Clock.TFrame')
        self.clock.pack(side=tk.RIGHT)

        self.tree = ttk.Treeview(self.main_frame, columns=("ID", "Name", "Target", "Saved", "Progress", "Status", "Monthly Req."), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Goal Name")
        self.tree.heading("Target", text=f"Target ({CURRENCY_SYMBOL})")
        self.tree.heading("Saved", text=f"Saved ({CURRENCY_SYMBOL})")
        self.tree.heading("Progress", text="Progress (%)")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Monthly Req.", text=f"Required Monthly ({CURRENCY_SYMBOL})")

        self.tree.column("ID", width=70, anchor=tk.CENTER)
        self.tree.column("Name", width=150, anchor=tk.W)
        self.tree.column("Target", width=100, anchor=tk.E)
        self.tree.column("Saved", width=100, anchor=tk.E)
        self.tree.column("Progress", width=80, anchor=tk.CENTER)
        self.tree.column("Status", width=120, anchor=tk.CENTER)
        self.tree.column("Monthly Req.", width=120, anchor=tk.E)
        self.tree.pack(fill='both', expand=True)

        self.button_frame = ttk.Frame(self.main_frame, padding="10 0 0 0", style='TFrame')
        self.button_frame.pack(fill='x', pady=(10, 0))

        ttk.Button(self.button_frame, text="Add New Goal", command=self.add_goal_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Edit Goal", command=self.edit_goal_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Record Contribution", command=self.add_contribution_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="View History", command=self.view_goal_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Delete Selected Goal", command=self.delete_goal).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Refresh", command=self.refresh_goal_list).pack(side=tk.RIGHT, padx=5)

        self.refresh_goal_list()

    def back_menu(self):
        if hasattr(self, 'clock'):
            self.clock.stop()
        self.mainmenu.deiconify()
        self.master.destroy()

    # --- EDITED REFRESH GOAL LIST: SEQUENTIAL ID REARRANGEMENT ---
    def refresh_goal_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Sort goals by creation date to maintain sequence consistency
        sorted_goals = sorted(self.goals.items(), key=lambda item: item[1].get('date_created', '0'))

        # Iterate using enumerate to create sequential A1001, A1002 style IDs
        for index, (goal_id, goal) in enumerate(sorted_goals, start=1):
            display_id = f"A{1000 + index}" 

            required_monthly, months_remaining, current_status = calculate_pacing_and_status(goal)
            target = goal.get('target', 0.0)
            saved = goal.get('saved', 0.0)
            name = goal.get('name', 'Untitled')
            percentage = (saved / target * 100) if target > 0 else 0
            monthly_req_display = f"{required_monthly:,.2f}" if current_status not in ["Complete", "Needs Date", "Date Error", "Overdue"] else "N/A"
            
            # Use the internal unique key as iid, but show display_id to the user
            self.tree.insert("", tk.END, iid=goal_id, values=(
                display_id, 
                name, 
                f"{target:,.2f}", 
                f"{saved:,.2f}", 
                f"{percentage:,.1f}", 
                current_status, 
                monthly_req_display
            ), tags=(current_status.replace(" ", "_"),))
            
        self.tree.tag_configure('Falling_Behind', background='#ffcdd2')
        self.tree.tag_configure('Overdue', background='#ffcdd2')
        self.tree.tag_configure('Complete', background='#c8e6c9')
        self.tree.tag_configure('On_Track', background='#bbdefb')

    def add_goal_dialog(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Add New Goal")
        dialog.geometry("300x250")
        dialog.transient(self.master)
        dialog.grab_set()
        
        self.current_vars = {
            "name": tk.StringVar(master=dialog),
            "target": tk.StringVar(master=dialog),
            "date": tk.StringVar(master=dialog, value=datetime.date.today().strftime(DATE_FORMAT))
        }

        form_frame = ttk.Frame(dialog, padding=10)
        form_frame.pack(fill='both', expand=True)
        
        ttk.Label(form_frame, text="Goal Name:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(form_frame, textvariable=self.current_vars["name"]).grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(form_frame, text=f"Target Amount ({CURRENCY_SYMBOL}):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(form_frame, textvariable=self.current_vars["target"]).grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(form_frame, text=f"Target Date ({DATE_FORMAT}):").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(form_frame, textvariable=self.current_vars["date"]).grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        ttk.Button(form_frame, text="Create Goal", 
                   command=lambda: self._submit_new_goal(dialog)).grid(row=3, column=0, columnspan=2, pady=10)
        form_frame.grid_columnconfigure(1, weight=1)

    def _submit_new_goal(self, dialog):
        name = self.current_vars["name"].get().strip()
        target_str = self.current_vars["target"].get().strip()
        date_str = self.current_vars["date"].get().strip()

        if not name:
            messagebox.showerror("Validation Error", "Goal Name is required.")
            return
        try:
            target_amount = float(target_str)
            if target_amount <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Target Amount must be a positive number.")
            return

        try:
            datetime.datetime.strptime(date_str, DATE_FORMAT)
        except ValueError:
            messagebox.showerror("Validation Error", f"Date must be in {DATE_FORMAT} format.")
            return

        new_id = str(uuid.uuid4())
        self.goals[new_id] = {
            'id': new_id, 'name': name, 'target': target_amount, 'saved': 0.0,
            'target_date': date_str, 'contributions': [], 'date_created': datetime.datetime.now().isoformat()
        }
        
        save_goals(self.goals, self.filename)
        self.refresh_goal_list()
        messagebox.showinfo("Success", f"Goal '{name}' successfully added.")
        dialog.destroy()

    def edit_goal_dialog(self):
        selected_item_id = self.tree.focus()
        if not selected_item_id:
            messagebox.showwarning("Selection Error", "Please select a goal to edit.")
            return

        goal = self.goals.get(selected_item_id)
        dialog = tk.Toplevel(self.master)
        dialog.title("Edit Goal Details")
        dialog.geometry("300x250")
        dialog.transient(self.master)
        dialog.grab_set()
        
        self.current_vars = {
            "name": tk.StringVar(master=dialog, value=goal['name']),
            "target": tk.StringVar(master=dialog, value=str(goal['target'])),
            "date": tk.StringVar(master=dialog, value=goal['target_date'])
        }

        form_frame = ttk.Frame(dialog, padding=10)
        form_frame.pack(fill='both', expand=True)
        
        ttk.Label(form_frame, text="Goal Name:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(form_frame, textvariable=self.current_vars["name"]).grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(form_frame, text=f"Target Amount ({CURRENCY_SYMBOL}):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(form_frame, textvariable=self.current_vars["target"]).grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(form_frame, text=f"Target Date ({DATE_FORMAT}):").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(form_frame, textvariable=self.current_vars["date"]).grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        ttk.Button(form_frame, text="Update Goal", 
                   command=lambda: self._submit_edit_goal(dialog, selected_item_id)).grid(row=3, column=0, columnspan=2, pady=10)
        form_frame.grid_columnconfigure(1, weight=1)

    def _submit_edit_goal(self, dialog, goal_id):
        name = self.current_vars["name"].get().strip()
        target_str = self.current_vars["target"].get().strip()
        date_str = self.current_vars["date"].get().strip()

        if not name:
            messagebox.showerror("Error", "Goal Name is required.")
            return
        try:
            target_amount = float(target_str)
            if target_amount < self.goals[goal_id]['saved']:
                messagebox.showerror("Error", f"New target cannot be less than your current savings.")
                return
        except ValueError:
            messagebox.showerror("Error", "Target Amount must be a number.")
            return

        try:
            datetime.datetime.strptime(date_str, DATE_FORMAT)
        except ValueError:
            messagebox.showerror("Error", "Invalid date format.")
            return

        self.goals[goal_id]['name'] = name
        self.goals[goal_id]['target'] = target_amount
        self.goals[goal_id]['target_date'] = date_str
        
        save_goals(self.goals, self.filename)
        self.refresh_goal_list()
        messagebox.showinfo("Success", "Goal details updated.")
        dialog.destroy()

    def add_contribution_dialog(self):
        selected_item_id = self.tree.focus()
        if not selected_item_id:
            messagebox.showwarning("Selection Error", "Please select a goal.")
            return

        goal = self.goals.get(selected_item_id)
        target_val = goal.get('target', 0.0)
        saved_val = goal.get('saved', 0.0)
        remaining_needed = target_val - saved_val

        if remaining_needed <= 0:
            messagebox.showinfo("Goal Completed", "This goal is already fully reached!")
            return

        amount_str = simpledialog.askstring("Record Contribution", 
                                            f"Enter amount for '{goal['name']}'\n"
                                            f"(Remaining Limit: {CURRENCY_SYMBOL}{remaining_needed:,.2f}):",
                                            parent=self.master)
        
        if amount_str is None: return
            
        try:
            contribution_amount = float(amount_str.strip())
            if contribution_amount <= 0:
                messagebox.showerror("Validation Error", "Amount must be positive.")
                return
            if contribution_amount > remaining_needed:
                messagebox.showerror("Limit Exceeded", f"Maximum allowed: {CURRENCY_SYMBOL}{remaining_needed:,.2f}")
                return
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter a number.")
            return

        new_saved = goal['saved'] + contribution_amount
        self.goals[selected_item_id]['saved'] = new_saved
        self.goals[selected_item_id]['contributions'].append({
            'amount': contribution_amount, 'timestamp': datetime.datetime.now().isoformat()
        })
        
        save_goals(self.goals, self.filename)
        self.refresh_goal_list()
        messagebox.showinfo("Success", f"Recorded {CURRENCY_SYMBOL}{contribution_amount:,.2f}.")

    def view_goal_history(self):
        selected_item_id = self.tree.focus()
        if not selected_item_id:
            messagebox.showwarning("Selection Error", "Please select a goal.")
            return

        goal = self.goals.get(selected_item_id)
        contributions = goal.get('contributions', [])

        if not contributions:
            messagebox.showinfo("History", "No contributions recorded yet.")
            return

        history_win = tk.Toplevel(self.master)
        history_win.title(f"History: {goal['name']}")
        history_win.geometry("400x300")

        cols = ("Date", "Amount")
        history_tree = ttk.Treeview(history_win, columns=cols, show="headings")
        history_tree.heading("Date", text="Date & Time")
        history_tree.heading("Amount", text=f"Amount ({CURRENCY_SYMBOL})")
        history_tree.column("Date", width=200, anchor=tk.CENTER)
        history_tree.column("Amount", width=150, anchor=tk.E)
        history_tree.pack(fill='both', expand=True, padx=10, pady=10)

        for entry in contributions:
            dt = datetime.datetime.fromisoformat(entry['timestamp']).strftime("%d-%m-%Y %I:%M %p")
            history_tree.insert("", tk.END, values=(dt, f"{entry['amount']:,.2f}"))

    def delete_goal(self):
        selected_item_id = self.tree.focus()
        if not selected_item_id:
            messagebox.showwarning("Selection Error", "Please select a goal.")
            return
            
        goal = self.goals.get(selected_item_id)
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete goal: '{goal['name']}'?"):
            del self.goals[selected_item_id]
            save_goals(self.goals, self.filename)
            self.refresh_goal_list()
            messagebox.showinfo("Success", "Goal successfully deleted. IDs rearranged.")

# --- STANDALONE TESTING BLOCK ---
if __name__ == "_main_":
    root = tk.Tk()
    root.withdraw()
    
    class MockMainMenu:
        def deiconify(self): print("Returned to Main Menu (Mock)")
        def withdraw(self): pass
        def destroy(self): root.destroy()

    app = GoalTrackerApp("TestUser", MockMainMenu())
    #root.mainloop()