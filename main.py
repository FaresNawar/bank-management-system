from graphics import *
from bank_classes import Teller
from login_window import Login


# Main program function
if __name__ == '__main__':
    registered_tellers = (
        Teller("Fares",
               "Mostafa",
               28,
               2,
               2008,
               "Cairo",
               "Egypt",
               1234,
               "1234"),
    )

    root = Window(650, 700, "Mashriq Solutions", resizable=False)
    try:
        Login(root, registered_tellers)
    except KeyboardInterrupt:
        root.obj.quit()
