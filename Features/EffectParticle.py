import pygame
import random


class EffectParticle():
    life = 1
    def __init__(self, pos, vel, size, decay, color=(255, 255, 255)):
        self.pos = pos
        self.vel = vel
        self.size = size
        self.decay = decay
        self.color = list(color)
        
        

class SplashParticle(EffectParticle):
    def __init__(self, pos, vel, size, decay, color=(255, 255, 255)):
        super().__init__(pos, vel, size, decay, color)
        # transparency?
        # self.screen = pygame.Surface((int(size), int(size)), pygame.SRCALPHA)

    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        self.vel[0] -= 0.1 * self.vel[0]
        self.vel[1] -= 0.1 * self.vel[1]

        self.life -= self.decay

    def draw(self, window):
        pygame.draw.circle(
            window,
            tuple(map(lambda rgb: int(rgb*self.life), self.color)),
            (int(self.pos[0]), int(self.pos[1])),
            int(self.size*self.life)
        )
        # transparency?
        # window.blit(self.screen, self.pos)

# flickery flame
'''
vel = [random.uniform(-0.5, 0.5), random.uniform(-4, -2)],
size = random.randint(3, 7),
decay = random.uniform(0.05, 0.15)
[[random.uniform(-1, 1), random.uniform(-4, -2)], random.randint(3, 7), random.uniform(0.05, 0.15)]
'''

# splash
'''
vel = [random.uniform(-5, 5), random.uniform(-5, 5)],
size = random.randint(3, 7),
decay = 0.1
[[random.uniform(-5, 5), random.uniform(-5, 5)], random.randint(3, 7), 0.1]
'''
