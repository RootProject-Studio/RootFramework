import rootFramework as rf
import pygame

from abc import abstractmethod

class Drawable(rf.Entity):
    """Classe de base pour les entités dessinables."""
    def __init__(
            self, 
            size: tuple[int, int] | None = None, 
            visible: bool = True, 
            convert_alpha: bool = True,
            surface_flags: int = pygame.SRCALPHA,  # Par défaut, supporter la transparence
            *args, 
            **kwargs):
        """Initialise l'entité dessinable."""
        super().__init__(*args, **kwargs)
        self.visible: bool = visible
        self.convert_alpha: bool = convert_alpha
        self.surface_flags: int = surface_flags
        self.rect.size = (10,10) if size is None else size
        self.surface: pygame.Surface = pygame.Surface(self.rect.size, self.surface_flags)
        if self.surface_flags & pygame.SRCALPHA:
            self.surface.fill((0, 0, 0, 0))  # Transparent par défaut
        else:
            self.surface.fill((255, 255, 255))


    def draw(self, surface: pygame.Surface) -> None:
        """Dessine l'entité sur la surface donnée."""
        if self.visible:
            surface.blit(self.surface, self.rect.topleft)