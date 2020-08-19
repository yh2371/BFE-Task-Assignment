Genetic Algorithm
=================

This section contains documentation on functions used to start the genetic algorithm, for documentation on how the individual stages of the genetic algorithm works, please refer to the Generation, Schedule, Week and Day classes.

.. toctree::
   :maxdepth: 1


.. function:: genetic(filename, checkerlist, generationSize, numOfReproductions, mutationRate, fitnessThreshold, month=None, year=None):

    Starts genetic algorithm to run for a certain number of reproductions of generations at a given size, returns the individual (schedule) with the best score out of all generations

    :param filename: name of sample set file
    :type filename: string
    :param checkerlist: CheckerList object
    :type checkerlist: CheckerList
    :param generationSize: number of schedules in the generation
    :type generationSize: int
    :param numOfReproductions: number of reproductions
    :type numOfReproductions: int
    :param mutationRate: the probability of mutation during reproduction for all individuals
    :type mutationRate: float
    :param fitnessThreshold: the minimum fitness score an individual must have to participate in reproduction (added to the mating pool)
    :type fitnessThreshold: float
    :param month: month of schedule
    :type month: int
    :param year: year of schedule
    :type year: int
    :rtype: Schedule object
