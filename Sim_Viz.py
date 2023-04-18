from SimulationTest import *
from GroteMarkt import GroteMarktModel
from CreateMap import CreateMap

import pyAgrum as gum
import pyAgrum.lib.image as bng
import matplotlib.pyplot as plt

import os

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import TextElement
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.UserParam import UserSettableParameter


from vizModule import WorkaroundCanvas, Image


from SimulationClasses.StreetAgent import StreetAgent
from SimulationClasses.Walkway import Walkway
from SimulationClasses.House import House
from SimulationClasses.Vision import Vision
from SimulationClasses.Goodie import Goodie
from SimulationClasses.Camera import Camera, SecurityCamera


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
        if agent.steal_state == "LOSER":
            portrayal["Color"] = "red"

        portrayal["Shape"] = "circle"
        portrayal["text_color"] = "black"
        if agent.role in ["victim", "thief"]:
            portrayal["text"] = agent.name + " " + str(agent.age) + " " + agent.ag_text
            portrayal["Layer"] = 2
            portrayal["r"] = 2
        portrayal["opacity"] = 1

    elif type(agent) is SecurityCamera:
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = "false"
        portrayal["Color"] = ["blue"]
        portrayal["r"] = agent.radius * 2
        portrayal["Layer"] = 2
        portrayal["opacity"] = 0.1

    elif str(type(agent)) == "<class 'GroteMarkt.Background'>":
        portrayal["Shape"] = str(agent.model.topic)
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
        for key in model.reporters.relevant_events:
            str_ = str_ + str(key) + " : " + str(model.reporters.history_dict[model.reporters.run][key]) + ",\t"
        return str_

class ScenarioDescription(TextElement):
    def render(self, model):
        return model.model_description






# params from map making
# y = 45
# x = int(y*1.5)
rel_events = []
n = 5
y = 20
coverage = None
topic_gen = os.getcwd() + "/groteMarkt.png"
C = CreateMap(topic_gen, coverage, y)
x = int(y*C.rel)

grid = WorkaroundCanvas(agent_portrayal1, x, y, int((C.rel)*500), 500)
model_params = {"N": n,
    "scenario" : UserSettableParameter(
        "slider",
        "Scenario",
        2,  # actual value
        1,  # min value
        4,  # max value
        1,  # step size
      description="what scenario do you want to investigate?",

    ),

    "width": x, "height": y, "topic":topic_gen, "reporters": None, "output_file":"GroteMarktOutcomes.csv", "torus":False}

text = Test()
model_text = ScenarioDescription()

#bnPic = Image("imgBNGroteMarkt.png", 250, 500, 250, 500)
server = ModularServer(GroteMarktModel, [model_text, grid, text], "Grote Markt", model_params)   #we're making a case model from previous data!!




#server.port = 8521 # The default
server.launch()