import numpy as np
import matplotlib.pyplot as plt
import random

#random.seed(3)
#np.random.seed(3)

N = 3
minDays = 3
maxDays = 5
population = np.zeros((N,N))
# not immune
S = population
# probability an ill person infects not immune neighbour
prOfInfect = 5

# probability an individual dies a day they are ill
prOfDeath = 5
# location of initially ill people
NinitiallyIll = 2

# length of time an individual is ill
timeOfIllness = np.zeros((1,NinitiallyIll))
for i in range(NinitiallyIll):
    timeOfIllness[0][i] = random.randint(minDays, maxDays)

#population[2][1] = 1
population[2][2] = 1
#listInfected = [[(2,1),timeOfIllness], [(2,2),random.randint(minDays, maxDays)]]
initialIllInd = np.argwhere(population==1)

oldMatrix = -1*np.ones((N,N))
# newMatrix = population.copy()


# initialize the days for initially infected indices
def appointDaysForInitiallyIll(timeOfillness, oldMatrix, initialIllInd):
    count = 0
    for x in initialIllInd:
        oldMatrix[x[0]][x[1]] = timeOfillness[0][count]
        count += 1



appointDaysForInitiallyIll(timeOfIllness, oldMatrix, initialIllInd)

#print('old pop:', oldMatrix)


# find neighbour indices of an infected individual
def findNeigh(population, ill):
    neighs = []
    illX = ill[0]
    illY = ill[1]
    for x in range(-1,2):
        for y in range(-1,2):
            if (illX+x < population.shape[0]) and (illX+x >= 0):
                if (illY+y < population.shape[1]) and (illY+y >= 0):
                    if illX+x != illX or illY+y != illY:
                        neighs.append([illX+x,illY+y])
    return neighs


# infect the neighbour
def infected(infectedNeighbour, population, newMatrix):
    population[infectedNeighbour[0]][infectedNeighbour[1]] = 1
    daysill = random.randint(minDays, maxDays)
    oldMatrix[infectedNeighbour[0]][infectedNeighbour[1]] = daysill
    newMatrix[infectedNeighbour[0]][infectedNeighbour[1]] = daysill
    return [(infectedNeighbour[0],infectedNeighbour[1]), daysill]


def infecting(ill, population, prOfInfect, initialIll, newMatrix):
    illX = ill[0]
    illY = ill[1]

    # nr of neighbours
    neighsIll = findNeigh(population, ill)

    for x in initialIllInd:
        for neigh in neighsIll:
            if [x[0], x[1]] == neigh:
                neighsIll.remove(neigh)

    #nr of neighbours that should be infected
    for neigh in neighsIll:
        Nrandom = random.randint(0,100)
        if Nrandom <= prOfInfect:
            infected(neigh, population, newMatrix)


def death(population, x, y, deathPr, newMatrix, oldMatrix):
    Nrandom = random.randint(0, 100)
    if Nrandom <= deathPr:
        population[x][y] = 3
        newMatrix[x][y] = -1
        oldMatrix[x][y] = -1

def immune(population, x, y):
    population[x][y]=2

def infect(population, initialIllInd, prOfinfect, prOfdeath, oldMatrix, newMatrix):
    for x in initialIllInd:
        infecting(x, population, prOfinfect, initialIllInd, newMatrix)
        illX = x[0]
        illY = x[1]

        if oldMatrix[illX][illY] == 0:
            immune(population, illX, illY)
        elif oldMatrix[illX][illY] > 0:
            #oldMatrix[illX][illY] -= 1
            newMatrix[illX][illY] -= 1
            death(population, illX, illY, prOfdeath, newMatrix, oldMatrix)


def infectingGeneral(i,j,population, infectPr, oldM, newM):
    neighsIll = findNeigh(population, [i, j])

    #for i in range(population.shape[0]):
    #    for j in range(population.shape[1]):
    for neigh in neighsIll:
        if population[neigh[0]][neigh[1]]== 1 or population[neigh[0]][neigh[1]]==2 or population[neigh[0]][neigh[1]]==3:
            neighsIll.remove(neigh)

    #nr of neighbours that should be infected
    for neigh in neighsIll:
        Nrandom = random.randint(0,100)
        if Nrandom <= prOfInfect:
            infected(neigh, population, newM)

# check every ill element and infect only non immune elements
def infectGeneral(population, infectPr, oldM, newM,i,j):
    #for i in range(population.shape[0]):
    #    for j in range(population.shape[1]):
    if population[i][j] == 1:
        infectingGeneral(i,j, population, infectPr, oldM, newM)
                #neighsIll = findNeigh(population, [i,j])




def deduct(newM):
    for i in range(newM.shape[0]):
        for j in range(newM.shape[1]):
            if newM[i][j] > 0:
                newM[i][j] -= 1


def checkStatus(pop, oldM, newM, deathPr, infectionPr):

    deduct(newM)

    for i in range(oldM.shape[0]):
        for j in range(oldM.shape[1]):
            if newM[i][j]==0:
                immune(pop, i, j)
            elif oldM[i][j] != newM[i][j]:
                death(pop, i, j, deathPr, newM, oldM)
                infectGeneral(population,infectionPr, oldM, newM,i,j)

print(population)
# infect(population,initialIllInd,prOfInfect, prOfDeath, oldMatrix, newMatrix)

# check if still ill or immune
# if ill infect more and remove one day
# if ill death wiht a certain probability
# if no longer ill, then immune
# checkStatus(population, oldMatrix, newMatrix, prOfDeath, prOfInfect)


#print(population)

def findNrInfected(newM, oldM):
    count = 0
    for i in range(newM.shape[0]):
        for j in range(newM.shape[1]):
            if newM[i][j]==oldM[i][j] and newM[i][j]>-1:
                count += 1

    return count

def findNrIll(newM, oldM):
    count = 0
    for i in range(newM.shape[0]):
        for j in range(newM.shape[1]):
            if newM[i][j] != oldM[i][j] and newM[i][j]>0:
                count += 1

    return count

def findNrDeath(population):
    count = 0
    for i in range(population.shape[0]):
        for j in range(population.shape[1]):
            if population[i][j]==3:
                count += 1

    return count

def findNrRecovered(population):
    count = 0
    for i in range(population.shape[0]):
        for j in range(population.shape[1]):
            if population[i][j] == 2:
                count += 1

    return count


def disease(population, oldM, deathpr, illpr, initialIllInd, nr):

    newM = np.asarray(oldMatrix).copy()

    # day 1 the already ill people infected other members in population
    infect(population, initialIllInd, illpr, deathpr, oldM, newM)

    listInfected = []
    listDeath = []
    listRecovered = []
    listIll = []
    listRecovered.append(findNrRecovered(population))
    listInfected.append(findNrInfected(newM, oldM))
    listDeath.append(findNrDeath(population))
    listIll.append(findNrIll(newM, oldM))
    day = 2
    while(np.any(population==1) == True):
        checkStatus(population, oldM, newM, deathpr, illpr)
        listInfected.append(findNrInfected(newM, oldM))
        listDeath.append(findNrDeath(population))
        listRecovered.append(findNrRecovered(population))
        listIll.append(findNrIll(newM, oldM))
        day += 1
        # print(day)
        # print(population)
        # print('new: ',newM)
        # print('Old: ',oldM)
    print('infected \n',listInfected)
    print('dead \n',listDeath)
    print('recovered \n',listRecovered)
    print(listIll)
    print(len(listInfected))
    print('The accumulated number of infected every day: ', sum(listInfected))
    print('The accumulated number of deaths per day: ', sum(listDeath))


disease(population, oldMatrix, prOfDeath, prOfInfect, initialIllInd, 1)
print(population)
