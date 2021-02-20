import pygame
import os

pygame.init()

WIDTH = 500
HEIGHT = 600
SHIP_WIDTH = 72
SHIP_HEIGHT = 72
BRICK_WIDTH = 90
BRICK_HEIGHT = 20
END_LINE = 475

WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
BRICK_COLOR = (212, 212, 212)

ARROW_POS_PLAY = (165,266)
ARROW_POS_EXIT = (205, 300)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wall")

BG = pygame.image.load(os.path.join('images', 'BG.jpg'))

SHIP = pygame.transform.scale( pygame.image.load(os.path.join('images', 'ship.png')), (SHIP_WIDTH, SHIP_HEIGHT) )
VEL = 10
VEL_BULLET = 15

ARROW = pygame.transform.scale( pygame.image.load(os.path.join('images', 'arrow.png')), (15, 25) )

BRICK_ROW = []

for x in range(5,505,100):
        BRICK_ROW.append( pygame.Rect(x, 0 - BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT) )


FPS = 60

def restartGame():
    BRICK_ROW.clear()
    for x in range(5,505,100):
        BRICK_ROW.append( pygame.Rect(x, 0 - BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT) )

def colision(oneShot, BRICK_ROW):

    for x in BRICK_ROW:
        if oneShot.colliderect(x):
            return x
            break
    
    return 0
              

def anotherRow():
    
    for x in range(5,505,100):
        BRICK_ROW.append(pygame.Rect(x, 0 - BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT))    
    

def movement(key_pressed, position):

    if key_pressed[pygame.K_RIGHT] and position.x + SHIP_WIDTH < WIDTH:
        position.x += VEL
    
    if key_pressed[pygame.K_LEFT] and position.x > 0:
        position.x -= VEL
    
def handle_bullet(bullet):

    for oneShot in bullet:
        oneShot.y -= VEL_BULLET


def draw(position, bullet, score, move, end):

    WIN.fill(BLACK)
    WIN.blit(BG, (0,0))
    WIN.blit(SHIP, (position.x, position.y))
    

    if move == True:
        for x in BRICK_ROW:
            x.y += 25
            pygame.draw.rect(WIN, BRICK_COLOR, x)
            if x.y >= END_LINE:
                end[0] = 1
                return end[0]
        anotherRow()
    else:    
        for x in BRICK_ROW:
            pygame.draw.rect(WIN, BRICK_COLOR, x)
            if x.y >= END_LINE:
                end[0] = 1
                return end[0]
    
    for oneShot in bullet:
        
        pygame.draw.rect(WIN, YELLOW, oneShot)
        if oneShot.y < 0 or colision(oneShot,BRICK_ROW):
            bullet.remove(oneShot)
            BRICK_ROW.remove(colision(oneShot,BRICK_ROW))
            score[0] += 1
    

    font = pygame.font.SysFont('ComicSans', 30)
    text = font.render('Score: {0}'.format(score[0]), True, WHITE)
    WIN.blit(text, (10, HEIGHT-35))

    pygame.display.update()

def gameOver(score, button):
    WIN.fill(BLACK)
    WIN.blit(BG, (0,0))

    gameOverFont = pygame.font.SysFont('ComicSans', 50)
    playExit = pygame.font.SysFont('ComicSans', 30)
    
    gameOver = gameOverFont.render('GAME OVER', True, WHITE)
    play = playExit.render('PLAY AGAIN', True, WHITE)
    exitGame = playExit.render('EXIT', True, WHITE)
    
    WIN.blit(gameOver, (WIDTH//2 - 105, HEIGHT//2 - 100))
    WIN.blit(play, (WIDTH//2 - 60, HEIGHT//2 - 30))
    WIN.blit(exitGame, (WIDTH//2 - 20, HEIGHT//2 + 5))

    if button[0] == 0:
        WIN.blit(ARROW, ARROW_POS_PLAY)
    
    if button[0] == 1:
        WIN.blit(ARROW, ARROW_POS_EXIT)

    pygame.display.update()


def main():

    run = True
    clock = pygame.time.Clock()
    
    position = pygame.Rect(220, END_LINE, SHIP_WIDTH, SHIP_HEIGHT)
    bullet = []
    score = [0]
    frames = 0
    button = [0]
    end = [0]

    while(run):

        clock.tick(FPS)
        frames += 1
        move = False
        if frames == 180:
            '''
                Every 180 frames (3 seconds) the wall will move down !!!
            '''
            move = True
            frames = 0

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                run = False
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE and end[0] == 0:

                    shot = pygame.Rect(position.x + SHIP_WIDTH//2 - 5, position.y, 5, 10)
                    
                    if len(bullet) < 1:
                        bullet.append(shot)
                
                if event.key == pygame.K_UP and end[0] == 1:

                    button[0] = 0

                if event.key == pygame.K_DOWN and end[0] == 1:

                    button[0] = 1
                
                if event.key == pygame.K_RETURN and end[0] == 1:

                    if button[0] == 0:
                        restartGame()
                        position.x = 220
                        position.y = END_LINE
                        score[0] = 0
                        end[0] = 0

                    if button[0] == 1:
                        run = False

        if end[0] == 0:
            handle_bullet(bullet)
            key_pressed = pygame.key.get_pressed()
            movement(key_pressed, position)
            draw(position, bullet, score, move, end)
        
        if end[0] == 1:
            gameOver(score, button)
        
    pygame.quit()

main()