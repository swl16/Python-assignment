from tkinter import *
from tkinter import ttk , messagebox
from tkcalendar import DateEntry
from datetime import datetime
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#class include the whole module
class ExpensesTracker:
    def __init__(ET, username,mainpage): #ET = Expenses Tracker
        ET.window = Tk()
        ET.Username = username
        ET.mainpage = mainpage
        ET.Empty_label = None
        ET.Category = ('Food', 'Household', 'Health', 'Beauty', 'Entertainment', 'Other')

        #close the main menu page
        ET.mainpage.withdraw()

        #Main window
        ET.window.geometry("550x700")
        ET.window.title("Expenses Tracker")
        ET.window.config(background='#f7f2e9')
        ET.window.protocol("WM_DELETE_WINDOW", ET.back_to_menu)  #if the user press x above the window, it will back to main menu page

        try:
            icon = PhotoImage(file='coin.png')
            ET.window.iconphoto(True, icon)
        except:
            pass

        #Frame of the whole window
        Container = Frame(ET.window)
        Container.pack(fill='both', expand=True)

        ET.Mainpage = Frame(Container, bg='#f7f2e9')
        ET.MonthPage = Frame(Container, bg='#f7f2e9')
        ET.Statistic_page = Frame(Container, bg='#f7f2e9')

        #make sure all the frame same position
        for frame in (ET.Mainpage, ET.MonthPage, ET.Statistic_page):
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        #bottom menu button
        bottom_menu = Frame(ET.window, bg='#7e9aed', height=90)
        bottom_menu.pack(side='bottom', fill='x')

        Main_button = Button(bottom_menu, text="< Back", font=("Arial", 15, 'bold'), bg='#7e9aed', fg='white',
                             command=ET.back_to_menu)
        show_record_button = Button(bottom_menu, text="Expenses Tracker", font=("Arial", 15, 'bold'), bg='#7e9aed', fg='white',
                              command=lambda: ET.show_page(ET.Mainpage))
        Statistic_button = Button(bottom_menu, text="Statistic", font=("Arial", 15, 'bold'), bg='#7e9aed', fg='white',
                                  command=lambda: ET.show_page(ET.Statistic_page))

        Main_button.pack(side='left', expand=True, fill='both')
        show_record_button.pack(side="left", expand=True, fill="both")
        Statistic_button.pack(side="left", expand=True, fill="both")

        #show expenses tracker
        ET.show_page(ET.Mainpage)

        #Expenses Tracker Page
        ET.total_frame = Frame(ET.Mainpage, bg='#f7f2e9',height=80)
        ET.total_frame.pack(fill='x',pady=(10, 0),padx=20)

        main_frame = Frame(ET.Mainpage, bg='#f7f2e9')
        main_frame.pack(fill='both', expand=True, padx=20, pady=(0, 10))

        #Scroll bar to see all the expenses
        main_canvas = Canvas(main_frame, bg='#f7f2e9', highlightthickness=0)
        scrollbar = Scrollbar(main_frame, orient="vertical", command=main_canvas.yview)
        ET.scrollPage = Frame(main_canvas, bg='#f7f2e9')  #main frame to put widget

        ET.scrollPage.bind("<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))

        main_canvas.create_window((0, 0), anchor="nw", window=ET.scrollPage)
        main_canvas.configure(yscrollcommand=scrollbar.set)

        main_canvas.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")

        #Add Button
        Button(ET.Mainpage, text='+', font=('Arial', 20, 'bold'), bg='#7e9aed', fg='white', width=3, height=1,
               command=ET.add_new_expenses).pack(side="bottom", anchor="e", padx=20, pady=(10,20))

        ET.Check_empty_file() #check the file, if empty show label
        ET.refresh_mainpage() #show record (if have)

        # Statistic page
        Title_label = Label(ET.Statistic_page, text='Monthly Statistics', font=('Arial', 18, 'bold'), fg='white',
                            bg='#7e9aed', relief='ridge', bd=3, padx=20, pady=15)
        Title_label.pack(fill='x', padx=20, pady=(30, 20))

        Month_frame = Frame(ET.Statistic_page, bg='#fcf7ed', relief='ridge', bd=2)
        Month_frame.pack(padx=20, pady=(10, 40), fill='both', expand=True)

        ET.in_frame = Frame(Month_frame, bg='#fcf7ed')
        ET.in_frame.pack(padx=30, pady=30, fill='both', expand=True)

        ET.select_month = None
        ET.refresh_statistics()  #show statistic

    def add_new_expenses(ET):
    #window for this page
        ET.expenses = Toplevel(ET.window)
        ET.expenses.geometry("500x650")
        ET.expenses.title('Expenses Tracker')
        ET.window.withdraw()
        ET.expenses.config(background='#f7f2e9')
        ET.expenses.protocol("WM_DELETE_WINDOW", ET.back_to_mainmenu)  #user can back to showing record page if press x button above

    #Main Title
        title_label = Label(ET.expenses, text="Expenses Tracker", font=('Arial', 18, 'bold'), fg='white', bg='#7e9aed',
                            relief='ridge', bd=3, padx=20, pady=15
                            #,image=icon,compound='left'
                            )
        title_label.pack(fill='x', padx=20, pady=(20,30))

    #Form a frame which can let arrangement become easier
        form_frame = Frame(ET.expenses, bg='#fcf7ed', relief='ridge', bd=2)
        form_frame.pack(padx=20, pady=10, fill='both', expand=True)

        inner_frame = Frame(form_frame, bg='#fcf7ed')
        inner_frame.pack(padx=30, pady=30, fill='both', expand=True)

    #Date (choose from calendar)
        date_frame = Frame(inner_frame, bg='#fcf7ed')
        date_frame.pack(fill='x', pady=(0, 20))

        date_label = Label(date_frame, text="Date        :", font=('Arial', 15, 'bold'), fg='black', bg='#fcf7ed', width=11, anchor='w')
        date_label.pack(side='left')

        ET.date_picker = DateEntry(date_frame, width=30, font=('Arial', 11), borderwidth=2, date_pattern='dd/mm/yyyy', background='#7e9aed', foreground='white',state='readonly')
        ET.date_picker.pack(side='left')

    #Amount (key in by keyboard)
        amount_frame = Frame(inner_frame, bg='#fcf7ed')
        amount_frame.pack(fill='x',pady=(0,20))

        amount_label = Label(amount_frame,text="Amount   :",font=("Arial", 15,'bold'),fg='black',bg='#fcf7ed',width=11, anchor='w')
        amount_label.pack(side="left")

    #Show RM symbol
        RM_label = Label(amount_frame,text='RM',font=("Arial", 11),fg='black',bg='white',borderwidth=1, relief='ridge')
        RM_label.pack(side="left")

        ET.amount_enter = Entry(amount_frame,width=30,font=("Arial", 11))
        ET.amount_enter.pack(side="left")
        ET.amount_enter.focus()

    #Category (Choose 1 category)
        category_frame = Frame(inner_frame, bg='#fcf7ed')
        category_frame.pack(fill='x',pady=(0,20))

        category_label = Label(category_frame,text="Category :",font=("Arial", 15,'bold'),fg='black',bg='#fcf7ed',width=11, anchor='w')
        category_label.pack(side="left")

        ET.category_combobox = ttk.Combobox(category_frame, font=("Arial", 11), width=30,values=ET.Category,state='readonly')
        ET.category_combobox.set('')

        ET.category_combobox.pack(side='left')

    #Remark made by user (Key in by keyboard) (can be empty)
        remark_frame = Frame(inner_frame, bg='#fcf7ed')
        remark_frame.pack(fill='x',pady=(0,20))

        remark_label = Label(remark_frame,text='Remark   :',font=("Arial", 15,'bold'),fg='black',bg='#fcf7ed',width=11, anchor='w')
        remark_label.pack(side="left")

        ET.remark_entry = Text(remark_frame,width=32,font=("Arial", 11),height=5)
        ET.remark_entry.pack(side="left")

    #Confirm Button to proceed and cancel button to back to main page
        Button_frame = Frame(inner_frame, bg='#fcf7ed')
        Button_frame.pack(fill='x', pady=40)

        Button_store = Frame(Button_frame, bg='#fcf7ed')
        Button_store.pack(anchor='center')

        Button(Button_store,text="Add Expense",font=("Arial",15,'bold'), fg='white',bg='#7e9aed',relief='ridge', bd=2, padx=10,
               command=ET.Get_user_input).pack(side='left',padx=10)

        Button(Button_store,text='Cancel',font=("Arial",15,'bold'), fg='white',bg='#7e9aed',relief='ridge', bd=2, padx=10,
               command=ET.back_to_mainmenu).pack(side='left',padx=10)

    #To let it have a space at the bottom
        Bottom_frame = Frame(ET.expenses, bg='#f7f2e9')
        Bottom_frame.pack(fill='x',pady=20)

    def Get_user_input(ET):
        #Read all user input
        date_input = ET.date_picker.get()
        amount_input = ET.amount_enter.get().strip()
        category_input = ET.category_combobox.get()
        remark_input = ET.remark_entry.get("1.0", "end-1c").strip()

        #check if it is empty
        if not amount_input:
            messagebox.showerror("Error", "Please enter a valid amount.")
            return

        #check input error
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

        #format to 2 decimal point

        amount = f"{amount:.2f}"

        #append the record to file
        with open(f'{ET.Username}/expenses_record.csv', 'a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([date_input, amount, category_input, remark_input])

        ET.back_to_mainmenu()
        ET.refresh_mainpage()
        ET.refresh_statistics()
        messagebox.showinfo("Success!", "Your expense is added!")

    def back_to_mainmenu(ET):
        ET.expenses.destroy()
        ET.window.deiconify()

    def show_page(ET,page):
        page.tkraise()

        if page == ET.Statistic_page:
            ET.refresh_statistics()

    def back_to_menu(ET):
        ET.mainpage.deiconify()
        ET.window.destroy()

    def Check_empty_file(ET):
        try:
            if ET.Empty_label:
                ET.Empty_label.destroy()
        except:
            pass

        data = ET.read_expenses()

        #if no data show label
        if not data:
            ET.Empty_label = Label(ET.Mainpage, text="There is no record yet...", font=('Arial', 15, 'bold'), fg='#7e9aed',
                                bg='#f7f2e9')
            ET.Empty_label.place(anchor='center', relx=0.5, rely=0.5)
            return True

        return False

    def Show_total_expenses(ET):
        for widget in ET.total_frame.winfo_children():
            widget.destroy()

        total = 0
        data = ET.read_expenses()

        for row in data:
            total += float(row[1]) #add all expenses in the record

        total_label = Label(ET.total_frame,text=f"Total expenses : RM{total:.2f}",font=('Arial', 18, 'bold'),bg='#7e9aed',fg='white',relief='ridge', bd=3,padx=40,pady=15)
        total_label.place(anchor='center', relx=0.5, rely=0.5)

    def read_expenses(ET):
        os.makedirs(ET.Username,exist_ok=True) #check if there is a folder for the username, if no create one

        if not os.path.exists(f'{ET.Username}/expenses_record.csv') or os.path.getsize(f'{ET.Username}/expenses_record.csv') == 0:
            return []

        try:
            #read the file of the specific user
            with open(f'{ET.Username}/expenses_record.csv', "r", encoding='utf-8') as file:
                reader = csv.reader(file)
                data = [row for row in reader if row]

                return data
        except:
            return []

    def delete_expense(ET,index):
        if messagebox.askyesno(title="Delete Expense", message="Are you sure you want to delete this expense?"):
            data = ET.read_expenses()
            data.pop(index)

            with open(f'{ET.Username}/expenses_record.csv', "w", newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(data)

            ET.refresh_mainpage()
            ET.refresh_statistics()

        else:
            return

    def Edit_expense(ET,index):
        ET.data = ET.read_expenses()
        ET.index = index

        ET.expenses = Toplevel(ET.window)
        ET.expenses.geometry("500x650")
        ET.expenses.title('Edit Expense')
        ET.window.withdraw()
        ET.expenses.config(background='#f7f2e9')
        ET.expenses.protocol("WM_DELETE_WINDOW", ET.back_to_mainmenu)

        # Main Title
        title_label = Label(ET.expenses, text="Expenses Tracker", font=('Arial', 18, 'bold'), fg='white', bg='#7e9aed',
                            relief='ridge', bd=3, padx=20, pady=15
                            # ,image=icon,compound='left'
                            )
        title_label.pack(fill='x', padx=20, pady=(20, 30))

        # Form a frame which can  let arrangement become easier
        form_frame = Frame(ET.expenses, bg='#fcf7ed', relief='ridge', bd=2)
        form_frame.pack(padx=20, pady=10, fill='both', expand=True)

        inner_frame = Frame(form_frame, bg='#fcf7ed')
        inner_frame.pack(padx=30, pady=30, fill='both', expand=True)

        # Date (choose from calendar)
        date_frame = Frame(inner_frame, bg='#fcf7ed')
        date_frame.pack(fill='x', pady=(0, 20))

        date_label = Label(date_frame, text="Date        :", font=('Arial', 15, 'bold'), fg='black', bg='#fcf7ed', width=11,
                           anchor='w')
        date_label.pack(side='left')

        ET.date_picker = DateEntry(date_frame, width=30, font=('Arial', 11), borderwidth=2, date_pattern='dd/mm/yyyy',
                                background='#7e9aed', foreground='white') #didn't use readonly
        ET.date_picker.delete(0, 'end')  #if let the date entry become readonly, the date cannot show the previous selected date in this record because it cannot be edited (delete and insert)
        ET.date_picker.insert(0,ET.data[ET.index][0]) #insert previous data
        ET.date_picker.pack(side='left')

        # Amount (key in by keyboard)
        amount_frame = Frame(inner_frame, bg='#fcf7ed')
        amount_frame.pack(fill='x', pady=(0, 20))

        amount_label = Label(amount_frame, text="Amount   :", font=("Arial", 15, 'bold'), fg='black', bg='#fcf7ed',
                             width=11, anchor='w')
        amount_label.pack(side="left")

        # Show RM symbol
        RM_label = Label(amount_frame, text='RM', font=("Arial", 11), fg='black', bg='white', borderwidth=1, relief='ridge')
        RM_label.pack(side="left")

        ET.amount_enter = Entry(amount_frame, width=30, font=("Arial", 11))
        ET.amount_enter.insert(0,ET.data[ET.index][1])
        ET.amount_enter.pack(side="left")
        ET.amount_enter.focus()

        # Category (Choose 1 category)
        category_frame = Frame(inner_frame, bg='#fcf7ed')
        category_frame.pack(fill='x', pady=(0, 20))

        category_label = Label(category_frame, text="Category :", font=("Arial", 15, 'bold'), fg='black', bg='#fcf7ed',
                               width=11, anchor='w')
        category_label.pack(side="left")

        ET.category_combobox = ttk.Combobox(category_frame, font=("Arial", 11), width=30,values=ET.Category,state='readonly')
        ET.category_combobox.set(ET.data[ET.index][2])

        ET.category_combobox.pack(side='left')

        # Remark made by user (Key in by keyboard)
        remark_frame = Frame(inner_frame, bg='#fcf7ed')
        remark_frame.pack(fill='x', pady=(0, 20))

        remark_label = Label(remark_frame, text='Remark   :', font=("Arial", 15, 'bold'), fg='black', bg='#fcf7ed',
                             width=11, anchor='w')
        remark_label.pack(side="left")

        ET.remark_entry = Text(remark_frame, width=32, font=("Arial", 11), height=5)
        ET.remark_entry.insert("1.0",ET.data[ET.index][3])
        ET.remark_entry.pack(side="left")

        # Confirm Button to proceed and cancel button to back to main page
        Button_frame = Frame(inner_frame, bg='#fcf7ed')
        Button_frame.pack(fill='x', pady=40)

        Button_store = Frame(Button_frame, bg='#fcf7ed')
        Button_store.pack(anchor='center')

        Button(Button_store, text="Save", font=("Arial", 15, 'bold'), fg='white', bg='#7e9aed', relief='ridge', bd=2,
               padx=10,
               command=ET.Save_expense).pack(side='left', padx=10)

        Button(Button_store, text='Cancel', font=("Arial", 15, 'bold'), fg='white', bg='#7e9aed', relief='ridge', bd=2,
               padx=10,
               command=ET.back_to_mainmenu).pack(side='left', padx=10)

        # To let it have a space at the bottom
        Bottom_frame = Frame(ET.expenses, bg='#f7f2e9')
        Bottom_frame.pack(fill='x', pady=20)

    def Save_expense(ET):
        date_input = ET.date_picker.get()
        amount_input = ET.amount_enter.get().strip()
        category_input = ET.category_combobox.get()
        remark_input = ET.remark_entry.get("1.0", "end-1c").strip()

        try:
            datetime.strptime(date_input, "%d/%m/%Y")  #user still can edit the date entry box, so to prevent the user enter invalid date
        except ValueError:
            messagebox.showerror("Error", "Please choose a valid date.")
            return

        if not amount_input: #no input
            messagebox.showerror("Error", "Please enter a valid amount.")
            return

        try: #not number
            amount = float(amount_input)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
            return

        if not category_input: #no selection
            messagebox.showerror('Error', 'Please select a category.')
            return

        amount = f"{amount:.2f}"  #format to 2 decimal

        ET.data[ET.index] = [date_input, amount, category_input, remark_input]  #store new data into the file

        with open(f'{ET.Username}/expenses_record.csv', 'w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)  #write all data into file again
            writer.writerows(ET.data)

        ET.back_to_mainmenu()
        ET.refresh_mainpage()
        ET.refresh_statistics()
        messagebox.showinfo("Success!", "Your expense is edited successfully!")

    def refresh_mainpage(ET):
        ET.Check_empty_file()
        ET.Show_total_expenses()

        for widget in ET.scrollPage.winfo_children():
            widget.destroy()

        if ET.Empty_label:  #double check that if there has an empty label
            ET.Empty_label.pack_forget()

        if ET.Check_empty_file():
            return

        data = ET.read_expenses()
        if not data:
            return

        data_Index = [(i,row) for i,row in enumerate(data)]

        #sort the date according descending order
        data_Index.sort(key=lambda x: datetime.strptime(x[1][0], "%d/%m/%Y"), reverse=True)

        for index,row in data_Index:
            Outer_frame = Frame(ET.scrollPage, bg='#f7f2e9',width=400,height=80)
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

            Edit_button = Button(Outer_frame,text='📝',bg='#7e9aed', fg='white',width=2,height=1,command=lambda idx=index:ET.Edit_expense(idx))
            Edit_button.pack(side="right",padx=(0,10))

            Delete_button = Button(Outer_frame,text="⌫",bg='#7e9aed', fg='white',height=1,width=2,command=lambda idx=index:ET.delete_expense(idx))
            Delete_button.pack(side="right",padx=(0,8))

    def Get_month_data(ET):
        pie_data = []
        data = ET.read_expenses()

        for row in data:
            month = datetime.strptime(row[0], "%d/%m/%Y").strftime('%m/%Y')  #get month and year
            pie_data.append([month, row[1], row[2]])

        pie_data.sort(key=lambda row: (datetime.strptime(row[0], "%m/%Y")), reverse=True)  #sort the data based on month

        month = []
        seen = set() #use as a filter
        for row in pie_data:
            if row[0] not in seen:  #seen is to filter the month appeared before
                month.append(row[0])
                seen.add(row[0])

        return pie_data, month

    def show_pie_chart(ET,Month):
        #show the statistic using pie chart

        pie_data, _ = ET.Get_month_data()  #only the data is used in this function
        category_amount = {}

        #clear all previous widget
        for widget in ET.pie_frame.winfo_children():
            widget.destroy()

        plt.close('all') #close all pie chart

        for row in pie_data:
            if Month == "All" or row[0] == Month: #If all month is selected, get every row data if no check it is selected month or not
                category = row[2]  #store category
                amount = float(row[1])  #store amount
                category_amount[category] = category_amount.get(category, 0) + amount #dictionary that the category is the key
                #to add the amount of same category together (add the amount in the category and the new amount together)

        if not category_amount: #If no data
            No_data_label = Label(ET.pie_frame, text="There is no record.", font=('Arial', 15, 'bold'),
                                  fg='#7e9aed', bg='#fcf7ed')
            No_data_label.place(anchor='center', relx=0.5, rely=0.5)
            return

        piechart_label = list(category_amount.keys())
        piechart_sizes = list(category_amount.values())

        fig, ax = plt.subplots(figsize=(4, 4), dpi=100)  #generate pie chart data
        ax.pie(piechart_sizes, labels=piechart_label, autopct="%1.1f%%", textprops={'fontsize': 8})
        ax.axis('equal')

        match Month:  #title
            case "All":
                ax.set_title("Expenses for All Months")
            case _:
                ax.set_title(f"Expenses for {Month}")

        chart = FigureCanvasTkAgg(fig, master=ET.pie_frame)
        chart.draw()
        chart.get_tk_widget().pack(fill='both', expand=True)

    def refresh_statistics(ET):
        for widget in ET.in_frame.winfo_children(): #clear all
            widget.destroy()

        MonthCombo_frame = Frame(ET.in_frame,bg='#fcf7ed')
        MonthCombo_frame.pack(fill='x',pady=(0,20))

        MonthCombo_label = Label(MonthCombo_frame,text='Select Month:',font=("Arial", 15,'bold'),fg='black',bg='#fcf7ed')
        MonthCombo_label.pack(side='left',padx=(0,40))

        MonthCombo_combobox = ttk.Combobox(MonthCombo_frame, font=("Arial", 11), width=15,state='readonly')
        MonthCombo_combobox.pack(side='left')

        ET.pie_frame = Frame(ET.in_frame,bg='#fcf7ed')
        ET.pie_frame.pack(fill='both',expand=True)

        MonthCombo_combobox.bind("<<ComboboxSelected>>", lambda event: ET.show_pie_chart(MonthCombo_combobox.get()))

        pie_data, month = ET.Get_month_data()

        if month:
            values_combobox = ["All"] + month
        else:
            values_combobox = ["All"]

        MonthCombo_combobox['values'] = values_combobox

        if ET.select_month and ET.select_month in values_combobox: #show selected month
            MonthCombo_combobox.set(ET.select_month)
            ET.show_pie_chart(ET.select_month)
        else:  #show all month
            MonthCombo_combobox.set("All")
            ET.select_month = "All"
            ET.show_pie_chart(ET.select_month)