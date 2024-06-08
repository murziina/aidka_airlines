import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройка экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# FPS
clock = pygame.time.Clock()
fps = 60

# Параметры препятствий
obstacle_size = 50
obstacle_pos = [random.randint(0, screen_width-obstacle_size), 0]
obstacle_list = [obstacle_pos]
obstacle_speed = 10

# Параметры игрока
player_size = 50  # Эта строка должна быть определена до загрузки изображений
player_pos = [screen_width // 2, screen_height - 2 * player_size]
player_velocity = 5

player_image = pygame.image.load('C:/Users/murzz/.vscode/plane.png')
player_image = pygame.transform.scale(player_image, (player_size, player_size))
obstacle_image = pygame.image.load('C:/Users/murzz/.vscode/cloud.png')
obstacle_image = pygame.transform.scale(obstacle_image, (obstacle_size, obstacle_size))

# Если вы используете badcloud.png, убедитесь, что у вас есть переменная для его размера
bad_obstacle_image = pygame.image.load('C:/Users/murzz/.vscode/badcloud.png')
bad_obstacle_image = pygame.transform.scale(bad_obstacle_image, (obstacle_size, obstacle_size))



# Загрузка изображений и изменение их размеров
player_image = pygame.image.load('C:/Users/murzz/.vscode/plane.png')
player_image = pygame.transform.scale(player_image, (player_size, player_size))





# Счет
score = 0

# Шрифт для счета
font = pygame.font.SysFont("monospace", 35)

# Функции
def drop_obstacles(obstacle_list):
    delay = random.random()
    if len(obstacle_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, screen_width-obstacle_size)
        y_pos = 0
        obstacle_list.append([x_pos, y_pos])

def draw_obstacles(obstacle_list):
    for obstacle_pos in obstacle_list:
        screen.blit(obstacle_image, (obstacle_pos[0], obstacle_pos[1]))


def update_obstacle_positions(obstacle_list, score):
    for idx, obstacle_pos in enumerate(obstacle_list):
        if obstacle_pos[1] >= 0 and obstacle_pos[1] < screen_height:
            obstacle_pos[1] += obstacle_speed
        else:
            obstacle_list.pop(idx)
            score += 1
    return score

def collision_check(obstacle_list, player_pos):
    for obstacle_pos in obstacle_list:
        if detect_collision(obstacle_pos, player_pos):
            return True
    return False

def detect_collision(obstacle_pos, player_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    o_x = obstacle_pos[0]
    o_y = obstacle_pos[1]

    if (o_x >= p_x and o_x < (p_x + player_size)) or (p_x >= o_x and p_x < (o_x + obstacle_size)):
        if (o_y >= p_y and o_y < (p_y + player_size)) or (p_y >= o_y and p_y < (o_y + obstacle_size)):
            return True
    return False



# Игровой цикл
game_over = False
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()

    screen.blit(player_image, (player_pos[0], player_pos[1]))


    if keys[pygame.K_LEFT] and player_pos[0] > player_velocity:
        player_pos[0] -= player_velocity

    if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_size - player_velocity:
        player_pos[0] += player_velocity

    screen.fill(black)

    drop_obstacles(obstacle_list)
    score = update_obstacle_positions(obstacle_list, score)
    text = "Score: " + str(score)
    label = font.render(text, 1, white)
    screen.blit(label, (screen_width-200, screen_height-40))

    if collision_check(obstacle_list, player_pos):
        game_over = True
        break

    draw_obstacles(obstacle_list)

    pygame.draw.rect(screen, white, (player_pos[0], player_pos[1], player_size, player_size))

    pygame.display.update()
    clock.tick(fps)

    clock.tick(fps)

pygame.quit()