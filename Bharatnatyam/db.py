import mysql.connector
from mysql.connector import Error
connection = None  # ✅ Define it first

try:
    # Connect to MySQL database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',  # replace with your actual password
        database='adavu_internship'   # replace with your actual database name
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # Your SQL insert query
        insert_query = "INSERT INTO data (id, name, age) VALUES (%s, %s, %s)"
        values = (12, "kk", 56)

        # Execute the insert query
        cursor.execute(insert_query, values)
        connection.commit()

        print("✅ Data inserted successfully into 'data' table")

except Error as e:
    print("❌ Error while connecting to MySQL:", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("🔌 MySQL connection is closed")
