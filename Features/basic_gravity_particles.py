import pygame
import sys # exit
import math # sqrt
from random import randint



# Setup Window ------------------------------------------------ #
pygame.init()
SIZE = WIDTH, HEIGHT = 600, 600

FPS = 60
main_clock = pygame.time.Clock()

WINDOW = pygame.display.set_mode((SIZE))
pygame.display.set_caption('Something')

# The gravitational constant in this universe in pixels^3 kg^-1 s^-2.
# The real one is 6.67384*(10^-11) m^3 kg^-1 s^-2
# m := pixel
# kg := size in pixel
# s := frame
# r = distance
# F = G * m1*m2 / r**2
# a1 = F1 / m1 = G * m2/r**2
G = 50000.0
dt = 1 / FPS # to simulate one second for the formula
M1, M2 = 15, 5

# particles
CENTER_OF_THE_WORLD = (300, 300)
particles = []
music = 0

# Loop -------------------------------------------------------- #
while True:
    if particles and not music:
        music = 1
        pygame.mixer.music.load('Inerstellar.mp3')
        pygame.mixer.music.play()

    # Background ---------------------------------------------- #
    WINDOW.fill((0,0,0))

    # Buttons n stuff ----------------------------------------- #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN: # event has no key attribute
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Particles n stuff --------------------------------------- #
    pygame.draw.circle(WINDOW, (255,255,255), CENTER_OF_THE_WORLD, M1)

    # reset
    if pygame.mouse.get_pressed()[2] == 1:
        particles = []

    if pygame.mouse.get_pressed()[0] == 1:
        # initialize particle somewhere
        x = randint(0, WIDTH)
        y = randint(0, HEIGHT)
        x_vel = randint(-100,100)
        y_vel = randint(-100,100)
        #print(x_vel, y_vel)
        particles.append([[x, y], [x_vel, y_vel]])

    for particle in particles:
        # calculate new forces
        dx = particle[0][0] - CENTER_OF_THE_WORLD[0]
        dy = particle[0][1] - CENTER_OF_THE_WORLD[1]
        # r
        distance = math.sqrt(dx**2 + dy**2)
        #m1 = 15, m2 = 5; size of circles... at the moment fixed
        force = (G * M1 * M2) / distance**2
        # scale force in x and y direction - negative, otherwise they repel
        x_force = -dx/distance * force
        y_force = -dy/distance * force
        # calculate new velocity of particle - current vel + acceleration
        x_a = dt * x_force / M2 # F = MA -> A = F/M
        y_a = dt * y_force / M2
        #print(particles.index(particle), particle[1][0], particle[1][1])
        particle[1][0] += x_a
        particle[1][1] += y_a
        # calculate new position of particle - before or after new vel?
        particle[0][0] += dt * particle[1][0]
        particle[0][1] += dt * particle[1][1]

        # draw each particle
        pygame.draw.circle(WINDOW, (180, 180, 180), (int(particle[0][0]), int(particle[0][1])), M2)
        
    # Update window ------------------------------------------- #
    pygame.display.update()
    main_clock.tick(FPS)
    
    
# Close Pygame ------------------------------------------------ #
pygame.quit()
sys.exit()
