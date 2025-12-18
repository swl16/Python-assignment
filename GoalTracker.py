import json
import os
import uuid
import datetime
import math
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from time import strftime

# --- Configuration and Constants ---
DATA_FILE = "savings_goals.json"
DATE_FORMAT = "%d-%m-%Y"
MALAYSIA_TIMEZONE_OFFSET = datetime.timezone(datetime.timedelta(hours=8)) # GMT+8
CURRENCY_SYMBOL = "RM" # Changed to Malaysia Ringgit

# --- Core Logic Functions ---

def load_goals():
    # Chapter 4C: Text File Processing (Files, Opening Files)
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        # Chapter 4C: Handling File Exceptions
        with open(DATA_FILE, 'r') as f:
            # Chapter 5B: Dictionaries (Loading the goal data structure)
            return json.load(f)
    except json.JSONDecodeError:
        # Chapter 4B: Exception Handling (Handling corrupted data)
        messagebox.showwarning("Data Error", "Data file is corrupted. Starting with an empty goal list.")
        return {}
    except IOError as e:
        messagebox.showerror("File Error", f"Error reading file: {e}")
        return {}

def save_goals(goals):
    try:
        # Chapter 4C: Manipulating Files (Writing to a file)
        with open(DATA_FILE, 'w') as f:
            json.dump(goals, f, indent=4)
    except IOError as e:
        # Chapter 4B: Exception Handling (Handling file write errors)
        messagebox.showerror("File Error", f"Error: Could not save data to file. {e}")

def get_countdown_string(target_date_str):
    """
    Chapter 2C: Strings & Formatting
    Calculates the live time remaining until the target date.
    """
    try:
        target_date = datetime.datetime.strptime(target_date_str, DATE_FORMAT)
        now = datetime.datetime.now()
        diff = target_date - now

        if diff.total_seconds() <= 0:
            return "Time's Up!"
        
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        else:
            return f"{hours}h {minutes}m"
    except:
        return "N/A"

def calculate_pacing_and_status(goal):
    target_date_str = goal.get('target_date')
    saved = goal.get('saved', 0.0)
    target = goal.get('target', 0.0)
    date_created_str = goal.get('date_created')

    # Chapter 3A: Selection Control Structure (One-Way if)
    if target <= saved:
        return 0.0, 0, "Complete"

    # Chapter 3A: Selection Control Structure (Two-Way if-else)
    if not target_date_str or not date_created_str:
        return target - saved, 1, "Needs Date"

    try:
        # Chapter 4B: Exception Handling (Date parsing errors)
        target_date = datetime.datetime.strptime(target_date_str, DATE_FORMAT).date()
        date_created = datetime.datetime.fromisoformat(date_created_str).date() 
    except ValueError:
        return target - saved, 1, "Date Error"

    today = datetime.date.today()
    
    if target_date <= today:
        return max(0, target - saved), 0, "Overdue"

    # Calculate remaining months.
    months_remaining = (target_date.year - today.year) * 12 + (target_date.month - today.month)
    if target_date.day > today.day:
        months_remaining += 1

    months_remaining = max(1, months_remaining)

    amount_remaining = target - saved
    required_monthly = amount_remaining / months_remaining

    # Calculate pacing.
    total_months = (target_date.year - date_created.year) * 12 + (target_date.month - date_created.month)
    total_months = max(1, total_months)
    months_elapsed = (today.year - date_created.year) * 12 + (today.month - date_created.month)
    
    expected_saved = 0.0
    # Chapter 3A: Multi-Way if-elif-else Statements
    if months_elapsed > 0 and months_elapsed < total_months:
        expected_saved = (target / total_months) * months_elapsed
    elif months_elapsed >= total_months:
        expected_saved = target

    # Determine status.
    if saved >= expected_saved:
        current_status = "On Track"
    else:
        current_status = "Falling Behind"

    return required_monthly, months_remaining, current_status

# --- World Clock Class ---

class WorldClock(ttk.Frame):
    def __init__(self, master, style_name, refresh_callback=None, *args, **kwargs):
        super().__init__(master, style=style_name, *args, **kwargs)
        self.refresh_callback = refresh_callback
        
        self.time_label = ttk.Label(self, 
                                    font=('Arial', 12, 'bold'), 
                                    foreground='#004d40', 
                                    background='#b3e5fc', 
                                    padding=5,
                                    justify='center')
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
        
        if self.refresh_callback:
            self.refresh_callback()
            
        self.timer_id = self.after(1000, self.update_time)

    def stop(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None


# --- Tkinter GUI Application Class ---

class GoalTrackerApp:
    def __init__(self, username, mainmenu):

        self.username = username
        self.mainmenu = mainmenu
        self.mainmenu.withdraw()

        self.master = tk.Tk()
        self.master.protocol("WM_DELETE_WINDOW", self.back_menu)
        self.master.title(f"Savings Goal Tracker ({CURRENCY_SYMBOL})")
        
        # Chapter 5B: Dictionaries (The primary data structure for goals)
        self.goals = load_goals()
        
        # --- Light Blue and Creative Style Configuration ---
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

        # --- Main Frame ---
        self.main_frame = ttk.Frame(self.master, padding="15 15 15 15", relief='raised', borderwidth=2)
        self.main_frame.pack(fill='both', expand=True)

        self.back_frame = ttk.Frame(self.main_frame, style='TFrame')
        self.back_frame.pack(fill='x',padx=20,pady=(10,0))

        back_button = ttk.Button(self.back_frame,text = "< Back",command=self.back_menu)
        back_button.pack(side="left")

        # --- Treeview for Goals List (MOVED UP to prevent AttributeError) ---
        cols = ("ID", "Name", "Target", "Saved", "Progress", "Status", "Time Left", "Monthly Req.")
        self.tree = ttk.Treeview(self.main_frame, columns=cols, show="headings")
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Goal Name")
        self.tree.heading("Target", text=f"Target ({CURRENCY_SYMBOL})")
        self.tree.heading("Saved", text=f"Saved ({CURRENCY_SYMBOL})")
        self.tree.heading("Progress", text="Progress (%)")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Time Left", text="Time Left")
        self.tree.heading("Monthly Req.", text=f"Required Monthly ({CURRENCY_SYMBOL})")

        self.tree.column("ID", width=70, anchor=tk.CENTER)
        self.tree.column("Name", width=140, anchor=tk.W)
        self.tree.column("Target", width=90, anchor=tk.E)
        self.tree.column("Saved", width=90, anchor=tk.E)
        self.tree.column("Progress", width=80, anchor=tk.CENTER)
        self.tree.column("Status", width=110, anchor=tk.CENTER)
        self.tree.column("Time Left", width=110, anchor=tk.CENTER)
        self.tree.column("Monthly Req.", width=110, anchor=tk.E)
        
        self.tree.pack(fill='both', expand=True)

        # --- Top Control Panel (Title and Clock) ---
        self.top_panel = ttk.Frame(self.main_frame, style='TFrame')
        self.top_panel.pack(fill='x', pady=(0, 20), before=self.tree) # Place before tree visually
        
        title_label = ttk.Label(self.top_panel, text=f"Welcome, {self.username}!", 
                                font=('Arial', 16, 'bold'), 
                                background=PRIMARY_BLUE, 
                                foreground='#004d40') 
        title_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Now we create the clock AFTER self.tree is defined
        self.clock = WorldClock(self.top_panel, style_name='Clock.TFrame', refresh_callback=self.refresh_countdown_only)
        self.clock.pack(side=tk.RIGHT)

        # --- Buttons Frame ---
        self.button_frame = ttk.Frame(self.main_frame, padding="10 0 0 0", style='TFrame')
        self.button_frame.pack(fill='x', pady=(10, 0))

        ttk.Button(self.button_frame, text="Add New Goal", command=self.add_goal_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Record Contribution", command=self.add_contribution_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Delete Selected Goal", command=self.delete_goal).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Refresh All", command=self.refresh_goal_list).pack(side=tk.RIGHT, padx=5)

        self.refresh_goal_list()

    def back_menu(self):
        if hasattr(self, 'clock'):
            self.clock.stop()
        self.mainmenu.deiconify()
        self.master.destroy()

    def refresh_countdown_only(self):
        """Updates just the 'Time Left' column values."""
        # Safety check: ensure tree exists before trying to access it
        if not hasattr(self, 'tree') or not self.tree.winfo_exists():
            return

        for goal_id in self.tree.get_children():
            if goal_id in self.goals:
                goal = self.goals[goal_id]
                new_countdown = get_countdown_string(goal.get('target_date', ''))
                current_values = list(self.tree.item(goal_id, 'values'))
                if len(current_values) > 6:
                    current_values[6] = new_countdown 
                    self.tree.item(goal_id, values=current_values)

    def refresh_goal_list(self):
        # Chapter 5A: Lists (Traversing of Lists and clearing Treeview)
        for item in self.tree.get_children():
            self.tree.delete(item)

        sorted_goals = sorted(self.goals.items(), key=lambda item: item[1].get('date_created', '0'), reverse=True)

        # Chapter 3B: Loop Control Structure (Iterating through goals)
        for goal_id, goal in sorted_goals:
            required_monthly, months_remaining, current_status = calculate_pacing_and_status(goal)
            
            target = goal.get('target', 0.0)
            saved = goal.get('saved', 0.0)
            name = goal.get('name', 'Untitled')
            percentage = (saved / target * 100) if target > 0 else 0
            
            monthly_req_display = f"{required_monthly:,.2f}" if current_status not in ["Complete", "Needs Date", "Date Error", "Overdue"] else "N/A"
            countdown = get_countdown_string(goal.get('target_date', ''))
            
            self.tree.insert("", tk.END, iid=goal_id, values=(
                goal_id[:8], 
                name, 
                f"{target:,.2f}", 
                f"{saved:,.2f}", 
                f"{percentage:,.1f}", 
                current_status, 
                countdown,
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
        
        vars = {
            "name": tk.StringVar(),
            "target": tk.StringVar(),
            "date": tk.StringVar(value=datetime.date.today().strftime(DATE_FORMAT))
        }

        form_frame = ttk.Frame(dialog, padding=10)
        form_frame.pack(fill='both', expand=True)
        
        ttk.Label(form_frame, text="Goal Name:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(form_frame, textvariable=vars["name"]).grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(form_frame, text=f"Target Amount ({CURRENCY_SYMBOL}):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(form_frame, textvariable=vars["target"]).grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        ttk.Label(form_frame, text=f"Target Date ({DATE_FORMAT}):").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(form_frame, textvariable=vars["date"]).grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        ttk.Button(form_frame, text="Create Goal", 
                   command=lambda: self._submit_new_goal(dialog, vars)).grid(row=3, column=0, columnspan=2, pady=10)
                   
        form_frame.grid_columnconfigure(1, weight=1)

    def _submit_new_goal(self, dialog, vars):
        name = vars["name"].get().strip()
        target_str = vars["target"].get().strip()
        date_str = vars["date"].get().strip()

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
        
        save_goals(self.goals)
        self.refresh_goal_list()
        messagebox.showinfo("Success", f"Goal '{name}' added.")
        dialog.destroy()

    def add_contribution_dialog(self):
        selected_item_id = self.tree.focus()
        if not selected_item_id:
            messagebox.showwarning("Selection Error", "Please select a goal first.")
            return

        goal = self.goals.get(selected_item_id)
        amount_str = simpledialog.askstring("Record Contribution", 
                                            f"Enter contribution for '{goal['name']}' ({CURRENCY_SYMBOL}):",
                                            parent=self.master)
        
        if amount_str is None: return
            
        try:
            contribution_amount = float(amount_str.strip())
            if contribution_amount <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Positive number required.")
            return

        self.goals[selected_item_id]['saved'] += contribution_amount
        self.goals[selected_item_id]['contributions'].append({
            'amount': contribution_amount,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
        save_goals(self.goals)
        self.refresh_goal_list()

    def delete_goal(self):
        selected_item_id = self.tree.focus()
        if not selected_item_id: return
            
        goal = self.goals.get(selected_item_id)
        if messagebox.askyesno("Confirm", f"Delete '{goal['name']}'?"):
            del self.goals[selected_item_id]
            save_goals(self.goals)
            self.refresh_goal_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = GoalTrackerApp("User", root)
    root.mainloop()