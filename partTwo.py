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

numStudents = len(studentChoices)
numSupervisors = len(supervisors)
numAllocations = 6
fitness = [0 for i in range(numAllocations)]
allocations = [[0 for i in range(numStudents)] for j in range(numSupervisors)]
bestAllocation = []
bestAllocationFitness = 1000
fittestAllocations = [0, 0, 0, 0, 0]
rand = 0
averagePreference = []


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
        fitness[i] += get_preference(j, allocations[i][j])

for i in range(5000):
    fitnessCopy = fitness.copy()

    for j in range(3):
        fittest = min(fitnessCopy)
        fittestIndex = fitnessCopy.index(fittest)
        fittestAllocations[j] = allocations[fittestIndex]
        fitnessCopy[fittestIndex] = 1000
        if fittest < bestAllocationFitness:
            bestAllocationFitness = fittest
            bestAllocation = allocations[fittestIndex]

    for j in range(3):
        rand = random.randint(0, numStudents-1)
        allocations[0] = fittestAllocations[0][0:rand] + fittestAllocations[1][rand:46]
        allocations[1] = fittestAllocations[0][0:rand] + fittestAllocations[2][rand:46]
        allocations[2] = fittestAllocations[1][0:rand] + fittestAllocations[0][rand:46]
        allocations[3] = fittestAllocations[1][0:rand] + fittestAllocations[2][rand:46]
        allocations[4] = fittestAllocations[2][0:rand] + fittestAllocations[0][rand:46]
        allocations[5] = fittestAllocations[2][0:rand] + fittestAllocations[1][rand:46]

    for j in range(numAllocations):
        for k in range(numStudents):
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
            fitness[j] += get_preference(k, allocations[j][k])

    averagePreference.append(mean(fitness)/numStudents)

print(fitness)
print(bestAllocation)
print(bestAllocationFitness)
print(bestAllocationFitness/numStudents)

plt.plot(averagePreference)
plt.ylabel('Average preference allocated to student')
plt.xlabel('Generations')
plt.show()
