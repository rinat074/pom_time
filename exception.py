

class UserNotFoundError(Exception):
    detail = "User not found"

class UserPasswordError(Exception):
    detail = "Invalid username or password"
