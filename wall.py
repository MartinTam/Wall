import pygame
import os

pygame.init()

WIDTH = 500
HEIGHT = 600
SHIP_WIDTH = 72
SHIP_HEIGHT = 72
BRICK_WIDTH = 90
BRICK_HEIGHT = 20

WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wall")

BG = pygame.image.load(os.path.join('images', 'BG.jpg'))

SHIP = pygame.transform.scale( pygame.image.load(os.path.join('images', 'ship.png')), (SHIP_WIDTH, SHIP_HEIGHT) )
VEL = 10
VEL_BULLET = 15

BRICK_ROW = [   pygame.Rect(5, 10, BRICK_WIDTH, BRICK_HEIGHT),
                pygame.Rect(105, 10, BRICK_WIDTH, BRICK_HEIGHT),
                pygame.Rect(205, 10, BRICK_WIDTH, BRICK_HEIGHT),
                pygame.Rect(305, 10, BRICK_WIDTH, BRICK_HEIGHT),
                pygame.Rect(405, 10, BRICK_WIDTH, BRICK_HEIGHT)
            ]

FPS = 60
FRAMES = 0

def movement(key_pressed, position):

    if key_pressed[pygame.K_RIGHT] and position.x + SHIP_WIDTH < WIDTH:
        position.x += VEL
    
    if key_pressed[pygame.K_LEFT] and position.x > 0:
        position.x -= VEL
    
def handle_bullet(bullet):

    for oneShot in bullet:
        oneShot.y -= VEL_BULLET


def draw(position, bullet, score, move):

    WIN.fill(BLACK)
    #WIN.blit(BG, (-1000,-1000))
    WIN.blit(SHIP, (position.x, position.y))
    
    if move == True:
        for x in BRICK_ROW:
            x.y += 20
            pygame.draw.rect(WIN, WHITE, x)
    else:    
        for x in BRICK_ROW:
            pygame.draw.rect(WIN, WHITE, x)
    
    for oneShot in bullet:
        
        pygame.draw.rect(WIN, YELLOW, oneShot)
        if oneShot.y < 0:
            bullet.remove(oneShot)
            score[0] += 1
    
    
    font = pygame.font.SysFont('ComicSans', 30)
    text = font.render('Score: {0}'.format(score[0]), True, WHITE)
    WIN.blit(text, (10, HEIGHT-35))

    pygame.display.update()

def main():

    run = True
    clock = pygame.time.Clock()
    
    position = pygame.Rect(250,475, SHIP_WIDTH, SHIP_HEIGHT)
    bullet = []
    score = [0]
    frames = 0

    while(run):

        clock.tick(FPS)
        frames += 1
        move = False
        if frames == 60:
            move = True
            frames = 0

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                run = False
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    shot = pygame.Rect(position.x + SHIP_WIDTH//2 - 5, position.y, 5, 10)
                    
                    if len(bullet) < 1:
                        bullet.append(shot)
                
        handle_bullet(bullet)
            
        key_pressed = pygame.key.get_pressed()
        movement(key_pressed, position)
        draw(position, bullet, score, move)

    pygame.quit()

main()