#!/bin/bash
set -e

echo "Installing Nginx..."

if command -v nginx &> /dev/null; then
  echo "Nginx already installed: $(nginx -v 2>&1)"
  exit 0
fi

if uname | grep -qi linux; then
  sudo apt update
  sudo apt install -y nginx
elif uname | grep -qi darwin; then
  brew install nginx
else
  echo "Unsupported OS for nginx installation"
  exit 1
fi

echo "Nginx installed successfully."
