class OutOfRange(Exception):
    ...


class AlreadyExists(Exception):
    ...


class InsufficientFunds(Exception):
    ...


class NotFound(Exception):
    ...


class Empty(Exception):
    ...


class InvalidCredentials(Exception):
    ...


def error(reason):
    print(f"Error: {reason}")


def success(reason):
    print(f"Success: {reason}")


def cont():
    print("Press ENTER to return...")
    input()
