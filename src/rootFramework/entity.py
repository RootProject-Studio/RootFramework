import pygame
import rootFramework as rf
from typing import Self
from abc import ABC, abstractmethod

class Entity(ABC):
    count = 0
    available_uids: set[int] = set()

    def __init__(self, *args, **kwargs):
        """Initialise l'entité avec des arguments et des mots-clés."""

        if Entity.available_uids:
            self.uid = Entity.available_uids.pop()
        else:
            self.uid = Entity.count
            Entity.count += 1

        self.rect = pygame.FRect(0, 0, 0, 0)
        self.tags: list[str] = []
        self.parent_scene: rf.Scene | None = None
        self.debug_color: tuple = (255, 0, 0)

    def __del__(self):
        """Nettoyage de l'entité."""
        Entity.available_uids.add(self.uid)

    def set_position(self, x: float, y: float) -> Self:
        """Définit la position de l'entité par rapport au coin supérieur gauche."""
        self.rect.topleft = (x, y)
        return self
    
    def set_center(self, x: float, y: float) -> Self:
        """Définit le centre de l'entité."""
        self.rect.center = (x, y)
        return self
    
    def set_parent_scene(self, scene: rf.Scene) -> Self:
        """Définit la scène parente de l'entité."""
        if scene == self.parent_scene:
            return self
        if self.parent_scene is not None:
            self.do_when_removed()
        self.parent_scene = scene
        if scene is not None:
            self.do_when_added()
        return self
    
    def do_when_added(self) -> None:
        """Actions à effectuer lorsque l'entité est ajoutée à une scène."""
        pass

    def do_when_removed(self) -> None:
        """Actions à effectuer lorsque l'entité est retirée d'une scène."""
        pass

    def add_tags(self, *tags: str) -> Self:
        """Ajoute des tags à l'entité."""
        for tag in tags:
            if tag not in self.tags:
                self.tags.append(tag)
        self.tags.sort()
        return self

    def remove_tags(self, *tags: str):
        """Retire des tags de l'entité."""
        self.tags = [tag for tag in self.tags if tag not in tags]

    def has_tags(self, *tags: str) -> bool:
        """Vérifie si l'entité a tous les tags spécifiés."""
        return all(tag in self.tags for tag in tags)
    
    def get_tags(self) -> list[str]:
        """Retourne la liste des tags de l'entité."""
        return self.tags
    
    def process_event(self, event: pygame.Event):
        self.do_process_actions(event)
        self.do_handle_event(event)

    def do_process_actions(self, event: pygame.Event) -> None:
        """Actions à effectuer lors du traitement d'un événement."""
        pass

    def do_reset_actions(self) -> None:
        """Réinitialise les actions de l'entité."""
        pass

    def do_handle_event(self, event: pygame.Event) -> None:
        """Gère les événements spécifiques à l'entité."""
        pass

    @abstractmethod
    def update(self, dt: float):
        """Met à jour l'entité avec le temps écoulé."""
        pass