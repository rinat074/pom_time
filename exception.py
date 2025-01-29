

class UserNotFoundError(Exception):
    detail = "User not found"

class UserPasswordError(Exception):
    detail = "Invalid username or password"

class TokenExpiredError(Exception):
    detail = "Token expired"

class TokenNotValidError(Exception):
    detail = "Token not valid"

class TaskNotFoundError(Exception):
    detail = "Task not found"