# MARIO vs AI GOOMBAS – FINAL WORKING VERSION
import pygame, sys, math
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

pygame.init()
W, H = 600, 660
TILE = 30
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Mario vs AI Goombas")
clock = pygame.time.Clock()

# Colors
GRASS = (34, 139, 34)
BRICK = (139, 69, 19)
RED   = (220, 20, 60)
BROWN = (101, 67, 33)
WHITE = (255,255,255)

# 19×20 maze – 100% correct
maze = [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,1],
[1,2,1,1,2,1,2,1,2,1,2,1,2,1,2,1,1,2,2,1],
[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
[1,2,1,1,2,1,1,2,1,1,1,1,2,1,1,2,1,1,2,1],
[1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,1],
[1,1,1,1,2,1,2,1,1,1,1,1,2,1,2,1,1,1,1,1],
[0,0,0,1,2,1,2,2,2,1,2,2,2,1,2,1,0,0,0,0],
[1,1,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,1,1,1],
[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
[1,1,1,1,2,1,2,2,2,2,2,2,2,1,2,1,1,1,1,1],
[1,2,2,2,2,1,2,1,1,0,1,1,2,1,2,2,2,2,2,1],
[1,2,1,1,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,1],
[1,2,2,2,2,1,1,1,2,1,2,1,1,1,2,2,2,2,2,1],
[1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1],
[1,2,2,2,1,2,1,2,1,1,1,1,2,1,2,1,2,2,2,1],
[1,2,1,1,1,2,2,2,2,1,2,2,2,2,1,1,1,2,2,1],
[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

mario = [9*TILE+8, 15*TILE+8]
goombas = [[9*TILE+8,9*TILE+8],[9*TILE+8,10*TILE+8],[8*TILE+8,9*TILE+8],[10*TILE+8,9*TILE+8]]
score = 0

def grid():
    return Grid(matrix=[[0 if cell != 1 else 1 for cell in row] for row in maze])

def next_target(pos, target):
    g = grid()
    sx = int((pos[0] + TILE//2) // TILE)
    sy = int((pos[1] + TILE//2) // TILE)
    tx = int((target[0] + TILE//2) // TILE)
    ty = int((target[1] + TILE//2) // TILE)
    if not (0 <= sx <20 and 0 <= sy <19 and 0 <= tx <20 and 0 <= ty <19):
        return None
    path, _ = AStarFinder().find_path(g.node(sx,sy), g.node(tx,ty), g)
    return (path[1][0]*TILE + TILE//2, path[1][1]*TILE + TILE//2) if len(path)>1 else None

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: pygame.quit(); sys.exit()

    keys = pygame.key.get_pressed()
    nx, ny = mario[0], mario[1]
    if keys[pygame.K_LEFT]:  nx -= 4
    if keys[pygame.K_RIGHT]: nx += 4
    if keys[pygame.K_UP]:    ny -= 4
    if keys[pygame.K_DOWN]:  ny += 4
    gx = int((nx + TILE//2)//TILE)
    gy = int((ny + TILE//2)//TILE)
    if 0<=gx<20 and 0<=gy<19 and maze[gy][gx] != 1:
        mario = [nx, ny]
        if maze[gy][gx] == 2:
            maze[gy][gx] = 0
            score += 10

    for g in goombas:
        nxt = next_target(g, mario)
        if nxt:
            dx = nxt[0] - g[0] - TILE//2
            dy = nxt[1] - g[1] - TILE//2
            d = math.hypot(dx, dy) or 1
            g[0] += dx/d * 2.7
            g[1] += dy/d * 2.7

        if math.hypot(g[0]-mario[0], g[1]-mario[1]) < 25:
            print("GAME OVER – Goomba got you! Score:", score)
            pygame.time.wait(2000)
            pygame.quit(); sys.exit()

    if all(2 not in row for row in maze):
        print("YOU WIN!!! Score:", score)
        pygame.time.wait(3000)
        pygame.quit(); sys.exit()

    screen.fill(GRASS)
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, BRICK, (x*TILE, y*TILE, TILE, TILE))
            if cell == 2:
                pygame.draw.circle(screen, WHITE, (x*TILE + TILE//2, y*TILE + TILE//2), 5)

    # Mario
    mx = int(mario[0] + TILE//2)
    my = int(mario[1] + TILE//2)
    pygame.draw.rect(screen, RED, (mx-10, my-20, 20, 15))   # hat
    pygame.draw.circle(screen, (255,220,180), (mx, my), 14) # face
    pygame.draw.circle(screen, RED, (mx, my+4), 13)         # shirt

    # Goombas
    for g in goombas:
        gx = int(g[0] + TILE//2)
        gy = int(g[1] + TILE//2)
        pygame.draw.ellipse(screen, BROWN, (gx-14, gy-8, 28, 18))
        pygame.draw.circle(screen, WHITE, (gx-7, gy-3), 6)
        pygame.draw.circle(screen, WHITE, (gx+7, gy-3), 6)

    font = pygame.font.SysFont(None, 40)
    screen.blit(font.render(f"Score: {score}", True, WHITE), (20, 610))

    pygame.display.flip()
    clock.tick(60)