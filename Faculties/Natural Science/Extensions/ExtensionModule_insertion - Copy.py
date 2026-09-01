import csv
import mysql.connector
from mysql.connector import Error

def update_module_details(csv_file_path):
    mydatabase = None

    try:
        print(" Connecting to database to update module details...")
        mydatabase = mysql.connector.connect(
            host='127.0.0.1', 
            user='root', 
            password='4492340',
            database='rate_mm'
        )
        mycursor = mydatabase.cursor()

        print(f"Reading spreadsheet file from: {csv_file_path}")
        # 'utf-8-sig' ignores Excel's invisible BOM tag
        with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
            # Tell Python to look for the semicolons Excel used
            csv_reader = csv.reader(file, delimiter=';')
            header = next(csv_reader) # Skips the excel column header row
            modules_updated = 0

            for row in csv_reader:
                # Basic layout safety filter (ensuring row has enough columns up to Credits)
                if not row or len(row) < 9:
                    continue 
                
                # Extracting specific data positions based on your CSV layout
                mod_code         = row[0].strip()  # Column A (Module code)
                learning_outcome = row[6].strip()  # Column G (Learning Outcome)
                main_content     = row[7].strip()  # Column H (Main Content)
                credits          = row[8].strip()  # Column I (Credits)

                # UPDATE query targeting existing mod_code records
                update_mod_query = """
                    UPDATE modules 
                    SET learning_outcome = %s, 
                        main_content = %s, 
                        credits = %s
                    WHERE mod_code = %s
                """
                
                mycursor.execute(update_mod_query, (learning_outcome, main_content, credits, mod_code))
                
                # Count rows that were modified
                if mycursor.rowcount > 0:
                    modules_updated += 1

        # Commit transaction updates to permanent disk storage
        mydatabase.commit()
        print(f" Success! Updated {modules_updated} module records in the database.")

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
    # Point this to your saved Under.csv file location
    target_csv = r"C:\Users\mwamb\OneDrive\Desktop\Team_6_repo\Team19\Faculties\By programe code\Art\CSV\uwc-arts-humanities-modules-2026-v2_CSV_.csv"
    update_module_details(target_csv)