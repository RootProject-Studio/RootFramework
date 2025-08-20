import pygame
import rootFramework as rf

class MovableEntity(rf.PhysicalEntity):
    def __init__(self, move_force: float = 1500.0, jump_force: float = 600.0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move_force = move_force
        self.jump_force = jump_force

    def do_handle_event(self, event: pygame.Event) -> None:
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         self.jump(self.jump_force)
        pass

    def update(self, dt: float):
        # keys = pygame.key.get_pressed()

        # if keys[pygame.K_LEFT]:
        #     self.apply_force(-self.move_force, 0)
        # if keys[pygame.K_RIGHT]:
        #     self.apply_force(self.move_force, 0)

        super().update(dt)

        # pass
