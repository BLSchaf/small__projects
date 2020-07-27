import pygame
import sys
import os
import random


# Setup Window ------------------------------------------------ #
pygame.init()
SIZE = WIDTH, HEIGHT = 600, 200

FPS = 60
main_clock = pygame.time.Clock()

WINDOW = pygame.display.set_mode((SIZE))
pygame.display.set_caption('Something')

img_player = pygame.image.load(os.path.join('assets', 'ghost.png'))
IMG_BG = pygame.image.load(os.path.join('assets', 'BG.png'))
IMG_FG = pygame.image.load(os.path.join('assets', 'FG.png'))
HEIGHT_PLAYER = img_player.get_height()
HEIGHT_FG = IMG_FG.get_height()
HEIGHT_FLOOR = 10

fg_speed = 3

high_score = 0

def collision(obj1, obj2):
    if obj2.x < obj1.x + obj1.width and obj2.x + obj2.width > obj1.x:
        if obj1.y + obj1.height > obj2.y + obj2.height:
            return True
    return False

class VisualLayer():
    LAYER_SPEED = [3, 0.5]
    LAYER_POS = [[0, HEIGHT-HEIGHT_FG], [0, 0]]
    LAYER_IMG = [IMG_FG, IMG_BG]
    
    def __init__(self, layer_type, append=False):
        self.IMG = self.LAYER_IMG[layer_type]
        self.layer_type = layer_type
        
        if not append:
            self.x = self.LAYER_POS[layer_type][0]            
        else:
            self.x = WIDTH - self.LAYER_SPEED[self.layer_type]

        self.y = self.LAYER_POS[layer_type][1]
        self.width = self.IMG.get_width()

    def draw(self):
        self.x -= self.LAYER_SPEED[self.layer_type]
        WINDOW.blit(self.IMG, (int(self.x), self.y))
        
    
class Player():
    def __init__(self, window, img, pos):
        self.window = window
        self.img = img
        self.x = pos[0]
        self.y = pos[1]
        self.width = img.get_width()
        self.height = img.get_height()

    def draw(self):
        self.window.blit(self.img, (self.x, self.y))


class Obstacle():
    obstacle_vel = fg_speed
    def __init__(self):
        self.width = random.randint(1, 4) * 10
        self.height = - random.randint(HEIGHT_PLAYER//2, int(HEIGHT_PLAYER * 1.5))
        
        self.x = WIDTH
        self.y = HEIGHT - HEIGHT_FLOOR

    def draw(self):
        self.x -= self.obstacle_vel
        pygame.draw.rect(WINDOW, (120,120,120), (self.x, self.y, self.width, self.height))


def game_over(high_score):
    title_font = pygame.font.SysFont('Matura MT Script Capitals', 60, 1)
    title_label = title_font.render('Game Over', False, (33, 66, 112))

    sub_title_font = pygame.font.SysFont('Matura MT Script Capitals', 20, 1)
    sub_title_label = sub_title_font.render('Hit [SPACE] to play again', False, (33, 66, 112))

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type ==  pygame.KEYDOWN: # event has no key attribute
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_SPACE:
                    pygame.time.wait(500)
                    run = False
                
        WINDOW.blit(
            title_label,
            (
                (WIDTH - title_label.get_width())//2,
                round(HEIGHT*.33)
            )
        )

        WINDOW.blit(
            sub_title_label,
            (
                (WIDTH - sub_title_label.get_width())//2,
                round(HEIGHT*.33 + title_label.get_height() + 10)
            )
        )
        
        # Update window ------------------------------------------- #
        pygame.display.update()

    game_loop(high_score)
    
# Loop ------------------------------------------------------------ #
def game_loop(high_score):
    score = 0
    score_font = pygame.font.SysFont('Matura MT Script Capitals', 20, 1)
    hi_label = score_font.render(f'Hi: {high_score}', False, (33, 66, 112))
    
    player = Player(WINDOW, img_player, [50, HEIGHT - HEIGHT_PLAYER - HEIGHT_FLOOR])

    jump = False
    vel = vel_org = 10
    acc = 0.5

    obstacles = []
    obstacle_spawn_rate = 1.4
    spawn_timer = 0

    BG_x = 0
    bg_speed = 0.5
    bgs = []
    FG_x = 0
    fg_speed = 3
    visual_layer = {1: [VisualLayer(1)],
                    0: [VisualLayer(0)]}

    while True:
        # Clock --------------------------------------------------- #
        main_clock.tick(FPS)

        # Background ---------------------------------------------- #
        WINDOW.fill((0,0,0))

        score_label = score_font.render(f'Score: {score}', False, (33, 66, 112))

        # Buttons n stuff ----------------------------------------- #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN: # event has no key attribute
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
        # Jump ---------------------------------------------------- #
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not jump:
            jump = True
        if jump:
            player.y -= int(vel)
            vel -= acc
            if vel < -vel_org:
                vel = vel_org
                jump = False

        # Obstacle------------------------------------------------- #
        spawn_timer += 1
        if spawn_timer / FPS >= obstacle_spawn_rate:
            spawn_timer = 0
            obstacles.append(Obstacle())

        # Draw stuff ---------------------------------------------- #
        # Layer
        for layer_type, layer_list in visual_layer.items():
            last_layer = layer_list[-1]
            
            if WIDTH-last_layer.LAYER_SPEED[last_layer.layer_type]\
               <= last_layer.x + last_layer.width\
               <= WIDTH:
                    layer_list.append(VisualLayer(layer_type, append=True))
                    
            for layer in layer_list[:]:
                if layer.x + layer.width < 0:
                    layer_list.remove(layer)
                layer.draw()
        
        # Obstacles
        for obstacle in obstacles[:]:
            if obstacle.x + obstacle.width < 0:
                obstacles.remove(obstacle)
                score += 1
            else:
                obstacle.draw()

        # Player
        player.draw()
                
        # Score
        WINDOW.blit(
            score_label,
            (
                WIDTH - score_label.get_width() - 10,
                10
            )
        )

        WINDOW.blit(
            hi_label,
            (
                WIDTH - score_label.get_width() - 10 - hi_label.get_width() - 20,
                10
            )
        )
        
        # Update window ------------------------------------------- #
        pygame.display.update()

        # Collision ----------------------------------------------- #
        if obstacles:
            if collision(player, obstacles[0]):
                break
        
    if score > high_score:
        high_score = score
    game_over(high_score)

# Start Game Loop-------------------------------------------------- #    
game_loop(high_score)

# Close Pygame ---------------------------------------------------- #
pygame.quit()
sys.exit()
