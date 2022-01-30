from SimulationTest import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import TextElement

from mesa.visualization.ModularVisualization import ModularServer

from SimulationClasses.StreetAgent import StreetAgent
from SimulationClasses.Walkway import Walkway
from SimulationClasses.House import House
from SimulationClasses.Vision import Vision
from SimulationClasses.Goodie import Goodie
from Reporters import Reporters


_COLORS = [
    "Aqua",
    "Blue",
    "Fuchsia",
    "Gray",
    "Green",
    "Lime",
    "Maroon",
    "Navy",
    "Olive",
    "Orange",
    "Purple",
    "Red",
    "Silver",
    "Teal",
    "White",
    "Yellow",
]

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "false",
                 "r": 0.5,
                 "Layer":0,
                 "opacity": 1}

    if type(agent) is StreetAgent:
        if agent.seen_goodie == 0:
            portrayal["Color"] = ["yellow", "orange"]
            if agent.observed is True:
                portrayal["Color"] = ["fuchsia"]

        else:
            portrayal["Color"] = ["yellow", "orange", "red"]
            portrayal["r"] = 0.2
        portrayal["Layer"] = 2

        if agent.target is None:
            portrayal["text"] = "agent"
            portrayal["text_color"] = "black"
        else:
            portrayal["text"] = "thief"
            portrayal["text_color"] = "black"



    elif type(agent) is House:
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        if agent.compromised is False:
            portrayal["Color"] = "brown"
        else:
            portrayal["Color"] = "red"
        portrayal["stroke_color"] = "red"
        portrayal["Filled"] = "false"
        portrayal["w"] = agent.width
        portrayal["h"] = agent.height
        portrayal["Layer"] = 0

    elif type(agent) is Walkway:
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Color"] = ["#D0F0C0"]
        portrayal["stroke_color"] = "green"
        portrayal["Filled"] = "false"
        portrayal["w"] = agent.width*2
        portrayal["h"] = agent.height
        portrayal["opacity"] = 0.01
        portrayal["Layer"] = 0


    elif type(agent) is Goodie:
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        if agent.target_of == None:
            portrayal["Color"] = "teal"
        else:
            portrayal["Color"] = "black"
        portrayal["w"] = 0.25
        portrayal["h"] = 0.25
        portrayal["Layer"] = 3


    elif type(agent) is Vision:
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = "false"
        portrayal["Color"] = ["blue"]
        portrayal["r"] = agent.radius*2
        portrayal["Layer"] = 1
        portrayal["opacity"] = 0.4

    return portrayal

class Test(TextElement):
    def render(self, model):
        str_ = ""
        for key in model.reporters.pure_frequency_event_dict.keys():
            str_ = str_ + str(key) + " : " + str(model.reporters.history_dict[model.reporters.run][key]) + ",\t"
        return str_

grid = CanvasGrid(agent_portrayal, 16, 9, 400*1.7, 400)
text = Test()
new_reporters = Reporters()

server = ModularServer(StolenLaptop,
                       [grid, text],
                       "Stolen Laptop",
                       {"N_agents":2, "N_houses":2, "width":16, "height":9, "reporters":new_reporters})


'''
server = ModularServer(Street,
                       [grid],
                       "Street Model",
                       {"N_agents":2, "N_houses":2, "width":16, "height":9})
'''

server.port = 8521 # The default
server.launch()