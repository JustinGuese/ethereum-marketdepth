FROM python:3.12-slim
RUN mkdir -p /app/data/
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi
COPY grabBinanceOrderbook.py /app/grabBinanceOrderbook.py
CMD ["python", "grabBinanceOrderbook.py"]