import pygame
import random
import subprocess

# Инициализация Pygame
pygame.init()

# Размеры окна
width = 1500
height = 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Меню игры")

# Цвет фона
sky_blue = (135, 206, 250)

# Загрузка изображений облаков
cloud_image_1 = pygame.image.load('облако2.png')
cloud_image_2 = pygame.image.load('облако3.png')

# Масштабирование изображений облаков
cloud_image_1 = pygame.transform.scale(cloud_image_1, (100, 100))
cloud_image_2 = pygame.transform.scale(cloud_image_2, (100, 100))

# Настройки облаков
cloud_rects_1 = [cloud_image_1.get_rect(topleft=(random.randint(0, width), random.randint(0, height))) for _ in range(10)]
cloud_speeds_1 = [(random.choice([-1, 1]), random.choice([-1, 1])) for _ in range(10)]

cloud_rects_2 = [cloud_image_2.get_rect(topleft=(random.randint(0, width), random.randint(0, height))) for _ in range(10)]
cloud_speeds_2 = [(random.choice([-1, 1]), random.choice([-1, 1])) for _ in range(10)]

# Шрифт для кнопок и таблицы рекордов
font = pygame.font.Font(None, 74)

# Инициализация музыки
pygame.mixer.init()
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

# Функция для отображения текста
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Функция для рисования прямоугольников с закругленными углами
def draw_rounded_rect(surface, rect, color, corner_radius):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect(), border_radius=corner_radius)
    surface.blit(shape_surf, rect.topleft)

# Функция для чтения данных из файла и сортировки
def read_records(file_path):
    distances = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("Дистанция:"):
                distance = int(line.split(":")[1].strip())
                distances.append(distance)
    distances.sort(reverse=True)
    return distances

# Основной цикл игры
running = True
music_on = True
while running:
    screen.fill(sky_blue)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if start_button.collidepoint(mouse_pos):
                print("СТАРТ")
                pygame.quit()
                subprocess.run(["python", "your_other_script.py"])
                exit()
            elif records_button.collidepoint(mouse_pos):
                print("РЕКОРДЫ")
                distances = read_records('results.txt')  # Изменено на правильное имя файла
                top_distances = distances[:3]
                total_attempts = len(distances)
                screen.fill(sky_blue)
                draw_text('Top 3 :', font, (0, 0, 0), screen, width // 2 - 200, height // 2 - 200)
                for i, distance in enumerate(top_distances):
                    draw_text(f'{i+1}. {distance}', font, (0, 0, 0), screen, width // 2 - 50, height // 2 - 100 + i * 50)
                draw_text(f'Всего попыток: {total_attempts}', font, (0, 0, 0), screen, width // 2 - 200, height // 2 + 100)
                pygame.display.flip()
                pygame.time.wait(5000)  # Задержка для отображения таблицы рекордов
            elif music_button.collidepoint(mouse_pos):
                if music_on:
                    pygame.mixer.music.pause()
                    music_on = False
                else:
                    pygame.mixer.music.unpause()
                    music_on = True

    # Обновление положения облаков
    for i, rect in enumerate(cloud_rects_1):
        rect.x += cloud_speeds_1[i][0]
        rect.y += cloud_speeds_1[i][1]
        if rect.left < 0 or rect.right > width:
            cloud_speeds_1[i] = (-cloud_speeds_1[i][0], cloud_speeds_1[i][1])
        if rect.top < 0:
            cloud_speeds_1[i] = (cloud_speeds_1[i][0], -cloud_speeds_1[i][1])
        screen.blit(cloud_image_1, rect)

    for i, rect in enumerate(cloud_rects_2):
        rect.x += cloud_speeds_2[i][0]
        rect.y += cloud_speeds_2[i][1]
        if rect.left < 0:
            cloud_speeds_2[i] = (-cloud_speeds_2[i][0], cloud_speeds_2[i][1])
        if rect.top < 0:
            cloud_speeds_2[i] = (cloud_speeds_2[i][0], -cloud_speeds_2[i][1])
        screen.blit(cloud_image_2, rect)

    # Рисуем кнопки с тенью и закругленными углами
    shadow_offset = 5
    corner_radius = 20

    start_button = pygame.Rect(width // 2 - 100, height // 2 - 50, 200, 100)
    records_button = pygame.Rect(width // 2 - 100, height // 2 + 100, 200, 100)
    music_button = pygame.Rect(width // 2 - 100, height // 2 + 250, 200, 100)

    # Тени
    draw_rounded_rect(screen, start_button.move(shadow_offset, shadow_offset), (50, 50, 50), corner_radius)
    draw_rounded_rect(screen, records_button.move(shadow_offset, shadow_offset), (50, 50, 50), corner_radius)
    draw_rounded_rect(screen, music_button.move(shadow_offset, shadow_offset), (50, 50, 50), corner_radius)

    # Кнопки
    draw_rounded_rect(screen, start_button, (0, 255, 0), corner_radius)
    draw_rounded_rect(screen, records_button, (255, 0, 0), corner_radius)
    draw_rounded_rect(screen, music_button, (0, 0, 255), corner_radius)

    draw_text('Start', font, (255, 255, 255), screen, width // 2 - 50, height // 2 - 35)
    draw_text('Records', font, (255, 255, 255), screen, width // 2 - 100, height // 2 + 115)
    draw_text('Music', font, (255, 255, 255), screen, width // 2 - 70, height // 2 + 265)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()