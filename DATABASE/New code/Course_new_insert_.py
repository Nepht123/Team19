import csv
import re
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
        return result[0]  # Returns the integer id
    else:
        return None


def parse_codes(code_str):
    """
    Splits a course-code field into (code, tag) pairs.
    Handles simple codes like '7162' as well as combined
    full-time/part-time codes like '7712 (FT) / 7713 (PT)'.
    """
    parts = [p.strip() for p in code_str.split('/')]
    result = []
    for p in parts:
        m = re.match(r'(\d+)\s*(?:\(([^)]+)\))?', p)
        if m:
            code = m.group(1)
            tag = m.group(2).strip().upper() if m.group(2) else None
            result.append((code, tag))
    return result


def parse_durations(dur_str):
    """
    Splits a duration field into (years, tag) pairs.
    Handles plain values like '4 years' as well as combined
    full-time/part-time durations like
    '1 year full-time / 2 years part-time'.
    """
    parts = [p.strip() for p in dur_str.split('/')]
    result = []
    for p in parts:
        # Grabs the first run of digits in the field, regardless of
        # what surrounds it - handles '4', '4 years', 'Years 4', etc.
        m = re.search(r'(\d+)', p)
        years = int(m.group(1)) if m else None
        tag = None
        if re.search(r'full[\s-]*time', p, re.IGNORECASE):
            tag = 'FT'
        elif re.search(r'part[\s-]*time', p, re.IGNORECASE):
            tag = 'PT'
        result.append((years, tag))
    return result


def expand_row(course_name, course_code, abbreviation, duration_str):
    """
    Returns a list of (course_name, code, abbreviation, duration_years)
    tuples for a single CSV row. Most rows produce exactly one tuple.
    Rows that bundle a full-time and part-time variant into one line
    (e.g. code '7712 (FT) / 7713 (PT)', duration '1 year full-time /
    2 years part-time') are expanded into two separate course rows,
    matched up by their FT/PT tag where possible.
    """
    codes = parse_codes(course_code)
    durations = parse_durations(duration_str)

    rows = []

    if not codes or not durations:
        return rows

    if len(codes) == 1 and len(durations) == 1:
        rows.append((course_name, codes[0][0], abbreviation, durations[0][0]))
        return rows

    if len(codes) == len(durations):
        for i, (code, ctag) in enumerate(codes):
            match = None
            if ctag:
                for years, dtag in durations:
                    if dtag == ctag:
                        match = years
                        break
            if match is None:
                # Fall back to matching by position
                match = durations[i][0]
            rows.append((course_name, code, abbreviation, match))
    else:
        # Counts don't line up - fall back to using the first
        # duration value found for every code on this row.
        fallback_years = durations[0][0]
        for code, ctag in codes:
            rows.append((course_name, code, abbreviation, fallback_years))

    return rows


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

        print(f"Searching for the database ID corresponding to: '{faculty_name}'...")
        target_faculty_id = get_faculty_id_by_name(mycursor, faculty_name)

        if target_faculty_id is None:
            print(f"[CRITICAL ERROR] Could not find a faculty named '{faculty_name}' in your database.")
            print("Please make sure you have inserted the faculty name into the 'faculties' table first!")
            return

        print(f"[FOUND] '{faculty_name}' corresponds to internal Database ID: {target_faculty_id}")

        print(f"Reading spreadsheet file from: {csv_file_path}")
        # encoding='utf-8-sig' strips a leading BOM if Excel added one.
        # delimiter=';' matches Excel's "CSV UTF-8" export on SA locale settings.
        with open(csv_file_path, mode='r', encoding='utf-8-sig', newline='') as file:
            csv_reader = csv.reader(file, delimiter=';')
            header = next(csv_reader)  # Skips the column header row

            courses_inserted = 0
            rows_skipped = 0

            for row in csv_reader:
                # Layout safety filter: Ensure row has columns up to index 3 (Duration Years)
                if not row or len(row) < 4:
                    continue

                course_name  = row[0].strip()  # Column A
                course_code  = row[1].strip()  # Column B
                abbreviation = row[2].strip()  # Column C
                duration_raw = row[3].strip()  # Column D (may be free text)

                expanded_rows = expand_row(course_name, course_code, abbreviation, duration_raw)

                if not expanded_rows:
                    print(f"[SKIPPED] Could not parse row: {row}")
                    rows_skipped += 1
                    continue

                for name, code, abbr, duration_years in expanded_rows:
                    if duration_years is None:
                        print(f"[SKIPPED] Could not determine duration for: {row}")
                        rows_skipped += 1
                        continue

                    insert_course_query = """
                        INSERT IGNORE INTO courses (course_code, course_name, abbreviation, duration_years, faculty_id)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    query_values = (code, name, abbr, duration_years, target_faculty_id)
                    mycursor.execute(insert_course_query, query_values)

                    if mycursor.rowcount > 0:
                        courses_inserted += 1

            mydatabase.commit()
            print(f"[SUCCESS] Added {courses_inserted} new unique courses to faculty: '{faculty_name}' (ID: {target_faculty_id})")
            if rows_skipped:
                print(f"[NOTE] {rows_skipped} row(s) were skipped - review the [SKIPPED] lines above.")

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
    target_csv = r"C:\Users\mwamb\OneDrive\Desktop\Team_6_repo\Team19\Faculties\By programe code\EMS\CSV\uwc-ems-programmes-2026_CSV.csv"
    # 2. Type the exact name of the faculty as it appears in your database's 'faculties' table
    faculty_to_lookup = "EMS"

    insert_faculty_courses(target_csv, faculty_to_lookup)