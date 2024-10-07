import json
from abc import abstractmethod
from datetime import datetime
from pathlib import Path
from random import randint
from random import choice
from error_classes import *
from graphics import *


def current_time(): return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class BankAccount:
    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    @abstractmethod
    def get_balance(self):
        pass


class User:
    def __init__(self, first_name: str, last_name: str, birth_day: int, birth_month: int, birth_year: int, city: str, country: str, user_id: int, password: str):
        self.name = {"fn": first_name, "ln": last_name}
        self.dob = {"day": birth_day, "month": birth_month, "year": birth_year}
        self.location = {"city": city, "country": country}
        self.user_id = user_id
        self.password = password

    def edit_info(self, first_name: str = None, last_name: str = None, birth_day: int = None, birth_month: int = None, birth_year: int = None, city: str = None, country: str = None):
        if first_name:
            self.name["fn"] = first_name
        if last_name:
            self.name["ln"] = last_name
        if birth_day:
            self.dob["day"] = birth_day
        if birth_month:
            self.dob["month"] = birth_month
        if birth_year:
            self.dob["year"] = birth_year
        if city:
            self.location["city"] = city
        if country:
            self.location["country"] = country

    def inquire(self):
        print(self.name["fn"], self.name["ln"])
        print(f"{self.dob["day"]}, {self.dob["month"]}, {self.dob["year"]}")
        print(self.location["city"], self.location["country"])


class Customer(User):
    def __init__(self, first_name: str, last_name: str, birth_day: int, birth_month: int, birth_year: int, city: str, country: str, user_id: int, password: str):
        super().__init__(first_name, last_name, birth_day, birth_month, birth_year, city, country, user_id, password)
        self.accounts = []

    def find_account(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        return None

    def add_account(self, acc_type: str, acc_num: int, acc_pass: str, init_bal: int, int_rate=None):
        exists = self.find_account(acc_num)
        if exists is not None:
            return -1
        if acc_type.upper() == "CHECKING":
            new_account = CheckingAccount(acc_num, acc_pass, init_bal)
            self.accounts.append(new_account)
            success(f"New checking account {new_account.account_number} created.")
            self.accounts.sort(key=lambda x: x.account_number)
            return new_account
        else:
            new_account = SavingsAccount(acc_num, acc_pass, init_bal, int_rate)
            self.accounts.append(new_account)
            success(f"New savings account {new_account.account_number} created.")
            self.accounts.sort(key=lambda x: x.account_number)
            return new_account

    def delete_account(self, acc_num, acc_pass):
        account = self.find_account(acc_num)
        if account is None or account.account_password != acc_pass:
            return -1
        self.accounts.remove(account)
        self.accounts.sort(key=lambda x: x.account_number)
        return 0

    def count(self):
        return len(self.accounts)

    def deposit(self, account_number: int, account_password: str, amount: int):
        try:
            if amount > 9999999 or amount < 1:
                raise OutOfRange
            account = self.find_account(account_number)
            if account is None:
                raise NotFound
            if account.account_password != account_password:
                raise InvalidCredentials
            account.deposit(amount)
            return 0
        except OutOfRange:
            error("Invalid value")
            return -1
        except NotFound:
            error(f"No account found for number {account_number}")
            return -1
        except InvalidCredentials:
            error(f"Invalid account number or password")
            return -1

    def withdraw(self, account_number: int, account_password: str, amount: int):
        try:
            if amount > 9999999 or amount < 1:
                raise OutOfRange
            account = self.find_account(account_number)
            if account is None:
                raise NotFound
            if account.account_password != account_password:
                raise InvalidCredentials
            if amount > account.get_balance():
                raise InsufficientFunds
            account.withdraw(amount)
            return 0
        except OutOfRange:
            error("Invalid value")
            return -1
        except NotFound:
            error(f"No account found for number {account_number}")
            return -1
        except InsufficientFunds:
            error("Insufficient funds")
            return -1
        except InvalidCredentials:
            error(f"Invalid account number or password")
            return -1

    def add_interest(self, account_number, account_password: str):
        account: SavingsAccount = self.find_account(account_number)
        try:
            if account is None:
                raise NotFound
            if account.account_password != account_password:
                raise InvalidCredentials
            account.balance += (account.balance * (account.interest_rate / 100))
            return 0
        except NotFound:
            error(f"No account found for number {account_number}")
            return -1
        except InvalidCredentials:
            error(f"Invalid account number or password")
            return -1

    def get_balance(self, account_number: int, account_password: str):
        for account in self.accounts:
            if account_number == account.account_number:
                if account.account_password == account_password:
                    return account.get_balance
                else:
                    return -1
        return None

    def clear_accounts(self):
        self.accounts = []


class Teller(User):
    def __init__(self, first_name: str, last_name: str, birth_day: int, birth_month: int, birth_year: int, city: str, country: str, user_id: int, password: str):
        super().__init__(first_name, last_name, birth_day, birth_month, birth_year, city, country, user_id, password)


class CheckingAccount(BankAccount):
    def __init__(self, account_number, account_password, initial_balance):
        self.account_number = account_number
        self.account_password = account_password
        self.balance = initial_balance

    def deposit(self, amount):
        self.balance += amount
        return 0

    def withdraw(self, amount):
        self.balance -= amount
        return 0

    def get_balance(self):
        return self.balance


class SavingsAccount(BankAccount):
    def __init__(self, account_number, account_password, initial_balance, interest_rate):
        self.account_number = account_number
        self.account_password = account_password
        self.balance = initial_balance
        self.interest_rate = interest_rate

    def deposit(self, amount):
        self.balance += amount
        return 0

    def withdraw(self, amount):
        self.balance -= amount
        return 0

    def get_balance(self):
        return self.balance

    def add_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        return 0


class Bank:
    def __init__(self):
        self.customers = []

    def add_customer(self, first_name: str, last_name: str, birth_day: int, birth_month: int, birth_year: int, city: str, country: str, user_id: int, password: str):
        exists = self.find(user_id)
        if exists is not None:
            return -1
        new_customer = Customer(first_name, last_name, birth_day, birth_month, birth_year, city, country, user_id, password)
        self.customers.append(new_customer)
        success(f"New customer {new_customer.user_id} created.")
        return new_customer

    def terminate_customer(self, customer_id, customer_password):
        customer: Customer = self.find(customer_id)
        if customer is None or customer.password != customer_password:
            return -1
        self.customers.remove(customer)
        self.customers.sort(key=lambda x: x.name["fn"])
        return 0

    def find(self, customer_id):
        for customer in self.customers:
            if customer_id == customer.user_id:
                return customer
        return None

    def count(self):
        return len(self.customers)

    def clear_bank(self):
        for customer in self.customers:
            customer.clear_accounts()
        self.customers = []

    def import_data(self, origin: str, overwrite: bool = False):
        store = ""
        with open(f'{origin}', 'r+') as f:
            store += f.read()

        store_list = store.splitlines()
        if overwrite:
            self.clear_bank()
        for entry in store_list:
            data: dict = json.loads(entry.replace("'", '"'))
            print(data)
            if self.find(data["user_id"]) is not None:
                continue
            customer = self.add_customer(
                data["name"]["fn"],
                data["name"]["ln"],
                data["dob"]["day"],
                data["dob"]["month"],
                data["dob"]["year"],
                data["location"]["city"],
                data["location"]["country"],
                data["user_id"],
                data["password"]
            )
            for account in data["accounts"]:
                print(account)
                acc_type = "Savings" if "interest_rate" in account else "Checking"
                print(acc_type)
                if customer.find_account(account["account_number"]) is not None:
                    print("exists")
                    continue
                print("doesnt exist")
                customer.add_account(acc_type, account["account_number"], account["account_password"], account["balance"],
                                     account["interest_rate"] if acc_type == "Savings" else None)
                print("account added")

    def export_data(self, destination: str, overwrite: bool = False):
        with open(f'{destination}', 'w' if overwrite else 'a') as f:
            for customer in self.customers:
                new_accounts = []
                for account in customer.accounts:
                    new_accounts.append(account.__dict__)
                customer.accounts = new_accounts
                f.write(str(customer.__dict__) + "\n")

    def load_test_data(self, customer_count: int, accounts_per_customer: int):
        try:
            main_test_customer = self.add_customer("Fares", "Mostafa", 28, 2, 2008, "Cairo", "Egypt", 1234, "1234")
            main_test_customer.add_account("checking", 1234, "1234", 5000, 10)
        except AttributeError:
            pass

        _ = 0
        while _ < customer_count:
            try:
                x = 0
                id_pass = randint(1000, 9999)
                bd, bm, by = randint(1, 31), randint(1, 12), randint(1999, 2015)
                cust = self.add_customer("Test", f"Account #{_}", bd, bm, by, "Test city", "Test country", id_pass, str(id_pass))
                while x < accounts_per_customer:
                    try:
                        id_pass = randint(1000, 9999)
                        cust.add_account(choice(["Checking", "Savings"]),
                                         id_pass,
                                         str(id_pass),
                                         randint(0, 10) * (randint(0, 9) * 100),
                                         randint(1, 50))
                        x += 1
                    except:
                        pass
                _ += 1
            except NameError:
                pass


class BankProgram:
    def __init__(self, root, current_teller):
        self.data = Bank()
        self.active_customer: Customer or None = None
        self.active_account: CheckingAccount or SavingsAccount = None
        self.log = {}
        self.show_password = False
        self.teller = current_teller
        # self.data.load_test_data(10, 15)

        # Window setup
        self.root = root
        self.root.obj.state('zoomed')
        self.root.obj.protocol("WM_DELETE_WINDOW", lambda: self.button_handler("EXIT"))
        self.root.set_icon('assets/icon.ico')

        bg_image = tk.PhotoImage(file="assets/bg_full.png")
        bg = tk.Label(self.root.obj, image=bg_image)
        bg.place(relx=0.5, rely=0.5, anchor="center")
        _ = ttk.Style()
        _.configure(style='transparent.TFrame', background="#403333")
        self.content_frame = ttk.Frame(self.root.obj, padding=15, style="transparent.TFrame")
        self.content_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Heading
        # title = Label(self.content_frame, "Mashriq Bank", "Product Sans", 40, padding=15)
        logo_image = tk.PhotoImage(file='assets/logo.png').subsample(4)
        title = ttk.Label(self.content_frame, image=logo_image, padding=5, background="#403333")
        # title.obj.configure(foreground="#ffffff", background="#403333")
        title.pack(anchor='center')

        self.account_display = Label(self.content_frame, font="Product Sans", font_size=18)
        self.account_display.obj.configure(width=27, foreground="#ffffff", background='#4e3c3c', padding=5)
        self.account_display.set_text("Account: None")

        self.customer_display = Label(self.content_frame, font="Product Sans", font_size=18)
        self.customer_display.obj.configure(width=27, foreground="#ffffff", background='#4e3c3c', padding=5)
        self.customer_display.set_text("Customer: None")

        playsound('BOOT')
        self.root.obj.after(350)
        self.customer_display.pack()
        self.account_display.pack()

        self.buttons_init()

        self.log_entry("APPLICATION OPENED", "APPLICATION OPENED")
        self.ribbon_init()

        # Update cycle
        self.root.obj.mainloop()

    def ribbon_init(self):
        menubar = tk.Menu()
        self.root.obj.config(menu=menubar)

        menus = [
            {
                "label": "File",
                "commands": [{
                    "label": "Save...",
                    "accelerator": "Ctrl-S",
                    "command": lambda: self.button_handler("SAVE"),
                    "bindings": ["<Control-S>", "<Control-s>"]
                }, {
                    "label": "Load...",
                    "accelerator": "Ctrl-O",
                    "command": lambda: self.button_handler("LOAD"),
                    "bindings": ["<Control-O>", "<Control-o>"]
                }, {
                    "label": "Test data",
                    "accelerator": None,
                    "command": lambda: _(),
                    "bindings": None
                }, {
                    "label": "Clear",
                    "accelerator": None,
                    "command": lambda: self.button_handler("CLEAR"),
                    "bindings": None
                }, {
                    "label": "separator"
                }, {
                    "label": "Quit",
                    "accelerator": "Alt-F4",
                    "command": lambda: self.button_handler("EXIT"),
                    "bindings": None
                },
                ]
            }, {
                "label": "Teller",
                "commands": [{
                    "label": "Teller info",
                    "accelerator": None,
                    "command": lambda: self.button_handler("TELLER_INFO"),
                    "bindings": None
                }]
            }, {
                "label": "Help",
                "commands": [{
                    "label": "Documentation",
                    "accelerator": "Ctrl-H",
                    "command": lambda: mb.showinfo("Documentation", "For a detailed guide on the program, refer to the PDF file found alongside the executable", self.root.obj),
                    "bindings": ["<Control-H>", "<Control-h>"]
                }, {
                    "label": "Credits",
                    "accelerator": None,
                    "command": lambda: mb.showcredits(
                        "Credits",
                        "Made with <3 by Fares Mostafa Mohamed\n"
                        "Supervisor: Eng. Hassan Talal\n"
                        "\n"
                        "Special thanks:\n"
                        "Stackoverflow\n"
                        "Quora\n"
                        "GeeksforGeeks\n"
                        "Nitraine\n"
                        "tutorialspoint\n"
                        "pythonspot\n",
                        self.root.obj
                    ),
                    "bindings": None
                }, {
                    "label": "Support",
                    "accelerator": None,
                    "command": lambda: mb.showinfo("Support", "For further support, please contact me via..\nEmail:\nfaresmostafanawar@gmail.com", self.root.obj),
                    "bindings": None,
                }]
            }
        ]

        for menu in menus:
            new = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(menu=new, label=menu["label"])
            for command in menu["commands"]:
                if command["label"] == "separator":
                    new.add_separator()
                    continue
                new.add_command(label=command["label"], accelerator=command["accelerator"], command=command["command"])
                if command["bindings"] is not None:
                    for binding in command["bindings"]:
                        print(binding, command["command"])
                        self.root.obj.bind(binding, lambda x: command["command"])

        # file_menu = tk.Menu(menubar, tearoff=0)
        # menubar.add_cascade(menu=file_menu, label="File")
        #
        # file_menu.add_command(label="Save...", accelerator="Ctrl-S", command=lambda: self.button_handler("SAVE"))
        # self.root.obj.bind("<Control-S>", lambda: self.button_handler("SAVE"))
        # self.root.obj.bind("<Control-s>", lambda: self.button_handler("SAVE"))
        #
        # file_menu.add_command(label="Load...", accelerator="Ctrl-O", command=lambda: self.button_handler("LOAD"))
        # self.root.obj.bind("<Control-O>", lambda: self.button_handler("LOAD"))
        # self.root.obj.bind("<Control-o>", lambda: self.button_handler("LOAD"))
        #
        # file_menu.add_command(label="Clear", command=lambda: self.button_handler("CLEAR"))
        # file_menu.add_command(label="Load test data", command=lambda: _())
        # file_menu.add_separator()
        # file_menu.add_command(label="Quit", accelerator="Alt+F4", command=lambda: self.button_handler("EXIT"))
        #
        # help_menu = tk.Menu(menubar, tearoff=0)
        # menubar.add_cascade(menu=help_menu, label="Help")

        def _():
            self.data.load_test_data(50, 20)
            mb.showinfo("Test data", "500 test customers loaded into database with 200 accounts each", parent=self.root.obj)

    def buttons_init(self):
        ttk.Style().configure(style='transparent.TFrame', background="#403333")
        button_frame = ttk.Frame(self.content_frame, style="transparent.TFrame")
        button_frame.pack(pady=5)

        cb_frame = ttk.Frame(button_frame, style="transparent.TFrame", padding=5)
        ttk.Separator(button_frame, orient="horizontal").pack(fill=tk.X, pady=2)
        cb_label = Label(button_frame, text="Customer actions", font="Product Sans", font_size=15, background="#403333", foreground="white")
        cb_label.obj.configure()
        cb_label.obj.pack()
        cb_frame.pack(pady=0)
        ttk.Separator(button_frame, orient="horizontal").pack(fill=tk.X, pady=2)
        ab_frame = ttk.Frame(button_frame, style="transparent.TFrame", padding=5)
        ab_label = Label(button_frame, text="Account actions (Must select customer)", font="Product Sans", font_size=15, background="#403333", foreground="white")
        ab_label.pack()
        ab_frame.pack(pady=0)
        ttk.Separator(button_frame, orient="horizontal").pack(fill=tk.X, pady=2)

        customer_buttons = []
        customer_button_ref = {
            "Select": "SELECT_CUSTOMER", "New": "NEW_CUSTOMER", "Inquire": "VIEW_CUSTOMER",
            "Edit": "EDIT_CUSTOMER", "Terminate": "TERMINATE_CUSTOMER", "Registry": "CUSTOMER_REGISTRY",
            "Clear database": "CLEAR"
        }

        account_buttons = []
        account_button_ref = {
            "Select": "SET", "New": "NEW", "Terminate": "DELETE", "Deposit": "DEPOSIT",
            "Withdraw": "WITHDRAW", "Log": "LOG", "Inquire": "VIEW", "Interest": "INTEREST",
            "Save Data": "SAVE", "Load Data": "LOAD", "Clear": "CLEAR_ACCOUNTS", "Registry": "DISPLAY",
            "Sign Out": "EXIT"
        }

        for button_text in customer_button_ref.keys():
            # ttk.Style().configure(style='transparent.TButton', background="#403333")
            # b = Button(cb_frame, button_text, 20, 10)
            # b.obj.configure(style="transparent.TButton")
            # b.bind_function(lambda x=button_text: self.button_handler(customer_button_ref[x]))
            # customer_buttons.append(b)

            b = IconButton(cb_frame, button_text, lambda x=button_text: self.button_handler(customer_button_ref[x]), None, 12, 0, "white", "#795757", "white", "#6a4e4e")
            customer_buttons.append(b)

        _ = 0
        for i in range(2):
            for j in range(3):
                customer_buttons[_].obj.grid(row=i, column=j, padx=2, pady=2)
                _ += 1
        # customer_buttons[len(account_buttons) - 1].obj.configure(width=71)
        customer_buttons[len(account_buttons) - 1].obj.grid(row=5, column=0, columnspan=4, padx=2, pady=2)

        for button_text in account_button_ref.keys():
            # ttk.Style().configure(style='transparent.TButton', background="#403333")
            # b = Button(ab_frame, button_text, 15, 10)
            # b.obj.configure(style="transparent.TButton")
            # b.bind_function(lambda x=button_text: self.button_handler(account_button_ref[x]))
            # account_buttons.append(b)

            b = IconButton(ab_frame, button_text, lambda x=button_text: self.button_handler(account_button_ref[x]), None, 12, 0, "white", "#795757", "white", "#6a4e4e")
            account_buttons.append(b)

        _ = 0
        for i in range(3):
            for j in range(4):
                account_buttons[_].obj.grid(row=i, column=j, padx=2, pady=2)
                _ += 1
        # account_buttons[len(account_buttons) - 1].obj.configure(width=76)
        account_buttons[len(account_buttons) - 1].obj.grid(row=5, column=0, columnspan=4, padx=2, pady=2)
        del _

    @staticmethod
    def check_customer(inp, parent):
        try:
            if inp == "None":
                raise Empty
            customer_number = int(inp)
            if customer_number is None:
                raise Empty
            if customer_number > 100000000 or customer_number < 1:
                raise OutOfRange
        except OutOfRange:
            mb.showerror("Peculiar value", "Value outside of allowed range!", parent)
            return -1
        except ValueError:
            mb.showerror("Peculiar value", "Invalid value encountered!", parent)
            return -1
        return customer_number

    @staticmethod
    def check_account(inp, parent):
        try:
            if inp == "None":
                raise Empty
            account_number = int(inp)
            if account_number is None:
                raise Empty
            if account_number > 100000000 or account_number < 1:
                raise OutOfRange
        except Empty:
            mb.showerror("Forgetting something?",
                         "Did you forget to set an active account?", parent)
            return -1
        except OutOfRange:
            mb.showerror("Peculiar value", "Value outside of allowed range!", parent)
            return -1
        except ValueError:
            mb.showerror("Peculiar value", "Invalid value encountered!", parent)
            return -1
        return account_number

    def set_active_customer(self, customer: Customer):
        self.active_customer = customer
        self.customer_display.obj.configure(text=f"Customer: {customer.name["fn"]} {customer.name["ln"]}")

    def set_active_account(self, account: CheckingAccount or SavingsAccount):
        self.active_account = account
        self.account_display.obj.configure(text="Account: " + str(account.account_number))

    def clear_active_customer(self):
        self.active_customer = None
        self.customer_display.obj.configure(text=f"Customer: None")

    def clear_active_account(self):
        self.active_account = None
        self.account_display.obj.configure(text="Account: None")

    @staticmethod
    def check_value(value, parent):
        try:
            value = int(value)
            if value is None:
                raise Empty
            if value > 1000000 or value < 1:
                raise OutOfRange
        except Empty:
            mb.showerror("Forgetting something?",
                         "You left an entry box empty! Values, where art thou?", parent)
            return -1
        except OutOfRange:
            mb.showerror("Peculiar value", "Value outside of allowed range!", parent)
            return -1
        except ValueError:
            mb.showerror("Peculiar value", "Invalid value encountered!", parent)
            return -1
        return value

    def log_entry(self, key: str, content: str):
        self.log.update({f"[{current_time()}]: {key}": content})

    def button_handler(self, button_id: str = "NONE"):
        match button_id:
            case "TELLER_INFO":
                playsound("BEEP")
                toplevel = Window(300, 250, "Teller info", toplevel=True)
                toplevel.set_icon('assets/icon.ico')
                toplevel.obj.configure(bg="#795757")
                toplevel.obj.grab_set()

                frame = ttk.Frame(toplevel.obj, padding=15)
                frame.place(relx=0.5, rely=0.5, anchor="center")

                heading = Label(frame, "Teller info", "Product Sans", 20, padding=5)
                heading.grid(row=0, column=0, column_span=2)

                details = {
                    "ID:": self.teller.user_id,
                    "Name:": f"{self.teller.name["fn"]} {self.teller.name["ln"]}",
                    "DOB:": f"{self.teller.dob["day"]}/{self.teller.dob["month"]}/{self.teller.dob["year"]}",
                    "Location:": f"{self.teller.location["city"]} {self.teller.location["country"]}",
                }

                _ = 1
                for key, value in details.items():
                    Label(frame, text=key, font="Product Sans", font_size=12).grid(row=_, column=0)
                    Label(frame, text=value, font="Product Sans", font_size=12).grid(row=_, column=1)
                    _ += 1

                exit_button = Button(frame, text="Close", padding=5, width=20)
                exit_button.bind_function(lambda: toplevel.obj.destroy())
                toplevel.obj.bind("<Return>", func=lambda x: toplevel.obj.destroy())
                exit_button.obj.focus()

                self.log_entry("TELLER ACCESSED", f"TELLER: {self.teller.user_id}")

                frame.place(relx=0.5, rely=0.5, anchor='center')
                heading.grid(row=0, column_span=2)
                exit_button.obj.grid(row=5, pady=5, columnspan=2)



            case "NEW_CUSTOMER":
                playsound("BEEP")
                toplevel = Window(400, 400, "New customer", toplevel=True)
                toplevel.set_icon('assets/icon.ico')
                toplevel.obj.configure(bg="#795757")
                toplevel.obj.grab_set()

                frame = ttk.Frame(toplevel.obj, padding=15)
                frame.place(relx=0.5, rely=0.5, anchor="center")

                heading = Label(frame, "New customer", "Product Sans", 20, padding=5)

                fname_label = Label(frame, text="First name: ", font="Trebuchet MS", font_size=10, padding=5)
                fname_entry = ttk.Entry(frame)
                fname_entry.focus()

                lname_label = Label(frame, text="Last name: ", font="Trebuchet MS", font_size=10, padding=5)
                lname_entry = ttk.Entry(frame)

                dob_label = Label(frame, text="Date of birth: ", font="Trebuchet MS", font_size=10, padding=5)
                dob_entry = ttk.Labelframe(frame, text="Day, month, year")
                # dob_entry = DateEntry(frame, background="#403333", foreground="white")
                day_entry = ttk.Entry(dob_entry, width=4)
                month_entry = ttk.Entry(dob_entry, width=4)
                year_entry = ttk.Entry(dob_entry, width=4)

                city_label = Label(frame, "City:", font="Trebuchet MS", font_size=10, padding=5)
                city_entry = ttk.Entry(frame)

                country_label = Label(frame, "Country:", font="Trebuchet MS", font_size=10, padding=5)
                country_entry = ttk.Entry(frame)

                user_id_label = Label(frame, "Customer ID:", font="Trebuchet MS", font_size=10, padding=5)
                user_id_entry = ttk.Entry(frame)

                password_label = Label(frame, "Customer password:", font="Trebuchet MS", font_size=10, padding=5)
                password_input = ttk.Entry(frame, show="*")

                show_input = ToggleButton(frame, "", "", "visdark", lambda: toggle_password_visibility(password_input), "novisdark", 40, 0, None, "#f0f0f0", None, "#006cc1", 25)
                show_input.obj.configure(cursor="hand2")

                def toggle_password_visibility(entry):
                    entry["show"] = "" if not self.show_password else "*"
                    self.show_password = not self.show_password

                heading.grid(row=0, column=0, column_span=2)
                fname_label.grid(row=1, column=0)
                fname_entry.grid(row=1, column=1)
                lname_label.grid(row=2, column=0)
                lname_entry.grid(row=2, column=1)
                dob_label.grid(row=3, column=0)
                dob_entry.grid(row=3, column=1)
                day_entry.grid(row=3, column=0)
                month_entry.grid(row=3, column=1)
                year_entry.grid(row=3, column=2)
                city_label.grid(row=4, column=0)
                city_entry.grid(row=4, column=1)
                country_label.grid(row=5, column=0)
                country_entry.grid(row=5, column=1)
                user_id_label.grid(row=6, column=0)
                user_id_entry.grid(row=6, column=1)
                password_label.grid(row=7, column=0)
                password_input.grid(row=7, column=1)
                show_input.obj.grid(row=7, column=2, padx=5)

                confirm = Button(frame, text="Confirm", padding=5, width=15)
                confirm.bind_function(lambda: _())
                toplevel.obj.bind("<Return>", func=lambda x: _())
                cancel = Button(frame, text="Cancel", padding=5, width=15)
                cancel.bind_function(lambda: toplevel.obj.destroy())

                confirm.obj.grid(row=8, column=0)
                cancel.obj.grid(row=8, column=1)

                def _():
                    try:
                        fname, lname = fname_entry.get(), lname_entry.get()
                        if fname == "" or lname == "":
                            raise Empty
                    except Empty:
                        mb.showerror("Forgetting something?", "What's the name of the customer?", parent=toplevel.obj)
                        account_type.focus()
                        return

                    user_id = self.check_customer(user_id_entry.get(), toplevel.obj)
                    user_password = password_input.get()
                    customer = self.data.find(user_id)
                    if user_id == -1:
                        user_id_entry.focus()
                        return
                    if customer or customer is not None:
                        mb.showerror("Already exists", "This customer is already registered", parent=toplevel.obj)
                        user_id_entry.focus()
                        return
                    if len(user_password) < 4 or len(user_password) > 20:
                        mb.showerror("Invalid password length", "Password must be within 4-20 characters.", parent=toplevel.obj)
                        password_input.focus()
                        return

                    # dob = dob_entry.get().split('/')
                    day, month, year = int(day_entry.get()), int(month_entry.get()), int(year_entry.get())
                    if day < 1 or day > 31:
                        mb.showerror("Invalid day value", "Day must be between 1-31", parent=toplevel.obj)
                        day_entry.focus()
                        return
                    if month < 1 or month > 12:
                        mb.showerror("Invalid month value", "month must be between 1-31", parent=toplevel.obj)
                        month_entry.focus()
                        return
                    if year < 1 or year > 2009:
                        mb.showerror("Invalid year value", "year must be between 1925-2009", parent=toplevel.obj)
                        year_entry.focus()
                        return

                    city = city_entry.get()
                    country = country_entry.get()

                    customer = self.data.add_customer(fname, lname, day, month, year, city, country, user_id, user_password)
                    self.set_active_customer(customer)
                    playsound("SUCCESS")
                    mb.showinfo("Success!", f"New customer '{user_id}' added!", parent=toplevel.obj)
                    self.log_entry("NEW CUSTOMER", f"CUSTOMER: {user_id}")
                    print(customer)
                    toplevel.obj.destroy()

            case "SELECT_CUSTOMER":
                if self.data.count() < 1:
                    mb.showerror("No data", "You can't select an account from thin air", self.root.obj)
                    return
                playsound("BEEP")
                toplevel = Window(400, 250, "Select customer", toplevel=True)
                toplevel.obj.configure(bg="#795757")
                toplevel.set_icon('assets/icon.ico')
                toplevel.obj.grab_set()

                frame = ttk.Frame(toplevel.obj, padding=15)

                heading = Label(frame, "Select customer", "Product Sans", 20, 0)

                id_label = Label(frame, "Customer ID", font="Trebuchet MS", font_size=10, padding=0)
                id_entry = ttk.Entry(frame)
                id_entry.focus()
                customer_id: str

                password_label = Label(frame, "Customer password", font="Trebuchet MS", font_size=10, padding=10)
                password_input = ttk.Entry(frame, show="*")
                account_password: str
                show_input = ToggleButton(frame, "", "", "visdark", lambda: toggle_password_visibility(password_input), "novisdark", 40, 0, None, "#f0f0f0", None, "#006cc1", 25)
                show_input.obj.configure(cursor="hand2")

                def toggle_password_visibility(entry):
                    entry["show"] = "" if not self.show_password else "*"
                    self.show_password = not self.show_password

                confirm: Button = Button(frame, text="Set", padding=5, width=15)
                cancel: Button = Button(frame, text="Cancel", padding=5, width=15)

                confirm.bind_function(lambda: _(self.data))
                toplevel.obj.bind("<Return>", func=lambda x: _(self.data))
                cancel.bind_function(lambda: toplevel.obj.destroy())

                def _(bank):
                    customer_id = self.check_customer(id_entry.get(), toplevel.obj)
                    customer_password = password_input.get()
                    if customer_id == -1:
                        account_input.focus()
                        return
                    customer: Customer = bank.find(customer_id)

                    if customer is None:
                        mb.showerror("Not found", f"Could not find customer {customer_id}", parent=toplevel.obj)
                        id_entry.focus()
                        return
                    if customer.password != customer_password:
                        mb.showerror("Invalid credentials", "Customer ID or password is incorrect", parent=toplevel.obj)
                        password_input.focus()
                        return

                    self.clear_active_account()
                    self.set_active_customer(customer)
                    playsound("SUCCESS")
                    mb.showinfo("Set active",
                                f"Customer {customer_id} has been set as the active customer for all operations onwards!", parent=toplevel.obj)
                    self.log_entry("SET ACTIVE", f"CUSTOMER: {customer_id}")
                    toplevel.obj.destroy()
                    return

                frame.place(relx=0.5, rely=0.5, anchor='center')
                heading.grid(row=0, column=0, column_span=2)
                id_label.obj.grid(row=1, column=0)
                id_entry.grid(row=1, column=1)
                password_label.grid(row=2, column=0)
                password_input.grid(row=2, column=1)
                show_input.obj.grid(row=2, column=2, padx=2)
                confirm.obj.grid(row=3, column=0)
                cancel.obj.grid(row=3, column=1)

            case "VIEW_CUSTOMER":
                try:
                    customer = self.active_customer
                    if customer is None or not customer:
                        raise NotFound
                except NotFound or AttributeError:
                    mb.showerror("Forgetting something?", "Did you forget to select a customer?", parent=self.root.obj)
                    return
                playsound("BEEP")
                toplevel = Window(300, 250, f"Viewing customer '{customer.user_id}'", toplevel=True)
                toplevel.set_icon('assets/icon.ico')
                toplevel.obj.configure(bg="#795757")
                toplevel.obj.grab_set()
                frame = ttk.Frame(toplevel.obj, padding=15)

                title = Label(frame, "Account details", "Product Sans", 20)

                details = {
                    "ID:": customer.user_id,
                    "Name:": f"{customer.name["fn"]} {customer.name["ln"]}",
                    "DOB:": f"{customer.dob["day"]}/{customer.dob["month"]}/{customer.dob["year"]}",
                    "Location:": f"{customer.location["city"]} {customer.location["country"]}",
                }

                _ = 1
                for key, value in details.items():
                    Label(frame, text=key, font="Product Sans", font_size=12).grid(row=_, column=0)
                    Label(frame, text=value, font="Product Sans", font_size=12).grid(row=_, column=1)
                    _ += 1

                exit_button = Button(frame, text="Close", padding=5, width=20)
                exit_button.bind_function(lambda: toplevel.obj.destroy())
                toplevel.obj.bind("<Return>", func=lambda x: toplevel.obj.destroy())
                exit_button.obj.focus()

                self.log_entry("CUSTOMER ACCESSED", f"CUSTOMER: {customer.user_id}")

                frame.place(relx=0.5, rely=0.5, anchor='center')
                title.grid(row=0, column_span=2)
                exit_button.obj.grid(row=5, pady=5, columnspan=2)

            case "EDIT_CUSTOMER":
                try:
                    customer = self.active_customer
                    if customer is None or not customer:
                        raise NotFound
                except NotFound or AttributeError:
                    mb.showerror("Forgetting something?", "Did you forget to select a customer?", parent=self.root.obj)
                    return

                playsound("BEEP")
                toplevel = Window(400, 250, "Edit customer", toplevel=True)
                toplevel.set_icon('assets/icon.ico')
                toplevel.obj.configure(bg="#795757")

                frame = ttk.Frame(toplevel.obj, padding=10)
                frame.place(relx=0.5, rely=0.5, anchor="center")

                title = Label(frame, "Edit customer", "Product Sans", 20)
                title.grid(row=0, column=0, column_span=2)

                selector_label = Label(frame, "Select a value:", font="Trebuchet MS", font_size=10, padding=5)
                selector_label.grid(row=1, column=0)

                attribute_selector = ttk.Combobox(frame, values=[
                    "First name",
                    "Last name",
                    "Date of birth",
                    "Country",
                    "City",
                ], state="readonly")
                attribute_selector.bind("<<ComboboxSelected>>", lambda selection: update_inputs())
                attribute_selector.grid(row=1, column=1)
                attribute_selector.focus()

                new_val_label = Label(frame, "New value:", font="Trebuchet MS", font_size=10, padding=5)
                new_val_label.grid(row=2, column=0)

                new_val = ttk.Entry(frame)
                new_val.grid(row=2, column=1)

                dob_entry = ttk.Labelframe(frame, text="Day, month, year")
                day_entry = ttk.Entry(dob_entry, width=4)
                month_entry = ttk.Entry(dob_entry, width=4)
                year_entry = ttk.Entry(dob_entry, width=4)

                dob_entry.grid(row=3, column=1)
                day_entry.grid(row=0, column=1)
                month_entry.grid(row=0, column=2)
                year_entry.grid(row=0, column=3)

                confirm = Button(frame, text="Confirm", padding=5, width=15)
                confirm.bind_function(lambda: edit(attribute_selector, new_val))
                toplevel.obj.bind("<Return>", func=lambda x: edit(attribute_selector, new_val))
                cancel = Button(frame, text="Cancel", padding=5, width=15)
                cancel.bind_function(lambda: toplevel.obj.destroy())

                confirm.obj.grid(row=4, column=0)
                cancel.obj.grid(row=4, column=1)

                def update_inputs():
                    if attribute_selector.get() == "Date of birth":
                        new_val.configure(state='disabled')
                        # dob_entry = ttk.Labelframe(value_frame, text="Day, month, year")
                        # day_entry = ttk.Entry(dob_entry, width=4)
                        # month_entry = ttk.Entry(dob_entry, width=4)
                        # year_entry = ttk.Entry(dob_entry, width=4)
                        # dob_entry.grid(row=2, column=1)
                        # day_entry.grid(row=0, column=1)
                        # month_entry.grid(row=0, column=2)
                        # year_entry.grid(row=0, column=3)
                        day_entry.configure(state="enabled")
                        month_entry.configure(state="enabled")
                        year_entry.configure(state="enabled")
                    else:
                        # new_val = ttk.Entry(value_frame)
                        # new_val.grid(row=2, column=1)
                        day_entry.configure(state="disabled")
                        month_entry.configure(state="disabled")
                        year_entry.configure(state="disabled")
                        new_val.configure(state="enabled")

                def edit(combobox, entry):
                    selection = combobox.get()
                    value = entry.get()
                    match selection:
                        case "First name":
                            if len(value) > 15 or len(value) < 2:
                                mb.showerror("Invalid length", "Name must be between 2-15 characters", toplevel.obj)
                                return
                            self.active_customer.edit_info(first_name=value)

                        case "Last name":
                            if len(value) > 15 or len(value) < 2:
                                mb.showerror("Invalid length", "Name must be between 2-15 characters", toplevel.obj)
                                return
                            self.active_customer.edit_info(last_name=value)

                        case "Date of birth":
                            day, month, year = int(day_entry.get()), int(month_entry.get()), int(year_entry.get())
                            value = f"{day}/{month}/{year}"
                            if day < 1 or day > 31:
                                mb.showerror("Invalid day value", "Day must be between 1-31", parent=toplevel.obj)
                                day_entry.focus()
                                return
                            if month < 1 or month > 12:
                                mb.showerror("Invalid month value", "month must be between 1-31", parent=toplevel.obj)
                                month_entry.focus()
                                return
                            if year < 1 or year > 2009:
                                mb.showerror("Invalid year value", "year must be between 1925-2009", parent=toplevel.obj)
                                year_entry.focus()
                                return
                            self.active_customer.edit_info(birth_day=day, birth_month=month, birth_year=year)

                        case "Country":
                            if len(value) > 15 or len(value) < 2:
                                mb.showerror("Invalid length", "Country must be between 2-15 characters", toplevel.obj)
                                return
                            self.active_customer.edit_info(country=value)

                        case "City":
                            if len(value) > 15 or len(value) < 2:
                                mb.showerror("Invalid length", "City must be between 2-15 characters", toplevel.obj)
                                return
                            self.active_customer.edit_info(city=value)

                    self.log_entry("CUSTOMER MODIFIED", f"SET {selection.upper()} TO {value}")
                    mb.showinfo("Success", f"Successfully set {selection.lower()} to {value}", toplevel.obj)
                    toplevel.obj.destroy()

            case "TERMINATE_CUSTOMER":
                try:
                    customer = self.active_customer
                    if customer is None or not customer:
                        raise NotFound
                except NotFound or AttributeError:
                    mb.showerror("Forgetting something?", "Did you forget to select a customer?", parent=self.root.obj)
                    return

                resp = mb.askyesno("Confirmation", f"Are you sure you would like to delete customer '{customer.name["fn"]}'?", self.root.obj)
                if not resp:
                    return
                attempt = self.data.terminate_customer(customer.user_id, customer.password)
                self.log_entry("CUSTOMER TERMINATED", f"CUSTOMER: {customer.user_id}")
                if attempt == -1:
                    mb.showerror("Huston, we have a problem", "Something went wrong on our end", self.root.obj)
                    return

                self.clear_active_customer()
                self.clear_active_account()
                mb.showinfo("Done and dusted", "Customer terminated successfully", self.root.obj)

            case "CUSTOMER_REGISTRY":
                if self.data.count() < 1:
                    mb.showerror("Nuh uh", "No customers registered", parent=self.root.obj)
                    return

                playsound("BEEP")
                toplevel = Window(700, 500, "Customers registered", toplevel=True)
                toplevel.set_icon('assets/icon.ico')
                toplevel.obj.configure(bg="#795757")
                toplevel.obj.grab_set()

                frame = ttk.Frame(toplevel.obj, padding=20)
                frame.grid(row=0, column=0)

                canvas = tk.Canvas(frame)
                canvas.configure(width=toplevel.width - 40, height=toplevel.height - 40)
                scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
                canvas.configure(yscrollcommand=scrollbar.set)

                content_frame = ttk.Frame(canvas)
                content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

                heading = Label(content_frame, "Customer registry", "Product Sans", 20, padding=5)
                heading.grid(row=0, column=0, column_span=6)

                header1 = ttk.Label(content_frame, text="ID", width=12, font=("Product Sans", 12),
                                    background="#333333", foreground="#ffffff")
                header2 = ttk.Label(content_frame, text="Name", width=18, font=("Product Sans", 12),
                                    background="#333333", foreground="#ffffff")
                header3 = ttk.Label(content_frame, text="D.O.B.", width=8, font=("Product Sans", 12),
                                    background="#333333", foreground="#ffffff")
                header4 = ttk.Label(content_frame, text="City", width=10, font=("Product Sans", 12),
                                    background="#333333", foreground="#ffffff")
                header5 = ttk.Label(content_frame, text="Country", width=10, font=("Product Sans", 12),
                                    background="#333333", foreground="#ffffff")
                header6 = ttk.Label(content_frame, text="", width=5, font=("Product Sans", 12),
                                    background="#333333", foreground="#ffffff")

                header1.grid(row=1, column=0)
                header2.grid(row=1, column=1)
                header3.grid(row=1, column=2)
                header4.grid(row=1, column=3)
                header5.grid(row=1, column=4)
                header6.grid(row=1, column=5)

                for i, customer in enumerate(self.data.customers):
                    i += 2

                    customer_id: Label = ttk.Label(content_frame, text=customer.user_id, width=12, font=("Product Sans", 12),
                                                   background="#A39793" if i % 2 == 0 else "#ffffff")
                    name = ttk.Label(content_frame,
                                     text=f"{customer.name["fn"]} {customer.name["ln"]}",
                                     width=18, font=("Product Sans", 12),
                                     background="#A39793" if i % 2 == 0 else "#ffffff")
                    dob = ttk.Label(content_frame, text=f"{customer.dob["day"]}/{customer.dob["month"]}/{customer.dob["year"]}", width=8,
                                    font=("Product Sans", 12),
                                    background="#A39793" if i % 2 == 0 else "#ffffff")
                    city = ttk.Label(content_frame,
                                     text=customer.location["city"],
                                     width=10, font=("Product Sans", 12),
                                     background="#A39793" if i % 2 == 0 else "#ffffff")
                    country = ttk.Label(content_frame,
                                        text=customer.location["country"],
                                        width=10, font=("Product Sans", 12),
                                        background="#A39793" if i % 2 == 0 else "#ffffff")
                    set_button = ttk.Button(content_frame, text="Select", width=5, padding=2,
                                            command=lambda: set_active())

                    def set_active():
                        self.button_handler("SELECT_CUSTOMER")

                    customer_id.grid(row=i, column=0)
                    name.grid(row=i, column=1)
                    dob.grid(row=i, column=2)
                    city.grid(row=i, column=3)
                    country.grid(row=i, column=4)
                    set_button.grid(row=i, column=5)

                self.log_entry("VIEW", f"DATABASE ACCESSED")

                canvas.create_window((0, 0), window=content_frame, anchor="nw")
                canvas.grid(row=0, column=0)
                scrollbar.grid(row=0, column=1, sticky="ns")
                toplevel.obj.focus()

                def _on_mousewheel(event):
                    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

                canvas.bind_all("<MouseWheel>", _on_mousewheel)

            case "CLEAR_ACCOUNTS":
                try:
                    customer = self.active_customer
                    if customer is None or not customer:
                        raise NotFound
                except NotFound or AttributeError:
                    mb.showerror("Forgetting something?", "Did you forget to select a customer?", parent=self.root.obj)
                    return
                if customer.count() < 1:
                    mb.showinfo("Already empty", "No customers registered", parent=self.root.obj)
                    return

                resp = mb.askyesno("Confirm", f"This will terminate all accounts associated with {customer.user_id}", detail="Please confirm twice", parent=self.root.obj)
                if not resp:
                    return
                resp = mb.askyesno("Confirm", f"This will terminate all accounts associated with {customer.user_id}", self.root.obj)
                if not resp:
                    return
                customer.clear_accounts()
                self.clear_active_account()
                mb.showinfo("Success", f"Cleared all accounts for {customer.user_id}", parent=self.root.obj)

            case "SET":
                try:
                    customer = self.active_customer
                    if customer is None or not customer:
                        raise NotFound
                except NotFound or AttributeError:
                    mb.showerror("Forgetting something?", "Did you forget to select a customer?", parent=self.root.obj)
                    return

                playsound("BEEP")
                toplevel = Window(400, 250, "Set active account", toplevel=True)
                toplevel.obj.configure(bg="#795757")
                toplevel.set_icon('assets/icon.ico')
                toplevel.obj.grab_set()

                frame = ttk.Frame(toplevel.obj, padding=15)

                heading = Label(frame, "Select account", "Product Sans", 20, 0)

                number_label = Label(frame, "Account number", font="Trebuchet MS", font_size=10, padding=0)
                account_input = ttk.Entry(frame)
                account_input.focus()
                account_number: str

                password_label = Label(frame, "Account password", font="Trebuchet MS", font_size=10, padding=10)
                password_input = ttk.Entry(frame, show="*")
                account_password: str
                show_input = ToggleButton(frame, "", "", "visdark", lambda: toggle_password_visibility(password_input), "novisdark", 40, 0, None, "#f0f0f0", None, "#006cc1", 25)
                show_input.obj.configure(cursor="hand2")

                def toggle_password_visibility(entry):
                    entry["show"] = "" if not self.show_password else "*"
                    self.show_password = not self.show_password

                confirm: Button = Button(frame, text="Set", padding=5, width=15)
                cancel: Button = Button(frame, text="Cancel", padding=5, width=15)

                confirm.bind_function(lambda: _(account_input))
                toplevel.obj.bind("<Return>", func=lambda x: _(account_input))
                cancel.bind_function(lambda: toplevel.obj.destroy())

                def _(acc_in):
                    account_number = self.check_account(acc_in.get(), toplevel.obj)
                    account_password = password_input.get()
                    if account_number == -1:
                        account_input.focus()
                        return
                    account = customer.find_account(account_number)

                    if account is None:
                        mb.showerror("Not found", f"Could not find account {account_number}", parent=toplevel.obj)
                        account_input.focus()
                        return
                    if account.account_password != account_password:
                        mb.showerror("Invalid credentials", "Password is incorrect", parent=toplevel.obj)
                        password_input.focus()
                        return

                    self.set_active_account(account)
                    playsound("SUCCESS")
                    mb.showinfo("Set active",
                                f"Account {account_number} has been set as the active account for all operations onwards!", parent=toplevel.obj)
                    self.log_entry("SET ACTIVE", f"ACCOUNT: {account_number}")
                    toplevel.obj.destroy()
                    return

                frame.place(relx=0.5, rely=0.5, anchor='center')
                heading.grid(row=0, column=0, column_span=2)
                number_label.obj.grid(row=1, column=0)
                account_input.grid(row=1, column=1)
                password_label.grid(row=2, column=0)
                password_input.grid(row=2, column=1)
                show_input.obj.grid(row=2, column=2, padx=5)
                confirm.obj.grid(row=3, column=0)
                cancel.obj.grid(row=3, column=1)

            case "NEW":
                try:
                    customer = self.active_customer
                    if customer is None or not customer:
                        raise NotFound
                except NotFound or AttributeError:
                    mb.showerror("Forgetting something?", "Did you forget to select a customer?", parent=self.root.obj)
                    return

                playsound("BEEP")
                toplevel = Window(400, 300, "Set active account", toplevel=True)
                toplevel.set_icon('assets/icon.ico')
                toplevel.obj.configure(bg="#795757")
                toplevel.obj.grab_set()

                frame = ttk.Frame(toplevel.obj, padding=15)

                heading = Label(frame, "New account", "Product Sans", 20, padding=5)

                type_label = Label(frame, text="Account type: ", font="Trebuchet MS", font_size=10, padding=5)
                account_type = ttk.Combobox(frame, values=["Checking", "Savings"], state="readonly")
                account_type.focus()

                number_label = Label(frame, text="Account number: ", font="Trebuchet MS", font_size=10, padding=5)
                number_entry = ttk.Entry(frame)

                password_label = Label(frame, "Account password:", font="Trebuchet MS", font_size=10, padding=5)
                password_input = ttk.Entry(frame, show="*")
                account_password: str
                show_input = ToggleButton(frame, "", "", "visdark", lambda: toggle_password_visibility(password_input), "novisdark", 40, 0, None, "#f0f0f0", None, "#006cc1", 25)
                show_input.obj.configure(cursor="hand2")

                def toggle_password_visibility(entry):
                    entry["show"] = "" if not self.show_password else "*"
                    self.show_password = not self.show_password

                balance_label = Label(frame, text="Initial balance: ", font="Trebuchet MS", font_size=10, padding=5)
                initial_balance = ttk.Entry(frame)

                interest_label = Label(frame, text="Interest rate: ", font="Trebuchet MS", font_size=10, padding=5)
                interest_rate = ttk.Entry(frame)

                confirm = Button(frame, text="Confirm", padding=5, width=15)
                confirm.bind_function(lambda: _())
                toplevel.obj.bind("<Return>", func=lambda x: _())
                cancel = Button(frame, text="Cancel", padding=5, width=15)
                cancel.bind_function(lambda: toplevel.obj.destroy())

                def _():
                    try:
                        acc_type = account_type.get()
                        if acc_type is None or acc_type == "":
                            raise Empty
                    except Empty:
                        mb.showerror("Forgetting something?", "What kind of account are you creating?", parent=toplevel.obj)
                        account_type.focus()
                        return

                    account_number = self.check_account(number_entry.get(), toplevel.obj)
                    account_password = password_input.get()
                    customer_account = customer.find_account(account_number)
                    if account_number == -1:
                        number_entry.focus()
                        return
                    if customer_account or customer_account is not None:
                        mb.showerror("Already exists", "This account is already registered under this customer", parent=toplevel.obj)
                        number_entry.focus()
                        return
                    if len(account_password) < 4 or len(account_password) > 20:
                        mb.showerror("Invalid password length", "Password must be within 4-20 characters.", parent=toplevel.obj)
                        password_input.focus()
                        return

                    balance = self.check_value(initial_balance.get(), toplevel.obj)
                    if balance == -1:
                        initial_balance.focus()
                        return

                    if acc_type == "Savings":
                        int_rate = self.check_value(interest_rate.get(), toplevel.obj)
                        if int_rate == -1:
                            interest_rate.focus()
                            return
                    else:
                        int_rate = 0

                    account = self.active_customer.add_account(acc_type, account_number, account_password, balance, int_rate)
                    self.set_active_account(account)
                    playsound("SUCCESS")
                    mb.showinfo("Success!", f"New account '{account_number}' added to customer {customer.name["fn"]}!", parent=toplevel.obj)
                    self.log_entry("NEW ACCOUNT", f"ACCOUNT: {account_number}, TYPE: {acc_type}, CUSTOMER: {customer.user_id}")
                    toplevel.obj.destroy()

                confirm.obj.grid(row=6, column=0)
                cancel.obj.grid(row=6, column=1)
                interest_label.obj.grid(row=5, column=0)
                interest_rate.grid(row=5, column=1)
                balance_label.obj.grid(row=4, column=0)
                initial_balance.grid(row=4, column=1)
                password_label.obj.grid(row=3, column=0)
                password_input.grid(row=3, column=1)
                show_input.obj.grid(row=3, column=2, padx=5)
                number_label.obj.grid(row=2, column=0)
                number_entry.grid(row=2, column=1)
                type_label.grid(row=1, column=0)
                account_type.grid(row=1, column=1)
                frame.place(relx=0.5, rely=0.5, anchor='center')
                heading.grid(row=0, column=0, column_span=2)

            case "DELETE":
                try:
                    customer = self.active_customer
                    if customer is None or not customer:
                        raise NotFound
                except NotFound or AttributeError:
                    mb.showerror("Forgetting something?", "Did you forget to select a customer?", parent=self.root.obj)
                    return

                try:
                    resp = mb.askyesno("Confirm deletion",
                                       f"Are you sure you would like to delete account '{self.active_account.account_number}'?", parent=self.root.obj)
                except NameError and AttributeError and AttributeError:
                    mb.showerror("Forgetting something?", "Did you forget to set an active account?", parent=self.root.obj)
                    return

                if resp:
                    attempt = customer.delete_account(self.active_account.account_number, self.active_account.account_password)
                    if attempt != 0:
                        mb.showerror("Aw phooey",
                                     "An error occurred while attempting to delete that account.", parent=self.root.obj)
                    mb.showinfo("Sucks to suck",
                                f"Account {self.active_account.account_number} has been deleted successfully!", parent=self.root.obj)
                    self.log_entry("TERMINATE", f"ACCOUNT: {self.active_account.account_number}")
                    self.clear_active_account()

            case "DISPLAY":
                try:
                    customer = self.active_customer
                    if customer is None or not customer:
                        raise NotFound
                except NotFound or AttributeError:
                    mb.showerror("Forgetting something?", "Did you forget to select a customer?", parent=self.root.obj)
                    return

                if customer.count() < 1:
                    mb.showinfo("Nuh uh", "No accounts to display", parent=self.root.obj)
                    return

                playsound("BEEP")
                toplevel = Window(750, 500, "Accounts registered", toplevel=True)
                toplevel.set_icon('assets/icon.ico')
                toplevel.obj.configure(bg="#795757")
                toplevel.obj.grab_set()

                frame = ttk.Frame(toplevel.obj, padding=20)
                frame.grid(row=0, column=0)

                canvas = tk.Canvas(frame)
                canvas.configure(width=toplevel.width - 40, height=toplevel.height - 40)
                scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
                canvas.configure(yscrollcommand=scrollbar.set)

                content_frame = ttk.Frame(canvas)
                content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

                heading = Label(content_frame, "Account registry", "Product Sans", 20, padding=5)
                heading.grid(row=0, column=0, column_span=6)

                header1 = ttk.Label(content_frame, text="Index", width=12, font=("Product Sans", 12),
                                    background="#333333", foreground="#ffffff")
                header2 = ttk.Label(content_frame, text="Account type", width=12, font=("Product Sans", 12),
                                    background="#333333", foreground="#ffffff")
                header3 = ttk.Label(content_frame, text="Account number", width=18, font=("Product Sans", 12),
                                    background="#333333", foreground="#ffffff")
                header4 = ttk.Label(content_frame, text="Balance", width=12, font=("Product Sans", 12),
                                    background="#333333", foreground="#ffffff")
                header5 = ttk.Label(content_frame, text="Interest", width=8, font=("Product Sans", 12),
                                    background="#333333", foreground="#ffffff")
                header6 = ttk.Label(content_frame, text="", width=5, font=("Product Sans", 12),
                                    background="#333333", foreground="#ffffff")

                header1.grid(row=1, column=0)
                header2.grid(row=1, column=1)
                header3.grid(row=1, column=2)
                header4.grid(row=1, column=3)
                header5.grid(row=1, column=4)
                header6.grid(row=1, column=5)

                for i, account in enumerate(customer.accounts):
                    i += 2

                    index = ttk.Label(content_frame,
                                      text=i - 1,
                                      width=12, font=("Product Sans", 12),
                                      background="#DDDDDD" if i % 2 == 0 else "#ffffff")
                    acc_type = ttk.Label(content_frame,
                                         text="Checking" if type(account) is CheckingAccount else "Savings",
                                         width=12, font=("Product Sans", 12),
                                         background="#DDDDDD" if i % 2 == 0 else "#ffffff")
                    acc_num = ttk.Label(content_frame, text=account.account_number, width=18, font=("Product Sans", 12),
                                        background="#DDDDDD" if i % 2 == 0 else "#ffffff")
                    balance = ttk.Label(content_frame, text=f"${account.balance:,}", width=12,
                                        font=("Product Sans", 12),
                                        background="#DDDDDD" if i % 2 == 0 else "#ffffff")
                    int_rate = ttk.Label(content_frame,
                                         text=f"{account.interest_rate}%" if type(account) is SavingsAccount else "",
                                         width=8, font=("Product Sans", 12),
                                         background="#DDDDDD" if i % 2 == 0 else "#ffffff")
                    set_button = ttk.Button(content_frame, text="Set", width=5, padding=2,
                                            command=lambda x=account: set_active())

                    def set_active():
                        self.button_handler("SET")

                    index.grid(row=i, column=0)
                    acc_type.grid(row=i, column=1)
                    acc_num.grid(row=i, column=2)
                    balance.grid(row=i, column=3)
                    int_rate.grid(row=i, column=4)
                    set_button.grid(row=i, column=5)

                self.log_entry("VIEW", f"DATABASE ACCESSED")

                canvas.create_window((0, 0), window=content_frame, anchor="nw")
                canvas.grid(row=0, column=0)
                scrollbar.grid(row=0, column=1, sticky="ns")
                toplevel.obj.focus()

                def _on_mousewheel(event):
                    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

                canvas.bind_all("<MouseWheel>", _on_mousewheel)

            case "DEPOSIT":
                try:
                    account_number: int = self.active_account.account_number
                except NameError and AttributeError:
                    mb.showerror("Forgetting something?", "Did you forget to set an active account?", parent=self.root.obj)
                    return

                playsound("BEEP")
                toplevel = Window(300, 200, "Deposit", toplevel=True)
                toplevel.set_icon('assets/icon.ico')
                toplevel.obj.configure(bg="#795757")
                toplevel.obj.grab_set()

                frame = ttk.Frame(toplevel.obj, padding=15)

                heading = Label(frame, "Deposit", "Product Sans", 20, 5)

                number_label = ttk.Label(frame, text="Amount: ", font=("Trebuchet MS", 10))
                amount_entry = ttk.Entry(frame)
                amount_entry.focus()

                def _():
                    amount = self.check_value(amount_entry.get(), toplevel.obj)
                    if amount == -1:
                        amount_entry.focus()
                        return
                    self.active_account.deposit(amount)
                    mb.showinfo("Success!", f"Deposited ${amount:,} to account '{account_number}' successfully", parent=toplevel.obj)
                    self.log_entry("DEPOSIT",
                                   f"ACCOUNT: {self.active_account.account_number}, BEFORE: {self.active_account.balance - amount}, AFTER: {self.active_account.balance}")
                    toplevel.obj.destroy()

                confirm = Button(frame, text="Deposit", padding=5, width=15)
                confirm.bind_function(_)
                toplevel.obj.bind("<Return>", func=lambda x: _())
                cancel = Button(frame, text="Cancel", padding=5, width=15)
                cancel.bind_function(lambda: toplevel.obj.destroy())

                frame.place(relx=0.5, rely=0.5, anchor='center')
                heading.grid(row=0, column=0, column_span=2)
                number_label.grid(row=1, column=0)
                amount_entry.grid(row=1, column=1)
                confirm.obj.grid(row=2, column=0, pady=5)
                cancel.obj.grid(row=2, column=1, pady=5)

            case "WITHDRAW":
                try:
                    account_number: int = self.active_account.account_number
                except NameError and AttributeError:
                    mb.showerror("Forgetting something?", "Did you forget to set an active account?", parent=self.root.obj)
                    return

                playsound("BEEP")
                toplevel = Window(300, 200, "Withdraw", toplevel=True)
                toplevel.set_icon('assets/icon.ico')
                toplevel.obj.configure(bg="#795757")
                toplevel.obj.grab_set()

                frame = ttk.Frame(toplevel.obj, padding=15)

                heading = Label(frame, "Withdraw", "Product Sans", 20, 5)

                number_label = ttk.Label(frame, text="Amount: ", font=("Trebuchet MS", 10))
                amount_entry = ttk.Entry(frame)
                amount_entry.focus()

                def _():
                    amount = self.check_value(amount_entry.get(), toplevel.obj)
                    if amount == -1:
                        amount_entry.focus()
                        return
                    if amount > self.active_account.balance:
                        mb.showerror("Poor", "You cannot afford this transaction", parent=toplevel.obj)
                        amount_entry.focus()
                        return
                    self.active_account.withdraw(amount)
                    mb.showinfo("Success!", f"Withdrew ${amount:,} from account '{account_number}' successfully", parent=toplevel.obj)
                    self.log_entry("WITHDRAW",
                                   f"ACCOUNT: {self.active_account.account_number}, BEFORE: {self.active_account.balance + amount}, AFTER: {self.active_account.balance}")
                    toplevel.obj.destroy()

                confirm = Button(frame, text="Withdraw", padding=5, width=15)
                confirm.bind_function(_)
                toplevel.obj.bind("<Return>", func=lambda x: _())
                cancel = Button(frame, text="Cancel", padding=5, width=15)
                cancel.bind_function(lambda: toplevel.obj.destroy())

                frame.place(relx=0.5, rely=0.5, anchor='center')
                heading.grid(row=0, column=0, column_span=2)
                number_label.grid(row=1, column=0)
                amount_entry.grid(row=1, column=1)
                confirm.obj.grid(row=2, column=0, pady=5)
                cancel.obj.grid(row=2, column=1, pady=5)

            case "LOG":
                self.log_entry("LOG ACCESS", f"LOG ACCESSED")
                playsound("BEEP")

                toplevel = Window(650, 550, "Operations log", toplevel=True, resizable=True)
                toplevel.set_icon('assets/icon.ico')
                toplevel.obj.configure(bg="#795757")
                toplevel.obj.grab_set()
                toplevel.obj.focus()

                frame = ttk.Frame(toplevel.obj, padding=15)
                frame.place(relx=0.5, rely=0.5, anchor='center')

                heading = Label(frame, "Operations log", "Product Sans", 20, 5)
                heading.pack()

                log_text = ''
                for key, value in self.log.items():
                    log_text += f"{key}: {value}\n"
                logbox = Label(frame, text=log_text, font="Consolas", font_size=10)
                logbox.pack()

            case "VIEW":
                try:
                    account_number: int = self.active_account.account_number
                except NameError and AttributeError:
                    mb.showerror("Forgetting something?", "Did you forget to set an active account?", parent=self.root.obj)
                    return

                playsound("BEEP")
                toplevel = Window(300, 250, f"Viewing account '{account_number}'", toplevel=True)
                toplevel.set_icon('assets/icon.ico')
                toplevel.obj.configure(bg="#795757")
                toplevel.obj.grab_set()
                frame = ttk.Frame(toplevel.obj, padding=15)

                title = Label(frame, "Account details", "Product Sans", 20)

                details = {
                    "Account number:": account_number,
                    "Account type:": "Checking" if type(self.active_account) is CheckingAccount else "Savings",
                    "Balance:": f"${self.active_account.get_balance():,}",
                    "Interest:": str(self.active_account.interest_rate) + "%" if type(
                        self.active_account) is SavingsAccount else "No interest"
                }

                _ = 1
                for key, value in details.items():
                    Label(frame, text=key, font="Product Sans", font_size=12).grid(row=_, column=0)
                    Label(frame, text=value, font="Product Sans", font_size=12).grid(row=_, column=1)
                    _ += 1

                exit_button = Button(frame, text="Close", padding=5, width=20)
                exit_button.bind_function(lambda: toplevel.obj.destroy())
                toplevel.obj.bind("<Return>", func=lambda x: toplevel.obj.destroy())
                exit_button.obj.focus()

                self.log_entry("ACCOUNT ACCESSED", f"ACCOUNT: {account_number}")

                frame.place(relx=0.5, rely=0.5, anchor='center')
                title.grid(row=0, column_span=2)
                exit_button.obj.grid(row=5, pady=5, columnspan=2)

            case "INTEREST":
                try:
                    account_number: int = self.active_account.account_number
                except NameError and AttributeError:
                    mb.showerror("Forgetting something?", "Did you forget to set an active account?", parent=self.root.obj)
                    return
                if type(self.active_account) is not SavingsAccount:
                    mb.showerror("Invalid account type", "Cannot apply interest to checking account", parent=self.root.obj)
                    return
                self.active_account.balance = self.active_account.balance + (
                        self.active_account.balance * self.active_account.interest_rate)
                mb.showinfo("Interest applied", f"Successfully applied {self.active_account.interest_rate}% interest", parent=self.root.obj)
                self.log_entry("INTEREST",
                               f"ACCOUNT: {self.active_account.account_number}, INTEREST: {self.active_account.interest_rate}")

            case "SAVE":
                f = Path("BANK_DATA.txt")
                if self.data.count() < 1:
                    mb.showerror("No data", "No data to save", parent=self.root.obj)
                    self.log_entry("DATA SAVE", f"ATTEMPT TO SAVE TO DISK UNSUCCESSFULLY")
                    return
                resp: bool = False
                if f.is_file():
                    resp = mb.askyesnocancel("Overwrite confirmation", "There is already data on disk\n\n"
                                                                       "Overwrite with current data?\n\n"
                                                                       "Yes to override\n"
                                                                       "No to append to existing\n\n"
                                                                       "Note: already existing accounts will be ignored", parent=self.root.obj)
                    if resp is None:
                        return
                try:
                    self.data.export_data("BANK_DATA.txt", overwrite=resp)
                    mb.showinfo("Export successful", "Data has been saved to disk", parent=self.root.obj)
                    self.log_entry("DATA SAVE", f"DATA WAS SAVED TO DISK")
                except Exception as e:
                    mb.showerror("An error occurred", "Something went wrong", detail=f"Details: {e}", parent=self.root.obj)
                    self.log_entry("DATA SAVE", f"ATTEMPT TO SAVE TO DISK UNSUCCESSFULLY")

            case "LOAD":
                f = Path("BANK_DATA.txt")
                if f.is_file():
                    if f.read_text() == "":
                        mb.showerror("No data", "No data stored on disk", parent=self.root.obj)
                        self.log_entry("DATA LOAD", f"ATTEMPT TO LOAD FROM DISK UNSUCCESSFULLY")
                        return
                    resp: bool = False
                    if self.data.count() > 0:
                        resp = mb.askyesnocancel("Overwrite confirmation", "There is already data in the database\n\n"
                                                                           "Overwrite with data from disk?\n\n"
                                                                           "Yes to override\n"
                                                                           "No to append to existing\n\n"
                                                                           "Note: already existing accounts will be ignored", parent=self.root.obj)
                        if resp is None:
                            return
                    try:
                        self.data.import_data("BANK_DATA.txt", overwrite=resp)
                        self.clear_active_account()
                        self.clear_active_customer()
                        mb.showinfo("Import successful", "Data has been loaded from disk", parent=self.root.obj)
                        self.log_entry("DATA LOAD", f"DATA WAS LOADED FROM DISK")
                    except Exception as e:
                        mb.showerror("An error occurred", f"Something went wrong", detail=f"Details: {e.args[0]}", parent=self.root.obj)
                        self.log_entry("DATA LOAD", f"ATTEMPT TO LOAD FROM DISK UNSUCCESSFULLY")
                else:
                    mb.showerror("No data", "Could not find data to load.", parent=self.root.obj)

            case "CLEAR":
                if self.data.count() < 1:
                    mb.showerror("No data", "Cannot clear an already empty database", parent=self.root.obj)
                    return
                confirm: bool = mb.askokcancel("Danger zone",
                                               "This action is irreversible and will clear ALL data out of "
                                               "the database.\n"
                                               "Please confirm TWICE that you would like to proceed.", parent=self.root.obj)
                if not confirm:
                    return
                resp: bool = mb.askyesno("Danger zone", "Are you really sure you would like to erase"
                                                        "all data from the database?", parent=self.root.obj)
                if not resp:
                    return
                self.clear_active_account()
                self.clear_active_customer()
                self.data.clear_bank()
                mb.showinfo("Peace of mind", "Successfully erased all data from database.", parent=self.root.obj)
                self.log_entry("DATABASE CLEAR", f"DATABASE WAS ERASED")

            case "EXIT":
                resp: str = mb.askquestion("Leaving so soon?", "Are you sure you would like to quit?", parent=self.root.obj)
                if resp == "yes":
                    playsound("GOODBYE")
                    self.root.obj.after(600)
                    self.root.obj.quit()

            case _:
                mb.showerror("Unimplemented", "Coming soon!", self.root.obj)
