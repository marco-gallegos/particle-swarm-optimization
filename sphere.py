import random
import numpy as np
from ORM import Optimizacion

W = 0.5
c1 = 0.8
c2 = 0.9

n_iterations = 4000
target_error = 0
n_particles = 50
target = 0
dimensiones = [2, 4, 8, 16]
ejecuciones = range(5)
funcion = "sphere"
limite_inferior = -5.12
limite_superior = 5.12

class Particle():
    def __init__(self , dimension = 2, limite_inferior=-10, limite_superior=10):
        self.limite_inferior = limite_inferior
        self.limite_superior = limite_superior

        arr = []
        vel_arr = []
        i=0
        while i < dimension:
            arr.append((-1) ** (bool(random.getrandbits(1))) * random.random() * self.limite_inferior)
            arr.append((-1) ** (bool(random.getrandbits(1))) * random.random() * self.limite_superior)
            vel_arr.append(0)
            vel_arr.append(0)
            i += 2
        self.position = np.array(arr)

        # self.position = np.array([(-1) ** (bool(random.getrandbits(1))) * random.random() * self.limite_inferior,
        #                          (-1) ** (bool(random.getrandbits(1))) * random.random() * self.limite_superior])
        self.pbest_position = self.position
        self.pbest_value = float('inf')
        self.velocity = np.array(vel_arr)

    def __str__(self):
        print("I am at ", self.position, " meu pbest is ", self.pbest_position)

    def move(self):
        self.position = self.position + self.velocity

    def fitness(self):
        f = 0
        for element in self.position:
            f+=element**2
        return f
        # return self.position[0] ** 2 + self.position[1] ** 2 + 1


class Space():

    def __init__(self, target, target_error, n_particles, dimension = 2, limite_inferior=-10, limite_superior=10):
        self.target = target
        self.target_error = target_error
        self.n_particles = n_particles
        self.particles = []
        self.gbest_value = float('inf')

        arr = []
        for i in range(dimension):
            arr.append(random.random() * limite_inferior)
        self.gbest_position = np.array(arr)
        # self.gbest_position = np.array([random.random() * 50, random.random() * 50])

    def print_particles(self):
        for particle in self.particles:
            particle.__str__()

    def fitness(self, particle):
        return particle.fitness()
        # print(particle.position)
        # return particle.position[0] ** 2 + particle.position[1] ** 2 + 1

    def set_pbest(self):
        for particle in self.particles:
            fitness_cadidate = self.fitness(particle)
            if (particle.pbest_value > fitness_cadidate):
                particle.pbest_value = fitness_cadidate
                particle.pbest_position = particle.position

    def set_gbest(self):
        for particle in self.particles:
            best_fitness_cadidate = self.fitness(particle)
            if (self.gbest_value > best_fitness_cadidate):
                self.gbest_value = best_fitness_cadidate
                self.gbest_position = particle.position

    def move_particles(self):
        for particle in self.particles:
            # print(particle.velocity)
            global W
            new_velocity = (W * particle.velocity) + (c1 * random.random()) * (
                        particle.pbest_position - particle.position) + \
                           (random.random() * c2) * (self.gbest_position - particle.position)
            particle.velocity = new_velocity
            # print(particle.velocity)
            particle.move()


for dimension in dimensiones:
    for ejecucion in ejecuciones:
        search_space = Space(target, target_error, n_particles, dimension=dimension, limite_inferior=limite_inferior, limite_superior=limite_superior)
        particles_vector = [Particle(dimension=dimension, limite_inferior=limite_inferior, limite_superior=limite_superior) for _ in range(search_space.n_particles)]
        search_space.particles = particles_vector
        # search_space.print_particles()

        iteration = 0
        while (iteration < n_iterations):
            search_space.set_pbest()
            search_space.set_gbest()

            #if (abs(search_space.gbest_value - search_space.target) <= search_space.target_error):
            #    break
            if iteration % 100 is 0:
                data = Optimizacion()
                data.funcion = funcion
                data.dimension = dimension
                data.fitness = search_space.gbest_value
                data.generacion = iteration
                data.save()

            search_space.move_particles()
            iteration += 1

            print("The best solution is: ", search_space.gbest_position," performance :  ",search_space.gbest_value, " in iteration: ", iteration, " ", ejecucion, " ", dimension)
