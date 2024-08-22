# Use same base image as for this project
FROM python:3.12

#set the working directory
WORKDIR /app

# install poetry
RUN pip install poetry

# copy project data and isntall dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install

# copy code into image
COPY . .

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install test-dependencies
RUN poetry add --dev pytest

# execute tests
CMD ["poetry", "run", "pytest"]