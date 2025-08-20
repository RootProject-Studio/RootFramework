import rootFramework as rf
from .constants import Constants
import math
import pygame

class Camera:
    """
    Classe gérant une caméra 2D avec suivi de cible, contrôle manuel, zoom fluide et limites.
    Compatible avec Pygame.
    """
    def __init__(self, size: tuple[int, int] | None = None, world_size: tuple[int, int] | None = None, zoom=1.0, smoothness=5.0):
        """
        Initialise la caméra.
        :param size: tuple (largeur, hauteur) de l'écran
        :param world_size: tuple (largeur, hauteur) du monde
        :param zoom: niveau de zoom initial
        :param smoothness: facteur de fluidité (plus grand = plus fluide mais moins réactif)
        """
        self.screen_width, self.screen_height = size if size else Constants.RESOLUTION
        self.world_width, self.world_height = world_size if world_size else (math.inf, math.inf)

        # Position actuelle et cible
        self.pos = pygame.Vector2(0, 0)
        self.target_pos = pygame.Vector2(0, 0)

        # Zoom actuel et cible
        self.zoom = zoom
        self.target_zoom = zoom

        # Suivi d'entité
        self.follow_target = None
        self.offset = pygame.Vector2(0, 0)

        # Facteur de fluidité
        self.smoothness = smoothness

        # Mode manuel (quand True, on ne suit pas de cible)
        self.manual_mode = False

    def follow(self, target, offset=(0, 0)):
        """
        Définit l'entité à suivre.
        :param target: objet ayant un attribut rect (Sprite Pygame)
        :param offset: décalage par rapport au centre de l'entité
        """
        self.follow_target = target
        self.offset = pygame.Vector2(offset)
        self.manual_mode = False

    def set_manual_mode(self, state=True):
        """
        Active/désactive le mode manuel (désactive le suivi).
        """
        self.manual_mode = state
        if state:
            self.follow_target = None

    def set_zoom(self, zoom):
        """
        Change le zoom tout en gardant le point de focus au même endroit.
        :param zoom: facteur de zoom (1.0 = taille normale)
        """
        zoom = max(0.1, zoom)  # Sécurité
        if self.follow_target:
            # On garde le centre de la cible comme point d’ancrage
            target_center = pygame.Vector2(self.follow_target.rect.center)
            self.target_pos = target_center - pygame.Vector2(
                self.screen_width / (2 * zoom),
                self.screen_height / (2 * zoom)
            ) + self.offset

        self.target_zoom = zoom

    def update(self, dt):
        """
        Met à jour la position et le zoom de la caméra.
        :param dt: delta time en secondes
        """
        if self.follow_target and not self.manual_mode:
            # Utiliser le zoom cible pour éviter le "saut" lors du changement
            target_center = pygame.Vector2(self.follow_target.rect.center)
            self.target_pos = target_center - pygame.Vector2(
                self.screen_width / (2 * self.target_zoom),
                self.screen_height / (2 * self.target_zoom)
            ) + self.offset

        # Interpolation fluide vers la position cible
        self.pos += (self.target_pos - self.pos) * min(1, self.smoothness * dt)

        # Interpolation fluide du zoom
        self.zoom += (self.target_zoom - self.zoom) * min(1, self.smoothness * dt)

        # Limites du monde
        max_x = max(0, self.world_width - self.screen_width / self.zoom)
        max_y = max(0, self.world_height - self.screen_height / self.zoom)
        self.pos.x = max(0, min(self.pos.x, max_x))
        self.pos.y = max(0, min(self.pos.y, max_y))


    def get_visible_area(self):
        """
        Renvoie la zone visible de la caméra sous forme de rectangle.
        """
        return pygame.Rect(
            self.pos.x,
            self.pos.y,
            self.screen_width / self.zoom,
            self.screen_height / self.zoom
        )

    def apply(self, rect):
        """
        Applique la transformation caméra sur un rectangle (pour placer un sprite à l'écran).
        :param rect: pygame.Rect de l'objet
        :return: pygame.Rect transformé
        """
        return pygame.Rect(
            (rect.x - self.pos.x) * self.zoom,
            (rect.y - self.pos.y) * self.zoom,
            rect.width * self.zoom,
            rect.height * self.zoom
        )

    def apply_surface(self, surface):
        """
        Applique le zoom à une surface entière (utile pour les tilesets ou décors fixes).
        """
        if self.zoom != 1:
            w = int(surface.get_width() * self.zoom)
            h = int(surface.get_height() * self.zoom)
            return pygame.transform.scale(surface, (w, h))
        return surface