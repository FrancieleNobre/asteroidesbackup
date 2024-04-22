import os
from entity import Entity
from sound import Sound
from utils import *

NUMBER_OF_SECONDS = 3

class CountDown(Entity):
    def __init__(self, galaxy):
        super().__init__(galaxy, "countdown", GREEN)

        self.font = pygame.font.Font(os.path.join(
            "res", "hyperspace-bold.otf"), 90)
        self.sequence = NUMBER_OF_SECONDS
        pygame.time.set_timer(COUNT_DOWN_EVENT, 1000, self.sequence + 1)
        pygame.time.set_timer(START_GAME, self.sequence*1000, 1)
        self.tick = False
        Sound().play('beep-countdown')

    def update(self, time_passed, event_list):
        super().update(time_passed, event_list)

        self.process_event(event_list)

        if self.sequence > 0:
            self.text = str(self.sequence)
        elif self.sequence == 0:
            self.text = "GO!"

        if self.tick:
            self.sequence -= 1
            if self.sequence == -1:
                self.dead = True

    def render(self, surface):
        super().render(surface)

        if self.sequence >= 0:
            countdown_surface = self.font.render(self.text, False, self.color)
            rect = countdown_surface.get_rect()
            rect.centery = self.galaxy.rect.centery/2
            rect.centerx = self.galaxy.rect.centerx
            surface.blit(countdown_surface, rect)

        if self.tick:
            self.tick = False
            if self.sequence > 0:
                Sound().play('beep-countdown')
            if self.sequence == 0:
                Sound().play('beep')

    def process_event(self, event_list):
        for event in event_list:
            if event.type == COUNT_DOWN_EVENT:
                self.tick = True
            if event.type == START_GAME:
                self.galaxy.get_entity_by_name('score').run_game()
                pygame.time.set_timer(UNSHIELD_EVENT, 5000, 1)
