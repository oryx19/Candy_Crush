import pygame
import random

pygame.init()

# Kích thước window
CELL_SIZE = 64
ROWS = 8
COLS = 8
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Candy Crush Demo")

clock = pygame.time.Clock()

# Màu candy
COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (128, 0, 128),  # Purple
]

# Tạo grid random
grid = [[random.choice(COLORS) for _ in range(COLS)] for _ in range(ROWS)]

def draw_grid():
    for y in range(ROWS):
        for x in range(COLS):
            cx = x * CELL_SIZE + CELL_SIZE // 2
            cy = y * CELL_SIZE + CELL_SIZE // 2
            radius = CELL_SIZE // 2 - 5
            pygame.draw.circle(screen, grid[y][x], (cx, cy), radius)
            pygame.draw.circle(screen, (0,0,0), (cx, cy), radius, 2)  # border

selected = None

def swap_cells(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    grid[y1][x1], grid[y2][x2] = grid[y2][x2], grid[y1][x1]

running = True
while running:
    screen.fill((50,50,50))
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            x = mx // CELL_SIZE
            y = my // CELL_SIZE
            
            if selected is None:
                selected = (x,y)
            else:
                swap_cells(selected, (x,y))
                selected = None

    pygame.display.flip()
    clock.tick(60)

pygame.quit()