import queue
import logging
import typing
from abc import abstractmethod
from contextlib import contextmanager
from threading import Thread, Event, current_thread

from .command import Command


_context: dict[str, 'Actor'] = {}


@contextmanager
def _set_context(actor: 'Actor'):
    _context[actor.name] = actor
    try:
        yield
    finally:
        _context.pop(actor.name)


def get_context(actor_name: str) -> typing.Optional['Actor']:
    return _context.get(actor_name)


class Actor:
    """В отельном потоке читает команды из очереди и исполняет их."""

    def __init__(self, name: typing.Optional[str] = None):
        """Конструктор актора.

        :param thread_name: имя для актора
        """
        self._queue = queue.Queue()

        self._thread = Thread(name=name, target=self._loop)
        self._hard_stop_event = Event()
        self._soft_stop_event = Event()

        self._logger = logging.getLogger(name=f'{__name__}.actor.{name}')

    def __repr__(self) -> str:
        return f'<Actor: {self.name}>'

    @property
    def name(self):
        return self._thread.name

    def add_command(self, command: Command):
        """Положить команду в очередь актору. (thread-safe)"""
        self._queue.put(command)

    def start(self) -> None:
        """Запустить актор."""
        self._thread.start()

    def hard_stop(self) -> None:
        """Остановить актор не дожидаясь завершения исполнения имеющихся команд."""
        self._hard_stop_event.set()

    def soft_stop(self) -> None:
        """Остановить актор после завершения исполнения имеющихся команд."""
        self._soft_stop_event.set()

    def join(self, timeout: typing.Optional[float] = None) -> None:
        """Блокировать вызывающий поток до тех пор, пока не остановится актор."""
        if self._thread.is_alive():
            self._thread.join(timeout)

    def _get_from_queue(self) -> typing.Optional[Command]:
        try:
            return self._queue.get(block=False)
        except queue.Empty:
            return None

    def _safe_execute_command(self, command: Command):
        try:
            command.execute()
        except Exception:
            self._logger.exception('Error command execution.')

    def _loop(self) -> None:
        with _set_context(self):
            while True:
                if self._hard_stop_event.is_set():
                    break

                command = self._get_from_queue()

                if command is None:
                    if self._soft_stop_event.is_set():
                        break
                else:
                    self._safe_execute_command(command)


class ActorCommand(Command):
    @abstractmethod
    def actor_action(self, actor: Actor):
        ...

    def execute(self) -> None:
        actor_name = current_thread().name
        actor_ctx = get_context(actor_name)
        if actor_ctx is None:
            raise RuntimeError(f'No context for thread "{actor_name}".')
        self.actor_action(actor_ctx)


class ActorCommandByFunction(ActorCommand):
    def __init__(self, callable: typing.Callable[[Actor], None]) -> None:
        self._callable = callable

    def actor_action(self, actor: Actor):
        self._callable(actor)


hard_stop_command = ActorCommandByFunction(lambda actor: actor.hard_stop())
soft_stop_command = ActorCommandByFunction(lambda actor: actor.soft_stop())
