from SimulationTest import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


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
        else:
            portrayal["Color"] = ["yellow", "orange", "red"]
            portrayal["r"] = 0.2
        portrayal["Layer"] = 2
        portrayal["text"] = "hi im agent"



    elif type(agent) is House:
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Color"] = "brown"
        portrayal["stroke_color"] = "red"
        portrayal["Filled"] = "false"
        portrayal["w"] = agent.width
        portrayal["h"] = agent.height
        portrayal["Layer"] = 0

    elif type(agent) is Walkway:
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Color"] = "silver"
        portrayal["stroke_color"] = "grey"
        portrayal["Filled"] = "false"
        portrayal["w"] = agent.width*2
        portrayal["h"] = agent.height
        portrayal["Layer"] = 0


    elif type(agent) is Goodie:
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Color"] = "yellow"
        portrayal["w"] = 0.1
        portrayal["h"] = 0.1
        portrayal["Layer"] = 3


    elif type(agent) is Vision:
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = "false"
        portrayal["Color"] = ["blue"]
        portrayal["r"] = 8
        portrayal["Layer"] = 1
        portrayal["opacity"] = 0.4

    return portrayal

grid = CanvasGrid(agent_portrayal, 16, 9, 400*1.7, 400)
server = ModularServer(Street,
                       [grid],
                       "Street Model",
                       {"N_agents":2, "N_houses":2, "width":16, "height":9})
server.port = 8521 # The default
server.launch()