from flask import Flask, render_template, request, redirect
import mysql.connector
from mysql.connector import Error







#Now what I need to do is to establish a connection with my database and get all the faculties into a list 

'''
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '4492340',
    'database': 'rate_mm'
}
'''

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






print((get_modules("Bachelor of Science in Computer Science")))


#def get_modulu


#I now need to iterate through this list of module_id dictionaries, to get the module name of each id


'''
ProG=[]



for programmes in prog:
        ProG.append(programmes["course_name"])

for programmes in ProG:
        print(programmes)

'''





app = Flask(__name__)


@app.route("/",methods=["GET"])
def index():
    Faculties = getfaculties()
    return render_template("1_index.html",Faculties=Faculties)


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





@app.route('/module')  # or whatever your module endpoint is
def module_page():
    code = request.args.get('code')
    # ...

