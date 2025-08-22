import pygame
from config import *
from tank_player import Player
from random import randint
from map import Block
from menu import Menu
from enemies import Enemy
from tank_player_two import *

pygame.init()
pygame.mixer.init()

"""Окно и сцены"""
screen = pygame.display.set_mode((Windows_Wight, Windows_Height))
pygame.display.set_caption("Battle City")
clock = pygame.time.Clock()
background = pygame.image.load('images/Fon.jpg')
background = pygame.transform.scale(background, (1000, 800))


current_scene = None
def switch_scene(scene):
    global current_scene
    current_scene = scene



# Списки блоков 
objects = {
    'armor': [],
    'brick': [],
    'bushes': [],
    'ice': [],
    'water': []
}
def generate_blocks(block_type, image_path):
        for _ in range(5):
            while True:
                x = randint(0, 834 // 32 - 1) * 32
                y = randint(0, 800 // 32 - 1) * 32
                rect = pygame.Rect(x, y, 32, 32)
            
                # Проверка на пересечение с другими объектами
                if not any(rect.colliderect(obj.rect) for block_list in objects.values() for obj in block_list):
                    block = Block(x, y, 32, screen, objects[block_type], image_path)
                    objects[block_type].append(block)  # Добавляем блок в соответствующий список объектов
                    break
def map():

    """Генерация блоков на карте"""#Временно
    

        # Генерация блоков для каждого типа
    for block_type, image_path in zip(objects.keys(), 
                                        ['images/block_armor.png', 'images/block_brick.png', 
                                            'images/block_bushes.png', 'images/block_ice.png', 
                                            'images/block_water.png']):
        generate_blocks(block_type, image_path)
    
 
    
"""Сцена 1 Меню"""
def scene1():
    running = True
    menu = Menu()
    menu.append_option('1 PLAYER',lambda: switch_scene(scene2)) 
    menu.append_option('2 PLAYER', lambda: switch_scene(scene3))
    menu.append_option('SETTINGS', lambda: switch_scene(scene4))
    menu.append_option('EXIT', quit)

    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    menu.switch(-1)
                elif event.key == pygame.K_s:
                    menu.switch(1)
                elif event.key == pygame.K_d:
                    menu.select()
                    running = False 


        
        menu.draw(screen, 350, 455, 55)
        menu.text_point(screen, 260,50, '100000')
        menu.text_point(screen, 210,50, 'I-')
        menu.text_point(screen, 435,50, 'HI-')
        menu.text_point(screen, 505,50, '100000')
        pygame.display.flip()
        clock.tick(60)


"""Сцена 2 Одиночный режим"""
def scene2():
    map()
    """Игрок для одиночного режима"""
    enemy_gr = pygame.sprite.Group()
    a= Enemy(200,200, 1, 100,1,'images/tank1.png', 1500)
    players = []  # Инициализация списка игроков
    player_tank = Player(speed=2, damage=10, image='images/tank1.png', hp=100,
                         reload_time=650, objects=objects, x=300, y=300)
    players.clear()
    players.append(player_tank)

    # Запуск звуков для всех игроков
    for player in players:
        player.start_sounds()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Выход
                for player in players:
                    player.stop_sounds()
                for key in objects.keys():
                    objects[key].clear()
                players.clear()    
                running = False
                switch_scene(None)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Смена сцены
                    for player in players:
                        player.stop_sounds()
                    for key in objects.keys():
                        objects[key].clear()
                    players.clear()
                    switch_scene(scene1)
                    running = False

                elif event.key == pygame.K_SPACE:  # Стрельба
                    for player in players:
                        player.shoot()
            


        # Отрисовка карты
        screen.blit(background, (0,0))
        a.update_bullets()

        # Отрисовка объектов на карте кроме кустов
        for block_list in objects.values():
            if block_list != objects['bushes']:  # Пропускаем кусты
                for obj in block_list:
                    obj.draw()

        # Обновление состояния и отрисовка танков игроков
        for player in players:
            player.movement(objects)  # Обновление состояния игрока
            player.update_bullets()    # Обновление пуль
            player.draw_bullets(screen) # Отрисовка пуль
            rotated_tank_img = pygame.transform.rotate(player.tank_img, player.angle)
            rotated_rect = rotated_tank_img.get_rect(center=player.tank_rect.center)
            x_p = rotated_rect.left
            y_p = rotated_rect.top
            screen.blit(rotated_tank_img, rotated_rect.topleft)
            
            
            
        rotated_img = pygame.transform.rotate(a.image, a.angle)
        rotated_rect1 = rotated_tank_img.get_rect(center=a.rect.center)
        x_e = rotated_rect1.left
        y_e = rotated_rect1.top
        screen.blit(rotated_img,rotated_rect1)
        for player in players:
            a.launch_bullets(a.shoot(), x_p, y_p)
        a.draw_bullets(screen)
        
        
        
        # Отрисовка кустов
        for bush in objects['bushes']:
            bush.draw()
        pygame.display.flip()
        clock.tick(60)

        
          
"""Сцена 3 Совместный режим """       
def scene3(): 
    map()
    """Игроки для совместного режима"""
    players2 = []
    players2.clear()
    player_tank = Player_Multiplayer(speed=1, damage=10, image='images/tank1.png', hp=100,
                         reload_time=1000, objects=objects, x=100, y=100)
    players2.append(player_tank)
    player_tank.stop_sounds()
    player_tank1 = Player_Multiplayer(speed=1, damage=10, image='images/tank1.png', hp=100,
                         reload_time=1000, objects=objects, x=200, y=200)
    players2.append(player_tank1)
    player_tank1.stop_sounds()
    

    # Запускаем звуки только для первого игрока
    if players2:
        players2[0].start_sounds()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for player in players2:
                    player.stop_sounds()
                for key in objects.keys():
                        objects[key].clear()
                players2.clear()
                running = False
                switch_scene(None)
                
                # Смена сцены на сцену 1
            elif event.type == pygame.KEYDOWN:    
                if event.key == pygame.K_q:
                    for player in players2:
                        player.stop_sounds()
                    for key in objects.keys():
                        objects[key].clear()
                    players2.clear()
                    players2.clear()
                    switch_scene(scene1)
                    running = False
                elif event.key == pygame.K_SPACE:
                    players2[0].shoot()
                elif event.key == pygame.K_RETURN:
                    players2[1].shoot()

        # Отрисовка карты
        screen.blit(background, (0,0))

        # Отрисовка объектов на карте кроме кустов
        for block_list in objects.values():
            if block_list != objects['bushes']:
                for obj in block_list:
                    obj.draw()

        # Отрисовка танков игроков
        for player in players2:
            rotated_tank_img = pygame.transform.rotate(player.tank_img, player.angle)
            rotated_rect = rotated_tank_img.get_rect(center=player.tank_rect.center)
            screen.blit(rotated_tank_img, rotated_rect.topleft)

            # Обновление состояния игрока
            players2[0].movement_one(objects)
            players2[1].movement_two(objects)
            player.update_bullets()
            player.draw_bullets(screen)

        # Отрисовка кустов
        for bush in objects['bushes']:
            bush.draw()

        pygame.display.flip()
        clock.tick(60)

    # Остановка звуков при выходе из сцены
    for player in players2:
        player.stop_sounds()


"""Сцена 4 Меню настроек (Несделано)"""
def scene4():
    print(1)




"""Запуск сцен"""
switch_scene(scene1)  # Начинаем с первой сцены
while current_scene is not None:
    current_scene()  # Вызов текущей сцены

pygame.quit()
