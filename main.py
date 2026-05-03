import pygame
import copy
import os
from constants import *
from pacman import Pacman
from ghost import Ghost

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()


FRUIT_DATA = {
    1: ("CERISE", 100), 2: ("FRAISE", 300), 
    3: ("ORANGE", 500), 4: ("ORANGE", 500),
    5: ("POMME", 700), 6: ("POMME", 700), 
    7: ("MELON", 1000), 8: ("MELON", 1000),
    9: ("GALBOSS", 2000), 10: ("GALBOSS", 2000), 
    11: ("CLOCHE", 3000), 12: ("CLOCHE", 3000)
}

GAME_W, GAME_H = SCREEN_WIDTH, SCREEN_HEIGHT + 140 
virtual_surface = pygame.Surface((GAME_W, GAME_H))
info = pygame.display.Info()
win_h = info.current_h - 100
screen = pygame.display.set_mode((int(win_h * (GAME_W/GAME_H)), win_h), pygame.RESIZABLE)

clock = pygame.time.Clock()
font_hud = pygame.font.SysFont("Arial", 22, bold=True)
font_msg = pygame.font.SysFont("Impact", 42)

ORIGINAL_MAP = copy.deepcopy(MAP)
player = Pacman()
ghosts = [Ghost(9, 8, RED), Ghost(8, 9, PINK), Ghost(10, 9, CYAN), Ghost(9, 9, ORANGE)]

score, lives, dots_eaten = 0, 3, 0
level = 1
extra_life_awarded = False
power_timer = 0
fruit_active = None
game_state = "READY"
ready_timer = 120


FRUIT_GRID_X, FRUIT_GRID_Y = 9, 11

def get_current_fruit():
    if level >= 13: return ("CLÉ", 5000)
    return FRUIT_DATA.get(level, ("CERISE", 100))

def draw_fruit_design(surf, name, x, y):
    if name == "CERISE":
        pygame.draw.circle(surf, (255, 0, 0), (x - 4, y + 4), 5)
        pygame.draw.circle(surf, (200, 0, 0), (x + 4, y + 2), 5)
        pygame.draw.lines(surf, (0, 255, 0), False, [(x-2, y), (x, y-8), (x+4, y-7)], 2)
    elif name == "FRAISE":
        pygame.draw.polygon(surf, (255, 50, 50), [(x, y+8), (x-7, y-2), (x, y-7), (x+7, y-2)])
        pygame.draw.circle(surf, (0, 200, 0), (x, y-7), 4)
    elif name == "ORANGE":
        pygame.draw.circle(surf, (255, 165, 0), (x, y), 8)
        pygame.draw.rect(surf, (0, 200, 0), (x-1, y-10, 2, 4))
    elif name == "POMME":
        pygame.draw.circle(surf, (255, 0, 0), (x, y+2), 8)
        pygame.draw.lines(surf, (139, 69, 19), False, [(x, y-6), (x+3, y-10)], 2)
    elif name == "MELON":
        pygame.draw.circle(surf, (144, 238, 144), (x, y), 8)
        pygame.draw.arc(surf, (0, 100, 0), (x-6, y-6, 12, 12), 0, 3.14, 2)
    elif name == "GALBOSS":
        pygame.draw.polygon(surf, (50, 50, 255), [(x-8, y+4), (x, y-8), (x+8, y+4), (x, y+2)])
    elif name == "CLOCHE":
        pygame.draw.rect(surf, (255, 215, 0), (x-6, y-2, 12, 8), border_radius=2)
        pygame.draw.circle(surf, (255, 215, 0), (x, y-4), 5)
    elif name == "CLÉ":
        pygame.draw.rect(surf, (192, 192, 192), (x-2, y-6, 4, 14))
        pygame.draw.circle(surf, (192, 192, 192), (x, y-6), 5, 2)

def draw_life_pacman(surf, x, y):
    pygame.draw.circle(surf, YELLOW, (x, y), 8)
    pygame.draw.polygon(surf, BLACK, [(x, y), (x + 10, y - 6), (x + 10, y + 6)])

def reset_positions():
    global game_state, ready_timer, fruit_active
    game_state = "READY"
    ready_timer = 120
    fruit_active = None
    player.reset()
    for g in ghosts: g.reset()

def next_level():
    global MAP, dots_eaten, level
    level += 1
    MAP = copy.deepcopy(ORIGINAL_MAP)
    dots_eaten = 0
    reset_positions()

def full_reset():
    global score, lives, dots_eaten, MAP, level, extra_life_awarded
    score, lives, level, dots_eaten = 0, 3, 1, 0
    extra_life_awarded = False
    MAP = copy.deepcopy(ORIGINAL_MAP)
    reset_positions()


while True:
    virtual_surface.fill(BLACK)
    frame_count = pygame.time.get_ticks() // 100
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); exit()
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_p or event.key == pygame.K_SPACE:
                if game_state == "PLAY": game_state = "PAUSE"
                elif game_state == "PAUSE": game_state = "PLAY"
                
                elif game_state == "GAMEOVER" and event.key == pygame.K_SPACE:
                    full_reset()
            
            if game_state == "PLAY":
                if event.key == pygame.K_LEFT: player.next_dir_x, player.next_dir_y = -1, 0
                elif event.key == pygame.K_RIGHT: player.next_dir_x, player.next_dir_y = 1, 0
                elif event.key == pygame.K_UP: player.next_dir_x, player.next_dir_y = 0, -1
                elif event.key == pygame.K_DOWN: player.next_dir_x, player.next_dir_y = 0, 1

    if game_state == "READY":
        ready_timer -= 1
        if ready_timer <= 0: game_state = "PLAY"

    if game_state == "PLAY":
        
        if fruit_active:
            px_c, py_c = int((player.x + 10) // 20), int((player.y + 10) // 20)
            if px_c == FRUIT_GRID_X and py_c == FRUIT_GRID_Y:
                score += fruit_active[1]
                fruit_active = None

        player.update()
        
        if player.x < -10: player.x = (len(MAP[0]) * 20) - 10
        elif player.x > (len(MAP[0]) * 20): player.x = -10

        if power_timer > 0: power_timer -= 1
        else: 
            for g in ghosts: g.vulnerable = False

        
        gx, gy = int((player.x + 10) // 20), int((player.y + 10) // 20)
        if 0 <= gy < len(MAP) and 0 <= gx < len(MAP[0]):
            if MAP[gy][gx] in [0, 3]:
                dots_eaten += 1
                score += 10 if MAP[gy][gx] == 0 else 50
                if MAP[gy][gx] == 3:
                    power_timer = 500
                    for g in ghosts: g.vulnerable = True
                MAP[gy][gx] = 2
                
                
                if dots_eaten == 5 or dots_eaten == 150: 
                    fruit_active = get_current_fruit()

        for g in ghosts:
            g.update(player.x, player.y) 
            if abs(player.x - g.x) < 12 and abs(player.y - g.y) < 12:
                if g.vulnerable: g.reset(); score += 200
                else:
                    lives -= 1
                    if lives <= 0: game_state = "GAMEOVER"
                    else: reset_positions()
        
        if not any(0 in row or 3 in row for row in MAP): next_level()

    
    for r_idx, row in enumerate(MAP):
        for c_idx, tile in enumerate(row):
            pos = (c_idx*20, r_idx*20)
            if tile == 1: pygame.draw.rect(virtual_surface, BLUE, (pos[0]+2, pos[1]+2, 16, 16), 2, border_radius=4)
            elif tile == 0: pygame.draw.circle(virtual_surface, WHITE, (pos[0]+10, pos[1]+10), 2)
            elif tile == 3: pygame.draw.circle(virtual_surface, WHITE, (pos[0]+10, pos[1]+10), 6)

    
    if fruit_active:
        fx, fy = FRUIT_GRID_X * 20 + 10, FRUIT_GRID_Y * 20 + 10
        draw_fruit_design(virtual_surface, fruit_active[0], fx, fy)

    for g in ghosts: g.draw(virtual_surface)
    player.draw(virtual_surface, frame_count)
    
    
    y_hud = SCREEN_HEIGHT + 30
    virtual_surface.blit(font_hud.render(f"SCORE: {score}", True, WHITE), (20, y_hud))
    virtual_surface.blit(font_hud.render(f"NIVEAU: {level}", True, YELLOW), (20, y_hud + 30))
    for i in range(lives): draw_life_pacman(virtual_surface, GAME_W - 35 - i*25, y_hud + 12)

    
    cx, cy = GAME_W // 2, SCREEN_HEIGHT // 2
    if game_state == "READY":
        txt = font_msg.render(f"NIVEAU {level}", True, YELLOW)
        virtual_surface.blit(txt, (cx - txt.get_width()//2, cy + 40))
    elif game_state == "PAUSE":
        txt = font_msg.render("PAUSE", True, WHITE)
        virtual_surface.blit(txt, (cx - txt.get_width()//2, cy))
    elif game_state == "GAMEOVER":
        txt_main = font_msg.render("GAME OVER", True, RED)
        virtual_surface.blit(txt_main, (cx - txt_main.get_width()//2, cy - 20))

    
    curr_w, curr_h = screen.get_size()
    target_w = int(curr_h * (GAME_W / GAME_H))
    scaled_win = pygame.transform.smoothscale(virtual_surface, (target_w, curr_h))
    screen.fill(BLACK)
    screen.blit(scaled_win, ((curr_w - target_w) // 2, 0))
    pygame.display.flip()
    clock.tick(60)