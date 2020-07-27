import pygame
import sys # exit
import math # sqrt, pi, cos, sin
from random import randint, uniform



# Setup Window ------------------------------------------------ #
pygame.init()
SIZE = WIDTH, HEIGHT = 600, 600

FPS = 60
main_clock = pygame.time.Clock()

WINDOW = pygame.display.set_mode((SIZE))
pygame.display.set_caption('Something')

'''
The gravitational constant in this universe in pixels^3 kg^-1 s^-2.
The real one is 6.67384*(10^-11) m^3 kg^-1 s^-2
# m := p * V
# kg := size in pixel
# s := FPS * dt
# r = distance
# F = G * m1*m2 / r**2
# a1 = F1 / m1 = G * m2/r**2
'''

G = 6.67384e-11#0.0000000000667384
#G = 6.7e-14
dt = 1 #/ FPS # to simulate one second for the formulas

P_EARTH = 5510 # in kg/m³ - earth 5,51 g/cm³ -> 5510
P_MOON = 3340
# mass earth 5,972 × 10^24 kg
#V = 4/3 * pi * r³
r_earth = 6.371e+6 # 6.371 km
r_moon = 1.737e+6 # 1.737 km
# entfernung zum mond 384.400 km
SIZE1 = 15
SIZE2 = int(round(r_moon/r_earth * SIZE1))
r_scale = r_earth / SIZE1
mass = lambda r: 4/3*math.pi * (r_scale*r)**3 * P_EARTH
#mass_moon = lambda r: 4/3*math.pi * (r_scale*r)**3 * P_MOON

vel_moon = int(1.022e+6 / r_scale) #Average orbital speed 1.022 km/s
max_initial_speed = vel_moon

#print(mass(SIZE1), mass(SIZE2))
            

# Particle[[pos], [vel], [force], size]

def calculate_force(particle1, particle2):
    # Calc Distance
    dx = particle1[0][0] - particle2[0][0]
    dy = particle1[0][1] - particle2[0][1]
    distance = math.sqrt(dx**2 + dy**2)

    # Calc Force
    force = G * mass(particle1[3]) * mass(particle2[3]) / (r_scale*distance)**2
    # Scale force in x and y direction; negative, otherwise they repel
    force_x = -dx/distance * force
    force_y = -dy/distance * force
    return force_x, force_y

def calculate_acceleration(particle, force):
    # Calculate new velocity of particle - current vel + acceleration
    a_x = dt * force[0] / mass(particle[3]) # F = MA -> A = F/M
    a_y = dt * force[1] / mass(particle[3])
    return a_x, a_y

def update_position(particles):
    for i, particle in enumerate(particles):
        for j, other_particle in enumerate(particles[i+1:]):
            
            force = calculate_force(particle, other_particle)
            
            particles[i][2][0] += force[0]
            particles[i][2][1] += force[1]
            
            particles[i+j+1][2][0] -= force[0]
            particles[i+j+1][2][1] -= force[1]
        
    for particle in particles[1:]: # don't include center
        a = calculate_acceleration(particle, particle[2])
        #print('x', particle[0][0]
        #print('vel', particle[1])
        #print('force', particle[2])
        #print('a_x', a[0])

        particle[1][0] += a[0]
        particle[1][1] += a[1]

        particle[0][0] += dt * particle[1][0]
        particle[0][1] += dt * particle[1][1]

        # Reset force
        particle[2] = [0,0]

# Particles
particles = []
CENTER_OF_THE_WORLD = [[300, 300], [0, 0], [0, 0], SIZE1]
particles.append(CENTER_OF_THE_WORLD)

music = 1

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
    pygame.draw.circle(WINDOW, (255,255,255),
                       (int(CENTER_OF_THE_WORLD[0][0]),
                       int(CENTER_OF_THE_WORLD[0][1])), SIZE1)

    # reset
    if pygame.mouse.get_pressed()[2] == 1:
        particles = []
        
    # spawn
    if pygame.mouse.get_pressed()[0] == 1:
        x = randint(0, WIDTH)
        y = randint(0, HEIGHT)
        angle = uniform(0.0, 2.0*math.pi)
        random_speed = uniform(0.0, max_initial_speed)
        vel_x, vel_y = [random_speed*math.cos(angle), random_speed*math.sin(angle)]
        print(len(particles))
        particles.append([[x, y], [vel_x, vel_y], [0, 0], SIZE2])
        
    # calc new position and draw
    if len(particles) > 1:
        
        update_position(particles)
        for particle in particles[1:]:
            pygame.draw.circle(WINDOW, (180, 180, 180),
                               (int(particle[0][0]), int(particle[0][1])), particle[3])
        
    # Update window ------------------------------------------- #
    pygame.display.update()
    main_clock.tick(FPS)
    
    
# Close Pygame ------------------------------------------------ #
pygame.quit()
sys.exit()
