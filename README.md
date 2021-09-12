# Архитектура и шаблоны проектирования

Мои решения домашних заданий. Ссылка на курс ([жми](https://otus.ru/lessons/patterns/?int_source=courses_catalog&int_term=programming)).

## Как подготовить окружение?

- Установите `python3.9` (чтобы не засорять систему разными версиями питона воспользуйся [pyenv](https://github.com/pyenv/pyenv))
- Установите [poetry](https://python-poetry.org/docs/#installation)
- Установите зависимости

```shell
$> poetry install
```

Poetry сам создаст [виртуальное окружение](https://docs.python.org/3/tutorial/venv.html).

Выполнить команду в виртуальном окружении

```shell
$> poetry run <command>
```

Войти в виртуальное окружение

```shell
$> poetry shell
```

Запустить тесты

```shell
$> poetry run pytest
```
