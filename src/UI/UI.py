import random
import tkinter
import datetime

import matplotlib
matplotlib.use("TkAgg")

from Algorithm import TSP
from Algorithm import City
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import UI.Color as Color

class UI(object):
	def __init__(self, Height = 500, Width = 500, Grid = 10, Seed = None):
		self.__RouteLines = list()
		self.__CityCircles = list()
		self.__Cities = list()
		self.__Grid = Grid
		self.__Height = Height
		self.__Width = Width

		# Create a new main window
		self.__MainWindow = tkinter.Tk()
		self.__MainWindow.title("Traveling-Salesman")
		self.__MainWindow.resizable(0, 0)

		# Initialize GUI variables
		self.__Generations = tkinter.IntVar(self.__MainWindow)
		self.__Generations.set(100)

		self.__CityCount = tkinter.IntVar(self.__MainWindow)
		self.__CityCount.set(25)

		self.__PopulationSize = tkinter.IntVar(self.__MainWindow)
		self.__PopulationSize.set(100)

		self.__EliteSize = tkinter.IntVar(self.__MainWindow)
		self.__EliteSize.set(20)

		self.__MutationRate = tkinter.IntVar(self.__MainWindow)
		self.__MutationRate.set(1)

		if(Seed is not None):
			random.seed(Seed)

		# Start the UI
		self.__InitUI()

	"""
	Canvas method for grid drawing.
	"""
	def __CreateGrid(self, event = None):
		w = self.__DrawingCanvas.winfo_width()
		h = self.__DrawingCanvas.winfo_height()

		# Remove "GridLine"
		self.__DrawingCanvas.delete("GridLine")

		# Creates all vertical lines at intevals
		for i in range(0, w, self.__Grid):
			Line = self.__DrawingCanvas.create_line([(i, 0), (i, h)], fill = "white smoke")
			self.__DrawingCanvas.tag_lower(Line)

		# Creates all horizontal lines at intevals
		for i in range(0, h, self.__Grid):
			Line = self.__DrawingCanvas.create_line([(0, i), (w, i)], fill = "white smoke")
			self.__DrawingCanvas.tag_lower(Line)

	"""
	Create a new list with random cities.
	"""
	def __CreateCities(self):
		self.__Cities.clear()

		for Index in range(0, self.__CityCount.get()):
			x = int(random.random() * self.__Width)
			y = int(random.random() * self.__Height)

			# Save each city
			self.__Cities.append(City(x = x, y = y, name = str(Index + 1)))

	"""
	Initialize the dataset.
	"""
	def __InitDataset(self, Radius = 5):
		# Create some random cities to visit
		self.__CreateCities()

		# Remove each city 
		for City in self.__CityCircles:
			self.__DrawingCanvas.delete(City[0])
			self.__DrawingCanvas.delete(City[1])

		# Draw each city. Use a different color for the first city
		for Index in range(len(self.__Cities)):
			LocX = self.__Cities[Index].x + 25
			LocY = self.__Cities[Index].y + 25

			Text = self.__DrawingCanvas.create_text(LocX - 15, LocY, fill = "black", font = "Times 10", text = self.__Cities[Index].name)
			Circle = self.__DrawingCanvas.create_oval(LocX - Radius, 
													LocY - Radius, 
													LocX + Radius, 
													LocY + Radius, 
													fill = Color.COLORS[random.randint(0, len(Color.COLORS))]
													)

			self.__CityCircles.append([Text, Circle])

	"""
	Initialize the user interface.
	"""
	def __InitUI(self):
		# Add GUI elements
		TopFrame = tkinter.Frame(self.__MainWindow)
		TopFrame.grid(row = 0, column = 0)
		BottomFrame = tkinter.Frame(self.__MainWindow)
		BottomFrame.grid(row = 1, column = 0)

		LeftFrame = tkinter.Frame(TopFrame, padx = 10)
		LeftFrame.grid(row = 0, column = 0)

		MiddleFrame = tkinter.Frame(TopFrame, padx = 10)
		MiddleFrame.grid(row = 0, column = 1)

		RightFrame = tkinter.Frame(TopFrame, padx = 10)
		RightFrame.grid(row = 0, column = 2)

		RightButtonFrame = tkinter.Frame(TopFrame, padx = 10)
		RightButtonFrame.grid(row = 0, column = 3)

		self.__StartButton = tkinter.Button(RightButtonFrame, text = "Run", command = self.__StartButtonCallback)
		self.__StartButton.grid(row = 0, column = 0)
		tkinter.Button(RightButtonFrame, text = "New", command = self.__NewCitiesButtonCallback).grid(row = 1, column = 0)
		
		self.__DrawingCanvas = tkinter.Canvas(BottomFrame, bg = "white", height = self.__Height + 50, width = self.__Width + 50)
		self.__DrawingCanvas.grid(row = 0, column = 0)

		tkinter.Label(LeftFrame, text = "Cities:").grid(row = 0, column = 0)
		tkinter.OptionMenu(LeftFrame, self.__CityCount, *[I for I in range(10, 51, 1)]).grid(row = 0, column = 1)

		tkinter.Label(MiddleFrame, text = "Generations:").grid(row = 0, column = 0)
		tkinter.OptionMenu(MiddleFrame, self.__Generations, *[I for I in range(100, 550, 50)]).grid(row = 0, column = 1)
		
		tkinter.Label(MiddleFrame, text = "Population:").grid(row = 1, column = 0)
		tkinter.OptionMenu(MiddleFrame, self.__PopulationSize, *[I for I in range(100, 320, 20)]).grid(row = 1, column = 1)
		
		tkinter.Label(RightFrame, text = "Mutation %:").grid(row = 0, column = 0)
		tkinter.OptionMenu(RightFrame, self.__MutationRate, *[I for I in range(1, 101, 1)]).grid(row = 0, column = 1)

		tkinter.Label(RightFrame, text = "Elite:").grid(row = 1, column = 0)
		tkinter.OptionMenu(RightFrame, self.__EliteSize, *[I for I in range(10, 42, 2)]).grid(row = 1, column = 1)

		# Add a grid to the canvas
		self.__DrawingCanvas.bind("<Configure>", self.__CreateGrid)

		# Add some data
		self.__InitDataset()

		# Enter mainloop
		self.__MainWindow.mainloop()

	"""
	Finish callback for the genetic algorithm.
	"""
	def __on_finish(self, Progress, Fitness, LastPopulation):
		# Print the result
		print("[INFO] {} - Finish!".format(datetime.datetime.now()))
		print("[INFO] Shortest route: {}".format(LastPopulation[0]))

		# Draw a line between each city
		for City in range(len(LastPopulation[0]) - 1):
			self.__RouteLines.append(self.__DrawingCanvas.create_line(LastPopulation[0][City + 1].x + 25, 
																		LastPopulation[0][City + 1].y + 25, 
																		LastPopulation[0][City].x + 25,
																		LastPopulation[0][City].y + 25,
																		width = 2
																		)
									)

		# Draw a line between the first and the last city
		self.__RouteLines.append(self.__DrawingCanvas.create_line(LastPopulation[0][0].x + 25, 
																	LastPopulation[0][0].y + 25, 
																	LastPopulation[0][len(LastPopulation[0]) - 1].x + 25,
																	LastPopulation[0][len(LastPopulation[0]) - 1].y + 25,
																	width = 2
																	)
									)

		# Enable button
		self.__StartButton["state"] = "normal"

		# Create the plot
		Plot = Figure(facecolor = "white")
		Axis = Plot.add_subplot(111)

		# Add the first plot
		Series1 = Axis.plot([I for I in range(len(Progress))], Progress, "--g", label = "Distance")
		Axis.set_xlabel("Generation")
		Axis.set_ylabel("Distance")
		Axis.set_xticks([I for I in range(0, len(Progress), int(self.__Generations.get() / 10))])

		# Add a second plot and a second y axis
		Axis2 = Axis.twinx()
		Series2 = Axis2.plot([I for I in range(len(Fitness))], Fitness, "--r", label = "Fitness")
		Axis2.set_ylabel("Fitness")
		Axis2.ticklabel_format(style = "sci", scilimits = (-3, 4), axis = "y")
	
		# Set a legend
		Series = Series1 + Series2
		Legends = [Legend.get_label() for Legend in Series]
		Axis.legend(Series, Legends, loc = 7)

		# Add a grid to the plot
		Axis.grid()

		# Add the plot to the canvas
		Canvas = FigureCanvasTkAgg(Plot, master = self.__MainWindow)
		Canvas.get_tk_widget().grid(row = 1, column = 1)

	"""
	Callback for the 'Start' button.
	"""
	def __StartButtonCallback(self):
		# Remove all old lines
		for Line in self.__RouteLines:
			self.__DrawingCanvas.delete(Line)

		# Disable button
		self.__StartButton["state"] = "disabled"

		# Run the genetic algorithm
		Finder = TSP(Cities = self.__Cities,
					PopulationSize = self.__PopulationSize.get(),
					EliteSize = self.__EliteSize.get(),
					MutationRate = self.__MutationRate.get() / 100.0,
					Generations = self.__Generations.get(),
					on_finish = self.__on_finish
					)

		Finder.start()

	"""
	Callback for the 'New' button.
	"""
	def __NewCitiesButtonCallback(self):
		# Remove all old lines
		for Line in self.__RouteLines:
			self.__DrawingCanvas.delete(Line)

		# Create new cities to visit
		self.__InitDataset()
