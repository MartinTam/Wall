import pygame
import os

pygame.init()

WIDTH = 500
HEIGHT = 600
SHIP_WIDTH = 72
SHIP_HEIGHT = 72

WHITE = (0,0,0)
YELLOW = (255,255,0)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wall")

SHIP = pygame.image.load(os.path.join('images', 'ship.png'))
VEL = 10
VEL_BULLET = 15

FPS = 60

def movement(key_pressed, position):

    if key_pressed[pygame.K_RIGHT] and position.x + SHIP_WIDTH < WIDTH:
        position.x += VEL
    
    if key_pressed[pygame.K_LEFT] and position.x > 0:
        position.x -= VEL
    
def handle_bullet(bullet):

    for oneShot in bullet:
        oneShot.y -= VEL_BULLET


def draw(position, bullet):

    WIN.fill(WHITE)
    WIN.blit(SHIP, (position.x, position.y))
    
    for oneShot in bullet:
        
        pygame.draw.rect(WIN, YELLOW, oneShot)
        if oneShot.y < 0:
            bullet.remove(oneShot)

    pygame.display.update()

def main():

    run = True
    clock = pygame.time.Clock()
    
    position = pygame.Rect(250,475, SHIP_WIDTH, SHIP_HEIGHT)
    bullet = []

    while(run):

        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                run = False
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    shot = pygame.Rect(position.x + SHIP_WIDTH//2 - 2, position.y, 5, 10)
                    
                    if len(bullet) < 1:
                        bullet.append(shot)
                
        handle_bullet(bullet)
            
        key_pressed = pygame.key.get_pressed()
        movement(key_pressed, position)
        draw(position, bullet)

    pygame.quit()

main()