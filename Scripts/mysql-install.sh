#!/bin/bash

# Define the sudo password
SUDO_PASSWORD='1234'

# Function to run sudo command non-interactively
run_sudo() {
  echo $SUDO_PASSWORD | sudo -S $@
}

run_sudo apt-get update
run_sudo apt-get install mysql-server

# Function to start MySQL service
start_mysql() {
  echo ">> Starting MySQL service..."
  run_sudo systemctl start mysql
  if [ $? -eq 0 ]; then
    echo ">> MySQL service started successfully."
  else
    echo ">> Failed to start MySQL service."
    exit 1
  fi
}

# Function to enable MySQL to start on boot
enable_mysql_service() {
  echo ">> Enabling MySQL service to start on boot..."
  run_sudo systemctl enable mysql
  if [ $? -eq 0 ]; then
    echo ">> MySQL service enabled to start on boot successfully."
  else
    echo ">> Failed to enable MySQL service to start on boot."
    exit 1
  fi
}

# Main script execution
echo ">>>Starting MySQL setup script..."

# Start MySQL
start_mysql

# Enable MySQL service to start on boot
enable_mysql_service

echo ">>> MySQL setup completed successfully."
