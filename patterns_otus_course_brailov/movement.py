import typing

from . import geometry as g
from .command import Command


class Movable(typing.Protocol):
    def get_position(self) -> g.Vector:
        """Получить вектор с позицией объекта."""
        raise NotImplementedError

    def set_position(self, position: g.Vector) -> None:
        """Задать вектор с позицией объекта."""
        raise NotImplementedError

    def get_velocity(self) -> g.Vector:
        """Получить вектор скорости объекта."""
        raise NotImplementedError


class MoveCommand(Command):
    """Команда отвечающая за прямолинейное равномерное движение объектов."""

    def __init__(self, movable: Movable) -> None:
        self.movable = movable

    def execute(self) -> None:
        self.movable.set_position(
            self.movable.get_position() + self.movable.get_velocity()
        )


class Acceleratable(typing.Protocol):
    def set_velocity(self, velocity: g.Vector) -> None:
        """Задать скорость объекту."""
        raise NotImplementedError


class SetVelocityCommand(Command):
    """Команда задающая скорость объекту."""

    def __init__(self, acceleratable: Acceleratable, velocity: g.Vector):
        self._acceleratable = acceleratable
        self._velocity = velocity

    def execute(self) -> None:
        return self._acceleratable.set_velocity(self._velocity)


class Rotating(typing.Protocol):
    def get_dirrection(self) -> g.Angle:
        """Получить угол-направление движения объекта."""
        raise NotImplementedError

    def set_dirrection(self, dirrection: g.Angle) -> None:
        """Установить вектор скорости объекта."""
        raise NotImplementedError

    def get_angle_speed(self) -> g.Angle:
        """Получить скорость вращения объекта."""
        raise NotImplementedError


class RotateCommand(Command):
    """Команда отвечающая за равномерный поворот объектов."""

    def __init__(self, rotating: Rotating):
        self.rotating = rotating

    def execute(self) -> None:
        self.rotating.set_dirrection(
            self.rotating.get_dirrection() + self.rotating.get_angle_speed()
        )


class Rotatable(typing.Protocol):
    def set_rotation_speed(self, speed: g.Angle) -> None:
        """Установить скорость вращения."""
        raise NotImplementedError


class SetRotationCommand(Command):
    def __init__(self, rotatable: Rotatable, speed: g.Vector):
        self._rotatable = rotatable
        self._speed = speed

    def execute(self) -> None:
        self._rotatable.set_rotation_speed(self._speed)
