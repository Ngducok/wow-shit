#!/bin/bash

pkg update -y && pkg upgrade -y

termux-change-repo

pkg install python -y

pip install --upgrade pip

pip install requests colorama pystyle

echo "Packages installed successfully"
