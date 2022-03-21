from SimulationTest import *
from GroteMarkt import MoneyModel

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
    portrayal = {"Shape": "rect", "Filled": "true", "r": 0.5,"w": 5, "h": 5,"Layer":0, "Color":"black"}
    print(type(agent))

    if str(type(agent)) == "<class 'GroteMarkt.MoneyAgent'>":
        portrayal["Shape"] = "circle"
        if agent.wealth > 0:
            portrayal["Color"] = "red"
            portrayal["Layer"] = 1
        else:
            portrayal["Color"] = "blue"
            portrayal["Layer"] = 1


    elif str(type(agent)) == "<class 'GroteMarkt.Dagobert'>":
        portrayal["Shape"] = "groteMarkt.png"
        portrayal["Color"] = "Blue"
        portrayal["scale"] = 25
        portrayal["h"] = 25
        portrayal["w"] = 25

        portrayal["Layer"] = 0
        portrayal["opacity"] = 0.3

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

    grid = CanvasGrid(agent_portrayal1, 25, 25, 500, 500)

    server = ModularServer(MoneyModel, [grid], "Grote Markt", {"N": 10,"width": 25, "height": 25})






server.port = 8521 # The default
server.launch()