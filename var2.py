import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Параметры экрана для мобильной версии
screen_width = 360
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# FPS
clock = pygame.time.Clock()
fps = 60

# Параметры игрока
player_size = 30
player_x = screen_width / 2 - player_size / 2
player_y = screen_height - 2 * player_size
player_speed = 5

# Параметры врага
enemy_size = 30
enemy_speed = 5

# Счет
score = 0
font = pygame.font.SysFont("Arial", 25)

# Функции
def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, red, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list, score, enemy_speed):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < screen_height:
            enemy_pos[1] += enemy_speed
        else:
            enemy_list.pop(idx)
            score += 1
            enemy_list.append([random.randint(0, screen_width-enemy_size), 0])
    return score

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False

def detect_collision(player_pos, enemy_pos):
    p_x, p_y = player_pos
    e_x, e_y = enemy_pos
    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    return False

def show_game_over_screen():
    screen.fill(black)
    game_over_font = pygame.font.SysFont("Arial", 30)
    game_over_text = game_over_font.render("Game Over!", True, white)
    play_again_text = game_over_font.render("Play Again", True, green)
    exit_text = game_over_font.render("Exit", True, red)
    score_text = game_over_font.render("Score: " + str(score), True, white)

    screen.blit(game_over_text, (screen_width / 2 - game_over_text.get_width() / 2, screen_height / 4))
    screen.blit(play_again_text, (screen_width / 2 - play_again_text.get_width() / 2, screen_height / 2))
    screen.blit(exit_text, (screen_width / 2 - exit_text.get_width() / 2, screen_height / 2 + 50))
    screen.blit(score_text, (screen_width / 2 - score_text.get_width() / 2, screen_height / 2 - 100))

    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (screen_width / 2 - play_again_text.get_width() / 2) <= mouse_x <= (screen_width / 2 + play_again_text.get_width() / 2) and \
                   (screen_height / 2) <= mouse_y <= (screen_height / 2 + play_again_text.get_height()):
                    waiting = False
                if (screen_width / 2 - exit_text.get_width() / 2) <= mouse_x <= (screen_width / 2 + exit_text.get_width() / 2) and \
                   (screen_height / 2 + 50) <= mouse_y <= (screen_height / 2 + 50 + exit_text.get_height()):
                    pygame.quit()
                    sys.exit()

def show_welcome_screen():
    screen.fill(black)
    welcome_font = pygame.font.SysFont("Arial", 30)
    welcome_text = welcome_font.render("Welcome to the Game!", True, white)
    play_text = welcome_font.render("Play", True, green)

    screen.blit(welcome_text, (screen_width / 2 - welcome_text.get_width() / 2, screen_height / 4))
    screen.blit(play_text, (screen_width / 2 - play_text.get_width() / 2, screen_height / 2))

    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (screen_width / 2 - play_text.get_width() / 2) <= mouse_x <= (screen_width / 2 + play_text.get_width() / 2) and \
                   (screen_height / 2) <= mouse_y <= (screen_height / 2 + play_text.get_height()):
                    waiting = False

def choose_difficulty():
    screen.fill(black)
    difficulty_font = pygame.font.SysFont("Arial", 30)
    
    easy_text = difficulty_font.render("Easy", True, green)
    medium_text = difficulty_font.render("Medium", True, yellow)
    hard_text = difficulty_font.render("Hard", True, red)
    
    screen.blit(easy_text, (screen_width / 2 - easy_text.get_width() / 2, screen_height / 4))
    screen.blit(medium_text, (screen_width / 2 - medium_text.get_width() / 2, screen_height / 2))
    screen.blit(hard_text, (screen_width / 2 - hard_text.get_width() / 2, screen_height * 3 / 4))
    
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (screen_width / 2 - easy_text.get_width() / 2) <= mouse_x <= (screen_width / 2 + easy_text.get_width() / 2):
                    if (screen_height / 4) <= mouse_y <= (screen_height / 4 + easy_text.get_height()):
                        return 'easy'
                    elif (screen_height / 2) <= mouse_y <= (screen_height / 2 + medium_text.get_height()):
                        return 'medium'
                    elif (screen_height * 3 / 4) <= mouse_y <= (screen_height * 3 / 4 + hard_text.get_height()):
                        return 'hard'

# Игровой цикл
def game_loop(difficulty):
    player_pos = [player_x, player_y]
    global score
    score = 0
    game_over = False
    
    # Настройки для разных уровней сложности
    if difficulty == 'easy':
        enemy_speed = 5
        number_of_enemies = 3
    elif difficulty == 'medium':
        enemy_speed = 7
        number_of_enemies = 5
    elif difficulty == 'hard':
        enemy_speed = 10
        number_of_enemies = 7

    enemy_list = [[random.randint(0, screen_width-enemy_size), 0] for _ in range(number_of_enemies)]

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > player_speed:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_size - player_speed:
            player_pos[0] += player_speed

        screen.fill(black)

        # Обновление позиций врагов и счета
        score = update_enemy_positions(enemy_list, score, enemy_speed)
        draw_enemies(enemy_list)

        # Проверка столкновений
        if collision_check(enemy_list, player_pos):
            game_over = True
            show_game_over_screen()
            break

        # Отрисовка игрока
        pygame.draw.rect(screen, blue, (player_pos[0], player_pos[1], player_size, player_size))

        # Отображение счета
        text = font.render("Score: " + str(score), True, white)
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(fps)

# Отображение приветственного экрана и выбор сложности
show_welcome_screen()
difficulty = choose_difficulty()

while True:
    game_loop(difficulty)
    action = show_game_over_screen()
    if action == 'play again':
        difficulty = choose_difficulty()  # Позволяет игроку выбрать сложность снова
    else:
        break

while True:
    difficulty = choose_difficulty()
    game_loop(difficulty)
    action = show_game_over_screen()
    if action == 'exit':
        break

pygame.quit()

# Запуск игрового цикла
game_loop(difficulty)

pygame.quit()