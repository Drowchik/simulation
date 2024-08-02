from action import Action
from const import PATH
from mapping import Map
from point import Point


class Render:
    def __init__(self, map_coord: Map, counter=None) -> None:
        self.map_matrix = map_coord
        self.counter = counter

    @staticmethod
    def print_info():
        dict_info_object = {
            'P': 'predator',
            'H': 'herbivores',
            'G': 'grass',
            'R': 'rock',
            'T': 'tree',
        }
        for key, value in dict_info_object.items():
            print(f'{key} - {value}')
        print()

    def draw_map(self):
        for i in range(self.map_matrix.height):
            for j in range(self.map_matrix.weight):
                obj = self.map_matrix.get_object(Point(j, i))
                if obj:
                    print("|" + obj.sprite + "|", end="")
                else:
                    print("|  |", end="")
            print()


class Simulation:
    def __init__(self, height: int, weight: int) -> None:
        self.move_count = 0
        self.matrix = Map(height, weight)
        self.render = Render(map_coord=self.matrix)
        self.action = Action(map_coord=self.matrix, proportion_file=PATH)

    def next_turn():
        pass

    def start_simulation(self):
        self.render.print_info()
        self.action.init_actions()
        print("1 итерация")
        self.render.draw_map()
        self.action.turn_actions()
        print("2 итерация")
        self.render.draw_map()
        # while(True):
        #     self.render.draw_map()
        #     self.action.turn_actions()

    def pause_simulation():
        pass
