# Архитектура проекта

## Технологии

### Pipenv - система сборки и управления зависимостями проекта

https://pipenv.pypa.io/en/latest/

- Восстановление зависимостей проекта (в том числе dev):
```shell
$ pipenv sync --dev
```

- Установка новой зависимости:
```shell
$ pipenv install <dependency>
```

- Удаление зависимости:
```shell
$ pipenv uninstall <dependency>
```


### Alembic - инструмент работы с миграциями

https://alembic.sqlalchemy.org/en/latest/

- Инициализация базы данных:
```shell
$ pipenv run upgrade-db
```

Проверка того, что все миграции были применены к базе данных:
```shell
$ alembic check
```

Создание миграции:
```shell
$ alembic revision --autogenerate -m "<comment>"
```


### pre-commit - хуки git

Регистрация хуков:
```shell
$ pipenv run pre-commit install
```

Запусить проверку всех файлов проекта:
```shell
$ pipenv run pre-commit run --all-files
```


### pytest - тестирование

Запустить тесты:
```shell
$ pipenv run pytest
```

Сформировать отчет о покрытии кода тестами:
```shell
$ pipenv run coverage
```


## Библиотеки и фреймворки

### logging - библиотека для логгирования

### fastapi - фреймворк для веб-сервиса

### pydantic - библиотека для создания схем DTO


## Структура модулей

Ядро проекта:
- `services` - сервисы доменной бизнес-логики
- `models` - модели ORM и доменные сущности
- `repositories` - репозитории проекта

Эндпоинты:
- `routers` - эндпоинты проекта
- `schemas` - описание структур Data Transfer Objects (DTOs)

Зависимости и прочее:
- `configs` - настройки сервиса
- `migrator` - утилита миграции `alembic`
  - `versions` - миграции базы данных
  - `todo-api.sqlite` - база данных проекта
- `docs` - документация проекта
