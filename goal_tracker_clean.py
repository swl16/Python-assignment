import json
import os
import uuid
import datetime
import math

DATA_FILE = "savings_goals.json"
#
DATE_FORMAT = "%d-%m-%Y"

def load_goals():
    
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        # File reading using context manager for reliable file handling. (Chapter 4C - Text File Processing.pptx)
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Warning: Data file is corrupted. Starting with an empty goal list.")
        return {}
    except IOError as e:
        print(f"Error reading file: {e}")
        return {}

def save_goals(goals):
    # File writing using context manager. (Chapter 4C - Text File Processing.pptx)
    try:
        with open(DATA_FILE, 'w') as f:
            
            json.dump(goals, f, indent=4)
    except IOError as e:
        print(f"Error: Could not save data to file. {e}")

# --- Core Calculation Logic ---

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
        # Exception handling for date parsing errors. (Chapter 4B - Exception Handling.pptx)
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
    
    # Calculate months elapsed since creation.
    months_elapsed = (today.year - date_created.year) * 12 + (today.month - date_created.month)

    # Determine expected savings for pacing.
    if months_elapsed <= 0:
        expected_saved = 0.0
    elif months_elapsed >= total_months:
        expected_saved = target
    else:
        expected_saved = (target / total_months) * months_elapsed
    
    # Selection control structure to determine status. (Chapter 3A - Selection.pptx)
    if saved >= expected_saved:
        current_status = "On Track"
    else:
        current_status = "Falling Behind"

    return required_monthly, months_remaining, current_status

# --- User Interface and Interaction Functions ---

def get_valid_input(prompt, input_type, error_message):
    # Loop control structure (while True + break) to ensure valid input (simulating do...while). (Chapter 3B - Loop.pptx)
    while True:
        try:
            value = input(prompt).strip()
            
            if not value and input_type in [str]: 
                return value
            
            if input_type == float:
                num = float(value)
                if num <= 0:
                    # Specific exception for non-positive numbers. (Chapter 4B - Exception Handling.pptx)
                    raise ValueError("Value must be positive.")
                return num
            elif input_type == str:
                if not value:
                    raise ValueError("Input cannot be empty.")
                return value
            elif input_type == datetime.date:
                datetime.datetime.strptime(value, DATE_FORMAT)
                return value 
            
            return value 
            
        except ValueError as e:
            # Catching and printing detailed error messages. (Chapter 4B - Exception Handling.pptx)
            print(f"Invalid input: {error_message}")
        except EOFError:
            print("\nOperation cancelled.")
            return None

def find_goal_by_partial_id(goals, partial_id):
    # Traversing dictionary items (keys and values) to find a goal. (Chapter 5B - Tuples, Sets and Dictionaries.pptx)
    for goal_id, goal in goals.items():
        # String operation (startswith) on the goal ID. (Chapter 4A - String Processing.pptx)
        if goal_id.startswith(partial_id):
            return goal_id, goal
    return None, None

def list_goals(goals):
    if not goals:
        print("\nNo goals set yet.")
        return

    print("\n--- Current Savings Goals ---")
    
    # Using sorted function with a lambda key for sorting goal items (based on date_created).
    sorted_goals = sorted(goals.items(), key=lambda item: item[1].get('date_created', '0'), reverse=True)

    for goal_id, goal in sorted_goals:
        target = goal.get('target', 0.0)
        saved = goal.get('saved', 0.0)
        name = goal.get('name', 'Untitled Goal')
        target_date_str = goal.get('target_date', 'N/A')
        
        required_monthly, months_remaining, current_status = calculate_pacing_and_status(goal)

        percentage = (saved / target * 100) if target > 0 else 0
        remaining = max(0, target - saved)
        
        # String formatting using f-strings for output display. (Chapter 4A - String Processing.pptx)
        print(f"\n===================================================================")
        print(f"ID: {goal_id[:8]}... | Name: {name}")
        print(f"Status: {current_status}")
        print(f"Progress: {percentage:.2f}% | Saved: ${saved:,.2f} / Target: ${target:,.2f}")
        print(f"Remaining: ${remaining:,.2f}")
        print(f"Target Date: {target_date_str} (Months Left: {months_remaining})")
        
        if current_status not in ["Complete", "Needs Date", "Date Error", "Overdue"]:
            print(f"Suggested Monthly Savings: ${required_monthly:,.2f}")
        
        print(f"===================================================================")

def add_goal(goals):
    print("\n--- Add New Goal ---")
    
    name = get_valid_input("Enter goal name: ", str, "Goal name cannot be empty.")
    if name is None: return

    target_amount = get_valid_input("Enter target amount ($): ", float, "Please enter a valid positive number.")
    if target_amount is None: return

    target_date_str = get_valid_input(
        f"Enter target completion date ({DATE_FORMAT}): ", 
        datetime.date, 
        f"Please use the format {DATE_FORMAT} (e.g., 31-12-2026)." 
    )
    if target_date_str is None: return

    new_id = str(uuid.uuid4())
    # Storing new goal data in the dictionary. (Chapter 5B - Tuples, Sets and Dictionaries.pptx)
    goals[new_id] = {
        'id': new_id,
        'name': name,
        'target': target_amount,
        'saved': 0.0,
        'target_date': target_date_str,
        # Contributions stored as a List. (Chapter 5A - Lists.pptx)
        'contributions': [],
        'date_created': datetime.datetime.now().isoformat()
    }
    save_goals(goals)
    print(f"\nGoal '{name}' successfully added with ID: {new_id[:8]}...")

def add_contribution(goals):
    if not goals:
        list_goals(goals)
        return
    
    print("\n--- Record Contribution ---")
    partial_id = get_valid_input("Enter first 8 chars of Goal ID to contribute: ", str, "ID not found.")
    if partial_id is None: return

    goal_id, goal = find_goal_by_partial_id(goals, partial_id)
    if not goal:
        print("Goal ID not found.")
        return

    print(f"Recording contribution for '{goal['name']}'. Current saved: ${goal['saved']:,.2f}")
    
    contribution_amount = get_valid_input("Enter new contribution amount ($): ", float, "Please enter a positive number.")
    if contribution_amount is None: return
    
    new_saved = goal['saved'] + contribution_amount
    goals[goal_id]['saved'] = new_saved

    # Appending a new dictionary (contribution) to the list in the goal. (Chapter 5A - Lists.pptx)
    goals[goal_id]['contributions'].append({
        'amount': contribution_amount,
        'timestamp': datetime.datetime.now().isoformat()
    })
    
    save_goals(goals)
    print(f"\nContribution of ${contribution_amount:,.2f} recorded.")
    print(f"New total saved for '{goal['name']}': ${new_saved:,.2f}")

def view_history(goals):
    if not goals:
        list_goals(goals)
        return

    print("\n--- View Contribution History ---")
    partial_id = get_valid_input("Enter first 8 chars of Goal ID to view history: ", str, "ID not found.")
    if partial_id is None: return

    goal_id, goal = find_goal_by_partial_id(goals, partial_id)
    if not goal:
        print("Goal ID not found.")
        return

    print(f"\n--- History for '{goal['name']}' ---")
    contributions = goal.get('contributions', [])
    
    if not contributions:
        print("No contributions recorded yet.")
        return

    # Iterating over the list in reverse order (newest first). (Chapter 5A - Lists.pptx)
    for entry in reversed(contributions):
        try:
            timestamp = datetime.datetime.fromisoformat(entry['timestamp']).strftime(f"{DATE_FORMAT} %H:%M")
            amount = entry['amount']
            print(f"Date: {timestamp} | Amount: ${amount:,.2f}")
        except (ValueError, KeyError):
            print("Invalid history entry found in data.")
            
    print("-----------------------------------")

def delete_goal(goals):
    if not goals:
        list_goals(goals)
        return

    print("\n--- Delete Goal ---")
    partial_id = get_valid_input("Enter first 8 chars of Goal ID to delete: ", str, "ID not found.")
    if partial_id is None: return
    
    goal_id, goal = find_goal_by_partial_id(goals, partial_id)
    if not goal:
        print("Goal ID not found.")
        return

    confirm = input(f"Are you sure you want to delete '{goal['name']}'? (yes/no): ").strip().lower()
    if confirm == 'yes':
        # Deleting a key-value pair from the dictionary. (Chapter 5B - Tuples, Sets and Dictionaries.pptx)
        del goals[goal_id]
        save_goals(goals)
        print(f"\nGoal '{goal['name']}' successfully deleted.")
    else:
        print("\nDeletion cancelled.")

def main_menu():
    goals = load_goals()
    
    while True:
        print("\n=============================================")
        print("    ROBUST SAVINGS GOAL TRACKER")
        print("=============================================")
        print("1. View All Goals (Pacing & Status)")
        print("2. Add New Goal (Requires Target Date)")
        print("3. Record Contribution")
        print("4. View Contribution History")
        print("5. Delete Goal")
        print("6. Exit")
        print("=============================================")
        
        try:
            # Selection control structure to route program flow based on user input. (Chapter 3A - Selection.pptx)
            choice = input("\nEnter your choice (1-6): ").strip() 
        except EOFError:
            break

        if choice == '1':
            list_goals(goals)
        elif choice == '2':
            add_goal(goals)
        elif choice == '3':
            add_contribution(goals)
        elif choice == '4':
            view_history(goals)
        elif choice == '5':
            delete_goal(goals)
        elif choice == '6':
            print("\nExiting Goal Tracker. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main_menu()