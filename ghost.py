import pygame
import math
from constants import *

class Ghost:
    def __init__(self, x, y, color):
        self.grid_start_x = x
        self.grid_start_y = y
        self.color = color
        self.reset()

    def reset(self):
        self.x = self.grid_start_x * TILE_SIZE
        self.y = self.grid_start_y * TILE_SIZE
        self.vulnerable = False
        self.dir_x, self.dir_y = 0, -1
        self.vel = 1 

    def update(self, px, py):
        
        if self.x % TILE_SIZE == 0 and self.y % TILE_SIZE == 0:
            dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            valid_moves = []

            for dx, dy in dirs:
                if dx == -self.dir_x and dy == -self.dir_y:
                    continue
                gx, gy = int(self.x // TILE_SIZE) + dx, int(self.y // TILE_SIZE) + dy
                if 0 <= gy < len(MAP) and 0 <= gx < len(MAP[0]):
                    if MAP[gy][gx] != 1:
                        valid_moves.append((dx, dy))

            if valid_moves:
                if self.vulnerable:
                    self.dir_x, self.dir_y = max(valid_moves, key=lambda d: self.get_dist(self.x + d[0]*20, self.y + d[1]*20, px, py))
                else:
                    self.dir_x, self.dir_y = min(valid_moves, key=lambda d: self.get_dist(self.x + d[0]*20, self.y + d[1]*20, px, py))

        self.x += self.dir_x * self.vel
        self.y += self.dir_y * self.vel

        if self.x < 0: self.x = (len(MAP[0]) - 1) * TILE_SIZE
        elif self.x >= len(MAP[0]) * TILE_SIZE: self.x = 0

    def get_dist(self, x1, y1, x2, y2):
        return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

    def draw(self, screen):
        color = BLUE_VULN if self.vulnerable else self.color
        cx, cy = int(self.x + 10), int(self.y + 10)
        
    
        pygame.draw.circle(screen, color, (cx, cy), 9)
        pygame.draw.rect(screen, color, (self.x + 1, cy, 18, 9))
        
        
        for i in range(3):
            shift = math.sin(pygame.time.get_ticks()*0.01 + i) * 2
            pygame.draw.circle(screen, color, (int(self.x + 4 + i*6), int(self.y + 18 + shift)), 3)

        
        eye_color = WHITE if not self.vulnerable else (200, 200, 200)
        ex, ey = self.dir_x * 3, self.dir_y * 3
        pygame.draw.circle(screen, eye_color, (cx - 4 + ex, cy - 2 + ey), 3)
        pygame.draw.circle(screen, eye_color, (cx + 4 + ex, cy - 2 + ey), 3)
        if not self.vulnerable:
            pygame.draw.circle(screen, BLACK, (cx - 4 + ex*1.5, cy - 2 + ey*1.5), 1.5)
            pygame.draw.circle(screen, BLACK, (cx + 4 + ex*1.5, cy - 2 + ey*1.5), 1.5)
