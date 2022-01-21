from flask import Flask, request, render_template,  redirect,  session , jsonify
import json
from datetime import datetime
from DBCon import get_db, close_db
from flask_cors import CORS

app = Flask('app')
app.debug = True
app.secret_key = "mysecretkey"
CORS(app)

from Student import views as StudentUrl
from Mentor import views as MentorUrl

# Student Urls
app.add_url_rule('/student/register' , view_func = StudentUrl.Std_register , methods=['GET','POST'])
app.add_url_rule('/student/login' , view_func = StudentUrl.Std_login , methods=['GET','POST'])
app.add_url_rule('/student/create_doubt' , view_func = StudentUrl.Stud_CreateDoubt , methods=['GET','POST'])
app.add_url_rule('/student/request' , view_func = StudentUrl.createMeetRequest , methods=['GET','POST'])
app.add_url_rule('/student/all-live' , view_func = StudentUrl.All_LiveClasses , methods=['GET','POST'])

# Mentor Urls
app.add_url_rule('/mentor/register' , view_func = MentorUrl.Men_register , methods=['GET','POST'])
app.add_url_rule('/mentor/login' , view_func = MentorUrl.Men_login , methods=['GET','POST'])
app.add_url_rule('/mentor/create_class' , view_func = MentorUrl.Men_CreateClass , methods=['GET','POST'])
app.add_url_rule('/mentor/create_blog' , view_func = MentorUrl.Men_CreateBlog , methods=['GET','POST'])
app.add_url_rule('/mentor/expertise' , view_func = MentorUrl.mentorsAvailibityCreate , methods=['GET','POST'])
app.add_url_rule('/mentor/studentreq' , view_func = MentorUrl.mappingStudentReq , methods=['GET','POST'])
app.add_url_rule('/mentor/accept-studentreq' , view_func = MentorUrl.AcceptingStudentReq , methods=['GET','POST'])


@app.route('/blogs', methods=['GET', 'POST'])
def Blogs():  
    if request.method == "GET":
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * from Blogs")
            r = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
            # myresult = cursor.fetchall()
            return json.dumps(r ,indent=4, sort_keys=True, default=str)
        except Exception as e:
            return jsonify({"msg":str(e), "status":"unsuccess"})

@app.route('/doubts', methods=['GET', 'POST'])
def Doubts():  
    if request.method == "GET":
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * from Doubts")
            r = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
            # myresult = cursor.fetchall()
            return json.dumps(r ,indent=4, sort_keys=True, default=str)
        except Exception as e:
            return jsonify({"msg":str(e), "status":"unsuccess"})


   
   


        
# @app.route('/', methods=['GET', 'POST'])
# def Home():  
#    return render_template('base.html')
   

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         try :
#             conn = get_db()
#             cursor = conn.cursor()
#             email = str(request.form['email'])
#             password = str(request.form["password"])
#             mydoc = cursor.execute("SELECT * from USERDETAILS WHERE U_EMAIL = :email AND U_PASSWORD = :password", email=email, password= password)
#             myresult = mydoc.fetchone()
#             cursor.close()
#             if myresult:
#                 session['email'] = str(myresult[1])
#                 session['user_role'] = str(myresult[12])
#                 session['fname'] = str(myresult[4])
#                 if myresult[12].strip() == "P":
#                     # code for passenger
#                     return redirect('/Home')
#                 elif myresult[12].strip() == "A":
#                     # code for admin
#                     return redirect('/admin/Home')
#                 else:
#                     return redirect('/Home')
#             else:
#                 return render_template('login.html', msg='email id or password is not matching')

#         except Exception as e:
#             return render_template('login.html', msg=e)
#     else:
#         return render_template('login.html')


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         try:
#             conn = get_db()
#             cursor = conn.cursor()
#             fname = str(request.form["fname"])
#             mname = str(request.form['mname'])
#             lname = str(request.form["lname"])
#             password = str(request.form["password"])
#             email = str(request.form['email'])
#             phone = str(request.form['phoneNo'])
#             state = str(request.form['state'])
#             district = str(request.form['district'])
#             addrline1 = str(request.form['addrline1'])
#             city = str(request.form['city'])
#             pincode = request.form['pincode']
#             cursor.execute("SELECT * from USERDETAILS WHERE U_EMAIL = :email", email = str(email))
#             if cursor.fetchall():
#                 return render_template("sign.html", msg="Email Already Exist Try Different")
#             else:
#                userdata = dict(U_EMAIL = email, U_PASSWORD = password, U_PHONE = phone, U_F_NAME = fname, U_M_NAME = mname, U_L_NAME = lname, STATE = state, DISTRICT = district, CITY = city, PINCODE = pincode, LINE1 = addrline1, U_ROLE = 'P')
#                cursor.execute('insert into USERDETAILS (U_EMAIL,U_PASSWORD,U_PHONE,U_F_NAME,U_M_NAME,U_L_NAME,STATE,DISTRICT,CITY,PINCODE,LINE1,U_ROLE) values (:U_EMAIL, :U_PASSWORD, :U_PHONE, :U_F_NAME, :U_M_NAME, :U_L_NAME, :STATE, :DISTRICT, :CITY, :PINCODE, :LINE1, :U_ROLE)', userdata)

#                mydoc = cursor.execute("SELECT * from USERDETAILS WHERE U_EMAIL = :email" , email = str(email))
#                myresult = mydoc.fetchone()
#                conn.commit()

#                 # print('Singin User :', myresult)
#                 # session['username'] = str(fname)+" "+str(lname)
#                 # session['email'] = str(email)
#                 # session['user_id'] = myresult[0]
#                 # session['user_role'] = str(myresult[4])
#             cursor.close()
#             # conn.close()
#             return render_template('login.html', msg = 'Successfully Registered')

#         except Exception as e:
#             return render_template('sign.html', msg=e)
#     else:
#         return render_template('sign.html')


# @app.route("/logout", methods=["GET", "POST"])
# def logout():
#     session.clear()
#     return redirect("/")

if __name__ == "__main__":   
    app.run(host='0.0.0.0', port=3000, debug=True ) # localhost
    # app.run(host='192.168.0.106', port=8080 )  #Router
