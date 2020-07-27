import pygame
import sys # exit
import math # sqrt
from random import randint
from Gravity import GravityParticle



# Setup Window ------------------------------------------------ #
pygame.init()
SIZE = WIDTH, HEIGHT = 600, 600

FPS = 60
main_clock = pygame.time.Clock()

WINDOW = pygame.display.set_mode((SIZE))
pygame.display.set_caption('Something')


dt = 1 / FPS # to simulate one second for the formula
M1, M2 = 15, 5

# particles
CENTER_OF_THE_WORLD = GravityParticle([300, 300], [0, 0], M1)
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
    CENTER_OF_THE_WORLD.draw(WINDOW)

    # reset particles
    if pygame.mouse.get_pressed()[2] == 1:
        particles = []

    # initialize particles somewhere
    if pygame.mouse.get_pressed()[0] == 1:
        x = randint(0, WIDTH)
        y = randint(0, HEIGHT)
        vel_x = randint(-100,100)
        vel_y = randint(-100,100)
        particles.append(GravityParticle([x, y], [vel_x, vel_y], M2))

    # calculate new forces
    for particle in particles:
        particle.recalculate_force(CENTER_OF_THE_WORLD)
        particle.recalculate_velocity()
        particle.move()
        particle.draw(WINDOW)

    # Update window ------------------------------------------- #
    pygame.display.update()
    main_clock.tick(FPS)
    
    
# Close Pygame ------------------------------------------------ #
pygame.quit()
sys.exit()
