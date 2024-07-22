#!/sandbox/bash

sudo -S apt-get update

# install dependencies
sudo apt-get install -y python3
sudo apt-get install -y python3-poetry
sudo apt-get install -y git
sudo apt-get install -y cmake
sudo apt-get install -y libboost-all-dev
sudo apt-get install -y sshpass
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev 
sudo apt-get install -y libsqlite3-dev wget curl llvm libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev 
sudo apt-get install -y libffi-dev liblzma-dev


# pull pyenv
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
~/.pyenv/bin/pyenv install 3.9.19

# pull the quafel repository
git clone https://github.com/cirKITers/Quafel.git Quafel

# install and setup the quafel repository
cd Quafel || exit 1
poetry env use ~/.pyenv/versions/3.9.19/bin/python3
poetry install --without dev

exit 0
