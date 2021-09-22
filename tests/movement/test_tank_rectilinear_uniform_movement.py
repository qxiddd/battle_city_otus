import pytest

from patterns_otus_course_brailov.movement.commands import MoveCommand
from patterns_otus_course_brailov.movement.interfaces import Movable
from patterns_otus_course_brailov.geometry import angles
from patterns_otus_course_brailov.geometry.vectors import Vector, roughly_equal


def test_move():
    position = Vector(12, 5)
    velocity = Vector(-7, 3)

    u_object = {
        'position': position,
        'velocity': velocity,
    }

    class MovableUObject(Movable):
        def __init__(self, u_object) -> None:
            self._u_object = u_object

        def get_position(self) -> Vector:
            return self._u_object['position']

        def set_position(self, position: Vector) -> None:
            """Задать вектор с позицией объекта."""
            self._u_object['position'] = position

        def get_velocity(self) -> Vector:
            """Получить вектор скорости объекта."""
            return self._u_object['velocity']

    MoveCommand(
        movable=MovableUObject(u_object)
    ).execute()

    assert roughly_equal(u_object['position'], position + velocity)


def test_move_without_position_getter():

    class FooBar(Movable):
        # нет реализации метода get_position

        def set_position(self, position: Vector) -> None:
            ...

        def get_velocity(self) -> Vector:
            return Vector(0, 0)

    obj = FooBar()

    with pytest.raises(NotImplementedError):
        MoveCommand(obj).execute()


def test_move_without_position_setter():

    class FooBar(Movable):
        def get_position(self) -> Vector:
            return Vector(0, 0)

        # нет реализации метода set_position

        def get_velocity(self) -> Vector:
            return Vector(0, 0)

    obj = FooBar()

    with pytest.raises(NotImplementedError):
        MoveCommand(obj).execute()


def test_move_without_velocity_getter():

    class FooBar(Movable):
        def get_position(self) -> Vector:
            return Vector(0, 0)

        def set_position(self, position: Vector) -> None:
            ...

        # нет реализации метода get_velocity

    obj = FooBar()

    with pytest.raises(NotImplementedError):
        MoveCommand(obj).execute()
