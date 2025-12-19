import json
import os
import datetime
import math
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# --- Configuration and Constants ---
DATA_FILE = "savings_goals.json"
DATE_FORMAT = "%d-%m-%Y"
HIST_TIME_FORMAT = "%d %b %Y   %I:%M %p" 
MALAYSIA_TIMEZONE_OFFSET = datetime.timezone(datetime.timedelta(hours=8)) # GMT+8
CURRENCY_SYMBOL = "RM"

# --- Core Logic Functions ---

def load_goals():
    # Chapter 4C: Text File Processing (Opening Files)
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r') as f:
            # Chapter 5B: Dictionaries (Loading data structure)
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_goals(goals):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(goals, f, indent=4)
    except IOError as e:
        messagebox.showerror("File Error", f"Could not save data: {e}")

def calculate_pacing_and_status(goal):
    target_date_str = goal.get('target_date')
    saved = goal.get('saved', 0.0)
    target = goal.get('target', 0.0)
    date_created_str = goal.get('date_created')

    # Chapter 3A: Selection Control (Checking completion)
    if target <= saved:
        return 0.0, 0, "Complete"

    try:
        target_date = datetime.datetime.strptime(target_date_str, DATE_FORMAT).date()
        date_created = datetime.datetime.fromisoformat(date_created_str).date() 
    except (ValueError, TypeError):
        return target - saved, 1, "Data Error"

    today = datetime.date.today()
    if target_date <= today:
        return max(0, target - saved), 0, "Overdue"

    months_remaining = (target_date.year - today.year) * 12 + (target_date.month - today.month)
    if target_date.day > today.day:
        months_remaining += 1
    months_remaining = max(1, months_remaining)
    
    required_monthly = (target - saved) / months_remaining
    total_months = max(1, (target_date.year - date_created.year) * 12 + (target_date.month - date_created.month))
    months_elapsed = (today.year - date_created.year) * 12 + (today.month - date_created.month)
    
    expected_saved = (target / total_months) * months_elapsed if months_elapsed < total_months else target
    current_status = "On Track" if saved >= expected_saved else "Falling Behind"

    return required_monthly, months_remaining, current_status

# --- UI Component: World Clock ---

class WorldClock(ttk.Frame):
    def __init__(self, master, style_name, *args, **kwargs):
        super().__init__(master, style=style_name, *args, **kwargs)
        self.time_label = ttk.Label(self, font=('Arial', 11, 'bold'), foreground='#004d40', background='#b3e5fc', padding=5)
        self.time_label.pack(fill='x', padx=10, pady=5)
        self.timer_id = None
        self.update_time()

    def update_time(self):
        if not self.winfo_exists(): return
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        malaysia_time = now_utc.astimezone(MALAYSIA_TIMEZONE_OFFSET)
        display_text = f"Malaysia Time (GMT+8)\n{malaysia_time.strftime('%d %b %Y')}\n{malaysia_time.strftime('%I:%M:%S %p')}"
        self.time_label.config(text=display_text)
        self.timer_id = self.after(1000, self.update_time)

    def stop(self):
        if self.timer_id: self.after_cancel(self.timer_id)

# --- Main Application ---

class GoalTrackerApp:
    def __init__(self, username, mainmenu):
        self.username = username
        self.mainmenu = mainmenu
        self.mainmenu.withdraw()

        self.master = tk.Tk()
        self.master.protocol("WM_DELETE_WINDOW", self.back_menu)
        self.master.title("Savings Goal Tracker")
        
        self.goals = load_goals()
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f7f2e9')
        style.configure('TLabel', background='#f7f2e9', font=('Arial', 10))
        style.configure('Clock.TFrame', background='#b3e5fc', relief='raised', borderwidth=1)
        
        self.main_frame = ttk.Frame(self.master, padding="15")
        self.main_frame.pack(fill='both', expand=True)

        self.top_panel = ttk.Frame(self.main_frame)
        self.top_panel.pack(fill='x', pady=(0, 20))
        
        ttk.Button(self.top_panel, text="< Back", command=self.back_menu).pack(side=tk.LEFT)
        ttk.Label(self.top_panel, text="Financial Goals Dashboard", font=('Arial', 16, 'bold')).pack(side=tk.LEFT, padx=20)
        self.clock = WorldClock(self.top_panel, style_name='Clock.TFrame')
        self.clock.pack(side=tk.RIGHT)

        # Table Setup
        self.tree = ttk.Treeview(self.main_frame, columns=("BILL", "Name", "Target", "Saved", "Progress", "Status", "Monthly Req."), show="headings")
        cols = ["BILL", "Name", "Target", "Saved", "Progress", "Status", "Monthly Req."]
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor=tk.CENTER)
        self.tree.pack(fill='both', expand=True)

        # Button Panel
        self.btn_frame = ttk.Frame(self.main_frame, padding="10 0 0 0") 
        self.btn_frame.pack(fill='x', pady=(10, 0))

        ttk.Button(self.btn_frame, text="Add New Goal", command=self.add_goal_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.btn_frame, text="Edit Selected", command=self.edit_goal_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.btn_frame, text="Add Contribution", command=self.add_contribution_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.btn_frame, text="View History", command=self.view_history_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.btn_frame, text="Delete Selected", command=self.delete_goal).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.btn_frame, text="Refresh", command=self.refresh_goal_list).pack(side=tk.RIGHT, padx=5)

        self.refresh_goal_list()

    def back_menu(self):
        if hasattr(self, 'clock'): self.clock.stop()
        self.mainmenu.deiconify()
        self.master.destroy()

    def reindex_goals(self):
        sorted_goals = sorted(self.goals.values(), key=lambda x: x['date_created'])
        new_goals = {}
        for index, goal_data in enumerate(sorted_goals, start=1):
            new_id = str(index)
            goal_data['id'] = new_id
            new_goals[new_id] = goal_data
        self.goals = new_goals
        save_goals(self.goals)

    def refresh_goal_list(self):
        self.reindex_goals()
        for item in self.tree.get_children(): self.tree.delete(item)
        sorted_keys = sorted(self.goals.keys(), key=lambda x: int(x))
        for goal_id in sorted_keys:
            goal = self.goals[goal_id]
            req, _, stat = calculate_pacing_and_status(goal)
            perc = (goal['saved'] / goal['target'] * 100) if goal['target'] > 0 else 0
            self.tree.insert("", tk.END, iid=goal_id, values=(
                goal_id, goal['name'], f"{CURRENCY_SYMBOL} {goal['target']:,.2f}", 
                f"{CURRENCY_SYMBOL} {goal['saved']:,.2f}", f"{perc:,.1f}%", stat, f"{CURRENCY_SYMBOL} {req:,.2f}"
            ))

    def add_goal_dialog(self):
        dialog = tk.Toplevel(self.master); dialog.title("Create New Goal")
        dialog.geometry("350x250"); dialog.grab_set() 
        f = ttk.Frame(dialog, padding=20); f.pack(fill='both', expand=True)

        ttk.Label(f, text="Goal Name:").grid(row=0, column=0, sticky='w', pady=5)
        name_ent = ttk.Entry(f, width=25); name_ent.grid(row=0, column=1, pady=5)
        ttk.Label(f, text=f"Target ({CURRENCY_SYMBOL}):").grid(row=1, column=0, sticky='w', pady=5)
        target_ent = ttk.Entry(f, width=25); target_ent.grid(row=1, column=1, pady=5)
        ttk.Label(f, text="Date (DD-MM-YYYY):").grid(row=2, column=0, sticky='w', pady=5)
        date_ent = ttk.Entry(f, width=25); date_ent.insert(0, datetime.date.today().strftime(DATE_FORMAT))
        date_ent.grid(row=2, column=1, pady=5)

        ttk.Button(f, text="Create Goal", command=lambda: self._submit_new_goal(dialog, name_ent, target_ent, date_ent)).grid(row=3, columnspan=2, pady=20)

    def _submit_new_goal(self, dialog, name_ent, target_ent, date_ent):
        name = name_ent.get().strip()
        try:
            target = float(target_ent.get())
            date_val = date_ent.get().strip()
            datetime.datetime.strptime(date_val, DATE_FORMAT)
            if not name or target <= 0: raise ValueError
        except ValueError:
            return messagebox.showerror("Error", "Check inputs.")

        temp_id = str(len(self.goals) + 1)
        self.goals[temp_id] = {
            'id': temp_id, 'name': name, 'target': target, 'saved': 0.0, 
            'target_date': date_val, 'contributions': [], 'date_created': datetime.datetime.now().isoformat()
        }
        save_goals(self.goals); self.refresh_goal_list(); dialog.destroy()

    def add_contribution_dialog(self):
        selected_id = self.tree.focus()
        if not selected_id: return messagebox.showwarning("Error", "Select a goal first.")
        
        goal = self.goals[selected_id]
        remaining = goal['target'] - goal['saved']
        if remaining <= 0: return messagebox.showinfo("Done", "Goal already funded!")

        amt = simpledialog.askfloat("Contribution", f"Remaining: {CURRENCY_SYMBOL}{remaining:,.2f}\nEnter amount:", minvalue=0.01, maxvalue=remaining)
        if amt:
            # Update values
            self.goals[selected_id]['saved'] += amt
            self.goals[selected_id]['contributions'].append({
                'amount': amt, 
                'timestamp': datetime.datetime.now().strftime(HIST_TIME_FORMAT)
            })
            
            # --- FEATURE: Goal Reached Celebration Logic ---
            if self.goals[selected_id]['saved'] >= goal['target']:
                messagebox.showinfo("CONGRATULATIONS! 🎉", 
                                    f"Amazing work! You have reached your goal for:\n\n'{goal['name']}'\n\nTotal Saved: {CURRENCY_SYMBOL} {self.goals[selected_id]['saved']:,.2f}")
            
            save_goals(self.goals); self.refresh_goal_list()

    def view_history_dialog(self):
        selected_id = self.tree.focus()
        if not selected_id: return messagebox.showwarning("Error", "Select a BILL to view its history.")
        
        goal = self.goals[selected_id]
        history_win = tk.Toplevel(self.master)
        history_win.title(f"History: {goal['name']}")
        history_win.geometry("450x350")
        
        frame = ttk.Frame(history_win, padding=15); frame.pack(fill='both', expand=True)
        ttk.Label(frame, text=f"Transactions for BILL {selected_id}", font=('Arial', 11, 'bold')).pack(pady=(0,10))
        
        hist_tree = ttk.Treeview(frame, columns=("Time", "Amount"), show="headings")
        hist_tree.heading("Time", text="Date & Time (H:M)")
        hist_tree.heading("Amount", text="Amount Paid")
        hist_tree.column("Time", width=250, anchor=tk.W)
        hist_tree.column("Amount", width=120, anchor=tk.CENTER)
        hist_tree.pack(fill='both', expand=True)

        for entry in goal.get('contributions', []):
            hist_tree.insert("", tk.END, values=(entry.get('timestamp', "N/A"), f"{CURRENCY_SYMBOL} {entry['amount']:,.2f}"))
        
        ttk.Button(frame, text="Close", command=history_win.destroy).pack(pady=10)

    def edit_goal_dialog(self):
        selected_id = self.tree.focus()
        if not selected_id: return messagebox.showwarning("Error", "Select a goal.")
        goal = self.goals[selected_id]
        dialog = tk.Toplevel(self.master); dialog.title("Edit Goal")
        f = ttk.Frame(dialog, padding=20); f.pack()
        name_ent = ttk.Entry(f, width=25); name_ent.insert(0, goal['name']); name_ent.grid(row=0, column=1)
        target_ent = ttk.Entry(f, width=25); target_ent.insert(0, str(goal['target'])); target_ent.grid(row=1, column=1)
        date_ent = ttk.Entry(f, width=25); date_ent.insert(0, goal['target_date']); date_ent.grid(row=2, column=1)
        ttk.Button(f, text="Save", command=lambda: self._submit_edit_goal(dialog, name_ent, target_ent, date_ent, selected_id)).grid(row=3, columnspan=2, pady=20)

    def _submit_edit_goal(self, dialog, name_ent, target_ent, date_ent, goal_id):
        try:
            target = float(target_ent.get())
            self.goals[goal_id].update({'name': name_ent.get(), 'target': target, 'target_date': date_ent.get()})
            save_goals(self.goals); self.refresh_goal_list(); dialog.destroy()
        except: messagebox.showerror("Error", "Invalid Edit.")

    def delete_goal(self):
        selected_id = self.tree.focus()
        if selected_id and messagebox.askyesno("Confirm", "Delete this goal? BILL sequence will update."):
            del self.goals[selected_id]
            save_goals(self.goals); self.refresh_goal_list()

if __name__ == "__main__":
    root = tk.Tk(); root.withdraw() 
    app = GoalTrackerApp("User", root)
    root.mainloop()