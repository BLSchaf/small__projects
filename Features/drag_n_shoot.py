import pygame
import math

pygame.init()
CLOCK = pygame.time.Clock()


SIZE = WIDTH, HEIGHT = 500, 500
WHITE = (255,255,255)
BLACK = (0,0,0)

WINDOW = pygame.display.set_mode(SIZE)


class Ball():
    radius = 5
    
    def __init__(self, center):
        self.center = self.x, self.y = center
        self.vel = 0
        self.radian = 0

    def draw(self):
        pygame.draw.circle(WINDOW, WHITE, (int(self.x), int(self.y)), self.radius)

    def move(self):
        self.x += self.vel * math.cos(self.radian)
        self.y += self.vel * math.sin(self.radian)

    def change_vel(self, force):
        # ********** change direction and velocity?
        # acceleration instead of vel?
        pass

    def change_direction(self, force):
        # ********** change direction and velocity?
        pass

# ********** make sense of functions
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
    
    rotation = math.atan2(-dy, dx)
    
    pygame.draw.polygon(
        window, WHITE,
        (
            (mirrored_end[0],
             mirrored_end[1]),

            (mirrored_end[0] - round(head_size*math.sin(rotation + 60*math.pi/180)),
             mirrored_end[1] - round(head_size*math.cos(rotation + 60*math.pi/180))),

            (mirrored_end[0] - round(head_size*math.sin(rotation + 130*math.pi/180)),
             mirrored_end[1] - round(head_size*math.cos(rotation + 130*math.pi/180)))
        )
    ) # ********** fix degrees later


balls = []

new_ball = False
run = True
while True:
    
    # set Frames
    CLOCK.tick(60)

    # clear screen
    WINDOW.fill(BLACK)

    # check for closing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            run = False

    # check if mouse gets pressed down
    if pygame.mouse.get_pressed()[0] == 1:
        if not new_ball:
            balls.append(Ball(pygame.mouse.get_pos()))
            new_ball = True
        start, end = balls[-1].center, pygame.mouse.get_pos()
        draw_arrow(WINDOW, WHITE, start, end, 2, 7)
            
    # set initial velocity and direction on mouse release
    if pygame.mouse.get_pressed()[0] == 0 and new_ball:
        balls[-1].radian = get_radian(start, end)
        balls[-1].vel = 5 * get_distance(start, end) / 60
        # ********** set .vel with more sense
        new_ball = False
            
    for ball in balls:
        #print(ball.x)
        ball.move()
        ball.draw()
    
    pygame.display.update()

        
        

        
pygame.quit()
