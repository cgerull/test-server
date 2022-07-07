#!/bin/bash
#
# Install python dev tools to  a Debian image
#
PYTHON_VERSION=3.9.13

# Start from home directory
PROJ_DIR=$(pwd)
cd

# Install build dependencies
sudo apt-get update
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev

# Get and install python
wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz
tar -xf Python-$PYTHON_VERSION.tgz
cd Python-$PYTHON_VERSION
./configure --enable-optimizations
make -j 2
sudo make altinstall

# Install venv in working directory
cd $PROJ_DIR
python3.9 -m venv .venv
