import pygame, rendering
from config import *

pygame.mixer.init()

            
class Player_Multiplayer:
    """Данные танка"""
    def __init__(self, speed, damage, image, hp, reload_time, objects, x, y):
        self.speed = speed #Скорость танка
        self.damage = damage #Урон танка
        self.hp = hp  #Хп танка
        self.x = x #Координата танка x
        self.y = y #Координата танка y
        self.angle = 0  # Начальный угол поворота танка
        self.tank_img = rendering.draw(image, 32).convert_alpha() #Картинка танка
        self.tank_rect = self.tank_img.get_rect(center=(self.x, self.y)) #Для коллизии и отрисовки танка
        self.reload_time = reload_time #Время перезарядки
        self.last_shot_time = 0 #Время последнего выстрела
        self.objects = objects #Словарь блоков 
        self.bullets = [] #Список пуль
        self.is_moving = False
        
        """Звуки"""
        self.move_not = pygame.mixer.Sound('sounds/engine.wav')
        self.move = pygame.mixer.Sound('sounds/move.wav')
        self.start = pygame.mixer.Sound('sounds/level_start.mp3')
        self.damage_brick  = pygame.mixer.Sound('sounds/damage_brick.wav')
        self.move_not.play(-1)

    """Звуки"""
    #! Остановить все звуки
    def stop_sounds(self):
        
        self.move_not.stop()
        self.move.stop()
        self.start.stop()
        self.damage_brick.stop()
    #* Старт игры (Звуки)"  
    def start_sounds(self):
        self.start.play()
        
    def movement_one(self, objects):
        keys = pygame.key.get_pressed()
        original_rect = self.tank_rect.copy()
        moving = False
    
        # Движение танка
        if keys[pygame.K_w]:  # Вверх
            self.angle = 0
            self.tank_rect.y -= self.speed
            moving = True
        elif keys[pygame.K_s]:  # Вниз
            self.angle = 180
            self.tank_rect.y += self.speed
            moving = True
        elif keys[pygame.K_d]:  # Вправо
            self.angle = 270
            self.tank_rect.x += self.speed
            moving = True
        elif keys[pygame.K_a]:  # Влево
            self.angle = 90
            self.tank_rect.x -= self.speed
            moving = True

        if moving != self.is_moving:
            if moving:
                self.move_not.stop()
                self.move.play(-1)  # Запускаем звук
            else:
                self.move.stop()  # Останавливаем звук
                self.move_not.play(-1)
            self.is_moving = moving
            
        
        # Ограничение внутри окна
        self.tank_rect.clamp_ip(pygame.Rect(0, 0, Windows_Wight_field, Windows_Height))
        
        for obj_type in ['armor', 'brick', 'water']:
            for obj in objects[obj_type]:
                if self.tank_rect.colliderect(obj.rect):
                    self.tank_rect = original_rect
                    break
       
            
        self.base_speed = 1
        for obj in objects['ice']:
            
            if self.tank_rect.colliderect(obj.rect):
                self.speed -= 1
                break
            else:
                self.speed = self.base_speed
                
    def movement_two(self, objects):
        keys = pygame.key.get_pressed()
        original_rect = self.tank_rect.copy()
        moving = False
    
        # Движение танка
        if keys[pygame.K_UP]:  # Вверх
            self.angle = 0
            self.tank_rect.y -= self.speed
            moving = True
        elif keys[pygame.K_DOWN]:  # Вниз
            self.angle = 180
            self.tank_rect.y += self.speed
            moving = True
        elif keys[pygame.K_RIGHT]:  # Вправо
            self.angle = 270
            self.tank_rect.x += self.speed
            moving = True
        elif keys[pygame.K_LEFT]:  # Влево
            self.angle = 90
            self.tank_rect.x -= self.speed
            moving = True

        if moving != self.is_moving:
            if moving:
                self.move_not.stop()
                self.move.play(-1)  # Запускаем звук
            else:
                self.move.stop()  # Останавливаем звук
                # self.move_not.play(-1)
            self.is_moving = moving
            
        
        # Ограничение внутри окна
        self.tank_rect.clamp_ip(pygame.Rect(0, 0, Windows_Wight_field, Windows_Height))
        
        for obj_type in ['armor', 'brick', 'water']:
            for obj in objects[obj_type]:
                if self.tank_rect.colliderect(obj.rect):
                    self.tank_rect = original_rect
                    break
       
            
        self.base_speed = 1
        for obj in objects['ice']:
            
            if self.tank_rect.colliderect(obj.rect):
                self.speed -= 1
                break
            else:
                self.speed = self.base_speed
    
    """Снаряды"""
    def shoot(self):
        current_time = pygame.time.get_ticks()  # Получаем текущее время в миллисекундах
        if current_time - self.last_shot_time >= self.reload_time:  # Проверяем, прошло ли время перезарядки
            bullet = rendering.Bullet(self.tank_rect.centerx, self.tank_rect.centery, self.angle, speed=10)
            self.bullets.append(bullet)
            self.last_shot_time = current_time  # Обновляем время последнего выстрела
            pygame.mixer.music.load('sounds/shot.wav')
            pygame.mixer.music.play()
            
    # Коллизия снаряда
    def update_bullets(self):
        for bullet in list(self.bullets):  # Используем list для безопасного удаления элементов
            bullet.update()
            # Удаляем пулю, если она вышла за пределы экрана
            if bullet.rect.x < 0 or bullet.rect.x > Windows_Wight_field or bullet.rect.y < 0 or bullet.rect.y > Windows_Height:
                self.bullets.remove(bullet)
            for obj in self.objects['brick']:
                if bullet.rect.colliderect(obj.rect):
                    self.objects['brick'].remove(obj)  # Удаляем блок
                    self.bullets.remove(bullet)  # Удаляем пулю
                    break  # Прерываем цикл после удаления
                
            for obj in self.objects['armor']:
                if bullet.rect.colliderect(obj.rect):
                    self.bullets.remove(bullet)  # Удаляем пулю
                    break  # Прерываем цикл после удаления
    # Отрисовка снаряда
    def draw_bullets(self, screen):
        for bullet in self.bullets:
            screen.blit(bullet.image, bullet.rect)