from abc import ABC, abstractmethod
import json
from random import randint
from typing import Dict, Tuple
from math import floor

from const import PATH


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, value: object) -> bool:
        return self.x == value.x and self.y == value.y

    def __str__(self) -> str:
        return f"X: {self.x} Y: {self.y}"


class Enity(ABC):
    def __init__(self, point: Point, sprite: str) -> None:
        self.coordinate = point
        self.sprite = sprite


class Grass(Enity):
    def __init__(self, point: Point, sprite: str = "G") -> None:
        super().__init__(point, sprite)


class Rock(Enity):
    def __init__(self, point: Point, sprite: str = "R") -> None:
        super().__init__(point, sprite)


class Tree(Enity):
    def __init__(self, point: Point, sprite: str = "T") -> None:
        super().__init__(point, sprite)


class Creature(Enity, ABC):
    def __init__(self, point: Point, sprite: str, speed: int, health: int) -> None:
        super().__init__(point, sprite)
        self.speed = speed
        self.health = health

        @abstractmethod
        def make_move():
            pass


class Herbivore(Creature):
    def __init__(self, point: Point, speed: int = 1, health: int = 5, sprite: str = "H") -> None:
        super().__init__(point, sprite, speed, health)

    def make_move():
        pass


class Predator(Creature):
    def __init__(self, point: Point, speed: int = 2, health: int = 8, atack: int = 5, sprite: str = "P") -> None:
        super().__init__(point, sprite, speed, health)
        self.atack = atack

    def make_move():
        pass

    def atake_herbivore():
        pass


class Map:
    def __init__(self, height: int, weight: int) -> None:
        self.height = height
        self.weight = weight
        self.map_coord = {}

    def get_size(self) -> Tuple[int]:
        return self.height, self.weight

    def get_area(self) -> int:
        return self.height*self.weight

    def add_object(self, obj: Enity) -> Dict:
        # возможно проверку на x, y у объекта выходит ли он за границы
        point = obj.coordinate
        self.map_coord[point] = obj
        return self.map_coord[point]

    def delete_object(self, point) -> None:
        del self.map_coord[point]

    def get_object(self, point) -> Enity | bool:
        if point in self.map_coord.keys():
            return self.map_coord[point]
        return False


class Action:
    def __init__(self, map_coord: Map, proportion_file: str) -> None:
        self.map_matrix = map_coord
        self.proportion = Reader.read_json(proportion_file)

    def calculate_count(self, proportion):
        return floor(self.map_matrix.get_area()*proportion)

    def add_objects(self, count, object_class):
        while (count):
            point = Point(randint(0, self.map_matrix.weight - 1),
                          randint(0, self.map_matrix.height - 1))
            if not self.map_matrix.get_object(point):
                obj = object_class(Point(randint(0, self.map_matrix.weight - 1),
                                         randint(0, self.map_matrix.height - 1)))
                self.map_matrix.add_object(obj)
                count -= 1

    def init_actions(self):
        object_map = {
            "Grass": Grass,
            "Rock": Rock,
            "Tree": Tree,
            "Herbivore": Herbivore,
            "Predator": Predator
        }
        for obj_name, proportion in self.proportion.items():
            self.add_objects(self.calculate_count(proportion),
                             object_map[obj_name])

    def turn_actions():
        pass


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
                    print("|" + obj.sprite + "|", end=" ")
                else:
                    print("| |", end=" ")
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
        self.render.draw_map()

    def pause_simulation():
        pass


class Reader:
    @staticmethod
    def read_json(filename: str):
        with open(filename, "r") as file:
            return json.load(file)


if __name__ == "__main__":
    a = Simulation(5, 5)
    a.start_simulation()
