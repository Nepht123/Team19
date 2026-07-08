from flask import Flask, render_template, request, redirect
import mysql.connector
from mysql.connector import Error





{Now I need to update the faculty buttons at the bottom of the screen}


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





def get_modules(faculty_id):
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

        get_query="SELECT * FROM modules WHERE faculty_code = %s"
        mycursor.execute(get_query)
        all_modules = mycursor.fetchall()

        return all_modules



    except Error as error:
        print(f" Database Error encountered: {error}")
        return None


    finally:
        # 4. ENVIRONMENT CLEANUP
        if mydatabase and mydatabase.is_connected():
            mycursor.close()
            mydatabase.close()
            print("MySQL database connection securely closed.")








app = Flask(__name__)


@app.route("/",methods=["GET"])
def index():
    Faculties = getfaculties()
    return render_template("1_index.html",Faculties=Faculties)


@app.route("/program",methods=["GET"])
def by_program():
    #Here I am just capturing the selected faculty id
    faculty_id = request.args.get('faculty')

    #Here I am getting all of the modules under that faculty
    filtered_modules = get_modules(request.args.get('faculty'))
    return render_template("by_program.html", faculty=faculty_id)
    '''I must make changes to by_program.html'''