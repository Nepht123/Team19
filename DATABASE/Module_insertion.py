'''I will use this to instert the data into my faculties while I am still learning Spring Boot'''

import csv
import mysql.connector
from mysql.connector import Error



def insert_standalone_modules(csv_file_path):
    mydatabase = None

    try:
        print(" Connecting to database to populate master modules directory...")
        mydatabase = mysql.connector.connect(
            host='127.0.0.1', 
            user='root', 
            password='4492340',
            database='rate_mm'
        )
        mycursor = mydatabase.cursor()

        print(f"Reading spreadsheet file from: {csv_file_path}")
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader) # Skips the excel column header row
            modules_inserted = 0

            for row in csv_reader:
                # Basic layout safety filter
                if not row or len(row) < 6:
                    continue 
                
                # Extracting specific data positions, ignoring columns C and D
                mod_code      = row[0].strip()  # Column A
                mod_name      = row[1].strip()  # Column B
                prerequisites = row[4].strip()  # Column E
                corequisites  = row[5].strip()  # Column F

                # Target query mapping to your exact schema definitions
                insert_mod_query = """
                    INSERT IGNORE INTO modules (mod_code, mod_name, prerequisites, corequisites)
                    VALUES (%s, %s, %s, %s)
                """
                
                mycursor.execute(insert_mod_query, (mod_code, mod_name, prerequisites, corequisites))
                
                # Count only if it's a brand new record added to the database
                if mycursor.rowcount > 0:
                    modules_inserted += 1

        # Commit transaction updates to permanent disk storage
        mydatabase.commit()
        print(f" Success! Added {modules_inserted} new unique modules to the directory database.")

    except Error as error:
        print(" Database Error encountered:", error)
    except FileNotFoundError:
        print(f" System Error: The file path '{csv_file_path}' does not exist.")
    finally:
        # Secure resource teardown
        if mydatabase and mydatabase.is_connected():
            mycursor.close()
            mydatabase.close()
            print(" MySQL session securely closed.")


if __name__ == "__main__":
    # Point this to your saved modules CSV file location
    target_csv = "C:/Users/mwamb/OneDrive/Desktop/Team_6_repo/Team19/Faculties/Natural Science/Experimental/CSVs/Post_mod_NS.csv"
    
    insert_standalone_modules(target_csv)