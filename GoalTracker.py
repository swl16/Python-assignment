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
    def __init__(self, master, style_name, *args, **kwargs):
        super().__init__(master, style=style_name, *args, **kwargs)
        
        self.time_label = ttk.Label(self, 
                                    font=('Arial', 12, 'bold'), 
                                    foreground='#004d40', # Dark teal
                                    background='#b3e5fc', # Secondary blue
                                    padding=5)
        self.time_label.pack(fill='x', padx=10, pady=5)

        self.timer_id = None
        self.update_time()

    def update_time(self):
        if not self.winfo_exists():
            return

        # Get current time and convert it to Malaysia Time (GMT+8)
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        malaysia_time = now_utc.astimezone(MALAYSIA_TIMEZONE_OFFSET)
        
        # Format the time display
        time_str = malaysia_time.strftime('%I:%M:%S %p %Z')
        date_str = malaysia_time.strftime('%A, %d %b %Y')
        
        display_text = f"Malaysia Time (GMT+8)\n{date_str}\n{time_str}"
        self.time_label.config(text=display_text)
        
        # Schedule the update every 1000 milliseconds (1 second)
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
        
        # Define light blue colors
        PRIMARY_BLUE = '#f7f2e9'
        SECONDARY_BLUE = '#b3e5fc' # Slightly darker blue for frames/buttons
        ACCENT_BLUE = '#7e9aed'   # A nice accent blue
        
        # Configure the main frame background
        style.configure('TFrame', background=PRIMARY_BLUE)
        style.configure('TLabel', background=PRIMARY_BLUE, font=('Arial', 10))
        
        # Configure a special style for the clock frame/label
        style.configure('Clock.TFrame', background=SECONDARY_BLUE, relief='raised', borderwidth=1)

        # Configure buttons with a subtle blue gradient/flat look
        style.configure('TButton', 
                        background=ACCENT_BLUE, 
                        foreground='white', 
                        font=('Arial', 10, 'bold'), 
                        padding=6, 
                        relief='flat')
        style.map('TButton', 
                 background=[('active', '#03a9f4'), ('pressed', '#0288d1')])
        
        # Configure Treeview style
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

        # --- Top Control Panel (Title and Clock) ---
        self.top_panel = ttk.Frame(self.main_frame, style='TFrame')
        self.top_panel.pack(fill='x', pady=(0, 20))
        
        # Title (Left Side)
        title_label = ttk.Label(self.top_panel, text="Financial Goals Dashboard", 
                                font=('Arial', 16, 'bold'), 
                                background=PRIMARY_BLUE, 
                                foreground='#004d40') # Dark teal for contrast
        title_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Malaysia Clock (Right Side)
        self.clock = WorldClock(self.top_panel, style_name='Clock.TFrame')
        self.clock.pack(side=tk.RIGHT)


        # --- Treeview for Goals List ---
        
        self.tree = ttk.Treeview(self.main_frame, columns=("ID", "Name", "Target", "Saved", "Progress", "Status", "Monthly Req."), show="headings")
        
        # Define column headings and widths
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Goal Name")
        # Updated Currency Header
        self.tree.heading("Target", text=f"Target ({CURRENCY_SYMBOL})")
        self.tree.heading("Saved", text=f"Saved ({CURRENCY_SYMBOL})")
        self.tree.heading("Progress", text="Progress (%)")
        self.tree.heading("Status", text="Status")
        # Updated Currency Header
        self.tree.heading("Monthly Req.", text=f"Required Monthly ({CURRENCY_SYMBOL})")

        self.tree.column("ID", width=70, anchor=tk.CENTER)
        self.tree.column("Name", width=150, anchor=tk.W)
        self.tree.column("Target", width=100, anchor=tk.E)
        self.tree.column("Saved", width=100, anchor=tk.E)
        self.tree.column("Progress", width=80, anchor=tk.CENTER)
        self.tree.column("Status", width=120, anchor=tk.CENTER)
        self.tree.column("Monthly Req.", width=120, anchor=tk.E)
        
        self.tree.pack(fill='both', expand=True)

        # --- Buttons Frame ---
        self.button_frame = ttk.Frame(self.main_frame, padding="10 0 0 0", style='TFrame') 
        self.button_frame.pack(fill='x', pady=(10, 0))

        # Command buttons bind to methods for user interaction.
        ttk.Button(self.button_frame, text="Add New Goal", command=self.add_goal_dialog).pack(side=tk.LEFT, padx=5)
        # NEW FEATURE: Edit/Rename Goal button
        ttk.Button(self.button_frame, text="Edit Selected Goal", command=self.edit_goal_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Record Contribution", command=self.add_contribution_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Delete Selected Goal", command=self.delete_goal).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Refresh", command=self.refresh_goal_list).pack(side=tk.RIGHT, padx=5)

        # Initial data load and display.
        self.refresh_goal_list()

    def back_menu(self):
        if hasattr(self, 'clock'):
            self.clock.stop()

        self.mainmenu.deiconify()
        self.master.destroy()

    def refresh_goal_list(self):
        # Chapter 5A: Lists (Traversing of Lists and clearing Treeview)
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Sort goals by creation date (newest first).
        sorted_goals = sorted(self.goals.items(), key=lambda item: item[1].get('date_created', '0'), reverse=True)

        # Chapter 3B: Loop Control Structure (Iterating through goals)
        for goal_id, goal in sorted_goals:
            # Calculate pacing and status for display.
            required_monthly, months_remaining, current_status = calculate_pacing_and_status(goal)
            
            target = goal.get('target', 0.0)
            saved = goal.get('saved', 0.0)
            name = goal.get('name', 'Untitled')
            
            percentage = (saved / target * 100) if target > 0 else 0
            
            monthly_req_display = f"{required_monthly:,.2f}" if current_status not in ["Complete", "Needs Date", "Date Error", "Overdue"] else "N/A"
            
            # Insert data into the treeview.
            self.tree.insert("", tk.END, iid=goal_id, values=(
                goal_id[:8], 
                name, 
                f"{target:,.2f}", 
                f"{saved:,.2f}", 
                f"{percentage:,.1f}", 
                current_status, 
                monthly_req_display
            ), tags=(current_status.replace(" ", "_"),))
            
        # Optional: Configure colors based on status (softened colors for light blue theme)
        self.tree.tag_configure('Falling_Behind', background='#ffcdd2') # Light red/pink
        self.tree.tag_configure('Overdue', background='#ffcdd2')
        self.tree.tag_configure('Complete', background='#c8e6c9') # Light green
        self.tree.tag_configure('On_Track', background='#bbdefb') # Light blue/accent

    def add_goal_dialog(self):
        # TopLevel window for input forms.
        dialog = tk.Toplevel(self.master)
        dialog.title("Add New Goal")
        dialog.geometry("300x250")
        dialog.transient(self.master)
        dialog.grab_set()
        
        # Use a dictionary to hold input variables.
        vars = {
            "name": tk.StringVar(),
            "target": tk.StringVar(),
            "date": tk.StringVar(value=datetime.date.today().strftime(DATE_FORMAT))
        }

        # Form layout
        form_frame = ttk.Frame(dialog, padding=10)
        form_frame.pack(fill='both', expand=True)
        
        # Labels and Entries
        ttk.Label(form_frame, text="Goal Name:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(form_frame, textvariable=vars["name"]).grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # Updated Label with CURRENCY_SYMBOL
        ttk.Label(form_frame, text=f"Target Amount ({CURRENCY_SYMBOL}):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(form_frame, textvariable=vars["target"]).grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(form_frame, text=f"Target Date ({DATE_FORMAT}):").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(form_frame, textvariable=vars["date"]).grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        # Add button to submit the form.
        ttk.Button(form_frame, text="Create Goal", 
                   command=lambda: self._submit_new_goal(dialog, vars)).grid(row=3, column=0, columnspan=2, pady=10)
                   
        form_frame.grid_columnconfigure(1, weight=1)

    # NEW FEATURE: Dialog for editing an existing goal
    def edit_goal_dialog(self):
        # Chapter 3A: Selection Control Structure (Checking for a selected item)
        selected_item_id = self.tree.focus()
        if not selected_item_id:
            messagebox.showwarning("Selection Error", "Please select a goal to edit.")
            return

        goal = self.goals.get(selected_item_id)
        
        dialog = tk.Toplevel(self.master)
        dialog.title("Edit/Rename Goal")
        dialog.geometry("300x250")
        dialog.transient(self.master)
        dialog.grab_set()
        
        # Chapter 5B: Dictionaries (Populating form with current values)
        vars = {
            "name": tk.StringVar(value=goal['name']),
            "target": tk.StringVar(value=str(goal['target'])),
            "date": tk.StringVar(value=goal['target_date'])
        }

        form_frame = ttk.Frame(dialog, padding=10)
        form_frame.pack(fill='both', expand=True)
        
        ttk.Label(form_frame, text="Goal Name:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(form_frame, textvariable=vars["name"]).grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(form_frame, text=f"Target Amount ({CURRENCY_SYMBOL}):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(form_frame, textvariable=vars["target"]).grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(form_frame, text=f"Target Date ({DATE_FORMAT}):").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(form_frame, textvariable=vars["date"]).grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        ttk.Button(form_frame, text="Save Changes", 
                   command=lambda: self._submit_edit_goal(dialog, vars, selected_item_id)).grid(row=3, column=0, columnspan=2, pady=10)
                   
        form_frame.grid_columnconfigure(1, weight=1)

    # NEW FEATURE: Logic for updating the goal data
    def _submit_edit_goal(self, dialog, vars, goal_id):
        name = vars["name"].get().strip()
        target_str = vars["target"].get().strip()
        date_str = vars["date"].get().strip()

        # Chapter 4B: Exception Handling (Validation)
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

        # Chapter 5B: Dictionaries (Updating specific fields while keeping ID and History)
        self.goals[goal_id]['name'] = name
        self.goals[goal_id]['target'] = target_amount
        self.goals[goal_id]['target_date'] = date_str
        
        save_goals(self.goals)
        self.refresh_goal_list()
        messagebox.showinfo("Success", "Goal successfully updated.")
        dialog.destroy()

    def _submit_new_goal(self, dialog, vars):
        name = vars["name"].get().strip()
        target_str = vars["target"].get().strip()
        date_str = vars["date"].get().strip()

        # Chapter 4B: Exception Handling (Data validation using try/except)
        if not name:
            messagebox.showerror("Validation Error", "Goal Name is required.")
            return
        try:
            target_amount = float(target_str)
            if target_amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Target Amount must be a positive number.")
            return

        try:
            datetime.datetime.strptime(date_str, DATE_FORMAT)
        except ValueError:
            messagebox.showerror("Validation Error", f"Date must be in {DATE_FORMAT} format.")
            return

        # Chapter 5B: Dictionaries (Creating a new dictionary entry)
        new_id = str(uuid.uuid4())
        self.goals[new_id] = {
            'id': new_id,
            'name': name,
            'target': target_amount,
            'saved': 0.0,
            'target_date': date_str,
            # Chapter 5A: Lists (Storing contributions history)
            'contributions': [],
            'date_created': datetime.datetime.now().isoformat()
        }
        
        save_goals(self.goals)
        self.refresh_goal_list()
        messagebox.showinfo("Success", f"Goal '{name}' successfully added.")
        dialog.destroy()

    def add_contribution_dialog(self):
        # Chapter 3A: Selection Control Structure (Checking for a selected item)
        selected_item_id = self.tree.focus()
        if not selected_item_id:
            messagebox.showwarning("Selection Error", "Please select a goal from the list first.")
            return

        goal = self.goals.get(selected_item_id)
        if not goal:
            messagebox.showerror("Data Error", "Selected goal data not found.")
            return

        # Updated Dialog Text with CURRENCY_SYMBOL
        amount_str = simpledialog.askstring("Record Contribution", 
                                            f"Enter contribution amount for '{goal['name']}' (Current: {CURRENCY_SYMBOL}{goal['saved']:.2f}):",
                                            parent=self.master)
        
        if amount_str is None: # User pressed Cancel
            return
            
        try:
            # Chapter 4B: Exception Handling (Input validation)
            contribution_amount = float(amount_str.strip())
            if contribution_amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Contribution must be a positive number.")
            return

        # Update goal data
        new_saved = goal['saved'] + contribution_amount
        self.goals[selected_item_id]['saved'] = new_saved
        # Chapter 5A: List Methods (Appending to the contributions list)
        self.goals[selected_item_id]['contributions'].append({
            'amount': contribution_amount,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
        save_goals(self.goals)
        self.refresh_goal_list()
        # Updated Success Message with CURRENCY_SYMBOL
        messagebox.showinfo("Success", f"Recorded {CURRENCY_SYMBOL}{contribution_amount:,.2f}. New saved total: {CURRENCY_SYMBOL}{new_saved:,.2f}")

    def delete_goal(self):
        selected_item_id = self.tree.focus()
        if not selected_item_id:
            messagebox.showwarning("Selection Error", "Please select a goal to delete.")
            return
            
        goal = self.goals.get(selected_item_id)
        if not goal:
            messagebox.showerror("Data Error", "Selected goal data not found.")
            return

        # Chapter 3A: Selection Control Structure (Confirmation before deletion)
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete goal: '{goal['name']}'?"):
            # Chapter 5B: Dictionaries (Deleting an item)
            del self.goals[selected_item_id]
            save_goals(self.goals)
            self.refresh_goal_list()
            messagebox.showinfo("Success", f"Goal '{goal['name']}' successfully deleted.")