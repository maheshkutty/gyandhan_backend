# import curses
from calendar import weekday
from operator import sub
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

def showPendingMeetReq():
    if request.method == "POST":
        try:
            req = request.json
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("select * from Session_Requests sr where sr.status = 0 and sr.Stud_id = %s", (int(req["sid"])))
            sessionResult = cursor.fetchall()
            allSessionRequest = []
            for item in sessionResult:
                individualReq = {}
                individualReq["startTime"] = item[2]
                individualReq["endTime"] = item[6]
                individualReq["sid"] = item[0]
                cursor.execute("select * from student_subjects where rid = %s", (int(item[0])))
                subjects = cursor.fetchall()
                individualReq["subjects"] = [item[1] for item in subjects]
                cursor.execute("select * from student_weekdays where rid = %s", (int(item[0])))
                weekdays = cursor.fetchall()
                individualReq["weekdays"] = [item[1] for item in weekdays]
                cursor.execute("select * from student_topics where rid = %s", (int(item[0])))
                topics = cursor.fetchall()
                individualReq["topics"] = [item[1] for item in topics]
                allSessionRequest.append(individualReq)
            cursor.close()
            res = {"pendingReq":allSessionRequest}
            return res
        except Exception as e:
            print(e)
            return jsonify({"msg":str(e), "status":"unsuccess"})
                

def showConfirmedRequest():
    if request.method == "POST":
        try:
            req = request.json
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("select * from Session_Requests sr where sr.status = 1 and sr.Stud_id = %s", (int(req["sid"])))
            sessionResult = cursor.fetchall()
            allSessionRequest = []
            for item in sessionResult:
                individualReq = {}
                individualReq["startTime"] = item[2]
                individualReq["endTime"] = item[6]
                individualReq["sid"] = item[0]
                meetLink = cursor.execute("select Men_mlink from Mentors where Men_id = %s", (int(item[5])))
                individualReq["meetLink"] = meetLink[0]
                cursor.execute("select * from student_subjects where rid = %s", (int(item[0])))
                subjects = cursor.fetchall()
                individualReq["subjects"] = [item[1] for item in subjects]
                cursor.execute("select * from student_weekdays where rid = %s", (int(item[0])))
                weekdays = cursor.fetchall()
                individualReq["weekdays"] = [item[1] for item in weekdays]
                cursor.execute("select * from student_topics where rid = %s", (int(item[0])))
                topics = cursor.fetchall()
                individualReq["topics"] = [item[1] for item in topics]
                allSessionRequest.append(individualReq)
            cursor.close()
            res = {"confiremdReq":allSessionRequest}
            return res
        except Exception as e:
            print(e)
            return jsonify({"msg":str(e), "status":"unsuccess"})

def All_LiveClasses():
    if request.method == "GET":
        try:
            conn = get_db()
            cursor = conn.cursor()
            # content = request.json
            cursor.execute("SELECT * from Classes")
            r = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
            # myresult = cursor.fetchall()
            op = []
            for cls in r:                
                flag = validDate( cls["Start_dateTime"] , cls["End_dateTime"]) 
                
                if flag[0]:
                    op.append(cls)
                    # print("===================",cls["Start_dateTime"]) 
            return json.dumps(op ,indent=4, sort_keys=True, default=str)


        except Exception as e:
            print(e)
            return jsonify({"msg":str(e), "status":"unsuccess"})
