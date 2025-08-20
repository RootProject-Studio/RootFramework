import pygame
from .resourceManager import ResourceManager

initialized = False

def init(resolution: tuple[int, int], resource_path: str = ".", caption: str = "Root Framework Project") -> None:
    """Initialise les modules rootFramework."""
    global initialized
    pygame.init()
    print("Pygame initialized successfully.")
    ResourceManager().set_resource_path(resource_path)
    pygame.display.set_caption(caption)
    pygame.display.set_mode(resolution)
    screen = pygame.display.get_surface()
    screen.fill((0, 0, 0))  # Fill the screen with black
    pygame.display.flip()
    initialized = True
    print("Display set up with caption and size.")
    return screen

from .scene import Scene
from .sceneManager import SceneManager
from .manager import Manager
from .constants import *  # Import all constants
from .utils import Singleton
from .time import Time, Timer
from .entity import Entity
from .drawable import Drawable
from .sprite import Sprite
from .animatedSprite import AnimatedSprite
from .physicalEntity import PhysicalEntity
from .movableEntity import MovableEntity
from .camera import Camera
