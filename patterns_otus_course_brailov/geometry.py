import math
import typing


def normalize(value: float, period: float) -> float:
    bound = period / 2
    if value >= bound:
        cycles = value // period + 1
        return value - period*cycles
    if value < -bound:
        cycles = value // -period + 1
        return value + period*cycles
    return value


class Angle:
    """Универсальное представление углов."""

    def __init__(self, radians: float):
        self._radians = normalize(radians, period=2*math.pi)

    @property
    def radians(self) -> float:
        return self._radians

    @property
    def degrees(self) -> float:
        return self.radians_to_degrees(self.radians)

    @property
    def pi_coefficient(self) -> float:
        return self.radians / math.pi

    @staticmethod
    def radians_to_degrees(radians: float) -> float:
        return normalize(
            value=radians * 180 / math.pi,
            period=360,
        )

    @staticmethod
    def degrees_to_radians(degrees: float) -> float:
        return degrees * math.pi / 180

    @classmethod
    def from_radians(cls, radians: float):
        return cls(radians)

    @classmethod
    def from_pi_coefficient(cls, coefficient: float):
        return cls.from_radians(coefficient * math.pi)

    @classmethod
    def from_degrees(cls, degrees: float):
        return cls(cls.degrees_to_radians(degrees))

    def __add__(self, other) -> 'Angle':
        if not isinstance(other, Angle):
            raise ValueError
        return Angle(self.radians + other.radians)

    def __mul__(self, other) -> 'Angle':
        if not isinstance(other, (int, float)):
            raise ValueError
        return Angle(self.radians * other)

    def __sub__(self, other) -> 'Angle':
        return self + other*(-1)

    def __lt__(self, other) -> bool:
        if not isinstance(other, Angle):
            raise ValueError
        return self.radians < other.radians

    def __gt__(self, other):
        if not isinstance(other, Angle):
            raise ValueError
        return self.radians > other.radians

    def __repr__(self) -> str:
        return f'Angle(radians={self.radians})'

    def __str__(self) -> str:
        return repr(self)

    @staticmethod
    def roughly_equal(
        a1: 'Angle',
        a2: 'Angle',
        precision=float('1e-15'),
    ):
        return (a1 - a2).radians < precision


class Vector(typing.NamedTuple):
    x: float
    y: float

    @classmethod
    def from_polar(cls, angle: Angle, dist: float):
        return Vector(math.cos(angle.radians), math.sin(angle.radians)) * dist

    @property
    def angle(self) -> typing.Optional[Angle]:
        """Получить угол в радианах относительно вектора Vector(x=1, y=0)."""

        if self.x == 0:
            if self.y == 0:
                return None
            if self.y > 0:
                return Angle.from_degrees(90)
            return Angle.from_degrees(-90)

        angle_radians = math.atan(self.y / self.x)
        if self.x > 0:
            return Angle(angle_radians)
        else:
            return Angle(angle_radians + math.pi)

    @property
    def dist(self) -> float:
        """Растояние до точки (0, 0)."""
        x, y = self.x, self.y
        return math.sqrt(x*x + y*y)

    def rotate(self, angle: Angle) -> 'Vector':
        """Повернуть вектор на величину angle."""
        if self.angle is None:
            return self

        return Vector.from_polar(
            angle=self.angle + angle,
            dist=self.dist,
        )

    def __add__(self, other) -> 'Vector':
        if not isinstance(other, Vector):
            raise ValueError
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other) -> 'Vector':
        if not isinstance(other, (float, int)):
            raise ValueError
        return Vector(self.x * other, self.y * other)

    def __sub__(self, other) -> 'Vector':
        return self + other*(-1)

    def __repr__(self) -> str:
        return f'Vector(x={self.x}, y={self.y})'

    def __str__(self) -> str:
        return repr(self)

    @staticmethod
    def roughly_equal(
        v1: 'Vector',
        v2: 'Vector',
        precision=float('1e-15'),
    ):
        return (v1 - v2).dist < precision
