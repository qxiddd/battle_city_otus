import pytest

from patterns_otus_course_brailov import tanks
from patterns_otus_course_brailov import movement
from patterns_otus_course_brailov import geometry as g


def test_rotation():
    dirrection = g.Angle.from_degrees(90)
    rotation_speed = g.Angle.from_degrees(1)

    tank = tanks.Tank(position=g.Vector(12, 5), dirrection=dirrection)

    movement.SetRotationCommand(
        rotatable=tanks.RotatableAdaper(tank),
        speed=rotation_speed,
    ).execute()

    movement.RotateCommand(
        rotating=tanks.RotatatingAdaper(tank)
    ).execute()

    assert g.Angle.roughly_equal(tank.dirrection, dirrection + rotation_speed)


def test_rotate_without_dirrection_getter():

    class FooBar(movement.Rotating):
        # нет реализации метода get_dirrection

        def set_dirrection(self, dirrection: g.Angle) -> None:
            ...

        def get_angle_speed(self) -> g.Angle:
            return g.Angle(1)

    obj = FooBar()

    with pytest.raises(NotImplementedError):
        movement.RotateCommand(obj).execute()


def test_rotate_without_dirrection_setter():

    class FooBar(movement.Rotating):

        def get_dirrection(self) -> g.Angle:
            return g.Angle(0)
        # нет реализации метода set_dirrection

        def get_angle_speed(self) -> g.Angle:
            return g.Angle(1)

    obj = FooBar()

    with pytest.raises(NotImplementedError):
        movement.RotateCommand(obj).execute()


def test_rotate_without_angle_speed_getter():

    class FooBar(movement.Rotating):

        def get_dirrection(self) -> g.Angle:
            return g.Angle(0)

        def set_dirrection(self, dirrection: g.Angle) -> None:
            ...

        # нет реализации метода get_angle_speed

    obj = FooBar()

    with pytest.raises(NotImplementedError):
        movement.RotateCommand(obj).execute()
