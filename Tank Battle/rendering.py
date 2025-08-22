import pygame
from random import randint
def draw(image, rec):
    # Загрузка изображения танка (или запасной прямоугольник)
    try:
        tank_img = pygame.image.load(image).convert_alpha()
        # при необходимости измените размер
        tank_img = pygame.transform.scale(tank_img, (rec, rec))
        return tank_img
    except:
        print("Не удалось загрузить изображение, используем прямоугольник. Ошибка")
        tank_img = pygame.Surface((64, 64), pygame.SRCALPHA)
        tank_img.fill((200, 40, 40))
        return tank_img
    
x = randint(0, 1000 // 32 - 1) * 32
y = randint(0, 800 // 32 - 1) * 32

class Bullet:
    """Данные пули"""
    def __init__(self, x, y, angle, speed):
        self.image = draw('images/bullet.png', 9).convert_alpha()
        self.original_image = self.image  
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.angle = angle
    
    def update(self):
        # Вращаем изображение пули в зависимости от угла
        self.image = pygame.transform.rotate(self.original_image, self.angle)  # Вращение изображения (отрицательный угол для правильного вращения)
        self.rect = self.image.get_rect(center=self.rect.center)  # Обновление rect после вращения
        
        # Перемещение пули в зависимости от угла
        if self.angle == 0:  # Вверх
            self.rect.y -= self.speed
        elif self.angle == 180:  # Вниз
            self.rect.y += self.speed
        elif self.angle == 270:  # Вправо
            self.rect.x += self.speed
        elif self.angle == 90:  # Влево
            self.rect.x -= self.speed