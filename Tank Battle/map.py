import pygame

class Block:
    def __init__(self, px, py, size, window, objects, image):
        self.objects = objects
        self.window = window
        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1
        self.image = pygame.image.load(image).convert_alpha()  # Замените на путь к вашему изображению
        self.image = pygame.transform.scale(self.image, (size, size))  # Масштабируем изображение под размер блока


    def draw(self):
        self.window.blit(self.image, self.rect.topleft)


    def damage(self, value):
        self.hp -= value
        if self.hp <= 0: self.objects.remove(self)
        
        
