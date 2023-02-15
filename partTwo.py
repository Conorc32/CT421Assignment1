import csv
import random
from statistics import mean
import matplotlib.pyplot as plt


def check_capacity(supervisor):
    if supervisors[supervisor][1] > 0:
        supervisors[supervisor][1] = supervisors[supervisor][1] - 1
        return True
    return False


def increase_capacity(supervisor):
    supervisors[supervisor][1] = supervisors[supervisor][1] + 1


def get_preference(student, supervisor):
    # +1 needed as first column contains student_1, Student_2 etc
    return int(studentChoices[student][supervisor+1])


def check_after_crossover(allocation, position):
    allocation_length = len(allocation)
    for j in range(allocation_length):
        supervisor = allocation[j]
        has_capacity = check_capacity(supervisor)
        while not has_capacity:
            supervisor = random.randint(0, numSupervisors-1)
            has_capacity = check_capacity(supervisor)
        allocation[j] = supervisor
    for j in range(numStudents):
        increase_capacity(allocations[position][j])


with open('C:\\Users\\Conor\\Downloads\\Student-choices.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    studentChoices = list(reader)

with open('C:\\Users\\Conor\\Downloads\\Supervisors.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    supervisors = list(reader)

for i in range(len(studentChoices)):
    studentChoices[i][1] = int(studentChoices[i][1])

for i in range(len(supervisors)):
    supervisors[i][1] = int(supervisors[i][1])

# ensure reproducible results
random.seed(0)

numStudents = len(studentChoices)
numSupervisors = len(supervisors)
numRuns = 1000
numAllocations = 6
fitness = [0 for i in range(numAllocations)]
allocations = [[0 for i in range(numStudents)] for j in range(numSupervisors)]
bestAllocation = []
bestAllocationFitness = 0
fittestAllocations = [0, 0, 0, 0, 0]
rand = 0
averageFitness = []


for i in range(numAllocations):
    for j in range(numStudents):
        hasCapacity = False
        while not hasCapacity:
            rand = random.randint(0, numSupervisors-1)
            hasCapacity = check_capacity(rand)
        allocations[i][j] = rand

    # must reset capacity or check_capacity will always be false after one allocation
    for j in range(numStudents):
        increase_capacity(allocations[i][j])

for i in range(numAllocations):
    for j in range(len(allocations[i])):
        fitness[i] += numSupervisors - get_preference(j, allocations[i][j])

for i in range(numRuns):
    fitnessCopy = fitness.copy()

    for j in range(3):
        fittest = max(fitnessCopy)
        fittestIndex = fitnessCopy.index(fittest)
        fittestAllocations[j] = allocations[fittestIndex]
        fitnessCopy[fittestIndex] = 0
        if fittest > bestAllocationFitness:
            bestAllocationFitness = fittest
            bestAllocation = allocations[fittestIndex]

    # use one-point crossover to generate children for next generation
    for j in range(3):
        rand = random.randint(0, numStudents-1)
        allocations[j*2] = fittestAllocations[0][0:rand] + fittestAllocations[(i+1) % 3][rand:46]
        allocations[j*2+1] = fittestAllocations[0][0:rand] + fittestAllocations[(i+1) % 3][rand:46]

    for j in range(numAllocations):
        for k in range(numStudents):
            # 3/100 chance for mutation, in this case I randomly swapped them with another students supervisor
            # as to prevent capacity being exceeded
            rand = random.randint(0, 100)
            if rand < 3:
                temp = allocations[j][k]
                rand2 = random.randint(0, numStudents-1)
                allocations[j][k] = allocations[j][rand2]
                allocations[j][rand2] = temp

    for j in range(numAllocations):
        check_after_crossover(allocations[j], j)
        fitness[j] = 0
        for k in range(numStudents):
            fitness[j] += numSupervisors - get_preference(k, allocations[j][k])

    averageFitness.append(mean(fitness)/numStudents)

print(bestAllocation)
print(bestAllocationFitness/numStudents)
print(numSupervisors - bestAllocationFitness/numStudents)

plt.plot(averageFitness)
plt.ylabel('Average Fitness')
plt.xlabel('Generations')
plt.show()

averagePreference = []
for i in range(numRuns):
    averagePreference.append(numSupervisors - averageFitness[i])

plt.plot(averagePreference)
plt.ylabel('Average preference allocated to student')
plt.xlabel('Generations')
plt.show()
