"""
Módulo de exceptions
"""


class EntityNotFound(Exception):
    """
    Exception de entidade não encontrada
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
