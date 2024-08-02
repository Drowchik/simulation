from abc import ABC, abstractmethod

from enity import Enity, Grass
from mapping import Map
from point import Point


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

    @abstractmethod
    def attack(self, map_matrix: Map):
        pass


class Herbivore(Creature):
    def __init__(self, point: Point, speed: int = 1, health: int = 5, sprite: str = "🐇") -> None:
        super().__init__(point, sprite, speed, health)

    def attack(self, map_matrix: Map):
        coord = self.coordinate.get_neighboors()
        point_herbivore = [i for i in coord if isinstance(
            map_matrix.get_object(i), Grass)]
        map_matrix.delete_object(point_herbivore[0])


class Predator(Creature):
    def __init__(self, point: Point, speed: int = 2, health: int = 8, atack: int = 5, sprite: str = '🐺') -> None:
        super().__init__(point, sprite, speed, health)
        self.atack = atack

    def attack(self, map_matrix: Map):
        coord = self.coordinate.get_neighboors()
        point_herbivore = [i for i in coord if isinstance(
            map_matrix.get_object(i), Herbivore)]
        enit = map_matrix.get_object(point_herbivore[0])
        enit.health -= self.atack
        if enit.health <= 0:
            map_matrix.delete_object(point_herbivore[0])
