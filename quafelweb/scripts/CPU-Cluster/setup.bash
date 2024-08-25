#!/bin/bash

# Install pyenv locally
if [ ! -d "$HOME/.pyenv" ]; then
  git clone https://github.com/pyenv/pyenv.git ~/.pyenv
fi

# Add pyenv to PATH and initialize it
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"

# Install Python 3.9.19 using pyenv
pyenv install -s 3.9.19
pyenv global 3.9.19

# Install Pipx
pip install --upgrade pip
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Install poetry
pipx install poetry

# Add Poetry to PATH
export PATH="$HOME/.local/bin:$PATH"

# Pull the Quafel repository
if [ ! -d "Quafel" ]; then
  git clone https://github.com/cirKITers/Quafel.git Quafel
fi

# Install and setup the Quafel repository
cd Quafel || exit 1
poetry env use ~/.pyenv/versions/3.9.19/bin/python3
poetry install --without dev

exit 0