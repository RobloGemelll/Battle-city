import pygame, rendering
from config import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, hp, damage, image, reload_time):
        super().__init__()
        self.angle = 0
        self.image = rendering.draw(image, 32).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.hp = hp
        self.damage = damage
        self.reload_time = reload_time
        self.last_shot_time = 0
        self.bullets = []
        self.is_shooting_allowed = True

    """Снаряды"""
    def shoot(self):
        current_time = pygame.time.get_ticks()  # Получаем текущее время в миллисекундах
        if current_time - self.last_shot_time >= self.reload_time:  # Проверяем, прошло ли время перезарядки
            bullet = rendering.Bullet(self.rect.centerx, self.rect.centery, self.angle, speed=10)
            self.bullets.append(bullet)
            self.last_shot_time = current_time  # Обновляем время последнего выстрела
            pygame.mixer.music.load('sounds/shot.wav')
            pygame.mixer.music.play()

    # Коллизия снаряда
    def update_bullets(self):
        for bullet in list(self.bullets):  # Используем list для безопасного удаления элементов
            bullet.update()
            # Удаляем пулю, если она вышла за пределы экрана
            if bullet.rect.x < 0 or bullet.rect.x > 834 or bullet.rect.y < 0 or bullet.rect.y > Windows_Height:
                self.bullets.remove(bullet)

    # Отрисовка снаряда
    def draw_bullets(self, screen):
        for bullet in self.bullets:
            screen.blit(bullet.image, bullet.rect)

    def launch_bullets(self, shoot, x_p, y_p):
        x_e = self.rect.left
        y_e = self.rect.top                
        if x_e == x_p:
            if y_e >= y_p:
                self.angle = 0
                shoot
            elif y_e <= y_p:
                self.angle = 180
                shoot
        elif y_e == y_p:
            if x_e >= x_p:
                self.angle = 90
                shoot
            elif x_e <= x_p:
                self.angle = 270
                shoot

        

