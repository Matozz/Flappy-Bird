import pygame
import sys
import random


# DRAW BASE
def draw_surface():
    screen.blit(bg_surface, (bg_x_position, 0))
    screen.blit(bg_surface, (bg_x_position + 576, 0))


def draw_floor():
    screen.blit(floor_surface, (floor_x_position, 900))
    screen.blit(floor_surface, (floor_x_position + 576, 900))


# DRAW PIPES
def create_pipe(gap):
    random_pipe_height = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_height))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_height - gap))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= pipe_move_speed
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flipped_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flipped_pipe, pipe)


# Collision
def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        death_sound.play()
        can_score = True
        return False
    return True


# Rotate
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


# Color
def bird_color_blue():
    bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
    bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
    bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
    return [bird_downflap, bird_midflap, bird_upflap]


def bird_color_yellow():
    bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
    bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
    bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
    return [bird_downflap, bird_midflap, bird_upflap]


def bird_color_red():
    bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-downflap.png').convert_alpha())
    bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-midflap.png').convert_alpha())
    bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-upflap.png').convert_alpha())
    return [bird_downflap, bird_midflap, bird_upflap]


# Animation
def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


# Scores
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'Highest Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)


def update_score(current, highest):
    if current > highest:
        highest = current
    return highest


def pipe_score_check():
    global score, can_score

    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                can_score = False
            if pipe.centerx < 0:
                can_score = True


pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 40)

# Game Variables
game_active = True
gravity = 0.25
bird_movement = 0
bird_flap_height = 8
pipe_move_speed = 4
initial_gap = 300
score = 0
high_score = 0
flap_rate = 200
can_score = True
bird_level = 1

bg_surface = pygame.transform.scale2x(pygame.image.load('assets/background-day.png').convert())
bg_x_position = 0

floor_surface = pygame.transform.scale2x(pygame.image.load('assets/base.png').convert())
floor_x_position = 0

# bird_surface = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
# bird_rect = bird_surface.get_rect(center=(100, 512))
bird_frames = bird_color_blue()
bird_index = 2
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 512))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, flap_rate)

pipe_surface = pygame.transform.scale2x(pygame.image.load('assets/pipe-green.png'))
pipe_list = []
CREATEPIPE = pygame.USEREVENT
pygame.time.set_timer(CREATEPIPE, 1500)
pipe_height = [400, 500, 600, 700, 800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png'))
game_over_rect = game_over_surface.get_rect(center=(288, 512))

# Sounds
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
levelup_sound = pygame.mixer.Sound('sound/sfx_point.wav')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= bird_flap_height
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active is False:
                # Reset Game Variables
                bird_frames = bird_color_blue()
                pygame.time.set_timer(BIRDFLAP, 200)
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
                pipe_move_speed = 4
                score = 0
                game_active = True
        if event.type == CREATEPIPE:
            pipe_list.extend(create_pipe(initial_gap))

        # Level Up
        if score >= 20 and bird_level == 2:
            levelup_sound.play()
            bird_frames = bird_color_yellow()
            pygame.time.set_timer(BIRDFLAP, 40)
            bird_level += 1
            pipe_move_speed += 1
        elif score >= 10 and bird_level == 1:
            levelup_sound.play()
            bird_frames = bird_color_red()
            pygame.time.set_timer(BIRDFLAP, 100)
            bird_level += 1
            pipe_move_speed += 2

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    # Background
    bg_x_position -= 1
    draw_surface()
    if bg_x_position <= -576:
        bg_x_position = 0

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird_surface = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird_surface, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Score
        pipe_score_check()
        score_display('main_game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor
    floor_x_position -= 1
    draw_floor()
    if floor_x_position <= -576:
        floor_x_position = 0

    pygame.display.update()
    clock.tick(120)
