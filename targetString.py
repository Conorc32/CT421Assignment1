import random
from statistics import mean
import matplotlib.pyplot as plt

digits = ["0", "1"]
population = ["", "", "", "", "", ""]
fitness = [0, 0, 0, 0, 0, 0]
meanFitness = []
generation = 1
targetString = "110011001100110011001100110011"

# ensure reproducible results
random.seed(0)

# Initial state of population
for i in range(6):
    for j in range(30):
        rand = random.randint(0, 1)
        if rand == 0:
            population[i] += digits[0]
        else:
            population[i] += digits[1]

print("Initial population Strings: ", population)

# continue until target string is reached
while (fitness[0] != 30) and (fitness[1] != 30) and (fitness[2] != 30) and (fitness[3] != 30) \
        and (fitness[4] != 30) and (fitness[5] != 30):
    for i in range(6):
        currFitness = 0
        currSequence = population[i]
        for j in range(30):
            # target string should contain only 1s
            if currSequence[j] == targetString[j]:
                currFitness += 1
        fitness[i] = currFitness

    fitnessCopy = fitness.copy()
    fittestSpecimens = []
    meanFitness.append(mean(fitness))
    print("Generation: ", generation)
    generation += 1
    print("Population: ", population)
    print("Fitness scores: ", fitness)
    print("Average fitness: ", meanFitness[generation-2])

    # determine which three specimens are the fittest
    for i in range(3):
        highestFitness = max(fitnessCopy)
        highestFitnessIndex = fitnessCopy.index(highestFitness)
        fitnessCopy[highestFitnessIndex] = 0
        fittestSpecimens.append(population[highestFitnessIndex])

    # use one-point crossover to generate children for next generation
    for i in range(3):
        rand = random.randint(0, 30)
        population[i*2] = fittestSpecimens[i][0:rand] + fittestSpecimens[(i+1) % 3][rand:30]
        population[i*2+1] = fittestSpecimens[i][0:rand] + fittestSpecimens[(i+2) % 3][rand:30]

    for i in range(6):
        currSequence = list(population[i])
        for j in range(30):
            # 1/30 chance for mutation, this will prevent convergence to a string which is not the optimal solution
            rand = random.randint(0, 30)
            if rand == 0:
                if currSequence[j] == '0':
                    currSequence[j] = '1'
                else:
                    currSequence[j] = '0'
        population[i] = "".join(currSequence)

    print("top 3 specimens: ", fittestSpecimens)
    print("\n")

print(meanFitness)

plt.plot(meanFitness)
plt.ylabel('Average fitness')
plt.xlabel('Generations')
plt.show()
