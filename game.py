import pygame
from pygame.locals import *
from asteroid import Asteroid
from countdown import CountDown
from fps import Fps
from galaxy import Galaxy
from ship import Ship
from score import Score
from utils import *

COLOR_DEPTH = 8
FPS = 60
NUMBER_ASTEROIDS = 6


class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            flags=pygame.FULLSCREEN, depth=COLOR_DEPTH)
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Asteróides, O jogo")
        self.clock = pygame.time.Clock()
        pygame.event.post(pygame.event.Event(NEW_GAME))

    def new_game(self):
        self.galaxy = Galaxy(self.screen_rect)
        self.galaxy.add_entity(Ship(self.galaxy))
        self.fps = Fps(self.galaxy)
        self.galaxy.add_entity(self.fps)
        self.score = Score(self.galaxy)
        self.galaxy.add_entity(self.score)
        for i in range(NUMBER_ASTEROIDS):
            self.galaxy.add_entity(Asteroid(self.galaxy))
        self.galaxy.add_entity(CountDown(self.galaxy))

    def run(self):

        done = False
        while not done:

            event_list = pygame.event.get()
            for event in event_list:
                if (event.type == KEYDOWN and event.key == K_q) or event.type == QUIT:
                    done = True

                if event.type == NEW_GAME:
                    self.new_game()

            if len(self.galaxy.get_entities_by_name("asteroid")) == 0:
                self.score.increase_game_difficulty_by(1.11)
                self.score.update_lives(+1)
                for i in range(NUMBER_ASTEROIDS):
                    self.galaxy.add_entity(Asteroid(self.galaxy))

            time_passed = self.clock.tick(FPS)
            self.fps.update_fps(self.clock.get_fps())
            self.galaxy.update(time_passed, event_list)
            self.galaxy.render(self.screen)
            self.galaxy.cleanup()

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    Game().run()