import pygame
import random
import math
from Features.EffectParticle import SplashParticle


# Setup Window ------------------------------------------------ #
pygame.init()
SIZE = WIDTH, HEIGHT = 600, 400

FPS = 60
main_clock = pygame.time.Clock()

WINDOW = pygame.display.set_mode((SIZE))
pygame.display.set_caption('test_collision')


particles = []
FLICKERY_FLAME = [[random.uniform(-0.5, 0.5), random.uniform(-4, -2)],
                  random.randint(3, 7),
                  random.uniform(0.05, 0.15)]

radius = 100
radius_orign = radius

random_geflacker = 0
flacker_timer_origin = FPS//10
flacker_timer = flacker_timer_origin

# Loop -------------------------------------------------------- #
while True:

    # Background ---------------------------------------------- #
    WINDOW.fill((255,255,255))
    pygame.draw.rect(WINDOW,(100,100,220),(80,80,100,100))
    # A black mask for the screen ----------------------------- #
    MASK = pygame.surface.Surface(SIZE).convert_alpha()
    MASK.fill((0,0,0,255))


    # Buttons n stuff ----------------------------------------- #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN: # event has no key attribute
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        # change radius
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                if radius < radius_orign*2:
                    radius += radius_orign*0.1
            elif event.button == 5:
                if radius > radius_orign//2:
                    radius -= radius_orign*0.1
    radius_quotient = radius / radius_orign

    # Particles n stuff --------------------------------------- #

    if pygame.mouse.get_pressed()[0] == 1:

        for _ in range(10):
            particles.append(
                SplashParticle(list(pygame.mouse.get_pos()),
                               # *FLICKERY_FLAME doesn't work?
                               [random.uniform(-0.25, 0.25)*radius_quotient, random.uniform(-2, -1)*radius_quotient],
                               random.randint(3, 7)*radius_quotient,
                               random.uniform(0.05, 0.15)/radius_quotient,
                               color=(255,120,50)
                )
            )

        # Flacker timer
        flacker_timer -= 1
        if flacker_timer <= 1:
            random_geflacker = random.randint(0,2)
            flacker_timer = flacker_timer_origin
               
        
        # for each frame, reset outer radius to radius
        radius_outer = radius
        alpha = 255
        radius_delta = 5
        alpha_delta = 10
        i = 0
        # for each frame, draw all circles from big to small
        while radius_outer - math.exp(i)//10 > radius_orign*0.4:
            pygame.draw.circle(MASK,
                               (0, 0, 0, int(max(0, alpha - math.exp(i)))),
                               (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - 10),
                               int(radius_outer + random_geflacker)
                               )
            radius_outer -= math.exp(i) // 10
            i += 0.5
            
    for particle in particles:
        particle.move()
        
        if particle.life <= 0:
            particles.remove(particle)
            
        else:
            particle.draw(WINDOW)

    pygame.draw.rect(MASK,(200,200,200),(WIDTH - 22, HEIGHT - 8, 14, -int(radius_orign*2 + 4)))
    pygame.draw.rect(MASK,(100,100,220),(WIDTH - 20, HEIGHT - 10, 10, -int(radius)))
    WINDOW.blit(MASK,(0,0))
    
        

    
    # Update window ------------------------------------------- #
    pygame.display.update()
    main_clock.tick(FPS)
    
    
# Close Pygame ------------------------------------------------ #
pygame.quit()
sys.exit()
