import math
import typing

from . import angles


class Vector(typing.NamedTuple):
    x: float
    y: float

    @classmethod
    def from_polar(cls, angle: angles.Angle, dist: float):
        return Vector(math.cos(angle.radians), math.sin(angle.radians)) * dist

    @property
    def angle(self) -> typing.Optional[angles.Angle]:
        """Получить угол в радианах относительно вектора Vector(x=1, y=0)."""

        if self.x == 0:
            if self.y == 0:
                return None
            if self.y > 0:
                return angles.from_degrees(90)
            return angles.from_degrees(-90)

        angle_radians = math.atan(self.y / self.x)
        if self.x > 0:
            return angles.Angle(angle_radians)
        else:
            return angles.Angle(angle_radians + math.pi)

    @property
    def dist(self) -> float:
        """Растояние до точки (0, 0)."""
        x, y = self.x, self.y
        return math.sqrt(x*x + y*y)

    def rotate(self, angle: angles.Angle) -> 'Vector':
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


def roughly_equal(
    v1: 'Vector',
    v2: 'Vector',
    precision=float('1e-15'),
):
    return (v1 - v2).dist < precision
