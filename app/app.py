from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error
from configparser import ConfigParser

app = Flask(__name__)

def get_db_config():
    config = ConfigParser()
    config.read('application.properties')
    
    # Print out the configuration to debug
    print("Config sections:", config.sections())
    print("Config items:", dict(config.items('DEFAULT')))
    
    return {
        'host': config.get('DEFAULT', 'MYSQL_HOST'),
        'port': config.getint('DEFAULT', 'MYSQL_PORT'),
        'user': config.get('DEFAULT', 'MYSQL_USER'),
        'password': config.get('DEFAULT', 'MYSQL_PASSWORD'),
        'database': config.get('DEFAULT', 'MYSQL_DB')
    }


# Function to establish a database connection
def get_db_connection():
    db_config = get_db_config()
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        if connection.is_connected():
            print(f"Connected to database: {db_config['database']}")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to create a hardcoded table if it doesn't exist
def create_table():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE
                )
            """)
            connection.commit()
            print("Table 'users' created or already exists.")
        except Error as e:
            print(f"Error creating table: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to the database for table creation.")

# Endpoint to display database version and contents of the users table
@app.route('/')
def show_users():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            db_version = cursor.fetchone()

            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            users_list = [{"id": row[0], "name": row[1], "email": row[2]} for row in users]

            return jsonify({
                "database_version": db_version[0],
                "users": users_list
            })
        except Error as e:
            return f"Error retrieving data: {e}", 500
        finally:
            cursor.close()
            connection.close()
    else:
        return "Failed to connect to the database", 500

if __name__ == "__main__":
    create_table()  # Ensure the table is created on startup
    app.run(host="0.0.0.0", port=5000)
