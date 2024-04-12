FROM docker.io/python:3.12-alpine AS init-db

RUN python -m pip install pip

RUN pip install --user pipenv

ENV PIPENV_VENV_IN_PROJECT=1

WORKDIR /build

COPY . .

RUN /root/.local/bin/pipenv sync --dev

RUN /build/.venv/bin/alembic upgrade head

#-

FROM docker.io/python:3.12-alpine AS init-deps

RUN python -m pip install pip

RUN pip install --user pipenv

ENV PIPENV_VENV_IN_PROJECT=1

WORKDIR /deps

COPY Pipfile Pipfile.lock ./

RUN /root/.local/bin/pipenv sync

#-

FROM docker.io/python:3.12-alpine AS runtime
LABEL org.opencontainers.image.source="https://github.com/vpo-tusur/todo-api"

COPY --from=init-deps /deps/.venv /app/.venv

COPY --from=init-db /build/migrator/todo-api.sqlite /app/migrator/

WORKDIR /app

COPY . .

EXPOSE 8000

CMD ["/app/.venv/bin/python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
