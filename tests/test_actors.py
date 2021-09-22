import threading
import time
import typing
from unittest.mock import Mock
from contextlib import contextmanager

from patterns_otus_course_brailov.command import Command, CommandByFuntion, combine_two_commands
from patterns_otus_course_brailov.actors import Actor, hard_stop_command, soft_stop_command


def current_threads_names() -> list[str]:
    """Отдает список имен запущенных потоков."""

    return [
        thread.name
        for thread in threading.enumerate()
    ]


@contextmanager
def context_manager(actor_start, actor_stop, join):
    """Позволяет использовать синтаксис `with` вместо синтаксиса `try/finally`."""

    actor_start()
    try:
        yield
    finally:
        actor_stop()
        join(timeout=0.3)


def test_thread_starts_and_finish():
    """Проверяет что запуск актора запускает поток, а hard_stop останавливает поток."""

    thread_name = 'test_actor'
    actor = Actor(name=thread_name)

    # проверка: нет запущенных потоков
    assert thread_name not in current_threads_names(), 'Поток запущен раньше времени'

    with context_manager(actor.start, actor.hard_stop, actor.join):
        # проверка: есть запущенный поток
        assert thread_name in current_threads_names(), 'Поток актора не запустился'

    # проверка: нет запущенных потоков
    assert thread_name not in current_threads_names(), 'Поток актора не был остановлен'


def create_observable_command(name: str) -> tuple[Command, typing.Callable[[], bool]]:
    """Отдает команду и функцию, через которую можно проверить была ли запущена команда."""

    mock = Mock(name=name)

    def command_executed() -> bool:
        return mock.called

    return CommandByFuntion(mock), command_executed


def test_actor_executes_commands():
    """Проверяем что актор выполняет посылаемые ему команды."""

    thread_name = 'test_actor'
    actor = Actor(name=thread_name)

    command, command_executed = create_observable_command('test_command')

    with context_manager(actor.start, actor.hard_stop, actor.join):
        actor.add_command(command)
        time.sleep(0.03)  # подождем пока актор исполнит команду

    assert command_executed(), 'Команда не была исполнена'


def delay_command(command, delay_seconds: float) -> Command:
    """Добавит задержку в команду. (Имитация длительного исполнения)"""

    return combine_two_commands(
        first_command=CommandByFuntion(lambda: time.sleep(delay_seconds)),
        second_command=command,
    )


def test_actor_hard_stop():
    """Проверяем что после события hard stop, поток завершается не дожижаясь того, как все задачи закончились."""

    thread_name = 'test_actor'
    actor = Actor(name=thread_name)

    first_command, first_command_executed = create_observable_command('first_command')
    second_command, second_command_executed = create_observable_command('second_command')

    actor.add_command(delay_command(first_command, 0.1))  # задержим команду, чтобы успело произойти событие hard_stop
    actor.add_command(second_command)

    actor.start()
    actor.hard_stop()
    actor.join(timeout=0.3)

    assert first_command_executed(), 'first_command не была исполнена.'
    assert not second_command_executed(), 'Вторая команда была исполнена, но не должна была.'


def test_actor_soft_stop():
    """Проверяем что после события soft stop, поток завершается только после того, как все задачи закончились."""

    thread_name = 'test_actor'
    actor = Actor(name=thread_name)

    first_command, first_command_executed = create_observable_command('first_command')
    second_command, second_command_executed = create_observable_command('second_command')

    actor.add_command(delay_command(first_command, 0.1))  # задержим команду, чтобы успело произойти событие soft_stop
    actor.add_command(second_command)

    actor.start()
    actor.soft_stop()
    actor.join(timeout=0.3)

    assert first_command_executed(), 'first_command не была исполнена'
    assert second_command_executed(), 'second_command не была исполнена'


def test_actor_hard_stop_command():
    """Проверяет что команда HardStop останавливает актор только после того, как все задачи закончились."""
    thread_name = 'test_actor'
    actor = Actor(name=thread_name)

    first_command, first_command_executed = create_observable_command('first_command')
    next_command, next_command_executed = create_observable_command('next_command')

    actor.add_command(first_command)
    actor.add_command(hard_stop_command)
    actor.add_command(next_command)

    actor.start()
    actor.join(timeout=0.3)

    # проверка: нет запущенных потоков
    assert thread_name not in current_threads_names(), 'Поток актора не был остановлен'

    assert first_command_executed(), 'first_command не была исполнена'
    assert not next_command_executed(), 'next_command была исполнена, но не должна была'


def test_actor_soft_stop_command():
    """Проверяет что команда SoftStop останавливает актор не дожидаясь того, как все задачи закончились."""
    thread_name = 'test_actor'
    actor = Actor(name=thread_name)

    first_command, first_command_executed = create_observable_command('first_command')
    next_command, next_command_executed = create_observable_command('next_command')

    actor.add_command(first_command)
    actor.add_command(soft_stop_command)
    actor.add_command(next_command)

    actor.start()
    actor.join(timeout=0.3)

    # проверка: нет запущенных потоков
    assert thread_name not in current_threads_names(), 'Поток актора не был остановлен'

    assert first_command_executed(), 'first_command не была исполнена'
    assert next_command_executed(), 'next_command не была исполнена'
