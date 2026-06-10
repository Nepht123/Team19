'''I will use this to instert the data into my faculties while I am still learning Spring Boot'''

import mysql.connector
from mysql.connector import Error



'''
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '4492340',
    'database': 'rate_mm'
}
'''

#Here I am now going too try to insert a row into my faculty table
def insert_faculty(faculty_name, icon_name):
    mydatabase = None

    try:
        mydatabase = mysql.connector.connect(
            host='127.0.0.1', 
            user='root', 
            password='4492340',
             database='rate_mm')
        

        print("Connecting to MySQL Database...")
        mycursor = mydatabase.cursor()


        '''# Practice to ensure that it is connected and working
        mycursor.execute("show tables")
        for i in mycursor:
            print(i)
        '''

        #DYNAMIC SAFETY CHECK
        check_query = "SELECT id FROM faculties WHERE fac_name = %s"
        mycursor.execute(check_query, (faculty_name,))
        existing_record = mycursor.fetchone()

        if existing_record:
            print(f"'{faculty_name}' already exists with ID: {existing_record[0]}. Skipping insertion.")
            return existing_record[0] # Return the ID of the row that already exists
        

        #Inserting the data
        insert_query = """
            INSERT INTO faculties (fac_name, is_available, icon_name)
            VALUES (%s, %s, %s)
        """

        faculty_data = (faculty_name, True, icon_name)

        print(f"Writing data: Inserting '{faculty_name}' into the faculties table...")
        mycursor.execute(insert_query, faculty_data)


        mydatabase.commit()
        
        generated_id = mycursor.lastrowid
        print(f"Success! New row generated for '{faculty_name}' at Primary Key ID: {generated_id}")
        return generated_id

    except Error as error:
        print(f"Error executing logic for '{faculty_name}':", error)
        return None


    finally:
        # 4. ENVIRONMENT CLEANUP
        if mydatabase and mydatabase.is_connected():
            mycursor.close()
            mydatabase.close()
            print("MySQL database connection securely closed.")



if __name__ == "__main__":
    # To insert your Natural Science faculty, you just pass its details here!
    insert_faculty("Law", "Scale")