import csv
import mysql.connector
from mysql.connector import Error


def get_faculty_id_by_name(cursor, faculty_name):
    """
    Queries the database dynamically to find the primary key ID 
    associated with a specific faculty name text string.
    """
    query = "SELECT id FROM faculties WHERE fac_name = %s"
    cursor.execute(query, (faculty_name.strip(),))
    result = cursor.fetchone()
    
    if result:
        return result[0] # Returns the integer id
    else:
        return None

def insert_faculty_courses(csv_file_path, faculty_name):
    mydatabase = None

    try:
        print("[START] Connecting to database...")
        mydatabase = mysql.connector.connect(
            host='127.0.0.1', 
            user='root', 
            password='4492340',
            database='rate_mm'
        )
        mycursor = mydatabase.cursor()

        # 🔍 NEW STEP: Dynamically fetch the faculty ID from the database using its name
        print(f"Searching for the database ID corresponding to: '{faculty_name}'...")
        target_faculty_id = get_faculty_id_by_name(mycursor, faculty_name)

        if target_faculty_id is None:
            print(f"[CRITICAL ERROR] Could not find a faculty named '{faculty_name}' in your database.")
            print("Please make sure you have inserted the faculty name into the 'faculties' table first!")
            return

        print(f"[FOUND] '{faculty_name}' corresponds to internal Database ID: {target_faculty_id}")

        print(f"Reading spreadsheet file from: {csv_file_path}")
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader) # Skips the column header row
            
            courses_inserted = 0

            for row in csv_reader:
                # Layout safety filter: Ensure row has columns up to index 3 (Duration Years)
                if not row or len(row) < 4:
                    continue 
                
                # Extracting specific data positions based on your excel format
                course_name    = row[0].strip()  # Column A
                course_code    = row[1].strip()  # Column B
                abbreviation   = row[2].strip()  # Column C
                duration_years = int(row[3].strip()) # Column D

                # Target query matching your exact database schema fields
                insert_course_query = """
                    INSERT IGNORE INTO courses (course_code, course_name, abbreviation, duration_years, faculty_id)
                    VALUES (%s, %s, %s, %s, %s)
                """
                
                # Using the target_faculty_id found dynamically above!
                query_values = (course_code, course_name, abbreviation, duration_years, target_faculty_id)
                mycursor.execute(insert_course_query, query_values)
                
                if mycursor.rowcount > 0:
                    courses_inserted += 1

            # Commit all changes to disk
            mydatabase.commit()
            print(f"[SUCCESS] Added {courses_inserted} new unique courses to faculty: '{faculty_name}' (ID: {target_faculty_id})")

    except Error as error:
        print("[ERROR] Database Error encountered:", error)
    except FileNotFoundError:
        print(f"[ERROR] System Error: The file path '{csv_file_path}' does not exist.")
    finally:
        if mydatabase and mydatabase.is_connected():
            mycursor.close()
            mydatabase.close()
            print("[CLOSE] MySQL session securely closed.")


if __name__ == "__main__":
    # 1. Update this to the exact path of your newly generated courses CSV file
    target_csv = "C:\\Users\\mwamb\\OneDrive\\Desktop\\Team_6_repo\\Team19\\Faculties\\Natural Science\\Experimental\\CSVs\\programs_NS_sorted.csv"
    
    # 2. Type the exact name of the faculty as it appears in your database's 'faculties' table
    faculty_to_lookup = "Natural Science"


    insert_faculty_courses(target_csv, faculty_to_lookup)