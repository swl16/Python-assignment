from tkinter import *
from tkinter import ttk , messagebox
from tkcalendar import DateEntry
from datetime import datetime
import csv
import os
import matplotlib.pyplot as plt

window = Tk()
Empty_label = None
Category = ('Food', 'Household', 'Health', 'Beauty', 'Entertainment', 'Other')

def add_new_expenses():

    def back_to_mainmenu():
        expenses.destroy()
        window.deiconify()

    def Get_user_input():
        date_input = date_picker.get()
        amount_input = amount_enter.get().strip()
        category_input = category_combobox.get()
        remark_input = remark_entry.get("1.0", "end-1c").strip()

        if not amount_input:
            messagebox.showerror("Error", "Please enter a valid amount.")

        try:
            amount = float(amount_input)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
            return

        if not category_input:
            messagebox.showerror('Error','Please select a category.')
            return

        amount = f"{amount:.2f}"

        with open('expenses_record.csv','a',newline='',encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([date_input,amount,category_input,remark_input])

        refresh_mainpage()
        messagebox.showinfo("Success!", "Your expense is added!")
        back_to_mainmenu()

#window for this page
    expenses = Toplevel(window)
    expenses.geometry("500x650")
    expenses.title('Expenses Tracker')
    window.withdraw()
    expenses.config(background='#f7f2e9')

#Main Title
    title_label = Label(expenses, text="Expenses Tracker", font=('Arial', 18, 'bold'), fg='white', bg='#7e9aed',
                        relief='ridge', bd=3, padx=20, pady=15
                        #,image=icon,compound='left'
                        )
    title_label.pack(fill='x', padx=20, pady=(20,30))

#Form a frame which can  let arrangement become easier
    form_frame = Frame(expenses, bg='#fcf7ed', relief='ridge', bd=2)
    form_frame.pack(padx=20, pady=10, fill='both', expand=True)

    inner_frame = Frame(form_frame, bg='#fcf7ed')
    inner_frame.pack(padx=30, pady=30, fill='both', expand=True)

#Date (choose from calendar)
    date_frame = Frame(inner_frame, bg='#fcf7ed')
    date_frame.pack(fill='x', pady=(0, 20))

    date_label = Label(date_frame, text="Date        :", font=('Arial', 15, 'bold'), fg='black', bg='#fcf7ed', width=11, anchor='w')
    date_label.pack(side='left')

    date_picker = DateEntry(date_frame, width=30, font=('Arial', 11), borderwidth=2, date_pattern='dd/mm/yyyy', background='#7e9aed', foreground='white')
    date_picker.pack(side='left')

#Amount (key in by keyboard)
    amount_frame = Frame(inner_frame, bg='#fcf7ed')
    amount_frame.pack(fill='x',pady=(0,20))

    amount_label = Label(amount_frame,text="Amount   :",font=("Arial", 15,'bold'),fg='black',bg='#fcf7ed',width=11, anchor='w')
    amount_label.pack(side="left")

#Show RM symbol
    RM_label = Label(amount_frame,text='RM',font=("Arial", 11),fg='black',bg='white',borderwidth=1, relief='ridge')
    RM_label.pack(side="left")

    amount_enter = Entry(amount_frame,width=30,font=("Arial", 11))
    amount_enter.pack(side="left")
    amount_enter.focus()

#Category (Choose 1 category)
    category_frame = Frame(inner_frame, bg='#fcf7ed')
    category_frame.pack(fill='x',pady=(0,20))

    category_label = Label(category_frame,text="Category :",font=("Arial", 15,'bold'),fg='black',bg='#fcf7ed',width=11, anchor='w')
    category_label.pack(side="left")

    category_combobox = ttk.Combobox(category_frame, font=("Arial", 11), width=30,values=Category,state='readonly')
    category_combobox.set('')

    category_combobox.pack(side='left')

#Remark made by user (Key in by keyboard)
    remark_frame = Frame(inner_frame, bg='#fcf7ed')
    remark_frame.pack(fill='x',pady=(0,20))

    remark_label = Label(remark_frame,text='Remark   :',font=("Arial", 15,'bold'),fg='black',bg='#fcf7ed',width=11, anchor='w')
    remark_label.pack(side="left")

    remark_entry = Text(remark_frame,width=32,font=("Arial", 11),height=5)
    remark_entry.pack(side="left")

#Confirm Button to proceed and cancel button to back to main page
    Button_frame = Frame(inner_frame, bg='#fcf7ed')
    Button_frame.pack(fill='x', pady=40)

    Button_store = Frame(Button_frame, bg='#fcf7ed')
    Button_store.pack(anchor='center')

    Button(Button_store,text="Add Expense",font=("Arial",15,'bold'), fg='white',bg='#7e9aed',relief='ridge', bd=2, padx=10,
           command=Get_user_input).pack(side='left',padx=10)

    Button(Button_store,text='Cancel',font=("Arial",15,'bold'), fg='white',bg='#7e9aed',relief='ridge', bd=2, padx=10,
           command=back_to_mainmenu).pack(side='left',padx=10)

#To let it have a space at the bottom
    Bottom_frame = Frame(expenses, bg='#f7f2e9')
    Bottom_frame.pack(fill='x',pady=20)

def show_page(page):
    page.tkraise()

#Main window
window.geometry("500x650")
window.title("Expenses Tracker")
window.config(background='#f7f2e9')

try:
    icon = PhotoImage(file='coin.png')
    window.iconphoto(True, icon)
except:
    pass

Container = Frame(window)
Container.pack(fill='both', expand=True)

Mainpage = Frame(Container, bg='#f7f2e9')
MonthPage = Frame(Container, bg='#f7f2e9')
Statistic_page = Frame(Container, bg='#f7f2e9')

for frame in (Mainpage, MonthPage, Statistic_page):
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

bottom_menu = Frame(window, bg='#7e9aed', height=90)
bottom_menu.pack(side='bottom', fill='x')

Main_button = Button(bottom_menu, text="Home", font=("Arial", 15, 'bold'), bg='#7e9aed', fg='white',
                     command=lambda: show_page(Mainpage))
Month_button = Button(bottom_menu, text="Monthly Expenses", font=("Arial", 15, 'bold'), bg='#7e9aed', fg='white',
                      command=lambda: show_page(MonthPage))
Statistic_button = Button(bottom_menu, text="Statistic", font=("Arial", 15, 'bold'), bg='#7e9aed', fg='white',
                          command=lambda: show_page(Statistic_page))

Main_button.pack(side='left', expand=True, fill='both')
Month_button.pack(side="left", expand=True, fill="both")
Statistic_button.pack(side="left", expand=True, fill="both")

show_page(Mainpage)

#Main Page
total_frame = Frame(Mainpage, bg='#f7f2e9',height=80)
total_frame.pack(fill='x',pady=(10, 0),padx=20)

main_frame = Frame(Mainpage, bg='#f7f2e9')
main_frame.pack(fill='both', expand=True, padx=20, pady=(0, 10))

main_canvas = Canvas(main_frame, bg='#f7f2e9', highlightthickness=0)
scrollbar = Scrollbar(main_frame, orient="vertical", command=main_canvas.yview)
scrollPage = Frame(main_canvas, bg='#f7f2e9')

scrollPage.bind("<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))

main_canvas.create_window((0, 0), anchor="nw", window=scrollPage)
main_canvas.configure(yscrollcommand=scrollbar.set)

main_canvas.pack(side="left", expand=True, fill="both")
scrollbar.pack(side="right", fill="y")

Button(Mainpage, text='+', font=('Arial', 20, 'bold'), bg='#7e9aed', fg='white', width=3, height=1,
       command=add_new_expenses).pack(side="bottom", anchor="e", padx=20, pady=20)


def Check_empty_file():
    global Empty_label
    try:
        if Empty_label:
            Empty_label.destroy()
    except:
        pass

    data = read_expenses()

    if not data:
        Empty_label = Label(Mainpage, text="There is no record yet...", font=('Arial', 15, 'bold'), fg='#7e9aed',
                            bg='#f7f2e9')
        Empty_label.place(anchor='center', relx=0.5, rely=0.5)
        return True

    return False

def Show_total_expenses():
    total = 0
    data = read_expenses()

    for row in data:
        total += float(row[1])

    total_label = Label(total_frame,text=f"Total expenses : RM{total:.2f}",font=('Arial', 18, 'bold'),bg='#7e9aed',fg='white',relief='ridge', bd=3,padx=40,pady=15)
    total_label.place(anchor='center', relx=0.5, rely=0.5)

def read_expenses():
    if not os.path.exists('expenses_record.csv') or os.path.getsize('expenses_record.csv') == 0:
        return []

    try:
        with open("expenses_record.csv", "r", encoding='utf-8') as file:
            reader = csv.reader(file)
            data = [row for row in reader if row]

            return data
    except:
        return []

def delete_expense(index):
    if messagebox.askyesno(title="Delete Expense", message="Are you sure you want to delete this expense?"):
        data = read_expenses()
        data.pop(index)

        with open("expenses_record.csv", "w", newline='',encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data)

        refresh_mainpage()

    else:
        return

def Edit_expense(index):
    data = read_expenses()

    edit_window = Toplevel(window)
    edit_window.geometry("500x650")
    edit_window.title('Edit Expense')
    window.withdraw()
    edit_window.config(background='#f7f2e9')

    def back_to_mainmenu():
        edit_window.destroy()
        window.deiconify()

    def Save_expense():
        date_input = date_picker.get()
        amount_input = amount_enter.get().strip()
        category_input = category_combobox.get()
        remark_input = remark_entry.get("1.0", "end-1c").strip()

        if not amount_input:
            messagebox.showerror("Error", "Please enter a valid amount.")

        try:
            amount = float(amount_input)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
            return

        if not category_input:
            messagebox.showerror('Error', 'Please select a category.')
            return

        amount = f"{amount:.2f}"

        data[index] = [date_input, amount , category_input, remark_input]

        with open('expenses_record.csv', 'w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(data)

        refresh_mainpage()
        messagebox.showinfo("Success!", "Your expense is edited successfully!")
        back_to_mainmenu()

    # window for this page


    # Main Title
    title_label = Label(edit_window, text="Expenses Tracker", font=('Arial', 18, 'bold'), fg='white', bg='#7e9aed',
                        relief='ridge', bd=3, padx=20, pady=15
                        # ,image=icon,compound='left'
                        )
    title_label.pack(fill='x', padx=20, pady=(20, 30))

    # Form a frame which can  let arrangement become easier
    form_frame = Frame(edit_window, bg='#fcf7ed', relief='ridge', bd=2)
    form_frame.pack(padx=20, pady=10, fill='both', expand=True)

    inner_frame = Frame(form_frame, bg='#fcf7ed')
    inner_frame.pack(padx=30, pady=30, fill='both', expand=True)

    # Date (choose from calendar)
    date_frame = Frame(inner_frame, bg='#fcf7ed')
    date_frame.pack(fill='x', pady=(0, 20))

    date_label = Label(date_frame, text="Date        :", font=('Arial', 15, 'bold'), fg='black', bg='#fcf7ed', width=11,
                       anchor='w')
    date_label.pack(side='left')

    date_picker = DateEntry(date_frame, width=30, font=('Arial', 11), borderwidth=2, date_pattern='dd/mm/yyyy',
                            background='#7e9aed', foreground='white')
    date_picker.delete(0, 'end')
    date_picker.insert(0,data[index][0])
    date_picker.pack(side='left')

    # Amount (key in by keyboard)
    amount_frame = Frame(inner_frame, bg='#fcf7ed')
    amount_frame.pack(fill='x', pady=(0, 20))

    amount_label = Label(amount_frame, text="Amount   :", font=("Arial", 15, 'bold'), fg='black', bg='#fcf7ed',
                         width=11, anchor='w')
    amount_label.pack(side="left")

    # Show RM symbol
    RM_label = Label(amount_frame, text='RM', font=("Arial", 11), fg='black', bg='white', borderwidth=1, relief='ridge')
    RM_label.pack(side="left")

    amount_enter = Entry(amount_frame, width=30, font=("Arial", 11))
    amount_enter.insert(0,data[index][1])
    amount_enter.pack(side="left")
    amount_enter.focus()

    # Category (Choose 1 category)
    category_frame = Frame(inner_frame, bg='#fcf7ed')
    category_frame.pack(fill='x', pady=(0, 20))

    category_label = Label(category_frame, text="Category :", font=("Arial", 15, 'bold'), fg='black', bg='#fcf7ed',
                           width=11, anchor='w')
    category_label.pack(side="left")

    category_combobox = ttk.Combobox(category_frame, font=("Arial", 11), width=30,values=Category,state='readonly')
    category_combobox.set(data[index][2])

    category_combobox.pack(side='left')

    # Remark made by user (Key in by keyboard)
    remark_frame = Frame(inner_frame, bg='#fcf7ed')
    remark_frame.pack(fill='x', pady=(0, 20))

    remark_label = Label(remark_frame, text='Remark   :', font=("Arial", 15, 'bold'), fg='black', bg='#fcf7ed',
                         width=11, anchor='w')
    remark_label.pack(side="left")

    remark_entry = Text(remark_frame, width=32, font=("Arial", 11), height=5)
    remark_entry.insert("1.0",data[index][3])
    remark_entry.pack(side="left")

    # Confirm Button to proceed and cancel button to back to main page
    Button_frame = Frame(inner_frame, bg='#fcf7ed')
    Button_frame.pack(fill='x', pady=40)

    Button_store = Frame(Button_frame, bg='#fcf7ed')
    Button_store.pack(anchor='center')

    Button(Button_store, text="Save", font=("Arial", 15, 'bold'), fg='white', bg='#7e9aed', relief='ridge', bd=2,
           padx=10,
           command=Save_expense).pack(side='left', padx=10)

    Button(Button_store, text='Cancel', font=("Arial", 15, 'bold'), fg='white', bg='#7e9aed', relief='ridge', bd=2,
           padx=10,
           command=back_to_mainmenu).pack(side='left', padx=10)

    # To let it have a space at the bottom
    Bottom_frame = Frame(edit_window, bg='#f7f2e9')
    Bottom_frame.pack(fill='x', pady=20)

def refresh_mainpage():
    Check_empty_file()
    Show_total_expenses()

    for widget in scrollPage.winfo_children():
        widget.destroy()

    if Empty_label:
        Empty_label.pack_forget()

    if Check_empty_file():
        return

    data = read_expenses()
    if not data:
        return

    data_Index = [(i,row) for i,row in enumerate(data)]

    #sort the date according descending order
    data_Index.sort(key=lambda x: datetime.strptime(x[1][0], "%d/%m/%Y"), reverse=True)

    for index,row in data_Index:
        Outer_frame = Frame(scrollPage, bg='#f7f2e9',width=400,height=80)
        Outer_frame.pack(fill='x', pady=(10, 0), padx=10)

        data_frame = Frame(Outer_frame, bg='#fcf7ed', relief='ridge', bd=2,width=350,height=80)
        data_frame.pack(side='left',fill='x', pady=13, padx=(0,10))
        data_frame.pack_propagate(False)

        inner_frame = Frame(data_frame, bg='#fcf7ed')
        inner_frame.pack(fill='x', pady=(10, 0), padx=25)

        Date_label = Label(inner_frame, text=row[0], font=('Arial', 11), fg='black', bg='#fcf7ed')
        Date_label.pack(side="left")

        Amount_label = Label(inner_frame, text='RM' + row[1], font=('Arial', 15), fg='black', bg='#fcf7ed')
        Amount_label.pack(side="right")

        Label_Frame = Frame(data_frame, bg='#fcf7ed')
        Label_Frame.pack(fill='x', pady=(5, 10), padx=25)

        Category_label = Label(Label_Frame, text=row[2], font=('Arial', 11), fg='black', bg='#fcf7ed')
        Category_label.pack(side="left", padx=(0, 20))

        if row[3].strip():
            Remark_label = Label(Label_Frame, text=row[3], font=('Arial', 10), fg='black', bg='#fcf7ed', wraplength=250,justify='left')
            Remark_label.pack(side="left")

        Edit_button = Button(Outer_frame,text='✏',bg='#7e9aed', fg='white',width=2,height=1,command=lambda idx=index:Edit_expense(idx))
        Edit_button.pack(side="right",padx=(0,10))

        Delete_button = Button(Outer_frame,text='🗑',bg='#7e9aed', fg='white',width=2,height=1,command=lambda idx=index:delete_expense(idx))
        Delete_button.pack(side="right",padx=(0,8))

Check_empty_file()
refresh_mainpage()


#Statistic
def Get_month_data():
    data = read_expenses()
    month = sorted({datetime.strptime(row[0],"%d/%m/%Y").strftime('%m/%Y') for row in data},reverse=True)

    MonthCombo_combobox['values'] = month
    if month:
        if MonthCombo_combobox.get() not in month:
            MonthCombo_combobox.set(month[0])
    else:
        MonthCombo_combobox.set('')

Title_label = Label(Statistic_page,text='Monthly Statistics',font=('Arial', 18, 'bold'), fg='white', bg='#7e9aed',relief='ridge', bd=3, padx=20, pady=15)
Title_label.pack(fill='x', padx=20, pady=(30,20))

Month_frame = Frame(Statistic_page, bg='#fcf7ed', relief='ridge', bd=2)
Month_frame.pack(padx=20,pady=(10,40),fill='both',expand=True)

in_frame = Frame(Month_frame,bg='#fcf7ed')
in_frame.pack(padx=30,pady=30,fill='both',expand=True)

MonthCombo_frame = Frame(in_frame,bg='#fcf7ed')
MonthCombo_frame.pack(fill='x',pady=(0,20))

MonthCombo_label = Label(MonthCombo_frame,text='Select Month:',font=("Arial", 15,'bold'),fg='black',bg='#fcf7ed')
MonthCombo_label.pack(side='left',padx=(0,40))

MonthCombo_combobox = ttk.Combobox(MonthCombo_frame, font=("Arial", 11), width=15,state='readonly')
Get_month_data()
MonthCombo_combobox.pack(side='left')

piechart_label = Category

window.mainloop()