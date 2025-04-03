import pygame 

from settings import *
from gameStateManager import GameStateManager
from dqn_level import Level
from menus import Start, Pause, Setting, Lost


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen = pygame.display.set_mode((WINDOW_HALF_WIDTH, WINDOW_HEIGHT))

        pygame.display.flip()

        self.gameStartManager = GameStateManager('start')
        self.start = Start(self.screen, self.gameStartManager)
        self.level = Level(self.screen, self.gameStartManager)
        self.pause = Pause(self.screen, self.gameStartManager)
        self.settings = Setting(self.screen, self.gameStartManager)
        self.lost = Lost(self.screen, self.gameStartManager, self.level)

        self.states = {'start':self.start,
                       'level':self.level,
                       'pause':self.pause,
                       'settings':self.settings,
                       'lost': self.lost}
    
    def step(self, action_step=4):
        while self.running: 
            if self.gameStartManager.get_state() == 'start':
                self.start.button1.button_clicked()
            
            action = action_step

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                action = 0
            if keys[pygame.K_RIGHT]:
                action = 1
            if keys[pygame.K_w]:
                action = 2

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit() 
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        action = 3

            observation, reward, terminated, truncated, info = self.level.step(action)

            self.delta_time = self.clock.tick(60) / 1000
            self.states[self.gameStartManager.get_state()].run(events, self.delta_time)

            fps = self.clock.get_fps()

            pygame.display.set_caption(f"FPS: {fps:.2f}")
            pygame.display.update()

            # return observation, reward, terminated, truncated, info 

def main():
    """ Main loop for running the game manually """
    game = Game()
    
    while game.running:
        obs, reward, terminated, truncated, info = game.step()

        # if terminated:
        #     game.level.restart()

if __name__ == '__main__':
    # print(pygame.font.get_fonts())
    game = Game()
    game.step()
    