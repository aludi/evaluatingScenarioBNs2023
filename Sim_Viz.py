from SimulationTest import *
from GroteMarkt import MoneyModel
from CreateMap import CreateMap

import pyAgrum as gum
import pyAgrum.lib.image as bng
import matplotlib.pyplot as plt


from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import TextElement
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.ModularVisualization import VisualizationElement


from SimulationClasses.StreetAgent import StreetAgent
from SimulationClasses.Walkway import Walkway
from SimulationClasses.House import House
from SimulationClasses.Vision import Vision
from SimulationClasses.Goodie import Goodie
from SimulationClasses.Camera import Camera

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

class SimpleCanvas(VisualizationElement):
    local_includes = ["simple_continuous_canvas.js"]
    portrayal_method = None
    canvas_height = 500
    canvas_width = 500

    def __init__(self, portrayal_method, canvas_height=500, canvas_width=500):
        """
        Instantiate a new SimpleCanvas
        """
        self.portrayal_method = portrayal_method
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        new_element = "new Simple_Continuous_Module({}, {})".format(
            self.canvas_width, self.canvas_height
        )
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        space_state = []
        for obj in model.schedule.agents:
            portrayal = self.portrayal_method(obj)
            x, y = obj.pos
            x = (x - model.space.x_min) / (model.space.x_max - model.space.x_min)
            y = (y - model.space.y_min) / (model.space.y_max - model.space.y_min)
            portrayal["x"] = x
            portrayal["y"] = y
            space_state.append(portrayal)
        return space_state


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
        portrayal["Layer"] = 4

        if agent.target is None:
            portrayal["text"] = "agent"
            portrayal["text_color"] = "black"
        else:
            portrayal["text"] = "thief"
            portrayal["text_color"] = "black"



    elif type(agent) is House:
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        if agent.curtains is True:
            portrayal["Color"] = "black"
        elif agent.compromised is True:
            portrayal["Color"] = "red"
        else:
            portrayal["Color"] = "brown"
        portrayal["stroke_color"] = "red"
        portrayal["w"] = agent.width + 1
        portrayal["h"] = agent.height + 1
        portrayal["Layer"] = 1

    elif type(agent) is Walkway:
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        if agent.model.raining == False:
            portrayal["Color"] = ["#D0F0C0"]
            portrayal["stroke_color"] = "green"
        else:
            portrayal["Color"] = ["#9ABCA7"]
            portrayal["stroke_color"] = "blue"
        portrayal["Filled"] = "false"
        portrayal["w"] = agent.width*2
        portrayal["h"] = agent.height
        portrayal["opacity"] = 0.01
        portrayal["Layer"] = 0


    elif type(agent) is Goodie:
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        if agent.target_of == None:
            portrayal["Color"] = "yellow"
        else:
            portrayal["Color"] = "black"

        if agent.lost:
            portrayal["w"] = 0.05
            portrayal["h"] = 0.05
        else:
            portrayal["w"] = 0.25
            portrayal["h"] = 0.25
        portrayal["Layer"] = 4


    elif type(agent) is Vision:
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = "false"
        portrayal["Color"] = ["blue"]
        portrayal["r"] = agent.radius*2
        portrayal["Layer"] = 2
        portrayal["opacity"] = 0.2

    elif type(agent) is Camera:
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = "false"
        portrayal["Color"] = ["blue"]
        portrayal["r"] = agent.radius * 2
        portrayal["Layer"] = 2
        portrayal["opacity"] = 0.05

    return portrayal


def agent_portrayal1(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r":0.75,"Layer":0, "Color":"yellow",  "opacity":0}


    if str(type(agent)) == "<class 'GroteMarkt.MoneyAgent'>":
        if agent.pos == agent.goal:
            portrayal["Color"] = "black"
        if agent.steal_state == "SNEAK":
            portrayal["Color"] = "pink"
        portrayal["Shape"] = "circle"
        portrayal["text_color"] = "black"
        portrayal["text"] =  agent.name + " " + str(agent.age) + " " + agent.ag_text
        portrayal["opacity"] = 1

    elif str(type(agent)) == "<class 'GroteMarkt.Background'>":
        portrayal["Shape"] = str(agent.model.topic) + ".png"
        portrayal["Color"] = "Blue"
        portrayal["scale"] = 50
        portrayal["h"] = 500
        portrayal["w"] = int((1.5)*500)
        portrayal["Layer"] = 0
        portrayal["opacity"] = 1



    return portrayal

def agent_portrayal2(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.05, "Layer": 0, "Color": "yellow", "opacity": 0}




    bnK2 = gum.loadBN("BNGroteMarkt/main.net")
    bng.export(bnK2, "imgBNGroteMarkt.png")
    bng.exportInference(bnK2, "imgBNGroteMarkt.png", evs={})




    if str(type(agent)) == "<class 'GroteMarkt.BN'>":
        portrayal["Shape"] = "imgBNGroteMarkt.png"
        portrayal["Color"] = "Blue"
        portrayal["scale"] = 1
        portrayal["h"] = 500
        portrayal["w"] = 250
        portrayal["Layer"] = 0
        portrayal["opacity"] = 1

    return portrayal



class Test(TextElement):
    def render(self, model):
        str_ = ""
        for key in model.reporters.pure_frequency_event_dict.keys():
            str_ = str_ + str(key) + " : " + str(model.reporters.history_dict[model.reporters.run][key]) + ",\t"
        return str_





sim = 1
if sim == 0:
    rel_events = ["lost_object", "know_object", "target_object", "motive", "compromise_house",
                                        "flees_startled", "successful_stolen", "raining", "curtains",
                                        "E_object_is_gone",
                                        "E_broken_lock",
                                        "E_disturbed_house",
                                        "E_s_spotted_by_house",
                                        "E_s_spotted_with_goodie",
                                        "E_private"]

    grid = CanvasGrid(agent_portrayal, 16, 9, 400*1.7, 400)
    text = Test()
    new_reporters = Reporters(rel_events)
    server = ModularServer(StolenLaptop,
                           [grid, text],
                           "Stolen Laptop",
                           {"N_agents":2, "N_houses":2, "width":16, "height":9, "reporters":new_reporters})
elif sim == 1:



    # params from map making
    # y = 45
    # x = int(y*1.5)
    rel = ["motive", "sneak", "stealing"]

    reporters = Reporters(rel)

    y = 20
    topic_gen = "groteMarkt4"
    C = CreateMap(topic_gen, y)
    x = int(y*C.rel)
    grid = CanvasGrid(agent_portrayal1, x, y, int((C.rel)*500), 500)
    text = Test()
    bnPic = CanvasGrid(agent_portrayal2, 250, 500, 250, 500)
    server = ModularServer(MoneyModel, [grid, text], "Grote Markt", {"N": 10,"width": x, "height": y, "topic":topic_gen,
                                                               "reporters": reporters,
                                                               "torus":False})






#server.port = 8521 # The default
server.launch()