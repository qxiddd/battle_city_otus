from ..command import Command
from ..geometry.angles import Angle
from ..geometry.vectors import Vector
from .interfaces import (
    Movable,
    Rotating,
)


class MoveCommand(Command):
    """Команда отвечающая за прямолинейное равномерное движение объектов."""

    def __init__(self, movable: Movable) -> None:
        self.movable = movable

    def execute(self) -> None:
        self.movable.set_position(
            self.movable.get_position() + self.movable.get_velocity()
        )


class RotateCommand(Command):
    """Команда отвечающая за равномерный поворот объектов."""

    def __init__(self, rotating: Rotating):
        self.rotating = rotating

    def execute(self) -> None:
        self.rotating.set_dirrection(
            self.rotating.get_dirrection() + self.rotating.get_angle_speed()
        )
