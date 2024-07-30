from collections import deque
import json

from abc import ABC, abstractmethod
from random import randint
from typing import Dict, List, Tuple
from math import floor

from const import PATH


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return f"X: {self.x} Y: {self.y}"

    def __repr__(self) -> str:
        return f"Point(X:{self.x}, Y:{self.y})"

    def get_neighboors(self) -> list:
        # возможна проверка не вышел ли я за границу
        return [Point(self.x, self.y+1), Point(self.x, self.y-1),
                Point(self.x+1, self.y), Point(self.x-1, self.y)]

    @property
    def point(self) -> tuple:
        return self.x, self.y

    @point.setter
    def point(self, x: int, y: int) -> None:
        self.x, self.y = x, y


class Enity(ABC):
    def __init__(self, point: Point, sprite: str) -> None:
        self.coordinate = point
        self.sprite = sprite

    def get_coord(self) -> tuple:
        return self.coordinate.x, self.coordinate.y


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
        point = obj.coordinate
        self.map_coord[point] = obj
        return self.map_coord[point]

    def delete_object(self, point) -> None:
        del self.map_coord[point]

    def get_object(self, point) -> Enity | bool:
        if point in self.map_coord.keys():
            return self.map_coord[point]
        return False

    def get_all_object(self, sprite: str) -> List[Enity]:
        return [point for point, enity in self.map_coord.items() if enity.sprite == sprite]

    def check_have_object(self, point: Point) -> bool:
        return 0 <= point.x < self.weight and 0 <= point.y < self.height
    # def check_point(self, point: Point) -> bool:
    #     return self.map_coord[point].sprite not in ["🌱", "⛰️ ", "🌲"]

    def search_path(self, start: Point, target: Point) -> List[Point]:
        queue = deque([(start, [start])])
        visited = set([start])
        neighbor_target = target.get_neighboors()
        while queue:
            current, path = queue.popleft()

            if current in neighbor_target:
                return path

            for neighbor in current.get_neighboors():
                if not self.check_have_object(neighbor):
                    continue
                if neighbor in self.map_coord:
                    continue
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return []


class Grass(Enity):
    def __init__(self, point: Point, sprite: str = "🌱") -> None:
        super().__init__(point, sprite)


class Rock(Enity):
    def __init__(self, point: Point, sprite: str = "⛰️ ") -> None:
        super().__init__(point, sprite)


class Tree(Enity):
    def __init__(self, point: Point, sprite: str = "🌲") -> None:
        super().__init__(point, sprite)


class Creature(Enity, ABC):
    def __init__(self, point: Point, sprite: str, speed: int, health: int) -> None:
        super().__init__(point, sprite)
        self.speed = speed
        self.health = health

    def make_move(self, new_x, new_y):
        self.point = Point(new_x. new_y)

    def find_eat(self, map_matrix, start, sprite):
        points = [Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0)]
        queue = list()
        visited = set()

        while queue:
            curr = queue.pop()

            if map_matrix.get(curr) == sprite:
                return curr

            for p in points:
                neighbor = Point(curr.x+p.x, curr,)


class Herbivore(Creature):
    def __init__(self, point: Point, speed: int = 1, health: int = 5, sprite: str = "🐇") -> None:
        super().__init__(point, sprite, speed, health)


class Predator(Creature):
    def __init__(self, point: Point, speed: int = 2, health: int = 8, atack: int = 5, sprite: str = '🐺') -> None:
        super().__init__(point, sprite, speed, health)
        self.atack = atack

    def atake_herbivore(map_coord: Map, point: Point):
        pass


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

    def turn_actions(self, spirit: str):
        for cord, enit in self.map_matrix.map_coord.items():
            if isinstance(enit, Predator):
                grass = self.map_matrix.get_all_object("🐇")
                short_path = []
                for i in grass:
                    short_path.append(self.map_matrix.search_path(cord, i))
                print(enit.sprite, cord)
                for i in short_path:
                    print(i, end="\n")
        # for cord, enit in self.map_matrix.map_coord.items:
        #     if type(enit) == Predator:
        #         neighbors = cord.get_neighboors()
        #         flag = False
        #         for point in neighbors:
        #             if type(self.map_matrix.get_object(point)) == Herbivore:
        #                 self.map_matrix.map_coord[point].health -= self.map_matrix.map_coord[cord].atack
        #                 if self.map_matrix.map_coord[point].health < 0:
        #                     self.map_matrix.delete_object(point)
        #                 flag = True
        #                 break
        #         if flag:
        #             grass = self.map_matrix.get_all_object("🌱")
        #             short_path = []
        #             for i in grass:
        #                 short_path.append(self.map_matrix.search_path(cord, i))
        #             print(*short_path)


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
        self.render.draw_map()
        self.action.turn_actions()
        # while(True):
        #     self.render.draw_map()

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

    # найти всех сущест +
    # функция получения соседних точек +
    # функция для поиска кратчайших путей bfs +
    # метод который будет для всех существ вызывать
    # метод поиска кратчайшего пути
    # пото
