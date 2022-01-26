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
app.add_url_rule('/student/askmeet' , view_func = StudentUrl.createMeetRequest , methods=['GET','POST'])
app.add_url_rule('/student/all-live' , view_func = StudentUrl.All_LiveClasses , methods=['GET','POST'])
app.add_url_rule('/student/showpendingmeet' , view_func = StudentUrl.showPendingMeetReq , methods=['GET','POST'])
app.add_url_rule('/student/showconfirmedmeet' , view_func = StudentUrl.showConfirmedRequest , methods=['GET','POST'])
app.add_url_rule('/student/details' ,view_func = StudentUrl.studPersonalDetails , methods=['GET','POST'])

# Mentor Urls
app.add_url_rule('/mentor/register' , view_func = MentorUrl.Men_register , methods=['GET','POST'])
app.add_url_rule('/mentor/login' , view_func = MentorUrl.Men_login , methods=['GET','POST'])
app.add_url_rule('/mentor/details', view_func = MentorUrl.personalDetails , methods=['GET','POST'])
app.add_url_rule('/mentor/create_class' , view_func = MentorUrl.Men_CreateClass , methods=['GET','POST'])
app.add_url_rule('/mentor/create_blog' , view_func = MentorUrl.Men_CreateBlog , methods=['GET','POST'])
app.add_url_rule('/mentor/expertise' , view_func = MentorUrl.mentorsAvailibityCreate , methods=['GET','POST'])
app.add_url_rule('/mentor/studentreq' , view_func = MentorUrl.mappingStudentReq , methods=['GET','POST'])
app.add_url_rule('/mentor/accept-studentreq' , view_func = MentorUrl.AcceptingStudentReq , methods=['GET','POST'])
app.add_url_rule('/mentor/showconfirmedmeet' , view_func = MentorUrl.showConfirmedMeet , methods=['GET','POST'])


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

@app.route('/blogs/comment', methods=['GET', 'POST'])
def BlogsComments():  
    if request.method == "GET":
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * from Blog_review")
            r = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
            # myresult = cursor.fetchall()
            return json.dumps(r ,indent=4, sort_keys=True, default=str)
        except Exception as e:
            return jsonify({"msg":str(e), "status":"unsuccess"})

    elif request.method == "POST":
            try:
                conn = get_db()
                cursor = conn.cursor()
                content = request.json
                
                b_id = str(content["b_id"])
                Stud_id = str(content["Stud_id"])
                Men_id = str(content["Men_id"])
                comment = str(content["comment"])

                print(  Stud_id)
                print( Men_id )

                if (Stud_id == "None"):
                    cursor.execute("insert into Blog_review (b_id,Men_id,comment) values (%s,%s,%s);", (int(b_id),int(Men_id),str(comment)))                
                else:
                    cursor.execute("insert into Blog_review (b_id,Stud_id,comment) values (%s,%s,%s);", (int(b_id),int(Stud_id),str(comment)))                

                conn.commit()               
                cursor.close()
                return jsonify({ "status":"success"})
                
            except Exception as e:
                return jsonify({"msg":str(e), "status":"unsuccess"})


@app.route('/blogs/like', methods=['GET', 'POST'])
def BlogsLike():  
    if request.method == "POST":
        try:
            conn = get_db()
            cursor = conn.cursor()
            content = request.json            
            b_id = int(content["b_id"])
            action = str(content["action"])
            cursor.execute("SELECT * from Blogs WHERE b_id = %s", (b_id))
            res = cursor.fetchone()

            res = dict((cursor.description[i][0], value) \
               for i, value in enumerate(res)) 

            print("============",res)
            if action == "like" :
                sql = "UPDATE Blogs SET b_likes = %s  WHERE b_id = %s" 
                cursor.execute(sql, (int(res["b_likes"] + 1) , int(b_id)))

            else:
                sql = "UPDATE Blogs SET b_dislikes = %s  WHERE b_id = %s" 
                cursor.execute(sql, (int(res["b_dislikes"] + 1) , int(b_id)))
           
            conn.commit()
            cursor.close()
            return jsonify({ "status":"success"})
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


@app.route('/doubts/comment', methods=['GET', 'POST'])
def DoubtsComments():  
    if request.method == "GET":
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * from Doubt_review")
            r = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
            # myresult = cursor.fetchall()
            return json.dumps(r ,indent=4, sort_keys=True, default=str)
        except Exception as e:
            return jsonify({"msg":str(e), "status":"unsuccess"})

    elif request.method == "POST":
            try:
                conn = get_db()
                cursor = conn.cursor()
                content = request.json
                
                dt_id = str(content["dt_id"])
                Stud_id = str(content["Stud_id"])
                Men_id = str(content["Men_id"])
                comment = str(content["comment"])

                print(  Stud_id)
                print( Men_id )

                if (Stud_id == "None"):
                    cursor.execute("insert into Doubt_review (dt_id,Men_id,comment) values (%s,%s,%s);", (int(dt_id),int(Men_id),str(comment)))                
                else:
                    cursor.execute("insert into Doubt_review (dt_id,Stud_id,comment) values (%s,%s,%s);", (int(dt_id),int(Stud_id),str(comment)))                

                conn.commit()               
                cursor.close()
                return jsonify({ "status":"success"})
                
            except Exception as e:
                return jsonify({"msg":str(e), "status":"unsuccess"})

@app.route('/doubts/like', methods=['GET', 'POST'])
def DoubtsLike():  
    if request.method == "POST":
        try:
            conn = get_db()
            cursor = conn.cursor()
            content = request.json            
            dt_id = int(content["dt_id"])
            action = str(content["action"])
            cursor.execute("SELECT * from Doubts WHERE dt_id = %s", (dt_id))
            res = cursor.fetchone()

            res = dict((cursor.description[i][0], value) \
               for i, value in enumerate(res)) 

            print("============",res)
            if action == "like" :
                sql = "UPDATE Doubts SET b_likes = %s  WHERE dt_id = %s" 
                cursor.execute(sql, (int(res["b_likes"] + 1) , int(dt_id)))

            else:
                sql = "UPDATE Doubts SET d_dislikes = %s  WHERE dt_id = %s" 
                cursor.execute(sql, (int(res["d_dislikes"] + 1) , int(dt_id)))
           
            conn.commit()
            cursor.close()
            return jsonify({ "status":"success"})
        except Exception as e:
            return jsonify({"msg":str(e), "status":"unsuccess"})


 

if __name__ == "__main__":   
    app.run(host='0.0.0.0', port=3000, debug=True ) # localhost
    # app.run(host='192.168.0.106', port=8080 )  #Router
