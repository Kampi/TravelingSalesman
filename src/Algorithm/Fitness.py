"""
    Fitness class for a given list of city tours.
"""
class Fitness(object):
    def __init__(self, TourList):
        self.__TourList = TourList
        self.__Distance = 0
        self.__Fitness = 0

    """
    Get the complete distance of the given tour.
    
    Returns:
        [double] -- Distance of the whole tour
    """
    def __TourDistance(self):
        if(self.__Distance == 0):
            PathDistance = 0
            for I in range(0, len(self.__TourList)):
                FromCity = self.__TourList[I]
                ToCity = None
                if((I + 1) < len(self.__TourList)):
                    # Get the distance to the next city
                    ToCity = self.__TourList[I + 1]
                else:
                    # Get the distance back to the start city
                    ToCity = self.__TourList[0]
                PathDistance += FromCity.Distance(ToCity)
            self.__Distance = PathDistance

        return self.__Distance

    """
    Calculate the fitness of the given tour.
    
    Returns:
        [double] -- Fitness of the whole tour
    """
    def TourFitness(self):
        if(self.__Fitness == 0):
            self.__Fitness = 1.0 / float(self.__TourDistance())

        return self.__Fitness