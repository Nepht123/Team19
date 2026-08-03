from flask import Flask, render_template, request, jsonify,redirect,session, url_for, flash
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from flask_session import Session
import mysql.connector
from mysql.connector import Error






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







print(vallid_user(4492340,"N@M51310"))


















app = Flask(__name__)

# Required: Flask needs a secret key to sign session cookies
app.secret_key = "dev"

#configuring the sessions. This will store the cookies on the server instead of a database or somewhere else
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)












@app.route("/",methods=["GET"])
def index():
    Faculties = getfaculties()





    #user_login=session.get("user")


    # True if user is logged in, False if None
    #status = user_login is not None


    return render_template("1_index.html",Faculties=Faculties,user=session.get("user") )



@app.route("/Loggin",methods=["Get"])
def log_in():
#I need to make changes to my 1 login.html by handeling the login in and the registering
    programmes=get_all_programmes()

    return render_template("1_login.html",programmes=programmes)





'''

I need to add a feature that will look in the database to see if a username (student number) already exist, if it does,
I need to send an error message to the user, telling them that user already exists and redirect them to the login page

'''
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




            #--------------------------------------------------------------------------------------------------





            session["user"]=student_number
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





@app.route('/Module')  
def module_page():
    module_code = request.args.get('code')
    program_name=request.args.get('program')
    module_info=get_single_module(module_code,program_name)
    return render_template("1_modulepage.html",module_code=module_code,module_info=module_info,user=session.get("user"))

#Now I need to get this data into the modules




@app.route('/add-review', methods=['POST'])
def add_review():
    """
    Endpoint that handles the JavaScript fetch() submission.
    """
    try:
        # Convert the raw JSON string payload sent by fetch() into a native Python dictionary
        data = request.get_json()




        # I first went to sort out the login info in order to be able to do this.


        
        return

    except Exception as error:
        # Handle unexpected server errors
        return jsonify({'status': 'error', 'message': str(error)}), 500