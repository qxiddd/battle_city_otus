import pytest

from patterns_otus_course_brailov.movement.commands import RotateCommand
from patterns_otus_course_brailov.movement.interfaces import Rotating
from patterns_otus_course_brailov.geometry import angles


def test_rotation():
    dirrection = angles.from_degrees(90)
    rotation_speed = angles.from_degrees(1)

    u_object = {
        'dirrection': dirrection,
        'rotation_speed': rotation_speed,
    }

    class RotatingUObject(Rotating):
        def __init__(self, u_object):
            self._u_object = u_object

        def get_dirrection(self) -> angles.Angle:
            return u_object['dirrection']

        def set_dirrection(self, dirrection: angles.Angle) -> None:
            u_object['dirrection'] = dirrection

        def get_angle_speed(self) -> angles.Angle:
            return self._u_object['rotation_speed']


    RotateCommand(
        rotating=RotatingUObject(u_object)
    ).execute()

    assert angles.roughly_equal(u_object['dirrection'], dirrection + rotation_speed)


def test_rotate_without_dirrection_getter():

    class FooBar(Rotating):
        # нет реализации метода get_dirrection

        def set_dirrection(self, dirrection: angles.Angle) -> None:
            ...

        def get_angle_speed(self) -> angles.Angle:
            return angles.Angle(1)

    obj = FooBar()

    with pytest.raises(NotImplementedError):
        RotateCommand(obj).execute()


def test_rotate_without_dirrection_setter():

    class FooBar(Rotating):

        def get_dirrection(self) -> angles.Angle:
            return angles.Angle(0)
        # нет реализации метода set_dirrection

        def get_angle_speed(self) -> angles.Angle:
            return angles.Angle(1)

    obj = FooBar()

    with pytest.raises(NotImplementedError):
        RotateCommand(obj).execute()


def test_rotate_without_angle_speed_getter():

    class FooBar(Rotating):

        def get_dirrection(self) -> angles.Angle:
            return angles.Angle(0)

        def set_dirrection(self, dirrection: angles.Angle) -> None:
            ...

        # нет реализации метода get_angle_speed

    obj = FooBar()

    with pytest.raises(NotImplementedError):
        RotateCommand(obj).execute()
