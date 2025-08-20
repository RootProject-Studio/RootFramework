import rootFramework as rf
import pygame

class Timer:
    """Classe pour gérer un minuteur dans le jeu"""

    def __init__(self, name: str, duration: int = 1000, 
                 loop: bool = False, end_callback = None, reusable: bool = False):
        """Initialise un minuteur avec 
            un nom, 
            une durée (ms), 
            un booléen si le minuteur se relance,
            une fonction appelée quand le timer se termine,
            un booléen pour savoir si le minuteur est réutilisable."""
        self.name: str = name
        self.duration: int = duration
        self.loop: bool = loop
        self.end_callback = end_callback
        self.reusable: bool = reusable

        self.start_time = None
        self.stopped = True
        self.elapsed_progress: float = 0.0

    def start(self):
        """Démarre le minuteur."""
        if self.start_time is None:
            Time().add_timer(self)

        self.start_time = pygame.time.get_ticks()
        self.stopped = False
        self.elapsed_progress = 0.0

    def update(self):
        """Met à jour le minuteur."""
        if self.stopped:
            return False
        
        current_time = pygame.time.get_ticks()
        if self.elapsed_progress < 1:
            self.elapsed_progress = (current_time - self.start_time) / self.duration
            if self.elapsed_progress >= 1:
                self.end()
                return True
        elif self.loop:
            self.start()
        return False
    
    def stop(self):
        """Arrête le minuteur."""
        self.stopped = True

    def end(self):
        """Appelle la fonction de fin du minuteur."""
        self.elapsed_progress = 1.0
        if not self.loop:
            self.stopped = True
        if self.end_callback:
            self.end_callback()

    def is_finished(self) -> bool:
        """Vérifie si le minuteur est terminé."""
        if self.start_time is None:
            return False
        # Un timer est fini s'il n'est pas en boucle et que le temps est écoulé
        return not self.loop and self.elapsed_progress >= 1.0

    def get_progress(self) -> float:
        """Retourne le pourcentage d'avancement du timer (0.0 à 1.0)."""
        return min(self.elapsed_progress, 1.0)
    
    def get_remaining_time(self) -> int:
        """Retourne le temps restant en millisecondes."""
        if self.is_finished():
            return 0
        return max(0, self.duration - int(self.elapsed_progress * self.duration))

class Time(metaclass=rf.Singleton):
    """Classe pour gérer le temps dans le jeu."""

    def __init__(self):
        self.timers = {}

    def add_timer(self, timer):
        """Ajoute un minuteur à la liste des minuteurs."""
        self.timers[timer.name] = timer

    def update(self):
        """Met à jour tous les minuteurs."""
        for timer in list(self.timers.values()):
            timer.update()

        # Retirer les timers finis qui ne sont pas réutilisables
        removed_timers = [name for name, timer in self.timers.items() 
                         if timer.is_finished() and not timer.reusable]
        
        for name in removed_timers:
            self.timers.pop(name)