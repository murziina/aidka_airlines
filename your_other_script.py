import pygame
import random

# Инициализация Pygame
pygame.init()

# Размеры окна
width = 1500
height = 1000
screen = pygame.display.set_mode((width, height))

# Загрузка изображений
player_img = pygame.image.load("самолет.png").convert_alpha()  # Замени на имя файла с самолетом
cloud_img1 = pygame.image.load("облако1.png").convert_alpha() # Замени на имя файла с облаком 1
cloud_img2 = pygame.image.load("облако2.png").convert_alpha() # Замени на имя файла с облаком 2
cloud_img3 = pygame.image.load("облако3.png").convert_alpha() # Замени на имя файла с облаком 3

# Игрок
player_x = 100
player_y = height // 2
player_speed = 2

# Облака
clouds = []
for i in range(5):
    cloud_x = random.randint(width, width + 500)
    cloud_y = random.randint(0, height - 100)
    cloud_speed = random.randint(1, 3)
    cloud_type = random.choice([cloud_img1, cloud_img2, cloud_img3])  # Случайный тип облака
    clouds.append([cloud_x, cloud_y, cloud_speed, cloud_type])

# Счетчик дистанции
distance = 0
font = pygame.font.Font(None, 36)

# Игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление самолетом
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Проверка выхода за границы экрана
    if player_y < 0:
        player_y = 0
    elif player_y > height - player_img.get_height():
        player_y = height - player_img.get_height()

    # Движение облаков
    for cloud in clouds:
        cloud[0] -= cloud[2]
        if cloud[0] < -cloud[3].get_width():
            cloud[0] = random.randint(width, width + 500)
            cloud[1] = random.randint(0, height - 100)
            cloud[2] = random.randint(1, 3)
            cloud[3] = random.choice([cloud_img1, cloud_img2, cloud_img3])  # Новый тип облака

    # Проверка столкновений
    player_rect = pygame.Rect(player_x, player_y, player_img.get_width(), player_img.get_height())
    for cloud in clouds:
        cloud_rect = pygame.Rect(cloud[0], cloud[1], cloud[3].get_width(), cloud[3].get_height())
        if player_rect.colliderect(cloud_rect):
            running = False  # Игра окончена

    # Обновление счетчика дистанции
    distance += 0.1

    # Отрисовка
    screen.fill((135, 206, 250))  # Голубой фон неба
    screen.blit(player_img, (player_x, player_y))
    for cloud in clouds:
        screen.blit(cloud[3], (cloud[0], cloud[1]))  # Отрисовка облака с учетом его типа
    
    # Отображение дистанции
    distance_text = font.render("Дистанция: " + str(int(distance)), True, (0, 0, 0))
    screen.blit(distance_text, (10, 10))

    # Обновление экрана
    pygame.display.flip()

# Завершение Pygame
pygame.quit()