import pygame
import random
from Features.EffectParticle import SplashParticle

CLOCK = pygame.time.Clock()

WIDTH = 600
HEIGHT = 400

# initialize window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT)) # save as variable to draw on
pygame.display.set_caption('PONG')


class Rectangle():
    def __init__(self, pos, size, window):
        self.pos = list(pos)
        self.size = size
        self.x, self.y = pos
        self.width, self.height = size
        self.window = window

    def draw(self):
        pygame.draw.rect(self.window,
                         (255, 255, 255),
                         (int(self.x), int(self.y), self.width, self.height),
                         0)


class Player(Rectangle):
    def __init__(self, pos, size, window, vel=5):
        super().__init__(pos, size, window)
        self.vel = vel

    def move_up(self):
        if self.y > 5:
            self.y -= self.vel

    def move_down(self):
        if self.y + self.height < self.window.get_height() - 5:
            self.y += self.vel


class Ball(Rectangle):
    sound = 0
    def __init__(self, pos, size, window):
        super().__init__(pos, size, window)
        self.vel_x = random.choice((-2, 2))
        self.vel_y = random.choice((-2, -1,5, -1, -0.5, 0.5, 1, 1.5, 2))

    def move(self):

        if self.game_over():
            return None
        else:
            if self.h_bound():
                #increase speed with each hit
                self.vel_x += self.vel_x//abs(self.vel_x) * 1
                self.vel_y += self.vel_y//abs(self.vel_y) * 1
                self.vel_x = -self.vel_x
            if self.v_bound():
                self.vel_y = -self.vel_y

            if self.h_bound():
                if self.sound == 0:
                    #print('ping')
                    self.sound = 1
                else:
                    #print('pong')
                    self.sound = 0

            self.x += self.vel_x
            self.y += self.vel_y

    def v_bound(self):
        if self.y + self.height > self.window.get_height()\
           or self.y < 0:
            return True
        return False
    
    def h_bound(self):
        if collision(self, player_l, 'l')\
           or collision(self, player_r, 'r'):
            return True
        return False

    def game_over(self):
        if self.x < 0 or self.x > self.window.get_width():
            return True
 

def collision(obj_1, obj_2, side):
    #print(obj_1, obj_2)
    if obj_1.y + obj_1.height > obj_2.y and obj_1.y < obj_2.y + obj_2.height:            
            if side == 'r':
                if obj_1.x + obj_1.width > obj_2.x and obj_1.x < obj_2.x:
                    return True
            else:
                if obj_1.x < obj_2.x + obj_2.width and obj_1.x + obj_1.width > obj_2.x:
                    return True
    return False


PLAYER_HEIGHT = 100
PLAYER_WIDTH = 20
WINDOW_VMID = (HEIGHT - PLAYER_HEIGHT) // 2
player_l = Player((10, WINDOW_VMID), (PLAYER_WIDTH, PLAYER_HEIGHT), WINDOW)
player_r = Player((WIDTH-PLAYER_WIDTH-10, WINDOW_VMID), (PLAYER_WIDTH, PLAYER_HEIGHT), WINDOW)

ball = Ball((WIDTH//2, HEIGHT//2), (10, 10), WINDOW)


effect_particles = []
#sound = 0

run = True
while run:

    CLOCK.tick(60)
    
    # draw static
    WINDOW.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            run = False
            #break

    # move player
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        player_l.move_up()
    if key[pygame.K_s]:
        player_l.move_down()
        
    if key[pygame.K_UP]:
        player_r.move_up()
    if key[pygame.K_DOWN]:
        player_r.move_down()

    if key[pygame.K_SPACE]:
        #reset
        ball = Ball((WIDTH//2, HEIGHT//2), (10, 10), WINDOW)
        

    # move ball
    ball.move()
    if ball.h_bound():
        for _ in range(10):
            effect_particles.append(
                SplashParticle([ball.x, ball.y],
                               [random.uniform(-5, 5), random.uniform(-5, 5)],
                               random.randint(3, 7),
                               0.1
                )
            )

    for particle in effect_particles:
        particle.move()
    
        if particle.life <= 0:
            effect_particles.remove(particle)
        
        else:
            particle.draw(WINDOW)
                    

    # draw stuff
    player_l.draw()
    player_r.draw()
    ball.draw()
    pygame.display.update()
