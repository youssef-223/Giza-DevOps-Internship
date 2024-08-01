#!/bin/bash

# Define database connection details
DB_HOST="jdbc:mysql://192.168.124.128:3306/"
DB_NAME="jenkins_giza_db"

SUDO_PASSWORD=1234

# Create the database
echo "Creating database ${DB_NAME}..."
echo $SUDO_PASSWORD | sudo -S mysql -u root -e "CREATE DATABASE IF NOT EXISTS ${DB_NAME};"

if [ $? -eq 0 ]; then
    echo ">> Database setup complete."
  else
    echo ">> Failed to create DB"
    exit 1
fi