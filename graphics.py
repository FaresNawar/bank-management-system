import tkinter as tk
from tkinter import ttk
from typing import Literal
from tkinter import messagebox
import winsound as sound
from PIL import Image, ImageTk


def playsound(f: Literal["BEEP", "BOOT", "ERROR", "FAIL", "GOODBYE", "QUESTION", "SUCCESS", "CREDITS"]): sound.PlaySound(f"assets/{f}.wav", sound.SND_ASYNC)


class mb:
    @staticmethod
    def showinfo(title: str, text: str, parent, detail: str = None):
        playsound("SUCCESS")
        return messagebox.showinfo(title, text, parent=parent, detail=detail, icon="question")

    @staticmethod
    def showerror(title: str, text: str, parent, detail: str = None):
        playsound("ERROR")
        return messagebox.showerror(title, text, parent=parent, detail=detail, icon="question")

    @staticmethod
    def showwarning(title: str, text: str, parent, detail: str = None):
        playsound("FAIL")
        return messagebox.showwarning(title, text, parent=parent, detail=detail, icon="question")

    @staticmethod
    def askyesno(title: str, text: str, parent, detail: str = None):
        playsound("QUESTION")
        return messagebox.askyesno(title, text, parent=parent, detail=detail, icon="question")

    @staticmethod
    def askyesnocancel(title: str, text: str, parent, detail: str = None):
        playsound("QUESTION")
        return messagebox.askyesnocancel(title, text, parent=parent, detail=detail, icon="question")

    @staticmethod
    def askquestion(title: str, text: str, parent, detail: str = None):
        playsound("QUESTION")
        return messagebox.askquestion(title, text, parent=parent, detail=detail, icon="question")

    @staticmethod
    def askokcancel(title: str, text: str, parent, detail: str = None):
        playsound("QUESTION")
        return messagebox.askokcancel(title, text, parent=parent, detail=detail, icon="question")

    @staticmethod
    def askretrycancel(title: str, text: str, parent, detail: str = None):
        playsound("QUESTION")
        return messagebox.askretrycancel(title, text, parent=parent, detail=detail, icon="question")

    @staticmethod
    def showcredits(title: str, text: str, parent, detail: str = None):
        playsound('CREDITS')
        return messagebox.showinfo(title, text, parent=parent, detail=detail, icon="question")


class Window:
    def __init__(self, width: int, height: int, title: str = None, pos: (int, int) = None, resizable: bool = False,
                 toplevel: bool = False):
        w = tk.Toplevel() if toplevel else tk.Tk()
        if toplevel:
            w.bind('<Escape>', lambda x: self.obj.destroy())

        self.obj = w
        self.width = width
        self.height = height
        self.title = title or "Untitled"

        if not pos:
            pos = ((w.winfo_screenwidth() // 2) - (width // 2), (w.winfo_screenheight() // 2) - (height // 2) - 25)

        self.obj.geometry("%dx%d+%d+%d" % (width, height, pos[0], pos[1]))
        self.obj.title(self.title)

        self.pos = pos
        self.obj.resizable(width=resizable, height=resizable)

    def set_icon(self, file: str):
        try:
            self.obj.iconbitmap(file)
            return 0
        except Exception as e:
            print(f"Problem occurred with setting icon: {e.args[0]}")
            return -1


class Button:
    def __init__(self, parent, text: str = "", width: int = 1, padding: int = 1):
        self.parent = parent
        self.text = text
        self.width = width
        self.padding = padding
        self.obj = ttk.Button(self.parent, text=self.text, width=self.width, padding=self.padding)

    def bind_function(self, function):
        self.obj.configure(command=function)

    def set_style(self, style_id, font, font_size):
        style = ttk.Style()
        style.configure(f'{style_id}.TButton', font=(font, font_size))
        self.obj.configure(style=f'{style_id}.TButton')


class IconButton:
    def __init__(self, root, text: str, command, icon: str = None, width: int = 10, height: int = 10, fg: str or None = "white", bg: str or None = "black", fg_selected: str or None = "black", bg_selected: str or None = "white", icon_scale: int = 27):
        self.icon = ImageTk.PhotoImage(Image.open(f'assets/icons/{icon}.png').resize((icon_scale, icon_scale))) if icon else None
        self.root = root
        self.bg = bg
        self.bg_selected = bg_selected
        self.fg = fg
        self.fg_selected = fg_selected
        self.obj = tk.Button(
            self.root,
            text=text,
            image=self.icon,
            relief="flat",
            command=command,
            fg=fg, bg=bg,
            activebackground=bg,
            activeforeground=fg,
            font=("Product Sans", 15),
            compound=tk.LEFT,
            border=0,
            width=width,
            height=height,
            padx=3,
            pady=3
        )
        self.obj.bind("<Enter>", lambda x: self.__enter__())
        self.obj.bind("<Leave>", lambda x: self.__leave__())

    def __enter__(self):
        self.obj["bg"] = self.bg_selected
        self.obj["fg"] = self.fg_selected

    def __leave__(self):
        self.obj["fg"] = self.fg
        self.obj["bg"] = self.bg


class ToggleButton(IconButton):
    def __init__(self, root, text: str,  inactive_text: str, inactive_icon, command, icon: str = None, width: int = 10, height: int = 10, fg: str or None = "white", bg: str or None = "black", fg_selected: str or None = "black", bg_selected: str or None = "white", icon_scale: int = 27):
        super().__init__(root, text, command, icon, width, height, fg, bg, fg_selected, bg_selected, icon_scale)
        self.state = True
        self.icon = ImageTk.PhotoImage(Image.open(f'assets/icons/{icon}.png').resize((icon_scale, icon_scale))) if icon else None
        self.inactive_icon = ImageTk.PhotoImage(Image.open(f'assets/icons/{inactive_icon}.png').resize((27, 27))) if inactive_icon else None
        self.text = text
        self.inactive_text = inactive_text
        self.root = root
        self.bg = bg
        self.bg_selected = bg_selected
        self.fg = fg
        self.fg_selected = fg_selected
        self.command = command
        self.obj = tk.Button(
            self.root,
            text=text,
            image=self.icon,
            relief="flat",
            fg=fg, bg=bg,
            activebackground=bg,
            activeforeground=fg,
            font=("Product Sans", 15),
            compound=tk.LEFT,
            border=0,
            width=width,
            height=height,
            padx=3,
            pady=3
        )
        self.obj.bind("<Enter>", lambda x: self.__enter__())
        self.obj.bind("<Leave>", lambda x: self.__leave__())
        self.obj.bind("<Button-1>", lambda x: self.__clicked__())

    def __enter__(self):
        self.obj["bg"] = self.bg_selected
        self.obj["fg"] = self.fg_selected

    def __leave__(self):
        self.obj["fg"] = self.fg
        self.obj["bg"] = self.bg

    def __clicked__(self):
        self.state = not self.state
        self.obj.configure(text=self.text if self.state else self.inactive_text)
        self.obj.configure(image=self.icon if self.state else self.inactive_icon)
        self.command()


class Label:
    def __init__(self, parent, text: str = "", font: str = "Arial", font_size: int = 5, padding: int = 0,
                 foreground: str = "#000000", background: str = ""):
        self.obj = ttk.Label(parent, text=text, font=(font, font_size), padding=padding, foreground=foreground,
                             background=background)
        self.parent = parent
        self.text = text
        self.font = font
        self.font_size = font_size,
        self.padding = padding
        self.foreground = foreground
        self.background = background

    def set_text(self, text):
        self.text = text
        self.obj.configure(text=text)
        self.obj.update()

    def pack(self):
        self.obj.pack()

    def grid(self, row: int = 0, column: int = 0, column_span: int = 1):
        self.obj.grid(row=row, column=column, columnspan=column_span)
