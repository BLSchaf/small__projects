from pygame import draw
from math import sqrt
#from somewhere import dt

# The gravitational constant in this universe in pixels^3 kg^-1 s^-2.
# The real one is 6.67384*(10^-11) m^3 kg^-1 s^-2
G = 50000.0

''' Formula works with seconds'''
dt = 1/60 # dependend on FPS


class GravityParticle():
    def __init__(self, pos, mass, color=(180, 180, 180)):
        # initial values
        self.pos = pos
        self.vel = [0,0]
        self.mass = mass #used as size
        self.color = color
        self.force = [0,0]

    # @staticmethod
    def get_distance(self, particle):
        ''' Gets the distance between two objects '''
        dx = self.pos[0] - particle.pos[0]
        dy = self.pos[1] - particle.pos[1]
        
        return [dx, dy, sqrt(dx**2 + dy**2)]
        
    def recalculate_force(self, particle, BILATERAL=True, PULL=1):
        #BILATERAL is meh
        '''
        F = G * M1*M2 / r**2
        G is a constant
        M1 = self.mass
        M2 = particle.mass
        r = Distance between particles
        '''
        dx, dy, distance = self.get_distance(particle)
        force = (G * self.mass * particle.mass) / distance**2
        # scale force in x and y direction - negative, otherwise they repel
        self.force[0] += PULL * -dx/distance * force
        self.force[1] += PULL * -dy/distance * force

        if BILATERAL:
            particle.force[0] -= PULL * -dx/distance * force
            particle.force[0] -= PULL * -dx/distance * force

    def recalculate_velocity(self):
        '''
        F = MA -> A = F/M
        Acceleration is added to the current velocity
        '''
        a_x = dt * self.force[0] / self.mass # F = MA -> A = F/M
        a_y = dt * self.force[1] / self.mass
        self.vel[0] += a_x
        self.vel[1] += a_y

    def move(self):
        self.pos[0] += dt * self.vel[0]
        self.pos[1] += dt * self.vel[1]
        self.force = [0,0]

    def draw(self, window):
        draw.circle(window,
                    self.color,
                    (int(self.pos[0]),
                     int(self.pos[1])),
                    self.mass)
