import csv
import mysql.connector
from mysql.connector import Error

def clean_and_parse_csv(file_path):
    """
    Normalizes the file content in-memory.
    If a line is wrapped in outer quotes (the Postgrad 'macro' format),
    it unwraps it and fixes the doubled-up quotes so the parser works.
    """
    cleaned_lines = []
    # encoding='utf-8-sig' strips a leading BOM if Excel added one.
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        for line in file:
            line_str = line.strip()
            if not line_str:
                continue
            
            # Logic: If a row is wrapped in quotes (Postgrad format), 
            # strip the outer ones and fix the internal double quotes.
            # If it's a normal row (Undergrad format), it leaves it alone.
            if line_str.startswith('"') and line_str.endswith('"'):
                line_str = line_str[1:-1]              # Remove outer "
                line_str = line_str.replace('""', '"') # Fix "" to "
            
            cleaned_lines.append(line_str)
    return cleaned_lines

def populate_course_modules(csv_file_path):
    connection = None
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1', user='root', password='4492340', database='rate_mm'
        )
        cursor = connection.cursor()

        # Step 1: Pre-process the file to handle varying Excel formats
        csv_lines = clean_and_parse_csv(csv_file_path)
        
        # Step 2: Parse the now-unified data
        # delimiter=';' matches Excel's "CSV UTF-8" export on SA locale settings.
        reader = csv.DictReader(csv_lines, delimiter=';', skipinitialspace=True)
        
        for row_idx, row in enumerate(reader, start=2):
            mod_code_raw = row.get('Module Code')
            year_raw = row.get('Year Level')
            programmes_raw = row.get('Programmes')

            if not mod_code_raw or not programmes_raw:
                continue

            mod_code = mod_code_raw.strip()
            year = year_raw.strip() if year_raw is not None else ""
            programmes_str = programmes_raw.strip()

            # 1. Resolve internal module ID
            cursor.execute("SELECT id FROM modules WHERE mod_code = %s", (mod_code,))
            mod_result = cursor.fetchone()
            if not mod_result: 
                continue
            mod_id = mod_result[0]

            # 2. Split comma-separated program items safely
            programmes = [p.strip() for p in programmes_str.split(',')]
            
            for prog in programmes:
                prog = prog.replace('"', '').strip()
                if len(prog) < 4: 
                    continue
                
                # Snip the 4-digit numeric code suffix string
                course_code = prog[-4:]

                # 3. Dynamic lookup based on the course code
                cursor.execute(
                    "SELECT id FROM courses WHERE course_code = %s", 
                    (course_code,)
                )
                course_result = cursor.fetchone()
                
                if course_result:
                    course_id = course_result[0]
                    # 4. Insert relationship entry
                    cursor.execute("""
                        INSERT IGNORE INTO course_modules (course_id, module_id, year_of_study)
                        VALUES (%s, %s, %s)
                    """, (course_id, mod_id, year))
                else:
                    print(f"[WARNING] Row {row_idx}: Code '{course_code}' linked to '{mod_code}' not found.")
                    
        connection.commit()
        print("\n[SUCCESS] Successfully populated data for this file!")

    except Error as e:
        print(f"Database Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()



if __name__ == "__main__":
    csv_path = r"C:\Users\mwamb\OneDrive\Desktop\Team_6_repo\Team19\Faculties\By programe code\EMS\CSV\uwc-ems-modules-2026_CSV.csv"
    populate_course_modules(csv_path)