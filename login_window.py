from graphics import *
from bank_classes import BankProgram


class Login:
    def __init__(self, root, tellers):
        # Window setup
        self.root = root
        self.root.obj.geometry("650x700")
        self.root.obj.state('normal')
        self.root.obj.title("Mashriq Solutions")
        # self.root.obj.protocol("WM_DELETE_WINDOW", lambda: self.button_handler("EXIT"))
        self.root.set_icon('assets/icon.ico')
        self.tellers = tellers

        bg_image = tk.PhotoImage(file='assets/bg.png')
        bg = tk.Label(self.root.obj, image=bg_image)
        bg.place(relx=0.5, rely=0.5, anchor="center")
        ttk.Style().configure(style='transparent.TFrame', background="#403333")
        self.content_frame = ttk.Frame(self.root.obj, padding=15, style="transparent.TFrame")
        self.content_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Heading
        # title = Label(self.content_frame, "Mashriq Bank", "Product Sans", 40, padding=15)
        logo_image = tk.PhotoImage(file='assets/logo.png').subsample(4)
        title = ttk.Label(self.content_frame, image=logo_image, padding=5, background="#403333")
        # title.obj.configure(foreground="#ffffff", background="#403333")
        title.grid(row=0, column=0, columnspan=3)

        playsound('BOOT')

        user_id_label = Label(self.content_frame, text="Teller ID:", font="Product Sans", font_size=15, background="#403333", foreground="white")
        self.user_id_entry = ttk.Entry(self.content_frame, width=30)
        user_password_label = Label(self.content_frame, text="Teller password:", font="Product Sans", font_size=15, background="#403333", foreground="white")
        self.user_password_entry = ttk.Entry(self.content_frame, show="*", width=30)

        self.show_password = True
        show_input = ToggleButton(self.content_frame, "", "", "vis", lambda: toggle_password_visibility(), "novis", 40, 0, None, "#403333", None, None, 25)
        show_input.obj.configure(cursor="hand2")

        def toggle_password_visibility():
            self.user_password_entry["show"] = "" if self.show_password else "*"
            self.show_password = not self.show_password

        confirm_button = IconButton(self.content_frame, "Log in", lambda: self.login(), "check", 100, 30, "white", "#795757", "white", "#6a4e4e")
        cancel_button = IconButton(self.content_frame, "Cancel", lambda: self.root.obj.quit(), "cross", 100, 30, "white", "#795757", "white", "#6a4e4e")
        self.root.obj.bind("<Return>", lambda x: self.login())

        user_id_label.obj.grid(row=1, column=0, sticky="w")
        self.user_id_entry.grid(row=1, column=1)
        user_password_label.obj.grid(row=2, column=0, sticky="w")
        self.user_password_entry.grid(row=2, column=1)
        show_input.obj.grid(row=2, column=2)
        confirm_button.obj.grid(row=3, column=0, columnspan=1, pady=3)
        cancel_button.obj.grid(row=3, column=1, columnspan=1, pady=3)

        # Update cycle
        self.root.obj.mainloop()

    def login(self):
        try:
            user_id = int(self.user_id_entry.get())
        except ValueError:
            mb.showerror("Invalid input", "User ID must only contain numbers", self.root.obj)
            return
        user_password = self.user_password_entry.get()

        for teller in self.tellers:
            if teller.user_id == user_id and teller.password == user_password:
                mb.showinfo("Log in success", f"Welcome, {teller.name["fn"]} {teller.name["ln"]}", self.root.obj)
                self.root.obj.unbind("<Return>")
                try:
                    BankProgram(self.root, teller)
                except KeyboardInterrupt:
                    self.root.obj.quit()
                self.root.obj.quit()
                return
        mb.showerror("Invalid credentials", "Did you put in your name instead of your user id?", self.root.obj)