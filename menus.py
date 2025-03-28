from settings import *
from pygame import Color
from button import Button
import pygame

button1 = Button(WINDOWN_HALF_WIDTH / 2 - HALF_BUTTON_WIDTH, 
                 WINDOW_HALF_HEIGHT + HALF_BUTTON_HEIGHT, 
                 BUTTON_WIDTH, 
                 BUTTON_HEIGHT, 
                 int(WINDOW_HEIGHT * 0.05),
                 font='fonts/sonic-advance-2-regular.ttf')

button1.set_border_color(Color('white'))
button1.set_fill_color(Color('black'))
button1.set_text('Play', Color('white'))

button2 = Button(WINDOWN_HALF_WIDTH / 2 - HALF_BUTTON_WIDTH, 
                WINDOW_HALF_HEIGHT + BUTTON_HEIGHT * 1.75, 
                BUTTON_WIDTH, 
                BUTTON_HEIGHT, 
                int(WINDOW_HEIGHT * 0.05),
                 font='fonts/sonic-advance-2-regular.ttf')

button2.set_border_color(Color('white'))
button2.set_fill_color(Color('black'))
button2.set_text('Quit', Color('white'))



class Start:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.buttons = [button1, button2]

    def run(self, events):
        font = pygame.font.Font('fonts/sonic-advance-2-regular.ttf', int(WINDOW_HEIGHT * 0.1))
        text = font.render('Meteor Mash', True, Color('white'))
        rect = text.get_rect()

        self.display.fill(Color('black'))
        self.display.blit(text, ((WINDOWN_HALF_WIDTH / 2) - rect.bottomright[0] * 1/2, int(WINDOW_HEIGHT * 0.25)))

        for button in self.buttons:
            button.update_buttons(self.display, events)
        
        if button1.clicked:
            self.gameStateManager.set_state('level')
            button1.button_clicked()
        
        if button2.clicked:
            pygame.quit()

button3 = Button(WINDOWN_HALF_WIDTH / 2 - HALF_BUTTON_WIDTH, 
                 WINDOW_HEIGHT * 2/5, 
                 BUTTON_WIDTH, 
                 BUTTON_HEIGHT, 
                 int(WINDOW_HEIGHT * 0.05),
                 font='fonts/sonic-advance-2-regular.ttf')

button3.set_border_color(Color('white'))
button3.set_fill_color(Color('black'))
button3.set_text('Resume', Color('white'))

button4 = Button(WINDOWN_HALF_WIDTH / 2 - HALF_BUTTON_WIDTH, 
                 WINDOW_HEIGHT * 3/5, 
                 BUTTON_WIDTH, 
                 BUTTON_HEIGHT, 
                 int(WINDOW_HEIGHT * 0.05),
                 font='fonts/sonic-advance-2-regular.ttf')

button4.set_border_color(Color('white'))
button4.set_fill_color(Color('black'))
button4.set_text('Settings', Color('white'))

button5 = Button(WINDOWN_HALF_WIDTH / 2 - HALF_BUTTON_WIDTH, 
                 WINDOW_HEIGHT * 4/5, 
                 BUTTON_WIDTH, 
                 BUTTON_HEIGHT, 
                 int(WINDOW_HEIGHT * 0.05),
                 font='fonts/sonic-advance-2-regular.ttf')

button5.set_border_color(Color('white'))
button5.set_fill_color(Color('black'))
button5.set_text('Quit', Color('white'))

class Pause:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.buttons = [button3, button4, button5]
    
    def run(self, events):
        font = pygame.font.Font('fonts/sonic-advance-2-regular.ttf', int(WINDOW_HEIGHT * 0.025))
        text = font.render('Meteor Mash: Pause Menu', True, Color('white'))

        self.display.fill(Color('black'))
        self.display.blit(text, (0, 0))

        for button in self.buttons:
            button.update_buttons(self.display, events)
        
        if button3.clicked:
            self.gameStateManager.set_state('level')
            button3.button_clicked()
        
        if button4.clicked:
            self.gameStateManager.set_state('settings')
            button4.button_clicked()
        
        if button5.clicked:
            pygame.quit()

class Setting:
    def __init__(self, display, gameStateManager):
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