from settings import *
from pygame import Color
from button import Button
import pygame

def generateButtons(heights, texts):
    buttons = []
    for i in range(len(heights)):
        button = Button(WINDOW_HALF_WIDTH / 2 - HALF_BUTTON_WIDTH, 
                 heights[i], 
                 BUTTON_WIDTH, 
                 BUTTON_HEIGHT, 
                 int(WINDOW_HEIGHT * 0.05),
                 font='fonts/sonic-advance-2-regular.ttf')

        button.set_border_color(Color('white'))
        button.set_fill_color(Color('black'))
        button.set_text(texts[i], Color('white'))
        buttons.append(button)
    return buttons

class Start:
    def __init__(self, display, gameStateManager):
        pygame.init()
        self.display = display
        self.gameStateManager = gameStateManager
        self.button_heights = [WINDOW_HALF_HEIGHT + HALF_BUTTON_HEIGHT, WINDOW_HALF_HEIGHT + BUTTON_HEIGHT * 1.75]
        self.button_texts = ['Play', 'Quit']

        self.buttons = generateButtons(self.button_heights, self.button_texts)

        self.button1 = self.buttons[0]
        self.button2 = self.buttons[1]

    def run(self, events):
        font = pygame.font.Font('fonts/sonic-advance-2-regular.ttf', int(WINDOW_HEIGHT * 0.1))
        text = font.render('Meteor Mash', True, Color('white'))
        rect = text.get_rect()

        self.display.fill(Color('black'))
        self.display.blit(text, ((WINDOW_HALF_WIDTH / 2) - rect.bottomright[0] * 1/2, int(WINDOW_HEIGHT * 0.25)))

        for button in self.buttons:
            button.update_buttons(self.display, events)
        
        if self.button1.clicked:
            self.gameStateManager.set_state('level')
            self.button1.button_clicked()
        
        if self.button2.clicked:
            pygame.quit()
            exit()

class Pause:
    def __init__(self, display, gameStateManager):
        pygame.init()
        self.display = display
        self.gameStateManager = gameStateManager
        self.button_heights = [WINDOW_HEIGHT * 2/5, WINDOW_HEIGHT * 3/5, WINDOW_HEIGHT * 4/5]
        self.button_texts = ['Resume', 'Settings', 'Quit']

        self.buttons = generateButtons(self.button_heights, self.button_texts)

        self.button3 = self.buttons[0]
        self.button4 = self.buttons[1]
        self.button5 = self.buttons[2]
    
    def run(self, events):
        font = pygame.font.Font('fonts/sonic-advance-2-regular.ttf', int(WINDOW_HEIGHT * 0.025))
        text = font.render('Meteor Mash: Pause Menu', True, Color('white'))

        self.display.fill(Color('black'))
        self.display.blit(text, (0, 0))

        for button in self.buttons:
            button.update_buttons(self.display, events)
        
        if self.button3.clicked:
            self.gameStateManager.set_state('level')
            self.button3.button_clicked()
        
        if self.button4.clicked:
            self.gameStateManager.set_state('settings')
            self.button4.button_clicked()
        
        if self.button5.clicked:
            pygame.quit()
            exit()

class Setting:
    def __init__(self, display, gameStateManager):
        pygame.init()
        self.display = display
        self.gameStateManager = gameStateManager
    
    def run(self, events):
        font = pygame.font.Font('fonts/sonic-advance-2-regular.ttf', int(WINDOW_HEIGHT * 0.025))
        text = font.render('Meteor Mash: Settings', True, Color('white'))

        self.display.fill(Color('black'))
        self.display.blit(text, (0, 0))

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.gameStateManager.set_state('pause')