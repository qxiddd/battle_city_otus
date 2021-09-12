import math


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
    def __init__(self, radians: float):
        self._radians = normalize(radians, period=2*math.pi)

    @property
    def radians(self) -> float:
        return self._radians

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


def roughly_equal(
    a1: 'Angle',
    a2: 'Angle',
    precision=float('1e-15'),
):
    return (a1 - a2).radians < precision


def radians_to_degrees(radians: float) -> float:
    return normalize(
        value=radians * 180 / math.pi,
        period=360,
    )


def degrees_to_radians(degrees: float) -> float:
    return degrees * math.pi / 180


def degrees(angle: Angle) -> float:
    return radians_to_degrees(angle.radians)


def pi_coefficient(angle: Angle) -> float:
    return angle.radians / math.pi


def from_pi_coefficient(coefficient: float) -> Angle:
    return Angle(coefficient * math.pi)


def from_degrees(degrees: float) -> Angle:
    return Angle(degrees_to_radians(degrees))
