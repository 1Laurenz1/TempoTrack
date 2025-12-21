class InvalidTokenError(Exception):
    """JWT token is invalid or expired"""
    
class UserNotFoundError(Exception):
    """Called when the user is not in the database"""

class InvalidUsernameOrEmailOrPasswordError(Exception):
    """Called when the user enters an incorrect username, email, or password"""