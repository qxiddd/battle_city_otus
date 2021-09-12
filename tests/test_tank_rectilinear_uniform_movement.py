import pytest

from patterns_otus_course_brailov import tanks
from patterns_otus_course_brailov import movement
from patterns_otus_course_brailov import geometry as g


def test_move():
    position = g.Vector(12, 5)
    velocity = g.Vector(-7, 3)

    tank = tanks.Tank(position=position, dirrection=g.Angle.from_degrees(90))

    movement.SetVelocityCommand(
        acceleratable=tanks.AcceleratableAdapter(tank),
        velocity=velocity,
    ).execute()

    movement.MoveCommand(
        movable=tanks.MovableAdapter(tank)
    ).execute()

    assert g.Vector.roughly_equal(tank.position, position + velocity)


def test_move_without_position_getter():

    class FooBar(movement.Movable):
        # нет реализации метода get_position

        def set_position(self, position: g.Vector) -> None:
            ...

        def get_velocity(self) -> g.Vector:
            return g.Vector(0, 0)

    obj = FooBar()

    with pytest.raises(NotImplementedError):
        movement.MoveCommand(obj).execute()


def test_move_without_position_setter():

    class FooBar(movement.Movable):
        def get_position(self) -> g.Vector:
            return g.Vector(0, 0)

        # нет реализации метода set_position

        def get_velocity(self) -> g.Vector:
            return g.Vector(0, 0)

    obj = FooBar()

    with pytest.raises(NotImplementedError):
        movement.MoveCommand(obj).execute()


def test_move_without_velocity_getter():

    class FooBar(movement.Movable):
        def get_position(self) -> g.Vector:
            return g.Vector(0, 0)

        def set_position(self, position: g.Vector) -> None:
            ...

        # нет реализации метода get_velocity

    obj = FooBar()

    with pytest.raises(NotImplementedError):
        movement.MoveCommand(obj).execute()
