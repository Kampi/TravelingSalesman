import numpy
import pandas
import random
import operator
import threading

from .Fitness import Fitness

class TSP(Fitness, threading.Thread):
	def __init__(self, Cities, PopulationSize, EliteSize, MutationRate, Generations, on_finish = None):
		threading.Thread.__init__(self)
		self.__Cities = Cities
		self.__PopulationSize = PopulationSize
		self.__EliteSize = EliteSize
		self.__MutationRate = MutationRate
		self.__Generations = Generations
		self.__on_finish = on_finish

	@property
	def Population(self):
		return self.__Population

	"""
	Run the genetic algorithm.
	"""
	def run(self):
		Distance = list()
		Fitness = list()
		Populations = list()

		# Create a new population
		self.CreatePopulation(self.__PopulationSize)
		Distance.append(1.0 / self.RankPopulation()[0][1])
		Fitness.append(self.RankPopulation()[0][1])

		for _ in range(0, (self.__Generations - 1)):
			self.NextGeneration(self.__EliteSize, self.__MutationRate)
			Distance.append(1.0 / self.RankPopulation()[0][1])
			Fitness.append(self.RankPopulation()[0][1])
			Populations.append(self.__Population)

		# Trigger finish callback
		if(self.__on_finish is not None):
			self.__on_finish(Distance, Fitness, Populations[-1])

	def NextGeneration(self, EliteSize, MutationRate):
		MatingPool = self.Selection(self.RankPopulation(), EliteSize)
		Children = self.BreedPopulation(MatingPool, EliteSize)
		self.MutatePopulation(Children, MutationRate)

	"""
	Randomize the given cities.
	
	Returns:
		[list] -- Random list with the given cities
	"""
	def CreateRandomRoutes(self):
		return random.sample(self.__Cities, len(self.__Cities))

	"""
	Create a new population with the given size.
	
    Arguments:
		Size {int} -- Size of the population
	"""
	def CreatePopulation(self, Size):
		self.__Population = list()

		for _ in range(0, Size):
			self.__Population.append(self.CreateRandomRoutes())

	"""
	Sort the population based on his fitness level.
	
	Returns:
		[list] -- Sorted population
	"""
	def RankPopulation(self):
		FitnessResults = dict()

		for I in range(0, len(self.__Population)):
			FitnessResults.update( {I : Fitness(self.__Population[I]).TourFitness()} )

		return sorted(FitnessResults.items(), key = operator.itemgetter(1), reverse = True)

	"""
	Create a new mating pool based on a ranked population.
	
    Arguments:
		RankedPopulation {list} -- Ranked population
		EliteSize {int} -- Size of the elite individuals

	Returns:
		[list] -- Selected individuals
	"""
	def Selection(self, RankedPopulation, EliteSize):
		MatingPool = list()
		Frame = pandas.DataFrame(numpy.array(RankedPopulation), columns = ["Population", "Fitness"])
		Frame["RelativeFitness"] = Frame.Fitness.cumsum() / Frame.Fitness.sum()

		# Pick the n best individuals of the population
		for I in range(0, EliteSize):
			MatingPool.append(self.__Population[RankedPopulation[I][0]])
		
		# Apply a fitness proportionate selection
		for _ in range(0, len(RankedPopulation) - EliteSize):
			Pick = random.random()
			for I in range(0, len(RankedPopulation)):
				if(Pick <= Frame.iat[I, 2]):
					MatingPool.append(self.__Population[RankedPopulation[I][0]])
					break
		
		return MatingPool

	"""
	Create the next generation of a individual.
	
    Arguments:
		Father {list} -- 
		Mother {list} -- 

	Returns:
		[] -- New individual
	"""
	def Breed(self, Father, Mother):
		ChildFather = list()
		ChildMother = list()

		# Choose a random number of features of booth parents
		GenA = int(random.random() * len(Father))
		GenB = int(random.random() * len(Mother))

		# Get the choosen features from the father
		for I in range(min(GenA, GenB), max(GenA, GenB)):
			ChildFather.append(Father[I])

		# Fill the rest with features from the mother
		ChildMother = [Item for Item in Mother if Item not in ChildFather]

		# Combine the features to create a child
		return ChildFather + ChildMother

	"""
	Create the next generation of the whole population.
	
    Arguments:
		MatingPool {list} -- 
		EliteSize {int} -- Size of the elite individuals

	Returns:
		[list] -- List with new children
	"""
	def BreedPopulation(self, MatingPool, EliteSize):
		Children = list()

		RandomPool = random.sample(MatingPool, len(MatingPool))

		# Select the best performing individuals
		for I in range(0, EliteSize):
			Children.append(MatingPool[I])

		for I in range(0, len(MatingPool) - EliteSize):
			Child = self.Breed(RandomPool[I], RandomPool[len(MatingPool) - I - 1])
			Children.append(Child)

		return Children

	"""
	Mutate a single individual by randomly swapping the cities.
	
    Arguments:
		Individual {list} -- 
		MutationRate {double} -- Mutation chance

	Returns:
		[] -- 
	"""
	def Mutate(self, Individual, MutationRate):
		for Swapped in range(len(Individual)):
			if(random.random() < MutationRate):
				SwapWith = int(random.random() * len(Individual))

				Temp1 = Individual[Swapped]
				Temp2 = Individual[SwapWith]

				Individual[Swapped] = Temp2
				Individual[SwapWith] = Temp1

		return Individual

	"""
	Mutate the whole population individual.
	
    Arguments:
		Population {list} -- Population
		MutationRate {double} -- Mutation chance
	"""
	def MutatePopulation(self, Population, MutationRate):
		MutatedPopulation = list()

		for I in range(0, len(Population)):
			MutatedPopulation.append(self.Mutate(Population[I], MutationRate))

		self.__Population = MutatedPopulation