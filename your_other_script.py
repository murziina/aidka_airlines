import pygame
import random
import time
import os
import subprocess  # Добавьте этот импорт в начало файла

# Инициализация Pygame
pygame.init()

# Инициализация микшера Pygame
pygame.mixer.init()

# Загрузка фоновой музыки
pygame.mixer.music.load("background_music1.mp3")  # Замените на имя файла с первой фоновой музыкой
pygame.mixer.music.set_volume(0.0)  # Начальная громкость 0
pygame.mixer.music.play(-1)  # -1 означает бесконечное повторение

# Загрузка второго фонового звука
background_music2 = pygame.mixer.Sound("background_music2.mp3")  # Замените на имя файла со второй фоновой музыкой
background_music2.set_volume(0.0)  # Начальная громкость 0
background_music2.play(-1)  # -1 означает бесконечное повторение

# Загрузка звука столкновения
try:
    collision_sound = pygame.mixer.Sound("collision_sound.mp3")  # Замените на имя файла со звуком столкновения
except pygame.error as e:
    print(f"Ошибка загрузки звука столкновения: {e}")
    collision_sound = None

# Размеры окна
width = 1500
height = 1000
screen = pygame.display.set_mode((width, height))


# Загрузка изображения текстуры земли
ground_img = pygame.image.load("земля.png").convert_alpha()  # Замените на имя файла с текстурой земли

# Параметры земли
ground_x = 0  # Начальная позиция земли по оси X
ground_speed = 2  # Скорость движения земли

# Загрузка изображений
player_img = pygame.image.load("самолет.png").convert_alpha()  # Замени на имя файла с самолетом
cloud_img1 = pygame.image.load("облако1.png").convert_alpha() # Замени на имя файла с облаком 1
cloud_img2 = pygame.image.load("облако2.png").convert_alpha() # Замени на имя файла с облаком 2
cloud_img3 = pygame.image.load("облако3.png").convert_alpha() # Замени на имя файла с облаком 3

# Загрузка изображения сердечка
heart_img = pygame.image.load("heart.png").convert_alpha()  # Замени на имя файла с изображением сердечка

# Игрок
player_x = 100
player_y = height // 2
player_speed = 2

# Облака
clouds = []
for i in range(5):
    cloud_x = random.randint(width, width + 500)
    cloud_y = random.randint(100, height - 200)  # Измените диапазон координат Y
    cloud_speed = random.randint(1, 3)
    cloud_type = random.choice([cloud_img1, cloud_img2, cloud_img3])  # Случайный тип облака
    clouds.append([cloud_x, cloud_y, cloud_speed, cloud_type])
    
# Счетчик дистанции
distance = 0
font = pygame.font.Font(None, 36)

# Функция отображения текста
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Создание шрифта для обратного отсчета
countdown_font = pygame.font.Font(None, 100)  # Измените размер шрифта здесь

# Параметры громкости
max_volume = 0.2  # Максимальная громкость
fade_speed = 0.01  # Скорость затухания и увеличения громкости

# Функция плавного увеличения громкости
def fade_in(sound, speed, max_volume):
    volume = sound.get_volume()
    while volume < max_volume:
        volume += speed
        if volume > max_volume:
            volume = max_volume
        sound.set_volume(volume)
        time.sleep(0.01)

# Параметры земли
ground_x = 500  # Начальная позиция земли по оси X
ground_speed = 1.5  # Скорость движения земли
ground_images = []  # Список для хранения копий текстур земли и их позиций по оси X

# Заполним список начальными позициями текстур земли
for i in range(6):  # Количество текстур земли
    ground_images.append(i * ground_img.get_width())

# Обратный отсчёт перед началом игры
for i in range(3, 0, -1):
    screen.fill((135, 206, 250))  # Голубой фон неба
    draw_text(str(i), countdown_font, (0, 0, 0), screen, width // 2, height // 2)
    pygame.display.flip()
    fade_in(pygame.mixer.music, fade_speed, max_volume)
    fade_in(background_music2, fade_speed, max_volume)
    time.sleep(0.5)

# Переменная для ограничения движения вниз
max_player_y = height - player_img.get_height() - ground_img.get_height()

# Игровой цикл
running = True
collision_time = 0
collision_duration = 3  # Длительность эффекта столкновения в секундах
collision_occurred = False  # Флаг для отслеживания состояния столкновения
lives = 3  # Количество жизней

# Деревья и дома
buildings = []
building_speed = 1.5  # Скорость движения зданий
building_images = []

# --- Настройки спавна зданий ---
building_spawn_rate = 150  # Каждые 150 пикселей дистанции будет появляться новое здание
last_building_spawn = 0  # Переменная для отслеживания последнего спавна здания

# Загружаем все изображения из папки "hom"
for filename in os.listdir("hom"):
    if filename.endswith(".png"):
        img = pygame.image.load(os.path.join("hom", filename)).convert_alpha()
        building_images.append(img)

building_baseline = 100  # Расстояние от нижней границы экрана до линии зданий


# --- Настройки спавна зданий ---
min_spawn_delay = 2  # Минимальная задержка между спавнами в секундах
max_spawn_delay = 10  # Максимальная задержка между спавнами в секундах
last_building_spawn_time = time.time()  # Время последнего спавна


while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление самолетом
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_y -= player_speed if collision_time == 0 else player_speed // 2
    if keys[pygame.K_DOWN]:
        player_y += player_speed if collision_time == 0 else player_speed // 2

    # Проверка выхода за границы экрана
    if player_y < 0:
        player_y = 0
    elif player_y > max_player_y:
        player_y = max_player_y

    # Движение облаков
    for cloud in clouds:
        cloud[0] -= cloud[2]
        if cloud[0] < -cloud[3].get_width():
            cloud[0] = random.randint(width, width + 500)
            cloud[1] = random.randint(100, height - 200)  # Измените диапазон координат Y
            cloud[2] = random.randint(1, 3)
            cloud[3] = random.choice([cloud_img1, cloud_img2, cloud_img3])  # Новый тип облака

    # --- Спавн зданий ---
    current_time = time.time()
    time_since_last_spawn = current_time - last_building_spawn_time
    if time_since_last_spawn >= min_spawn_delay and len(buildings) < 3:  # <--- Добавь эту проверку
        building_image = random.choice(building_images)
        building_x = width + building_image.get_width()
        building_y = height - building_baseline - building_image.get_height()
        buildings.append([building_x, building_y, building_image])
        last_building_spawn_time = current_time
        # Сбрасываем таймер с учетом случайной задержки
        min_spawn_delay = random.uniform(1, 5)  
    
    # --- Движение зданий ---
    for building in buildings:
        building[0] -= building_speed
        # Удаляем здания, ушедшие за левый край
        if building[0] < -building[2].get_width():
            buildings.remove(building)
    
    # Проверка столкновений
    player_rect = pygame.Rect(player_x, player_y, player_img.get_width(), player_img.get_height())
    for cloud in clouds:
        cloud_rect = pygame.Rect(cloud[0], cloud[1], cloud[3].get_width(), cloud[3].get_height())
        if player_rect.colliderect(cloud_rect) and not collision_occurred:
            if collision_sound:
                collision_sound.play()  # Проигрываем звук столкновения
            collision_time = time.time()  # Устанавливаем время столкновения
            collision_occurred = True  # Устанавливаем флаг столкновения
            lives -= 1  # Уменьшаем количество жизней
            # Отбрасываем самолетик вверх или вниз
            if random.choice([True, False]):
                player_y -= 50  # Отбрасываем вверх
            else:
                player_y += 50  # Отбрасываем вниз
            player_y = max(0, min(player_y, height - player_img.get_height()))  # Проверка выхода за границы экрана

    # Проверка окончания игры
    if lives <= 0:
        running = False

    # Обновление счетчика дистанции
    distance += 0.1

    # Отрисовка
    screen.fill((135, 206, 250))  # Голубой фон неба
    screen.blit(player_img, (player_x, player_y))
    for cloud in clouds:
        screen.blit(cloud[3], (cloud[0], cloud[1]))  # Отрисовка облака с учетом его типа

         # Движение земли и проверка, не ушла ли она за левый край экрана
    for i in range(len(ground_images)):
        ground_images[i] -= ground_speed
        if ground_images[i] <= -ground_img.get_width():
            # Перемещаем текстуру в конец списка, чтобы создать эффект непрерывности
            ground_images[i] += ground_img.get_width() * len(ground_images)

    # Отрисовка земли
    center_offset = 400  # Смещение ниже центра, можете настроить по вашему усмотрению
    ground_y = (height // 2) + center_offset  # Вычисляем Y так, чтобы земля была ниже центра на center_offset пикселей

    # Отрисовка всех текстур земли
    for ground_x in ground_images:
        screen.blit(ground_img, (ground_x, ground_y))

    # Отрисовка зданий
    for building_x, building_y, building_image in buildings:
        screen.blit(building_image, (building_x, building_y))
    
    # Отображение дистанции
    distance_text = font.render("Дистанция: " + str(int(distance)), True, (0, 0, 0))
    screen.blit(distance_text, (10, 10))

    # Отображение жизней
    for i in range(lives):
        screen.blit(heart_img, (width - (i + 1) * (heart_img.get_width() + 10), 10))

    # Обновление экрана
    pygame.display.flip()

    # Эффект тряски и замедления управления
    if collision_occurred:
        elapsed_time = time.time() - collision_time
        if elapsed_time < collision_duration:
            player_x += random.randint(-5, 5)  # Тряска самолета
        else:
            collision_occurred = False  # Сбрасываем флаг столкновения

# Завершение Pygame
pygame.quit()

# Запись результата в файл
results_file = "results.txt"
if not os.path.exists(results_file):
    with open(results_file, "w") as file:
        file.write(f"Дистанция: {int(distance)}\n")
else:
    with open(results_file, "a") as file:
        file.write(f"Дистанция: {int(distance)}\n")
        
# Запуск файла menu.py после записи результата
subprocess.run(["python", "menu.py"])