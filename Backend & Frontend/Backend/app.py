from flask import Flask, render_template, request, jsonify,redirect,session, url_for, flash, abort
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from datetime import datetime

from flask_session import Session
import mysql.connector
from mysql.connector import Error

import os
from google import genai

from functools import wraps

#This automatically grabs the API key from my Windows Environment variables
    #Side note:    You'd need to set up an gemini api key if you plan on working on this project


"""
client=genai.Client()

interaction = client.interactions.create(
    model="gemini-3.6-flash", input="I want you to look at the what is after the colon, and moderate it for me. Is it safe to post to a social university application. I want no unprofesional negativity towards a person or professor. ? Respond with True if yes and False if no.: I hate that professor drinks"

)

print(interaction.output_text)
"""




#I now neeeed to work on the reviews and AI api for verifying reviews



#I need to create a new html page fpor the AI side of the code as well as find a way to check reviews before They are posted 



#Now what I need to do is to establish a connection with my database and get all the faculties into a list 



def getfaculties():
    mydatabase = None

    try:
        mydatabase = mysql.connector.connect(
            host='127.0.0.1', 
            user='root', 
            password='4492340',
             database='rate_mm')
        

        print("Connecting to MySQL Database...")
        mycursor = mydatabase.cursor(dictionary=True)


        '''# Practice to ensure that it is connected and working
        mycursor.execute("show tables")
        for i in mycursor:
            print(i)
        '''

        get_query="SELECT * FROM faculties"
        mycursor.execute(get_query)
        all_faculties = mycursor.fetchall()

        return all_faculties



    except Error as error:
        print(f" Database Error encountered: {error}")
        return None


    finally:
        # 4. ENVIRONMENT CLEANUP
        if mydatabase and mydatabase.is_connected():
            mycursor.close()
            mydatabase.close()
            print("MySQL database connection securely closed.")


def getfaculties_id(Faculty_Name):
    mydatabase = None

    try:
        mydatabase = mysql.connector.connect(
            host='127.0.0.1', 
            user='root', 
            password='4492340',
             database='rate_mm')
        

        print("Connecting to MySQL Database...")
        mycursor = mydatabase.cursor(dictionary=True)


        '''# Practice to ensure that it is connected and working
        mycursor.execute("show tables")
        for i in mycursor:
            print(i)
        '''

        get_query="SELECT id FROM faculties where fac_name= %s"
        mycursor.execute(get_query, (Faculty_Name,))
        all_faculties_id = mycursor.fetchall()

        return all_faculties_id



    except Error as error:
        print(f" Database Error encountered: {error}")
        return None


    finally:
        # 4. ENVIRONMENT CLEANUP
        if mydatabase and mydatabase.is_connected():
            mycursor.close()
            mydatabase.close()
            print("MySQL database connection securely closed.")


def get_programmes(faculty_id):
    mydatabase = None

    try:
        mydatabase = mysql.connector.connect(
            host='127.0.0.1', 
            user='root', 
            password='4492340',
             database='rate_mm')
        

        print("Connecting to MySQL Database...")
        mycursor = mydatabase.cursor(dictionary=True)


        '''# Practice to ensure that it is connected and working
        mycursor.execute("show tables")
        for i in mycursor:
            print(i)
        '''

        get_query="SELECT * FROM courses Where faculty_id= %s"
        mycursor.execute(get_query,(faculty_id,))
        all_programmes = mycursor.fetchall()

        Programmes=[]

        for prog in all_programmes:
            Programmes.append(prog["course_name"])

        return Programmes
    




    except Error as error:
        print(f" Database Error encountered: {error}")
        return None


    finally:
        # 4. ENVIRONMENT CLEANUP
        if mydatabase and mydatabase.is_connected():
            mycursor.close()
            mydatabase.close()
            print("MySQL database connection securely closed.")


def get_modules(programme_name):
    mydatabase = None

    try:
        mydatabase = mysql.connector.connect(
            host='127.0.0.1', 
            user='root', 
            password='4492340',
             database='rate_mm')
        

        print("Connecting to MySQL Database...")
        mycursor = mydatabase.cursor(dictionary=True)


        '''# Practice to ensure that it is connected and working
        mycursor.execute("show tables")
        for i in mycursor:
            print(i)
        '''

        get_query="SELECT id FROM courses where course_name= %s"
        mycursor.execute(get_query,(programme_name,))
        programme_id = mycursor.fetchall()
        module_id=get_moduluse_from_id(programme_id[0]["id"])
     

        #Here I am creating a list of the years of study
        years_of_study = [items["year_of_study"] for items in module_id]

        #Here I am creating a list of the module ids of study
        modules_ids_for_names = [items["module_id"] for items in module_id]


        #module_names = [get_module_name(item) for item in modules_ids_for_names]



        #I will create a new function that will take both the years and module ids as parameters and then return the year but allong with the module name


        module_name_year=get_mod_name(modules_ids_for_names,years_of_study)



        # Create the 2D list of paired data
        #module_name_year = [list(pair) for pair in zip(years_of_study, module_names)]
        return module_name_year


    except Error as error:
        print(f" Database Error encountered: {error}")
        return None


    finally:
        # 4. ENVIRONMENT CLEANUP
        if mydatabase and mydatabase.is_connected():
            mycursor.close()
            mydatabase.close()
            print("MySQL database connection securely closed.")


def get_moduluse_from_id(programme_id):
    mydatabase = None

    try:
        mydatabase = mysql.connector.connect(
            host='127.0.0.1', 
            user='root', 
            password='4492340',
             database='rate_mm')
        

        print("Connecting to MySQL Database...")
        mycursor = mydatabase.cursor(dictionary=True)


        '''# Practice to ensure that it is connected and working
        mycursor.execute("show tables")
        for i in mycursor:
            print(i)
        '''

        get_query="SELECT module_id, year_of_study  FROM course_modules where course_id= %s"
        mycursor.execute(get_query,(programme_id,))
        module_ids = mycursor.fetchall()

        return module_ids


    except Error as error:
        print(f" Database Error encountered: {error}")
        return None


    finally:
        # 4. ENVIRONMENT CLEANUP
        if mydatabase and mydatabase.is_connected():
            mycursor.close()
            mydatabase.close()
            print("MySQL database connection securely closed.")


def get_module_name(module_id):
    mydatabase = None

    try:
        mydatabase = mysql.connector.connect(
            host='127.0.0.1', 
            user='root', 
            password='4492340',
             database='rate_mm')
        

        print("Connecting to MySQL Database...")
        mycursor = mydatabase.cursor(dictionary=True)


        '''# Practice to ensure that it is connected and working
        mycursor.execute("show tables")
        for i in mycursor:
            print(i)
        '''

        get_query="Select mod_name from modules where id= %s"
        mycursor.execute(get_query,(module_id,))
        module_name = mycursor.fetchall()

        return module_name[0]["mod_name"]


    except Error as error:
        print(f" Database Error encountered: {error}")
        return None


    finally:
        # 4. ENVIRONMENT CLEANUP
        if mydatabase and mydatabase.is_connected():
            mycursor.close()
            mydatabase.close()
            print("MySQL database connection securely closed.")


def get_mod_name(id,year):
    mydatabase = None

    try:
        mydatabase = mysql.connector.connect(
            host='127.0.0.1', 
            user='root', 
            password='4492340',
             database='rate_mm')
        

        print("Connecting to MySQL Database...")
        mycursor = mydatabase.cursor(dictionary=True)


        '''# Practice to ensure that it is connected and working
        mycursor.execute("show tables")
        for i in mycursor:
            print(i)
        '''

        module_name_code=[]

        for ids in id:
            get_query="Select mod_name,mod_code from modules where id= %s"
            mycursor.execute(get_query,(ids,))
            
            module_name_code.append(mycursor.fetchall()[0])

        
        #module_name_year=[list(pair) for pair in zip(module_name_code,year)]
        
        # New way (merges the year directly into each dictionary)
        module_name_year = [{**mod, "year": yr} for mod, yr in zip(module_name_code, year)]

        return module_name_year



    except Error as error:
        print(f" Database Error encountered: {error}")
        return None


    finally:
        # 4. ENVIRONMENT CLEANUP
        if mydatabase and mydatabase.is_connected():
            mycursor.close()
            mydatabase.close()
            print("MySQL database connection securely closed.")


def get_single_module(module_code,program_name):
    mydatabase = None

    try:
        mydatabase = mysql.connector.connect(
            host='127.0.0.1', 
            user='root', 
            password='4492340',
             database='rate_mm')
        

        print("Connecting to MySQL Database...")
        mycursor = mydatabase.cursor(dictionary=True)


        '''# Practice to ensure that it is connected and working
        mycursor.execute("show tables")
        for i in mycursor:
            print(i)
        '''

        get_query="SELECT * FROM modules where mod_code=%s"
        mycursor.execute(get_query,(module_code,))
        module_info = mycursor.fetchone()


        mod_id=module_info["id"]

    
        get_query_1="SELECT *  FROM courses WHERE course_name=%s"
        mycursor.execute(get_query_1,(program_name,))
        program_info= mycursor.fetchone()

        program_id=program_info["id"]



        get_query_2="SELECT year_of_study FROM course_modules WHERE course_id=%s AND module_id=%s"
        mycursor.execute(get_query_2,(program_id,mod_id,))
        year_study= mycursor.fetchone()

        programe_info_for_module=program_info
        programe_info_for_module["year"]=year_study["year_of_study"]
        programe_info_for_module["prereqs"]=module_info["prerequisites"]
        programe_info_for_module["coreqs"]=module_info["corequisites"]
        programe_info_for_module["learning_outcome"]=module_info["learning_outcome"]
        programe_info_for_module["main_content"]=module_info["main_content"]
        programe_info_for_module["credits"]=module_info["credits"]




        return programe_info_for_module



    except Error as error:
        print(f" Database Error encountered: {error}")
        return None


    finally:
        # 4. ENVIRONMENT CLEANUP
        if mydatabase and mydatabase.is_connected():
            mycursor.close()
            mydatabase.close()
            print("MySQL database connection securely closed.")

    
def get_all_programmes():
    mydatabase = None

    try:
        mydatabase = mysql.connector.connect(
            host='127.0.0.1', 
            user='root', 
            password='4492340',
             database='rate_mm')
        

        print("Connecting to MySQL Database...")
        mycursor = mydatabase.cursor(dictionary=True)


        '''# Practice to ensure that it is connected and working
        mycursor.execute("show tables")
        for i in mycursor:
            print(i)
        '''

        get_query="SELECT course_name FROM courses "
        mycursor.execute(get_query)
        # Extract just the 'course_name' value from each dictionary
        all_programmes = [row['course_name'] for row in mycursor.fetchall()]       

        return all_programmes



    except Error as error:
        print(f" Database Error encountered: {error}")
        return None


    finally:
        # 4. ENVIRONMENT CLEANUP
        if mydatabase and mydatabase.is_connected():
            mycursor.close()
            mydatabase.close()
            print("MySQL database connection securely closed.")

def add_user(student_number,password,programme,year_of_study,student_email):
    mydatabase = None

    try:
        mydatabase = mysql.connector.connect(
            host='127.0.0.1', 
            user='root', 
            password='4492340',
             database='rate_mm')
        

        print("Connecting to MySQL Database...")
        mycursor = mydatabase.cursor(dictionary=True)

        #Hashing the password before storing it

        check_query = "SELECT username FROM users WHERE username = %s"
        mycursor.execute(check_query, (student_number,))
        existing_user = mycursor.fetchone()


        if existing_user:
            print(
                f"Registration failed: Student number {student_number} already exists."
            )
            return False

        

        hashed_password = generate_password_hash(password)

        sql_query = """
            INSERT INTO users (username, student_email, password, degree_program, year_of_study)
            VALUES (%s, %s, %s, %s, %s)
        """

        user_data = (student_number, student_email, hashed_password, programme, year_of_study)


        mycursor.execute(sql_query, user_data)
        mydatabase.commit()



        print("User successfully registered!")
        return True



        



    except Exception as error:
        print(f" Database Error encountered: {error}")
        return False


    finally:
        # 4. ENVIRONMENT CLEANUP
        if mydatabase and mydatabase.is_connected():
            mycursor.close()
            mydatabase.close()
            print("MySQL database connection securely closed.")





    print()


def vallid_user(number,password):
    mydatabase = None

    try:
        mydatabase = mysql.connector.connect(
            host='127.0.0.1', 
            user='root', 
            password='4492340',
             database='rate_mm')
        

        print("Connecting to MySQL Database...")
        mycursor = mydatabase.cursor(dictionary=True)


        '''# Practice to ensure that it is connected and working
        mycursor.execute("show tables")
        for i in mycursor:
            print(i)
        '''

        get_query="SELECT * FROM users WHERE username= %s"
        mycursor.execute(get_query,(number,))
        user = mycursor.fetchone()
        #print(user)

        if user:
            # For Hashed Passwords (Flask standard):
            if check_password_hash(user['password'], password):
                return True

       


        return False



    except Error as error:
        print(f" Database Error encountered: {error}")
        return False


    finally:
        # 4. ENVIRONMENT CLEANUP
        if mydatabase and mydatabase.is_connected():
            mycursor.close()
            mydatabase.close()
            print("MySQL database connection securely closed.")


def get_all_modules():

    try:
        mydatabase = mysql.connector.connect(
            host='127.0.0.1', 
            user='root', 
            password='4492340',
             database='rate_mm')
        

        print("Connecting to MySQL Database...")
        mycursor = mydatabase.cursor(dictionary=True)


        '''# Practice to ensure that it is connected and working
        mycursor.execute("show tables")
        for i in mycursor:
            print(i)
        '''

        get_query="SELECT *FROM modules"
        mycursor.execute(get_query)
        full_module_list = mycursor.fetchall()

        return full_module_list


    except Error as error:
        print(f" Database Error encountered: {error}")
        return None


    finally:
        # 4. ENVIRONMENT CLEANUP
        if mydatabase and mydatabase.is_connected():
            mycursor.close()
            mydatabase.close()
            print("MySQL database connection securely closed.")


def get_mode_info(mode_code):

    try:
        mydatabase = mysql.connector.connect(
            host='127.0.0.1', 
            user='root', 
            password='4492340',
             database='rate_mm')
        

        print("Connecting to MySQL Database...")
        mycursor = mydatabase.cursor(dictionary=True)


        '''# Practice to ensure that it is connected and working
        mycursor.execute("show tables")
        for i in mycursor:
            print(i)
        '''

        get_query="SELECT *FROM modules WHERE mod_code=%s"
        mycursor.execute(get_query,(mode_code,))
        full_module_list = mycursor.fetchone()


        return full_module_list


    except Error as error:
        print(f" Database Error encountered: {error}")
        return None


    finally:
        # 4. ENVIRONMENT CLEANUP
        if mydatabase and mydatabase.is_connected():
            mycursor.close()
            mydatabase.close()
            print("MySQL database connection securely closed.")


def get_programs_single_module(mode_code):

    try:
        mydatabase = mysql.connector.connect(
            host='127.0.0.1', 
            user='root', 
            password='4492340',
             database='rate_mm')
        

        print("Connecting to MySQL Database...")
        mycursor = mydatabase.cursor(dictionary=True)


        '''# Practice to ensure that it is connected and working
        mycursor.execute("show tables")
        for i in mycursor:
            print(i)
        '''

        get_id="SELECT id FROM modules WHERE mod_code=%s"
        mycursor.execute(get_id,(mode_code,))
        mod_id = mycursor.fetchone()["id"]


        get_list="SELECT course_id,year_of_study FROM course_modules WHERE module_id=%s"
        mycursor.execute(get_list,(mod_id,))
        full_programs_id_list = mycursor.fetchall()

        course_names= get_programme_from_id(full_programs_id_list)

        for i in range (len(full_programs_id_list)):
            full_programs_id_list[i]["course_name"]=course_names[i]["course_name"]

        
        '''
        I have a slight issue, so my course_module table is 
        where we get the info on year and so on, but when you search just by module and not course, 
        it doesn't show the year and prereq... so I need to find a way to update my single module page
        -I could potentially get it to also get every program it is going to be in and list all of that in the mod info section 
        aong with each  the other info.
        '''
        

        return full_programs_id_list 


    except Error as error:
        print(f" Database Error encountered: {error}")
        return None


    finally:
        # 4. ENVIRONMENT CLEANUP
        if mydatabase and mydatabase.is_connected():
            mycursor.close()
            mydatabase.close()
            print("MySQL database connection securely closed.")


def get_programme_from_id(course_module):
    try:
        mydatabase = mysql.connector.connect(
            host='127.0.0.1', 
            user='root', 
            password='4492340',
             database='rate_mm')
        

        print("Connecting to MySQL Database...")
        mycursor = mydatabase.cursor(dictionary=True)


        '''# Practice to ensure that it is connected and working
        mycursor.execute("show tables")
        for i in mycursor:
            print(i)
        '''

        program_ids=[]

        for i in course_module:
            get_name="SELECT course_name FROM courses WHERE id=%s"
            mycursor.execute(get_name,(i["course_id"],))
            program_ids.append(mycursor.fetchone())



        

        return program_ids


    except Error as error:
        print(f" Database Error encountered: {error}")
        return None


    finally:
        # 4. ENVIRONMENT CLEANUP
        if mydatabase and mydatabase.is_connected():
            mycursor.close()
            mydatabase.close()
            print("MySQL database connection securely closed.")


def get_reviews(module_code):
    mydatabase = None
    try:
        mydatabase = mysql.connector.connect(
            host='127.0.0.1', 
            user='root', 
            password='4492340',
            database='rate_mm'
        )

        mycursor = mydatabase.cursor(dictionary=True)

        # 1. Fetch module primary key ID using mod_code
        get_id = "SELECT id FROM modules WHERE mod_code=%s"
        mycursor.execute(get_id, (module_code,))
        mod_result = mycursor.fetchone()
        
        # If module code doesn't exist, return empty list safely
        if not mod_result:
            return []

        mod_id = mod_result["id"]

        # 2. Fetch reviews using exact schema column names
        get_reviews_query = """
            SELECT 
                IF(r.is_anonymous, 'Anonymous Student', COALESCE(u.username, 'Student')) AS user_id,
                r.difficulty_rating,
                r.teaching_rating AS teaching,
                r.content_rating AS content,
                r.pros,
                r.cons,
                r.general_advice,
                DATE_FORMAT(r.date_posted, '%b %d, %Y') AS date
            FROM reviews r
            LEFT JOIN users u ON r.user_id = u.id
            WHERE r.module_id = %s
            ORDER BY r.id DESC
        """
        
        mycursor.execute(get_reviews_query, (mod_id,))
        mod_review_info = mycursor.fetchall()

        return mod_review_info or []

    except Exception as error:
        print(f"❌ DATABASE ERROR: {error}")
        return []

    finally:
        if mydatabase and mydatabase.is_connected():
            mycursor.close()
            mydatabase.close()
            print("MySQL database connection securely closed.")


def add_a_review(payload: dict):

    try:
        mydatabase = mysql.connector.connect(
            host='127.0.0.1', 
            user='root', 
            password='4492340',
             database='rate_mm')
        

        print("Connecting to MySQL Database...")
        mycursor = mydatabase.cursor(dictionary=True)

        mod_code=payload.get('code')
        get_mod_id="SELECT id FROM modules WHERE mod_code=%s"
        mycursor.execute(get_mod_id,(mod_code,))
        module_result = mycursor.fetchone()

        if not module_result:
            print(f"Module '{mod_code}' not found.")
            return False

        module_id=module_result["id"]          #The fetchone will return a dictionary, so I am doing this to get the integer value



        user=payload.get('user')
        get_user_id="SELECT id FROM users WHERE username=%s"
        mycursor.execute(get_user_id,(user,))
        user_result = mycursor.fetchone()

        if not user_result:
            print(f"User '{user}' not found.")
            return False

        user_id = user_result['id']          #The fetchone will return a dictionary, so I am doing this to get the integer value





        diff=payload.get('difficulty')
        teach=payload.get('teaching')
        content=payload.get('content')

        pros = payload.get('pros')
        cons= payload.get('cons')
        advice=payload.get('advice')

        review_values = (
            diff,
            teach,
            content,
            pros,
            cons,
            advice,
            user_id,
            module_id
        )

        insert_query = """
            INSERT INTO reviews (
                difficulty_rating,
                teaching_rating,
                content_rating,
                pros,
                cons,
                general_advice,
                user_id,
                module_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """


        mycursor.execute(insert_query, review_values)
        mydatabase.commit()


        print(f"Review inserted successfully! (Inserted Row ID: {mycursor.lastrowid})")
        return True


    except Error as error:
        if mydatabase:
            mydatabase.rollback()
        print(f" Database Error encountered: {error}")
        return None


    finally:
        # 4. ENVIRONMENT CLEANUP
        if mydatabase and mydatabase.is_connected():
            mycursor.close()
            mydatabase.close()
            print("MySQL database connection securely closed.")


def already_reviewed(mod_code,user):

    try:
        mydatabase = mysql.connector.connect(
            host='127.0.0.1', 
            user='root', 
            password='4492340',
             database='rate_mm')
        

        print("Connecting to MySQL Database...")
        mycursor = mydatabase.cursor(dictionary=True)

        get_mod_id="SELECT id FROM modules WHERE mod_code=%s"
        mycursor.execute(get_mod_id,(mod_code,))
        module_result = mycursor.fetchone()

        if not module_result:
            print(f"Module '{mod_code}' not found.")
            return False

        module_id=module_result["id"]          #The fetchone will return a dictionary, so I am doing this to get the integer value

        
        get_user_id="SELECT id FROM users WHERE username=%s"
        mycursor.execute(get_user_id,(user,))
        user_result = mycursor.fetchone()

        if not user_result:
            print(f"User '{user}' not found.")
            return False

        user_id = user_result['id']          #The fetchone will return a dictionary, so I am doing this to get the integer value


        check_query="SELECT id FROM reviews WHERE user_id=%s AND module_id=%s"
        mycursor.execute(check_query,(user_id,module_id))
        existing_review = mycursor.fetchone()

        # True if a review exists, False if user hasn't reviewed yet
        return existing_review is not None


    except Error as error:
        if mydatabase:
            mydatabase.rollback()
        print(f" Database Error encountered: {error}")
        return False


    finally:
        # 4. ENVIRONMENT CLEANUP
        if mydatabase and mydatabase.is_connected():
            mycursor.close()
            mydatabase.close()
            print("MySQL database connection securely closed.")


def safe_moderation(Pros, Cons, Advice):
    client=genai.Client()
    comment=Pros+Cons+Advice

    moderation_prompt = """
        You are a content moderator for a professional university social application. Analyze the comment provided after the colon. Determine whether it is safe to post. It must NOT contain:
        - Unprofessional negativity, harassment, or personal attacks directed at any student, person, or professor.
        - Hate speech, profanity, or malicious spam.
        - Bullying or toxic behavior.

        Constructive academic disagreement or casual conversation is allowed. 

        Respond with ONLY the exact word "True" if it is safe, or "False" if it violates the rules. Do not include any punctuation, explanation, or extra text.

        Comment to evaluate: 
        """

    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite", 
        input=moderation_prompt + comment,generation_config={
          "max_output_tokens": 5,  # Stop generating instantly after True/False
          "temperature": 0.0,  # Zero randomness speeds up processing
      },
        

    )

    if interaction.output_text.strip() == "True":
        return True
    else:
        return False    


def generate_ai_summary(mod_code):
    mod_data=get_mode_info(mod_code)
    mod_name=mod_data["mod_name"]
    content=mod_data["main_content"]
    outcome=mod_data["learning_outcome"]

    reviews=get_reviews(mod_code)

    all_general_advice=[]


    #If there were any comments
    if len(reviews) != 0:
        #I need an if statement that will only happen if the reviews list, isn't empty 
        for x in reviews:
            all_general_advice.append(x["pros"])
            all_general_advice.append(x["cons"])
            all_general_advice.append(x["general_advice"])


        prompt = f"""
        Write a concise 2-sentence summary for the module '{mod_name}'.
        
        Module name: {mod_name}
        Syllabus Content: {content}
        Learning Outcomes: {outcome}
        Student Reviews: {all_general_advice}
        
        Combine syllabus facts with real student sentiment. Keep it under 75 words and student-friendly.
        """

    #Here is where I will be generating the summary

    #if there weren't any comments

    else:
        prompt = f"""
        Write a concise 2-sentence summary for the module '{mod_name}'.
        
        Module name: {mod_name}
        Syllabus Content: {content}
        Learning Outcomes: {outcome}
        
        Base this strictly on the course details above. Keep it under 75 words and student-friendly.
        """
# 3. Call Gemini API
    try:
        client=genai.Client()
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            )
        return response.text.strip()
    
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "This module covers core foundational concepts, practical exercises, and structured assessments."

    



def get_user_role(user):
    mydatabase = None

    try:
        mydatabase = mysql.connector.connect(
            host='127.0.0.1', 
            user='root', 
            password='4492340',
             database='rate_mm')
        

        print("Connecting to MySQL Database...")
        mycursor = mydatabase.cursor(dictionary=True)

        person=session["user"]

        get_query="SELECT role FROM users WHERE username=%s"
        mycursor.execute(get_query,(user,))
        get_role_dict = mycursor.fetchone()

        get_role=get_role_dict["role"]

        return get_role



    except Error as error:
        print(f" Database Error encountered: {error}")
        return None


    finally:
        # 4. ENVIRONMENT CLEANUP
        if mydatabase and mydatabase.is_connected():
            mycursor.close()
            mydatabase.close()
            print("MySQL database connection securely closed.")


    

#print((get_user_role("4492340")))#I need to figure out what to do about the AI guide









app = Flask(__name__)

# Required: Flask needs a secret key to sign session cookies
app.secret_key = "dev"

#configuring the sessions. This will store the cookies on the server instead of a database or somewhere else
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)


# Decorator to protect all admin-only routes
def admin_required(func):
    @wraps(func)  # Prevents Flask endpoint naming conflicts
    def wrapper(*args, **kwargs):

        # Check if user is logged in AND has the admin role
        if "user" not in session or session.get("role") != "ADMIN":
            abort(403)

        # Executes original route if check succeeds
        return func(*args, **kwargs)

    return wrapper



    

#Standard User Section

@app.route("/",methods=["GET"])
def index():
    Faculties = getfaculties()

    module_list=get_all_modules()
    


    return render_template("1_index.html",Faculties=Faculties,user=session.get("user"),Modules=module_list )


@app.route("/Loggin",methods=["Get"])
def log_in():
#I need to make changes to my 1 login.html by handeling the login in and the registering
    programmes=get_all_programmes()

    return render_template("1_login.html",programmes=programmes)



@app.route("/register", methods=["POST"])
def register():
    # Read data sent from the HTML form
    student_number = request.form.get("student_number")
    password = request.form.get("password")
    programme = request.form.get("programme")
    year_of_study = request.form.get("year_of_study")



    print("\n--- NEW REGISTRATION ATTEMPT ---")
    print(f"Received student_number: '{student_number}' (Length: {len(student_number) if student_number else 0})")
    print(f"Received password: '{password}'")
    print(f"Received programme: '{programme}'")
    print(f"Received year_of_study: '{year_of_study}'")


    # Check if student_number exists AND has a length of 7
    if not student_number or len(student_number) != 7:
        flash("Student number must be exactly 7 digits.", "danger")
        return redirect(url_for("log_in"))
    else:
        # Generate user email automatically
        student_email = f"{student_number}@myuwc.ac.za"


        '''I need to do that username check somewhere around here. I will put everything bellow in the case where new user being created'''
        added=add_user(student_number,password,programme,year_of_study,student_email)
        if added:







            session["user"]=student_number
            session["role"]=get_user_role(student_number)

            return redirect(url_for("index"))
        else:
            flash("There was an error in creating new user, try again")
            return render_template(
            "1_login_error.html",
            title="Registration Failed",
            error="Registration failed because this student number is already registered in the system.",
            )


@app.route("/Login Error",methods=["GET"])
def login_error():
    return render_template("1_login_error.html")
   

@app.route("/Log",methods=["POST"])
def loged_in():
#I need to make changes to my 1 login.html by handeling the login in and the registering
    """I will check if the the student name and password are valid """



    student_number = request.form.get("uwc_student_number")
    password = request.form.get("uwc_password")


    print("Student number: "+student_number )
    print("Password: "+password)


    validity=vallid_user(student_number,password)
    if validity:


        #---------------------------------------------------------------------
        session["user"]=student_number
        session["role"]=get_user_role(student_number)



        return redirect(url_for("index"))


    else:    
        error_msg="The student number or password you entered is incorrect. Please verify your account details and try again."
        return render_template(
            "1_login_error.html",
            title="Login Failed",
            error="The student number or password you entered is incorrect. Please verify your account details and try again.",
        ) 



@app.route("/Log out")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/Program",methods=["GET"])
def Program():
    # Flask automatically grabs 'faculty' from the URL query string
    faculty_name = request.args.get('faculty')

    faculty_id=getfaculties_id(faculty_name)[0]["id"]

    faculty_programmes=get_programmes(faculty_id)
    return render_template('1_Program.html', faculty=faculty_name, programmes=faculty_programmes)


@app.route("/Modules", methods=["GET"])
def Program_modules():  
    programme = request.args.get("Programme")

    All_modules=get_modules(programme)
    #I first need a function that will get me the course id    
    return render_template("1_module.html",All_modules=All_modules)


@app.route('/Module by program')  
def module_page():
    module_code = request.args.get('code')
    program_name=request.args.get('program')
    module_info=get_single_module(module_code,program_name)


    reviews=get_reviews(module_code)

    return render_template("1_modulepage.html",module_code=module_code,module_info=module_info,user=session.get("user"),reviews=reviews)


@app.route('/Module')
def module_direct():
    mode_code=request.args.get("code")
    mode_info=get_mode_info(mode_code)
    programs=get_programs_single_module(mode_code)


    reviews=get_reviews(mode_code)



    #print(f"This is the mode: {mode_code}")


    return render_template("1_modulepage.html",module_code=mode_code,module_info=mode_info,user=session.get("user"),reviews=reviews,programs_list=programs)


@app.route('/add-review', methods=['POST'])
def add_review():

    # 1. Parse JSON body sent from the JS fetch request
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No data payload received.'}), 400

    # 2. Verify authentication on the server side
    # Don't rely strictly on client-side JS flags
    current_user = session.get('user')
    if not current_user:
        return jsonify({'status': 'error', 'message': 'Authentication required to post a review.'}), 401

    # 3. Extract and cast form values matching modal elements
    try:
        review_payload = {
                    'code': data.get('code'),
                    'program': data.get('program'),
                    'user': current_user,
                    'difficulty': int(data.get('difficulty_rating', 0)),
                    'teaching': int(data.get('teaching', 0)),
                    'content': int(data.get('content', 0)),
                    'pros': data.get('pros', '').strip(),
                    'cons': data.get('cons', '').strip(),
                    'advice': (data.get('general_advice') or '').strip()
                }



       
        

    except (ValueError, TypeError):
        return jsonify({'status': 'error', 'message': 'Invalid score rating payload.'}),400

    # 4. Input Vlidation

    
    if not safe_moderation(review_payload.get("pros"),review_payload.get("cons"),review_payload.get("advice")):
        return jsonify({'status': 'error', 'message': 'This review might be toxic or contain vulgar language'})
    

    if not review_payload.get('code') or not review_payload.get('pros') or not review_payload.get('cons') or not review_payload.get('advice'):
        return jsonify({'status': 'error', 'message': 'All required fields must be completed.'}), 400
    

    if already_reviewed(review_payload.get("code"),review_payload.get("user")):
        return jsonify({'status': 'error', 'message': 'A user cannot add multipple reviews to a singular module'}), 400


    if not (1 <= review_payload['difficulty'] <= 10 and 1 <= review_payload['teaching'] <= 10 and 1 <= review_payload['content'] <= 10):
        return jsonify({'status': 'error', 'message': 'Ratings must be between 1 and 10.'}),400

    # 5. Database Insertion Logic (Example: Flask-SQLAlchemy)
    success = add_a_review(review_payload)

    if not success:
        return jsonify({'status': 'error', 'message': 'Failed to save review to the database.'}), 500



    # 6. Response expected by frontend JS block (data.status === 'success')
    return jsonify({
        'status': 'success',
        'message': 'Evaluation posted successfully!'
    })


@app.route('/profile')
def user_profile():
    if 'user' not in session:
        return redirect(url_for('log_in'))
   
    username = session['user']
    '''I need to create a func that will get all the necessary user info and send it to that html page'''


    return render_template('1_profile.html') # You can create this template next!


I have a couple of orders of bussiness
- I need to complete the 1_profile.html 
- I need to complete the 1_admin_dashboard.html page
- I need to give normal users the aboiluity to delete or edit a review in the Module page

#AI Section

@app.route('/Ai Guide',methods=["GET"])
def ai_guide():
    return


@app.route("/api/module-summary")
def api_module_summary():
    # Grab module code from URL parameter e.g., /api/module-summary?code=COS101
    mod_code = request.args.get("code")

    if not mod_code:
        return jsonify({"error": "Module code parameter is required"}), 400

    summary = generate_ai_summary(mod_code)
    return jsonify({"summary": summary})









#Admin Section

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():

    '''Here I will just have a screen where the admin will have options to:
        Look at a particular module:
            -delete a comment under the module
            -
            
        Look at a particular user:
            -They can view the user details
            -They can decide to give the user admin permisions 
            -They can delete a user
            -They can view all comments by a user
            -They can remove a comment a user might have posted on a review'''


    return render_template('1_admin_dashboard.html')