# Class obtained from Raycaster Map Creator Repository
import pygame

class Button():

    def __init__(self, x, y, width, height, font_size=0, font=None, text='', text_color=(0,0,0),
                 border_color=(0,0,0), fill_color=(255,255,255), switch=False, switch_brightness=50):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.text = text
        self.text_color = text_color
        self.font = font
        self.font_size = font_size
        self.border_color = border_color if not switch else fill_color
        self.fill_color = fill_color if not switch else border_color
        self.orginial_color = border_color
        self.switch = switch
        self.switch_brightness = switch_brightness

        self.on = False
        self.clicked = False
        self.color_change = False
        
    
    def update(self, mouse_pos):
        if self.is_mouse_over(mouse_pos):
            if not self.on:
                self.adjust_fill_color(30)
                self.on = True
        elif self.on:
            self.adjust_fill_color(-30)
            self.on = False
        

    def draw(self, screen):
        # Create the outer rectangle
        outer_rect = pygame.Rect((self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, self.border_color, outer_rect)
        
        # Create the inner rectangle
        inner_rect = pygame.Rect((self.x + 5, self.y + 5, self.width - 10, self.height - 10))
        pygame.draw.rect(screen, self.fill_color, inner_rect)
        
        # Render the text
        font = pygame.font.Font(self.font, self.font_size)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=inner_rect.center)
        
        # Draw the text on the screen
        screen.blit(text, text_rect)


    def set_fill_color(self, fill_color):
        self.fill_color = fill_color


    def set_border_color(self, border_color):
        self.border_color = border_color
    

    def set_font(self, font, font_size=None):
        self.font = font
        self.font_size = font_size


    def set_text(self, text, text_color=(0,0,0)):
        self.text = text
        self.text_color = text_color
    

    def button_clicked(self):
        self.clicked = not self.clicked
        if self.switch:
            self.set_fill_color(self.border_color if self.clicked else self.orginial_color)


    def is_switch(self):
        self.switch = not self.switch
    

    def is_mouse_over(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        return self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height
    

    def adjust_fill_color(self, amount):
        if amount > 0:
            self.fill_color = tuple(min(255, x + amount) for x in self.fill_color)
        else:
            self.fill_color = tuple(max(0, x + amount) if x != 255 else 255 for x in self.fill_color)

    def update_buttons(self, display, events):
        mouse_pos = pygame.mouse.get_pos()
        self.draw(display)
        self.update(mouse_pos)
        for event in events:
            if event != None and self.on and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.button_clicked()