import pygame
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import rootFramework as rf

class Scene(ABC):
    """Classe de base pour une scène dans le framework."""

    def __init__(self, name: str):
        self.name = name
        self.visible = False
        self.active = False
        self.screen: pygame.Surface = None
        self.manager: "rf.SceneManager | None" = None
        self.index: int = 0
        self.world_entities: list[rf.Entity] = [] # Liste des entités du monde -> affetcté par la caméra
        self.hud_entities: list[rf.Entity] = [] # Liste des entités HUD -> non affecté par la caméra

    def __str__(self):
        return f"Scene(name={self.name}, visible={self.visible}, active={self.active})"
    
    def get_world_entities_count(self) -> int:
        """Retourne le nombre d'entités dans le monde."""
        return len(self.world_entities)
    
    def get_hud_entities_count(self) -> int:
        """Retourne le nombre d'entités dans le HUD."""
        return len(self.hud_entities)

    def get_name(self) -> str:
        """Retourne le nom de la scène."""
        return self.name

    def is_visible(self) -> bool:
        """Vérifie si la scène est visible."""
        return self.visible
    
    def set_visible(self, visible: bool) -> None:
        """Définit la visibilité de la scène."""
        self.visible = visible
    
    def is_active(self) -> bool:
        """Vérifie si la scène est active."""
        return self.active
    
    def set_active(self, active: bool) -> None:
        """Définit l'état actif de la scène."""
        self.active = active

    def set_manager(self, manager: "rf.SceneManager") -> None:
        """Assigne le gestionnaire de scène à cette scène."""
        self.manager = manager
        self.screen = manager.screen

    def set_index(self, index: int) -> None:
        """Assigne l'index de la scène dans le gestionnaire."""
        self.index = index

    def get_index(self) -> int:
        """Retourne l'index de la scène dans le gestionnaire."""
        return self.index

    def add_world_entity(self, *entities: "rf.Entity"):
        """Ajoute des entités au monde de la scène."""
        for entity in entities:
            if entity not in self.world_entities:
                self.world_entities.append(entity)
                entity.set_parent_scene(self)

    def remove_world_entity(self, *entities: "rf.Entity"):
        """Retire des entités du monde de la scène."""
        for entity in entities:
            if entity in self.world_entities:
                self.world_entities.remove(entity)
                entity.set_parent_scene(None)

    def add_hud_entity(self, *entities: "rf.Entity"):
        """Ajoute des entités au HUD de la scène."""
        for entity in entities:
            if entity not in self.hud_entities:
                self.hud_entities.append(entity)
                entity.set_parent_scene(self)

    def remove_hud_entity(self, *entities: "rf.Entity"):
        """Retire des entités du HUD de la scène."""
        for entity in entities:
            if entity in self.hud_entities:
                self.hud_entities.remove(entity)
                entity.set_parent_scene(None)

    def get_by_tags(self, *tags: str) -> list["rf.Entity"]:
        """Retourne une liste d'entités ayant tous les tags spécifiés."""
        return [entity for entity in self.world_entities + self.hud_entities if entity.has_tags(*tags)]

    def get_by_uid(self, uid: int) -> "rf.Entity | None":
        """Retourne une entité par son UID."""
        for entity in self.world_entities + self.hud_entities:
            if entity.uid == uid:
                return entity
        return None
    
    def do_update(self, dt: float) -> None:
        """Met à jour la scène."""
        for entity in self.world_entities + self.hud_entities:
            entity.update(dt)

        self.update(dt)

    @abstractmethod
    def update(self, dt: float) -> None:
        """Met à jour la scène. À implémenter dans les sous-classes (mis à jour plus spécific)."""
        pass

    @abstractmethod
    def draw(self) -> None:
        """Dessine la scène sur la surface donnée. À implémenter dans les sous-classes."""
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        """Gère les événements. Peut être surchargé dans les sous-classes."""
        pass

    def on_enter(self) -> None:
        """Action à effectuer lorsque la scène est activée."""
        self.set_active(True)
        self.set_visible(True)

    def on_exit(self) -> None:
        """Action à effectuer lorsque la scène est désactivée."""
        self.set_active(False)
        self.set_visible(False)

    def do_when_added(self):
        """Actions à effectuer lorsque la scène est ajoutée au gestionnaire."""
        pass
        