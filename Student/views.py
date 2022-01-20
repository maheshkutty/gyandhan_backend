# import curses
from unittest import result
from flask import Flask, request, render_template,  redirect,  session , jsonify
import json
from datetime import datetime
from DBCon import *

def Std_register():
    if request.method == "POST":
        try:
            conn = get_db()
            cursor = conn.cursor()
            content = request.json
            # print(content['email'] , content['pass'])
            Stud_name = str(content["name"])
            Stud_class = str(content["class"])
            Stud_address = str(content["address"])
            Stud_score = str(content["score"])
            Stud_phone = str(content["phone"])            
            Stud_email = str(content["email"])
            Stud_pass = str(content["pass"])
            cursor.execute("SELECT * from Students WHERE Stud_email = %s", (Stud_email))
            if cursor.fetchall():
                return jsonify({"msg":"Email Already Exist Try Different" , "status":"unsuccess"})
            else:
            #    userdata = dict(Stud_name = Stud_name , Stud_class = Stud_class , Stud_address = Stud_address , Stud_score = Stud_score , Stud_phone = Stud_phone , Stud_email = Stud_email , Stud_pass = Stud_pass)
                cursor.execute("insert into Students (Stud_name,Stud_class,Stud_address,Stud_score,Stud_phone,Stud_email,Stud_pass) values (%s,%s,%s,%s,%s,%s,%s);", (str(Stud_name),str(Stud_class),str(Stud_address),str(Stud_score),str(Stud_phone),str(Stud_email),str(Stud_pass),))                
                conn.commit()               
                cursor.close()
                return jsonify({"msg":"Successfully registerd", "status":"success"})
        except Exception as e:
            return jsonify({"Msg":str(e)})         
    else:
        return jsonify({"msg":"UnSuccessfully registerd" , "status":"unsuccess"})
        


def Std_login():
    if request.method == "POST":
        try :
            conn = get_db()
            cursor = conn.cursor()
            content = request.json
            print(content)
            Stud_email = str(content["email"])
            Stud_pass = str(content["pass"])

            cursor.execute("SELECT * from Students WHERE Stud_email = %s AND Stud_pass = %s", (Stud_email , Stud_pass))
            myresult = cursor.fetchone()
            # cursor.close()
            if myresult:  
                vals = userdata = dict(id = myresult[0] , dateTime = myresult[1] , name = myresult[2] , claass = myresult[3] , address = myresult[4] , score = myresult[5] , phone = myresult[6] , email = myresult[7])            
                conn.commit()               
                cursor.close()
                return jsonify({"msg":"Successfull Login", "status":"success" , "vals": vals})
               
            else:
                return jsonify({"msg":"Account Does not exists.", "status":"unsuccess"})

        except Exception as e:
            return jsonify({"Msg":str(e)})
  
def Stud_CreateDoubt():
    if request.method == "POST":
        try :
            conn = get_db()
            cursor = conn.cursor()
            content = request.json
            Stud_id = str(content["stdId"])
            d_title = str(content["title"])
            d_contents = str(content["contents"])

            cursor.execute("insert into Doubts (d_title,d_contents,Stud_id) values (%s,%s,%s);", (str(d_title),str(d_contents),str(Stud_id)))
           
            conn.commit()               
            cursor.close()
            return jsonify({"msg":"Successfully doubt created", "status":"success"})

        except Exception as e:
            return jsonify({"msg":str(e), "status":"unsuccess"})

def createMeetRequest():
    if request.method == "POST":
        try:
            conn = get_db()
            cursor = conn.cursor()
            content = request.json
            sid = content["sid"]
            daysOfWeek = content["daysOfWeek"]
            startTime = content["startTime"]
            endTime = content["endTime"]   
            topics = content["topics"] 
            subjects = content["subjects"]
            cursor.execute("insert into Session_Requests (Stud_id,Start_Datetime,status,endtime) values (%s, %s, %s, %s);", (int(sid),str(startTime),0,str(endTime)))
            cursor.execute("SELECT LAST_INSERT_ID()")
            myresult = cursor.fetchone()
            print(myresult)
            for i in daysOfWeek:
                print(i)
                cursor.execute("insert into student_weekdays (weekdays, rid) values (%s, %s); ", (str(i), myresult[0]))
            for i in topics:
                cursor.execute("insert into student_topics (topics, rid) values (%s, %s); ", (str(i), myresult[0]))
            for i in subjects:
                cursor.execute("insert into student_subjects (subjects, rid) values (%s, %s); ", (str(i), myresult[0]))
            conn.commit()               
            cursor.close()
            return jsonify({"msg":"meet request created", "status":"success"})
        except Exception as e:
            print(e)
            return jsonify({"msg":str(e), "status":"unsuccess"})