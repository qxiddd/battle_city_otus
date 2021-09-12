import typing

from ..geometry.vectors import Vector
from ..geometry.angles import Angle


class Movable(typing.Protocol):
    def get_position(self) -> Vector:
        """Получить вектор с позицией объекта."""
        raise NotImplementedError

    def set_position(self, position: Vector) -> None:
        """Задать вектор с позицией объекта."""
        raise NotImplementedError

    def get_velocity(self) -> Vector:
        """Получить вектор скорости объекта."""
        raise NotImplementedError


class Rotating(typing.Protocol):
    def get_dirrection(self) -> Angle:
        """Получить угол-направление движения объекта."""
        raise NotImplementedError

    def set_dirrection(self, dirrection: Angle) -> None:
        """Установить вектор скорости объекта."""
        raise NotImplementedError

    def get_angle_speed(self) -> Angle:
        """Получить скорость вращения объекта."""
        raise NotImplementedError
