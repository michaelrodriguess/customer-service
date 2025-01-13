"""
Exceptions module
"""


class EntityNotFound(Exception):
    """
    Entity exception not found
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
