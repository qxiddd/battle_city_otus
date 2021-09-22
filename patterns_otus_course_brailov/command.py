from abc import ABC, abstractmethod
from functools import reduce
import typing


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        ...


class CommandByFuntion(Command):
    def __init__(self, callable: typing.Callable[[], None]) -> None:
        self._callable = callable

    def execute(self) -> None:
        return self._callable()


def combine_two_commands(first_command: Command, second_command: Command) -> Command:
    def combination() -> None:
        first_command.execute()
        second_command.execute()

    return CommandByFuntion(combination)


empty_command = CommandByFuntion(callable=lambda: ...)


def combine_commands(commands: list[Command]) -> Command:
    return reduce(
        function=combine_two_commands,
        sequence=commands,
        initial=empty_command,
    )
