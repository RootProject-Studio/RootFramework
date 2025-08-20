import rootFramework as rf
import pygame
from typing import Sequence

class AnimatedSprite(rf.Sprite):
    """
    Sprite animé capable de contenir plusieurs séquences nommées,
    avec vitesse spécifique par animation, lecture en boucle ou ping-pong,
    et possibilité de contrôle manuel des frames.
    """
    
    def __init__(self, 
                 default_frame_duration: float = 0.1,  # Durée par frame par défaut
                 loop: bool = True,                    # Si True, l’animation recommence en boucle
                 pingpong: bool = False,               # Si True, lecture aller-retour
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Stockage des animations : { nom: [frames Surface] }
        self.animations: dict[str, list[pygame.Surface]] = {}
        
        # Vitesse par animation : { nom: frame_duration }
        self.animation_speeds: dict[str, float] = {}
        
        # Nom de l’animation en cours
        self.current_animation: str | None = None
        
        self.default_frame_duration = default_frame_duration
        self.loop = loop
        self.pingpong = pingpong
        
        # Variables d’état
        self.current_time = 0.0
        self.current_frame_index = 0
        self.direction = 1
        self.manual_mode = False  # True = contrôle manuel, l’update ne change plus les frames

    # ----------------------
    # Ajout d’animations
    # ----------------------
    def add_animation_from_surfaces(self, 
                                    name: str, 
                                    surfaces: Sequence[pygame.Surface],
                                    frame_duration: float | None = None):
        """
        Ajoute une animation depuis une liste de surfaces pygame.

        name           : nom de l'animation ("walk", "idle", etc.)
        surfaces       : liste de pygame.Surface représentant les frames
        frame_duration : durée par frame (s'il est None, on utilise la durée par défaut)
        """
        if not surfaces:
            return self
        
        # Normalise toutes les frames à la taille de la première
        base_size = surfaces[0].get_size()
        frames = [pygame.transform.scale(s.convert_alpha(), base_size) for s in surfaces]
        
        self.animations[name] = frames
        self.animation_speeds[name] = frame_duration if frame_duration else self.default_frame_duration
        
        # Si aucune animation n’est active, on active celle-ci
        if self.current_animation is None:
            self.set_animation(name)
        return self
    
    def add_animation_from_paths(self, 
                                 name: str, 
                                 paths: Sequence[str],
                                 frame_duration: float | None = None):
        """
        Ajoute une animation depuis des fichiers image.

        name           : nom de l'animation
        paths          : liste de chemins vers les images
        frame_duration : durée par frame
        """
        surfaces = []
        resource_manager = rf.ResourceManager()
        for path in paths:
            try:
                # Charger l'image puis la récupérer
                resource_manager.load_image(path)
                surf = resource_manager.get_image(path)
                if surf:
                    surfaces.append(surf)
                else:
                    print(f"Impossible de charger l'image: {path}")
            except pygame.error as e:
                print(f"Erreur lors du chargement de '{path}': {e}")
        return self.add_animation_from_surfaces(name, surfaces, frame_duration)

    # ----------------------
    # Contrôle d'animations
    # ----------------------
    def set_animation(self, name: str, reset: bool = True):
        """
        Change l'animation active.

        name  : nom de l'animation à activer
        reset : si True, recommence l'animation depuis la première frame
        """
        if name not in self.animations:
            print(f"Animation '{name}' introuvable.")
            return self
        
        self.current_animation = name
        frames = self.animations[name]
        
        if reset:
            self.current_frame_index = 0
            self.direction = 1
            self.current_time = 0.0
        else:
            if self.current_frame_index >= len(frames):
                self.current_frame_index = len(frames) - 1

        # Applique immédiatement la première frame
        self.original_surface = self.animations[name][self.current_frame_index]
        self.set_size(self.original_surface.get_size())
        self.surface.blit(self.original_surface, (0, 0))
        return self
    
    def set_frame(self, index: int):
        """
        Force l'affichage d'une frame précise et désactive l'animation automatique.
        
        index : numéro de la frame (0 = première image)
        """
        if not self.current_animation:
            return self
        
        frames = self.animations[self.current_animation]
        self.manual_mode = True
        self.current_frame_index = max(0, min(index, len(frames) - 1))
        
        # Remplace le contenu de la surface
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(frames[self.current_frame_index], (0, 0))
        return self
    
    def resume_animation(self):
        """
        Réactive l'animation automatique après un set_frame().
        """
        self.manual_mode = False
        return self

    # ----------------------
    # Mise à jour
    # ----------------------
    def update(self, dt: float):
        """
        Met à jour l'animation en fonction du temps écoulé.

        dt : temps écoulé depuis la dernière frame (en secondes)
        """
        if not self.current_animation or self.manual_mode:
            return
        
        frames = self.animations[self.current_animation]
        if not frames:
            return
        
        # Durée de frame spécifique ou par défaut
        speed = self.animation_speeds.get(self.current_animation, self.default_frame_duration)
        
        self.current_time += dt
        if self.current_time >= speed:
            self.current_time -= speed
            self.current_frame_index += self.direction
            
            # Gestion des limites
            if self.pingpong:
                if self.current_frame_index >= len(frames):
                    self.current_frame_index = len(frames) - 2
                    self.direction = -1
                elif self.current_frame_index < 0:
                    self.current_frame_index = 1
                    self.direction = 1
            else:
                if self.current_frame_index >= len(frames):
                    if self.loop:
                        self.current_frame_index = 0
                    else:
                        self.current_frame_index = len(frames) - 1
            
            # Applique la nouvelle frame
            self.surface.fill((0, 0, 0, 0))
            self.surface.blit(frames[self.current_frame_index], (0, 0))
