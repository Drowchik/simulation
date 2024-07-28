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

    def __repr__(self) -> str:
        return f"X: {self.x} Y: {self.y}"


a = Point(5, 10)
print(a)
