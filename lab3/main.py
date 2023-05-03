import random
import numpy as np
from functools import cmp_to_key

subjects = ["Math", "English", "Science", "History", "Physical Education"]
classrooms = [1, 2, 3]
time_slots = ["9-10", "10-11", "11-12", "12-1", "1-2"]

# Parameters
population_size = 100
num_generations = 1000
mutation_rate = 0.1
crossover_rate = 0.8
elite_size = 2

def generate_random_schedule():
    schedule = np.zeros((len(time_slots), len(classrooms)), dtype=int)
    for i, subject in enumerate(subjects):
        row, col = random.randint(0, len(time_slots)-1), random.randint(0, len(classrooms)-1)
        while schedule[row][col] != 0:
            row, col = random.randint(0, len(time_slots)-1), random.randint(0, len(classrooms)-1)
        schedule[row][col] = i + 1
    return schedule

def fitness(schedule):
    score = 0

    for row in range(len(time_slots)):
        for col in range(len(classrooms)):
            if np.count_nonzero(schedule[row] == schedule[row][col]) > 1:
                score -= 1

    subject_counts = np.array([np.count_nonzero(schedule == i + 1) for i in range(len(subjects))])
    score += np.sum(subject_counts == 1)

    return score

def tournament_selection(population, k=2):
    return random.sample(population, k=max(k, 2))

def crossover(parent1, parent2):
    crossover_point = random.randint(0, len(parent1))
    child1 = np.vstack((parent1[:crossover_point], parent2[crossover_point:]))
    child2 = np.vstack((parent2[:crossover_point], parent1[crossover_point:]))
    return child1, child2

def mutate(schedule):
    mutated_schedule = schedule.copy()
    for i in range(len(time_slots)):
        for j in range(len(classrooms)):
            if random.random() < mutation_rate:
                mutated_schedule[i][j] = random.choice(range(len(subjects))) + 1
    return mutated_schedule

population = [generate_random_schedule() for _ in range(population_size)]

for generation in range(num_generations):
    population.sort(key=cmp_to_key(lambda a, b: fitness(b) - fitness(a)))

    elites = population[:elite_size]

    parents = []
    for _ in range(population_size // 2 - elite_size):
        parent1, parent2 = tournament_selection(population)
        parents.append((parent1, parent2))

    children = []
    for parent1, parent2 in parents:
        if random.random() < crossover_rate:
            child1, child2 = crossover(parent1, parent2)
        else:
            child1, child2 = parent1, parent2
        children.append(child1)
        children.append(child2)

    for i in range(len(children)):
        children[i] = mutate(children[i])

    population = elites + children

best_schedule = max(population, key=fitness)

print("Best schedule (fitness score = {}):".format(fitness(best_schedule)))
for i, row in enumerate(best_schedule):
    for j, cell in enumerate(row):
        if cell != 0:
            print("{} in Classroom {} during {}".format(subjects[cell - 1], classrooms[j], time_slots[i]))