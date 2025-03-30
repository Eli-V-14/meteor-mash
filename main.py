import pygame 

from settings import *
from gameStateManager import GameStateManager
from level import Level
from menus import Start, Pause, Setting


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen = pygame.display.set_mode((WINDOW_HALF_WIDTH, WINDOW_HEIGHT))
        # self.delta_time = self.clock.tick(60) / 1000

        pygame.display.flip()

        self.gameStartManager = GameStateManager('start')
        self.start = Start(self.screen, self.gameStartManager)
        self.level = Level(self.screen, self.gameStartManager)
        self.pause = Pause(self.screen, self.gameStartManager)
        self.settings = Setting(self.screen, self.gameStartManager)

        self.states = {'start':self.start,
                       'level':self.level,
                       'pause':self.pause,
                       'settings':self.settings}
    
    def run(self):
        

        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.delta_time = self.clock.tick(60) / 1000
            
            self.states[self.gameStartManager.get_state()].run(events, self.delta_time)

            fps = self.clock.get_fps()

            pygame.display.set_caption(f"FPS: {fps:.2f}")

            pygame.display.update()

            
    
if __name__ == '__main__':
    # print(pygame.font.get_fonts())
    game = Game()
    game.run()
    