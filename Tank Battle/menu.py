
import pygame  # Убедитесь, что импортировали pygame
pygame.font.init()
font1 = pygame.font.Font('fonts/prstart.ttf', 25)


class Menu:
    def __init__(self):  # Исправлено на __init__
        self.option_surfaces = []
        self.callbacks = []
        self.points = []
        self.current_option_index = 0
        self.highlight_image = pygame.image.load("images/tank1 .png")  
        self.highlight_image = pygame.transform.scale(self.highlight_image, (33, 28))  # Измените размер изображения, если нужно
        self.background = pygame.image.load("images/Menu.jpg")
        self.background = pygame.transform.scale(self.background, (1000, 800))
        
    def append_option(self, option, callback):
        self.option_surfaces.append(font1.render(option, True, (255, 255, 255)))
        self.callbacks.append(callback)
    
    def switch(self, direction):
        self.current_option_index = max(0, min(self.current_option_index + direction, len(self.option_surfaces) - 1))
        
    def select(self):
        self.callbacks[self.current_option_index]()
        
    def draw(self, surf, x, y, option_y_padding): 
        surf.blit(self.background, (0, 0))
        for i, option in enumerate(self.option_surfaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x + 55 + self.highlight_image.get_width(), y + i * option_y_padding)  # Сдвигаем текст вправо на ширину изображения
        
            # Рисуем изображение для выбранной опции
            if i == self.current_option_index:
                surf.blit(self.highlight_image, (x + 40, y + i * option_y_padding))  # Рисуем изображение слева от текста
        
            surf.blit(option, option_rect)  # Рисуем текст
            
    def text_point(self, surf, x, y, point):
        text_points = font1.render(point, True, (255, 255, 255))
        surf.blit(text_points, (x, y))
        
 



