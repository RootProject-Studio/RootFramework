import rootFramework as rf
import pygame
from typing import Self

class Sprite(rf.Drawable):
    """Classe de base pour les sprites."""
    
    def __init__(self, size: tuple[int, int] | None = None, path=None, visible: bool = True, convert_alpha: bool = True):
        super().__init__(convert_alpha=convert_alpha)

        self.original_surface: pygame.Surface = None

        if path is not None:
            self.from_path(path)
        if size is not None and self.original_surface:
            self.set_size(self.original_surface.get_size())

    def from_path(self, path: str) -> Self:
        """Charge une image depuis un chemin donné."""
        try:
            self.original_surface = pygame.image.load(path).convert_alpha()
            size = self.original_surface.get_size()
            self.set_size(size)
        except pygame.error as e:
            print(f"Erreur lors du chargement de l'image '{path}': {e}")
            # Créer une surface par défaut en cas d'erreur
            self.original_surface = pygame.Surface((50, 50))
            self.original_surface.fill((255, 0, 255))  # Magenta comme indicateur d'erreur
            self.set_size((50, 50))
        return self

    def set_size(self, size: tuple[int, int]) -> Self:
        """Définit la taille du sprite."""
        if size == self.rect.size:
            return self
        self.rect.size = size
        
        self.surface = pygame.Surface(
            (int(self.rect.width), int(self.rect.height)), self.surface_flags
        )
        if self.convert_alpha:
            self.surface = self.surface.convert_alpha()
        self.surface.fill((0, 0, 0, 0 if self.convert_alpha else 255))
        self.surface.blit(
            pygame.transform.scale(self.original_surface, self.rect.size), (0, 0)
        )
        return self

    def from_surface(self, surface: pygame.Surface) -> Self:
        """Charge un sprite à partir d'une surface."""
        if surface is None:
            return self
        self.original_surface = surface
        size = self.original_surface.get_size()
        self.set_size(size)
        return self