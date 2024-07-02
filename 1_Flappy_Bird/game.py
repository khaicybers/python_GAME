# gaem flap bird khải tập code để học hỏi nên có nhu cầu thắc mắc thì cứ liên hệ hỏi tui 
#game chưa được hoàn thiện nhưng cũng được 1 phần 
#game này chỉ giupsd các bạn tính toán giỏi hơn nhưng khong giúp các việt coppy code 
# khaicybers

import pygame, sys, random

# tao ham tro choi
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))
# tao ong
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos)) #midtop la goc o giua tren cung
    top_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos - 650)) #midtop la goc o giua tren cung

    return bottom_pipe, top_pipe
# ham di chuyen ong
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
# ve ong
def draw_pipe(pipes):
    for pipe in pipe_list:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)
            
# xu ly va cham
def check_collision(pipes):
    for pipe in pipes:
        #cham cot
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    return True
    #cham tren cham duoi
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
def rotat_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement * 3 , 1) #rotozoom la hieu xoay con chim
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect
def score_display(game_state):
    if game_state == 'game bat dau':
        score_surface = game_font.render(str(int(score)) , True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 50))
        screen.blit(score_surface, score_rect)
    if game_state == 'game ket thuc':
        score_surface = game_font.render(f'diem cua ban: {int(score)}' , True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'diem cao nhat: {int(high_score)}' , True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (216, 850))
        screen.blit(high_score_surface, high_score_rect)
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()

screen= pygame.display.set_mode((432, 760))
# tao cac bien tro choi
clock = pygame.time.Clock()
#phong chu
game_font = pygame.font.Font('04B_19.ttf', 40)
# them trong luc
gravity = 0.15
bird_movement = 0
game_active = True
score = 0
high_score = 0
# background
bg = pygame.image.load('assets/background-night.png').convert()
bg= pygame.transform.scale2x(bg)
# chen san
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
# tao chim
bird_down = pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()
bird_mid = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
bird_up = pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()
bird_list = [bird_down,bird_mid,bird_up]
bird_index = 0
bird = bird_list[bird_index]
# bird = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
# bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100, 384))
#tao timer cho chim
birdflap = pygame.USEREVENT + 1  # event danh rieng cho chim
pygame.time.set_timer(birdflap,200)
# them ong cong
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
# tao timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_height = [200, 300, 400]
# tao man hinh ket thuc 
game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(216, 383))
# chen am thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
# chen nhac nen
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
# chen nhac vang
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
# chen nhac thua
die_sound = pygame.mixer.Sound('sound/sfx_die.wav')
# ham tro choi

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit ()
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and game_active:
                # print('bird jump')
                bird_movement = 0
                bird_movement -= 6
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
        if event.type == spawnpipe:
            # print('spawn pipe')
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            if bird_index < 2:
                bird_index +=1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    screen.blit(bg, (0,0))
    if game_active:
    # chim
        bird_movement += gravity
        rotated_bird = rotat_bird(bird)
        bird_rect.centery += int(bird_movement)
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
        # ong
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display('game bat dau')

    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = max(score, high_score)
        score_display('game ket thuc')
     # san
    floor_x_pos -= 1
    draw_floor()
   
    if floor_x_pos <= -432:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)

