import pygame
import sys
import random


# Setup Window ------------------------------------------------ #
pygame.init()
SIZE = WIDTH, HEIGHT = 600, 400

FPS = 60
main_clock = pygame.time.Clock()

WINDOW = pygame.display.set_mode((SIZE))
pygame.display.set_caption('Fountain')

# particles
particles = []

# Loop -------------------------------------------------------- #
while True:

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
    # perma spawn in center ----------------------------------- #
    # [pos, vel, size]
    particles.append([[300, 200], [random.uniform(-1, 1), -5], random.randint(3, 7)])

    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[1][1] += random.randint(10, 20) / 100
        particle[2] -= 0.1
        
        if particle[2] <= 0:
            particles.remove(particle)
            
        else:
            pygame.draw.circle(WINDOW, (255,255,255), (int(particle[0][0]), int(particle[0][1])), int(particle[2]))
        

    
    # Update window ------------------------------------------- #
    pygame.display.update()
    main_clock.tick(FPS)
    
    
# Close Pygame ------------------------------------------------ #
pygame.quit()
sys.exit()
