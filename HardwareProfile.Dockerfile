# Use the official Ubuntu image as a base
FROM ubuntu:latest

# Install OpenSSH server and sudo
RUN apt-get update && apt-get install -y openssh-server sudo

# Create the SSH directory and set permissions
RUN mkdir /var/run/sshd

# Create a user with a password and SSH access
RUN useradd -m -s /bin/bash user && echo 'user:password' | chpasswd

# Add the user to the sudo group
RUN usermod -aG sudo user

# Allow the user to run sudo without a password
RUN echo 'user ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN touch /etc/sudoers.d/user
RUN echo 'user All=(ALL) NOPASSWD:ALL' >> /etc/sudoers.d/user

# Allow root login over SSH (optional, for security you might want to disable this)
RUN echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config

# Allow password authentication
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Expose SSH port
EXPOSE 22

# Start the SSH service
CMD ["/usr/sbin/sshd", "-D"]