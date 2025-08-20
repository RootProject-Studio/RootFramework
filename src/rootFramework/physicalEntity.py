import pygame
import rootFramework as rf

class PhysicalEntity(rf.Entity):
    def __init__(
        self,
        mass: float = 1.0,
        gravity: float = 1500.0,  # pixels/s²
        friction_ground: float = 0.8,
        friction_air: float = 0.95,
        max_speed: float = 400.0,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.mass = mass
        self.gravity_value = gravity
        self.friction_ground = friction_ground
        self.friction_air = friction_air
        self.max_speed = max_speed

        self.on_ground = False

    # --------------------
    # Physique de base
    # --------------------
    def apply_force(self, fx: float, fy: float):
        """Ajoute une force à l'entité."""
        self.acceleration.x += fx / self.mass
        self.acceleration.y += fy / self.mass

    def apply_gravity(self):
        """Ajoute la gravité si pas au sol."""
        if not self.on_ground:
            self.apply_force(0, self.gravity_value)

    def limit_speed(self):
        """Limite la vitesse max."""
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

    # --------------------
    # Déplacement avec collisions
    # --------------------
    def move_and_collide(self, dx: float, dy: float):
        """Déplace et corrige la position si collision."""
        self.rect.x += dx
        self._resolve_collisions("x")
        self.rect.y += dy
        self._resolve_collisions("y")

    def _resolve_collisions(self, axis: str):
        """Corrige la position sur l'axe en cas de collision."""
        self.on_ground = False  # Reset, sera recalculé

        if not self.parent_scene:
            return

        for entity in getattr(self.parent_scene, "world_entities", []):
            if entity is self:
                continue
            if self.rect.colliderect(entity.rect):
                print(f"Collision detected with {entity.uid} on {axis} axis")
                if axis == "x":
                    if self.velocity.x > 0:
                        self.rect.right = entity.rect.left
                    elif self.velocity.x < 0:
                        self.rect.left = entity.rect.right
                    self.velocity.x = 0
                elif axis == "y":
                    if self.velocity.y > 0:
                        self.rect.bottom = entity.rect.top
                        self.on_ground = True
                    elif self.velocity.y < 0:
                        self.rect.top = entity.rect.bottom
                    self.velocity.y = 0

    # --------------------
    # Saut
    # --------------------
    def jump(self, force: float = 600.0):
        """Effectue un saut si l'entité est au sol."""
        if self.on_ground:
            self.velocity.y = -force
            self.on_ground = False

    # --------------------
    # Boucle d'update
    # --------------------
    def update(self, dt: float):
        # Appliquer gravité
        self.apply_gravity()

        # Intégrer accélération
        self.velocity += self.acceleration * dt
        self.acceleration.xy = (0, 0)  # Reset après application

        # Limiter vitesse max
        self.limit_speed()

        # Appliquer frottements
        if self.on_ground:
            self.velocity.x *= self.friction_ground
        else:
            self.velocity.x *= self.friction_air

        # Déplacement
        self.move_and_collide(self.velocity.x * dt, self.velocity.y * dt)
