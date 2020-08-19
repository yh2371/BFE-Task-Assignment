from util import *
from classes import *

"""# Genetic Algorithm"""

def genetic(filename, checkerlist, generationSize, numOfReproductions, mutationRate, fitnessThreshold, month=None, year=None):
  onoff = get_onandoff_sample(filename)

  genZero = Generation(0, generationSize, mutationRate, fitnessThreshold, month, year, onoff, checkerlist)
  genZero.initialize()

  generations = [genZero]
  bestSchedules = [genZero.get_bestIndividual()]
  #print(genZero.get_bestIndividual())

  currGen = genZero
  print("Generation 0")
  print("Best Schedule:")
  genZero.get_bestIndividual().evaluate()
  print()


  for i in range(numOfReproductions):
    nextGen = currGen.reproduce()
    generations.append(nextGen)
    bestSchedules.append(nextGen.get_bestIndividual())
    currGen = nextGen
    print("Generation", i+1)
    print("Best Schedule:")
    nextGen.get_bestIndividual().evaluate()
    print()

  maxfit = 0
  best = None
  for schedule in bestSchedules:
    if schedule.get_fitness() > maxfit:
      maxfit = schedule.get_fitness()
      best = schedule

  return schedule
