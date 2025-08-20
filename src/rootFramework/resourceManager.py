import pygame
from typing import Any
import os
from .utils import Singleton

class ResourceManager(metaclass=Singleton):
    """Manager pour gérer les ressources du jeu."""

    def __init__(self):
        self.shared_variables: dict[str, Any] = {}
        self.convert_image_cache: dict[str, pygame.Surface] = {}
        self.convert_alpha_image_cache: dict[str, pygame.Surface] = {}
        self.resource_path: str = "."

    def normalize_path(self, path: str) -> str:
        """Normalise le chemin pour éviter les problèmes de plateforme."""
        return os.path.normpath(path)

    def set_resource_path(self, path: str) -> None:
        """Définit le chemin de base pour les ressources."""
        self.resource_path = os.path.join(os.getcwd(), self.normalize_path(path))

    def get_resource_path(self) -> str:
        """Retourne le chemin de base pour les ressources."""
        return self.resource_path

    def get_path(self, path: str) -> str:
        """Retourne le chemin complet du path à partir du chemin de base."""
        return os.path.join(self.resource_path, self.normalize_path(path))

    #TODO: Implémenter autres que pour les images
    def load_from_dir(self, path: str):
        """Charge toutes les ressources d'un répertoire donné."""
        for root, dirs, files in os.walk(path):
            files = [f for f in files if not f[0] == "."]
            dirs[:] = [d for d in dirs if not d[0] == "."]

            for file in files:
                file_path = os.path.join(root, file)
                if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                    self.load_image(file_path)

                elif file.lower().endswith((".mp3", ".wav", ".ogg")):
                    print(f"Audio files loading not implemented: {file_path}")

                elif file.lower().endswith((".ttf", ".otf")):
                    print(f"Font files loading not implemented: {file_path}")
                    

    def load_image(self, path: str):
        """Charge une image depuis un chemin donné."""
        key = self.get_path(path)
        if key in self.convert_image_cache:
            return
        self.convert_image_cache[key] = pygame.image.load(key).convert()
        self.convert_alpha_image_cache[key] = pygame.image.load(key).convert_alpha()

    def get_image(self, path: str, convert_alpha: bool = True) -> pygame.Surface:
        """Retourne une image chargée depuis le cache ou la charge si elle n'est pas en cache."""
        key = self.get_path(path)
        return (
            self.convert_alpha_image_cache.get(key)
            if convert_alpha
            else self.convert_image_cache.get(key)
        )

    #TODO: Implement load_json method
    def load_json(self, path: str): 
        """Charge un fichier JSON depuis un chemin donné."""
        pass

    #TODO: Implement save_json method
    def save_json(self, path: str, data: dict) -> None:
        """Sauvegarde un dictionnaire dans un fichier JSON."""
        pass

    def set_shared_variable(self, name: str, value) -> bool:
        """Définit une variable partagée."""
        self.shared_variables[name] = value
        return True

    def get_shared_variable(self, name: str):
        """Retourne une variable partagée."""
        return self.shared_variables.get(name)
