# Basis-Image verwenden (Python)
FROM python:3.12

WORKDIR /app

# Installiere Python und andere notwendige Pakete
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copy the poetry configuration and lock file
COPY pyproject.toml poetry.lock ./

# Install the dependencies
RUN poetry install

COPY . /app/

# Umgebung variablen setzen
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

WORKDIR quafelweb
# Standardbefehl: Django Tests ausführen
CMD ["poetry", "run", "python", "manage.py", "test"]