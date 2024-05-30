#FROM python:alpine3.19 as build
#COPY ./requirements.txt /requirements.txt
#RUN python -m venv /pyvenv && \
#    /pyvenv/bin/pip install --upgrade pip && \
#    /pyvenv/bin/pip install -r requirements.txt
#
#FROM python:alpine3.19
#COPY ./app /app
#COPY --from=build /pyvenv /pyvenv
#WORKDIR /app
#RUN adduser --disabled-password appuser
#USER appuser
#ENV PATH="/pyvenv/bin:$PATH"

#
#FROM python:alpine3.19 as build
#COPY ./requirements.txt /requirements.txt
#RUN python -m venv /pyvenv && \
#    /pyvenv/bin/pip install --upgrade pip && \
#    /pyvenv/bin/pip install -r requirements.txt
#
#FROM python:alpine3.19
#COPY ./app /app
#COPY --from=build /pyvenv /pyvenv
#WORKDIR /app
#RUN adduser --disabled-password appuser
#USER appuser
#ENV PATH="/pyvenv/bin:$PATH"
#ENV PYTHONPATH="/app"
#ENTRYPOINT ["sh", "-c", "PYTHONPATH=/app alembic upgrade head && PYTHONPATH=/app uvicorn main:app --reload --host 0.0.0.0 --port 8000"]

FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

COPY . .

RUN pip install uvicorn

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
