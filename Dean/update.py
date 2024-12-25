import mysql.connector

def print_table_details(host, user, password, database, table_name):
    try:
        
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        if connection.is_connected():
            print(f"Connected to the database '{database}'")

            cursor = connection.cursor()
            
            
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            
            
            column_names = [desc[0] for desc in cursor.description]
            print(f"Table: {table_name}")
            print(f"Columns: {', '.join(column_names)}")
            
            rows = cursor.fetchall()
            for row in rows:
                print(row)
    
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.")


print_table_details(
    host="localhost",
    user="root",
    password="your_password",  
    database="users",        
    table_name="USERS.STUDENTS"      
)
def update_table_with_user_input():
    import mysql.connector
    
    try:
        
        host = input("Enter the database host (e.g., localhost): ")
        user = input("Enter the database user (e.g., root): ")
        password = input("Enter the database password: ")
        database = input("Enter the database name: ")
        table_name = input("Enter the table name: ")
        
        
        column_to_update = input("Enter the column you want to update: ")
        new_value = input("Enter the new value: ")
        condition = input("Enter the condition (e.g., id = 2): ")
        
        
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            
            query = f"UPDATE {table_name} SET {column_to_update} = %s WHERE {condition}"
            
            
            cursor.execute(query, (new_value,))
            connection.commit()
            
            print(f"Table {table_name} updated successfully.")
    
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


update_table_with_user_input()
