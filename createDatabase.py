import mysql.connector
from mysql.connector import Error

try:
    # MySQL connection details
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kishu31101999"
    )

    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS vaccination_analysis")
    print("✅ Database 'vaccination_analysis' created (or already exists).")

except Error as e:
    print("❌ Error:", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
