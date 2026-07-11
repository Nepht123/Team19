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





print(get_programmes(getfaculties_id("Natural Science")[0]["id"]))

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
def Program_modules():  # <--- url_for looks at THIS name right here!
    module = request.args.get("module")

    #Need to create a function that shows all the info regarding the particular module 
    
    return



'''
I need:
    Faculty name
    All programmes in faculty
    '''


