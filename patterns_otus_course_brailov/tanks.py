from .movement import Acceleratable, Movable, Rotatable, Rotating
from . import geometry as g


class Tank:
    def __init__(self, position: g.Vector, dirrection: g.Angle):
        self.position = position
        self.angle_speed = g.Angle(0)
        self.speed = 0
        self.dirrection = dirrection


class MovableAdapter(Movable):
    def __init__(self, tank: Tank) -> None:
        self._tank = tank

    def get_position(self) -> g.Vector:
        return self._tank.position

    def set_position(self, position: g.Vector) -> None:
        self._tank.position = position

    def get_velocity(self) -> g.Vector:
        return g.Vector.from_polar(
            angle=self._tank.dirrection,
            dist=self._tank.speed,
        )


class AcceleratableAdapter(Acceleratable):
    def __init__(self, tank: Tank) -> None:
        self._tank = tank

    def set_velocity(self, velocity: g.Vector) -> None:
        self._tank.speed = velocity.dist
        self._tank.dirrection = velocity.angle


class RotatatingAdaper(Rotating):
    def __init__(self, tank: Tank) -> None:
        self._tank = tank

    def get_dirrection(self) -> g.Angle:
        return self._tank.dirrection

    def set_dirrection(self, dirrection: g.Angle) -> None:
        self._tank.dirrection = dirrection

    def get_angle_speed(self) -> g.Angle:
        return self._tank.angle_speed


class RotatableAdaper(Rotatable):
    def __init__(self, tank: Tank):
        self._tank = tank

    def set_rotation_speed(self, speed: g.Angle) -> None:
        self._tank.angle_speed = speed
