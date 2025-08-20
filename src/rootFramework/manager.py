import rootFramework as rf
import pygame

class Manager(rf.SceneManager):
    
    def __init__(self, screen: pygame.Surface, *initial_scenes: rf.Scene) -> None:
        super().__init__()
        self.running = False
        self.time_manager = rf.Time()

        if initial_scenes:
            self.init_scenes(screen, *initial_scenes)

    def stop(self) -> None:
        """Arrête le gestionnaire de scènes."""
        self.running = False

    def update(self, dt: float):
        super().update(dt)

    def draw(self):
        super().draw()


    def run(self) -> None:
        """Lance la boucle principale du gestionnaire de scènes."""
        if len(self.scenes) == 0:
            raise ValueError("Manager can't run without scenes.")
        if self.running:
            raise RuntimeError("Manager is already running.")
        self.running = True
        clock = pygame.time.Clock()  # Créer le clock une fois
        while self.running:
            dt = clock.tick(60) / 1000.0  # Calculer dt à chaque frame
            for event in pygame.event.get():
                if event.type == rf.QUIT:
                    self.running = False
                self.process_event(event)
            # update
            self.update(dt)
            self.time_manager.update()
            # render
            self.draw()
            pygame.display.flip()

        pygame.quit()