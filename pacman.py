import pygame
import math
from constants import *

class Pacman:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = 9 * TILE_SIZE
        self.y = 15 * TILE_SIZE
        self.vel = 2
        self.dir_x, self.dir_y = 0, 0
        self.next_dir_x, self.next_dir_y = 0, 0
        self.angle = 0 

    def update(self):
        if self.x % TILE_SIZE == 0 and self.y % TILE_SIZE == 0:
            nx, ny = int(self.x//TILE_SIZE) + self.next_dir_x, int(self.y//TILE_SIZE) + self.next_dir_y
            if 0 <= ny < len(MAP) and 0 <= nx < len(MAP[0]) and MAP[ny][nx] != 1:
                self.dir_x, self.dir_y = self.next_dir_x, self.next_dir_y
            
            cx, cy = int(self.x//TILE_SIZE) + self.dir_x, int(self.y//TILE_SIZE) + self.dir_y
            if 0 <= cy < len(MAP) and 0 <= cx < len(MAP[0]) and MAP[cy][cx] == 1:
                self.dir_x, self.dir_y = 0, 0

        self.x += self.dir_x * self.vel
        self.y += self.dir_y * self.vel
        
        
        if self.dir_x == 1: self.angle = 0
        elif self.dir_x == -1: self.angle = 180
        elif self.dir_y == -1: self.angle = 90
        elif self.dir_y == 1: self.angle = 270

    def draw(self, screen, frame):
        center = (int(self.x + 10), int(self.y + 10))
        
        opening = abs(math.sin(frame * 0.8)) * 0.8 
        
        
        pygame.draw.circle(screen, YELLOW, center, 9)
        
    
        if self.dir_x != 0 or self.dir_y != 0:
            p1 = center
            
            p2 = (center[0] + 12 * math.cos(math.radians(self.angle - 45 * opening)),
                  center[1] - 12 * math.sin(math.radians(self.angle - 45 * opening)))
            p3 = (center[0] + 12 * math.cos(math.radians(self.angle + 45 * opening)),
                  center[1] - 12 * math.sin(math.radians(self.angle + 45 * opening)))
            pygame.draw.polygon(screen, BLACK, [p1, p2, p3])