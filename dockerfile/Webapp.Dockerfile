# Use the official Ubuntu image as a base
FROM ubuntu:latest

# Install OpenSSH server and sudo
RUN apt-get update && apt-get install -y openssh-server sudo
RUN apt-get install -y sshpass

# Create the SSH directory and set permissions
RUN mkdir /var/run/sshd

# Create a user with a password and SSH access
RUN useradd -m -s /bin/bash user && echo 'user:password' | chpasswd

# Add the user to the sudo group
RUN usermod -aG sudo user

# Allow the user to run sudo without a password
RUN echo 'user ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN touch /etc/sudoers.d/user
RUN echo 'user ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers.d/user

# Allow root login over SSH (optional, for security you might want to disable this)
RUN echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config

# Allow password authentication
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Expose SSH port
EXPOSE 22

# Start the SSH service
CMD ["/usr/sbin/sshd", "-D"]


# Django Webapp Server:
# Install python and poetry
RUN apt-get update && apt-get install -y python3 python3-poetry

# Copy the poetry configuration and lock file
COPY pyproject.toml poetry.lock ./

# Install the dependencies
RUN poetry install

# Create and set the working directory
RUN mkdir -p app
WORKDIR app

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# Copy the Django project and the quafel_simulators
#+COPY quafel_simulators/ quafel_simulators/
COPY quafelweb/ quafelweb/
COPY .env_secret .env_secret

# Run the Django server
WORKDIR quafelweb
CMD ["sh", "-c", "poetry run python manage.py migrate && poetry run python manage.py runserver 0.0.0.0:8000"]
EXPOSE 8000
