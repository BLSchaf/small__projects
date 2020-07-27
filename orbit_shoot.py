import pygame
import math
from Features.Gravity import GravityParticle


pygame.init()
CLOCK = pygame.time.Clock()


SIZE = WIDTH, HEIGHT = 500, 500
WHITE = (255,255,255)
BLACK = (0,0,0)

WINDOW = pygame.display.set_mode(SIZE)
RADIUS = 5

CENTER = (WIDTH//2, HEIGHT//2)
GRAVITY_FIELD = GravityParticle(CENTER, 15, color=(255, 255, 255))


# Some Functions
def get_coord_diff(start, end):
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    return dx, dy

def get_distance(start, end):
    dx, dy = get_coord_diff(start, end)
    return math.sqrt(dx**2 + dy**2)

def get_radian(start, end):
    dx, dy = get_coord_diff(start, end)
    return math.atan2(dy, dx)
    
def draw_arrow(window, colour, start, end, width, head_size):
    ''' draw a line in opposite direction of mouse and add a polygon '''
    dx, dy = get_coord_diff(start, end)
    mirrored_end = (start[0]+dx, start[1]+dy)
    
    pygame.draw.line(window, colour, start, mirrored_end, width)
    
##    rotation = math.atan2(-dy, dx)
##    
##    pygame.draw.polygon(
##        window, WHITE,
##        (
##            (mirrored_end[0],
##             mirrored_end[1]),
##
##            (mirrored_end[0] - round(head_size*math.sin(rotation + 60*math.pi/180)),
##             mirrored_end[1] - round(head_size*math.cos(rotation + 60*math.pi/180))),
##
##            (mirrored_end[0] - round(head_size*math.sin(rotation + 130*math.pi/180)),
##             mirrored_end[1] - round(head_size*math.cos(rotation + 130*math.pi/180)))
##        )
##    ) # ********** fix degrees later


balls = []

holding = False
run = True
while True:
    
    # set Frames
    CLOCK.tick(60)

    # clear screen
    WINDOW.fill(BLACK)
    GRAVITY_FIELD.draw(WINDOW)

    # check for closing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            run = False

    # clear balls
    if pygame.mouse.get_pressed()[2] == 1:
        balls = []
    # check if mouse gets pressed down
    if pygame.mouse.get_pressed()[0] == 1:
        
        if not holding:            
            new_ball = GravityParticle(list(pygame.mouse.get_pos()), RADIUS)
            holding = True
            
        start, end = new_ball.pos, pygame.mouse.get_pos()
        draw_arrow(WINDOW, WHITE, start, end, 2, 7)
        new_ball.draw(WINDOW)
            
    # set initial velocity and direction on mouse release
    if pygame.mouse.get_pressed()[0] == 0 and holding:
        radian = get_radian(start, end)
        vel = get_distance(start, end)
        new_ball.vel[0] += vel * math.cos(radian)
        new_ball.vel[1] += vel * math.sin(radian)
        holding = False
        balls.append(new_ball)
            
    for i, ball in enumerate(balls):
        ball.recalculate_force(GRAVITY_FIELD, BILATERAL=False)
        for other_ball in balls[i+1:]:
            ball.recalculate_force(other_ball)
            
        ball.recalculate_velocity()
        ball.move()
        ball.draw(WINDOW)
    
    pygame.display.update()

        
        

        
pygame.quit()
