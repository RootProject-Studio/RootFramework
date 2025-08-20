import rootFramework as rf
import pygame

class Singleton(type):
    """Metaclasse pour implémenter le pattern Singleton."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Retourne l'instance unique de la classe."""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
