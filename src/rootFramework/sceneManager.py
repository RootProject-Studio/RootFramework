import pygame
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import rootFramework as rf


class SceneManager(ABC):
    """Classe de base pour la gestion des scènes dans le framework."""

    def __init__(self):
        self.scenes: list["rf.Scene"] = []

    def init_scenes(self, screen: pygame.Surface, *initial_scenes: "rf.Scene") -> None:
        """Initialise les scènes avec le gestionnaire."""
        self.screen = screen
            
        for index, scene in enumerate(initial_scenes):
            scene.set_manager(self)
            scene.set_index(index)
            scene.do_when_added()
            self.scenes.append(scene)
        
        # Activer la première scène par défaut
        if self.scenes:
            self.scenes[0].on_enter()

    def get_current_scene(self) -> "rf.Scene":
        """Retourne la scène courante."""
        if self.scenes:
            return self.scenes[0]
        raise ValueError("Aucune scène courante.")
    
    def get_current_scene_name(self) -> str:
        """Retourne le nom de la scène courante."""
        if self.scenes:
            return self.scenes[0].name
        raise ValueError("Aucune scène courante.")
    
    def get_index_of_scene(self, name: str) -> int:
        """Retourne l'index de la scène par son nom."""
        if not self.has_scene(name):
            raise ValueError(f"Scene '{name}' not found in SceneManager.")
        for s in self.scenes:
            if s.name == name:
                return s.get_index()
    
    def update_scene_states(self):
        """Met à jour les états des scènes visibles et actives."""
        self.active_scenes = [s for s in reversed(self.scenes) if s.is_active]
        self.visible_scenes = [s for s in reversed(self.scenes) if s.is_visible]

    def add_scene(self, scene: "rf.Scene") -> None:
        """Ajoute une scène à la liste des scènes."""
        pass

    def remove_scene(self, scene: "rf.Scene") -> None:
        """Supprime une scène de la liste des scènes."""
        pass

    def has_scene(self, name: str) -> bool:
        """Vérifie si une scène est présente dans la liste des scènes."""
        return any(name == scene.name for scene in self.scenes)
    
    def get_scene(self, name: str) -> "rf.Scene":
        """Retourne une scène par son nom."""
        if not self.has_scene(name):
            return None
        for scene in self.scenes:
            if scene.name == name:
                return scene
        return None
    
    def set_scene(self, name: str, index: int = 0) -> None:
        """Définit la scène par son nom et son index."""
        if not self.has_scene(name):
            raise ValueError(f"Scene '{name}' not found in SceneManager.")
        if index < 0 or index >= len(self.scenes):
            raise IndexError("Index out of range for scenes list.")
        self.scenes[index] = self.get_scene(name)
        self.scenes[index].set_index(index)

    def transition_to_scene(self, name: str, transition=None) -> None:
        """Transition vers une scène par son nom."""
        if not self.has_scene(name):
            raise ValueError(f"Scene '{name}' not found in SceneManager.")
        
        # Désactiver l'ancienne scène courante
        self.get_current_scene().on_exit()
        
        current_index = 0 
        target_index = self.get_index_of_scene(name)
        
        # Échanger les scènes dans la liste
        self.scenes[current_index], self.scenes[target_index] = \
            self.scenes[target_index], self.scenes[current_index]
        self.scenes[current_index].set_index(current_index)
        self.scenes[target_index].set_index(target_index)

        # Activer la nouvelle scène courante
        self.get_current_scene().on_enter()

        print(f"Transitioning to scene '{name}' at index {target_index} with {self.get_current_scene()}.")

    def process_event(self, event: pygame.Event) -> None:
        """Traite les événements pour toutes les scènes."""
        self.scenes[0].handle_event(event)
    
    def update(self, dt: float) -> None:
        """Met à jour toutes les scènes actives."""
        for scene in self.scenes:
            if scene.is_active():
                scene.do_update(dt)

    def draw(self) -> None:
        """Dessine toutes les scènes visibles."""
        for scene in self.scenes:
            if scene.is_visible():
                scene.draw()