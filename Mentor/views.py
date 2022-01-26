from calendar import c
from flask import Flask, request, render_template,  redirect,  session , jsonify
import json
from datetime import datetime
from DBCon import *
from zoomAPI import *

def Men_register():
    if request.method == "POST":
        try:
            conn = get_db()
            cursor = conn.cursor()
            content = request.json
            
            Men_name = str(content["name"])            
            Men_address = str(content["address"])
            Men_score = str(content["score"])
            Men_phone = str(content["phone"])            
            Men_email = str(content["email"])
            Men_pass = str(content["pass"])
            Men_qual = str(content["qual"])
            # Men_mlink = str(content["mlink"])
            Men_mlink = createMeeting()
            cursor.execute("SELECT * from Mentors WHERE Men_email = %s", (Men_email))

            if cursor.fetchall():
                return jsonify({"msg":"Email Already Exist Try Different", "status":"unsuccess"})
            else:
            #    userdata = dict(Stud_name = Stud_name , Stud_class = Stud_class , Stud_address = Stud_address , Stud_score = Stud_score , Stud_phone = Stud_phone , Stud_email = Stud_email , Stud_pass = Stud_pass)
                cursor.execute("insert into Mentors (Men_name,Men_address,Men_score,Men_phone,Men_email,Men_pass,Men_qual,Men_mlink) values (%s,%s,%s,%s,%s,%s,%s,%s);", (str(Men_name),str(Men_address),str(Men_score),str(Men_phone),str(Men_email),str(Men_pass),str(Men_qual),str(Men_mlink)))

                # mydoc = cursor.execute("SELECT * from Mentors WHERE Men_email = %s" , (Men_email) )
                # myresult = mydoc.fetchone()
                conn.commit()               
                cursor.close()
                return jsonify({"msg":"Successfully registerd", "status":"success"})
                # return render_template('login.html', msg = 'Successfully Registered')

        except Exception as e:
            return jsonify({"msg":str(e), "status":"unsuccess"})
            
    else:
        return jsonify({"msg":"UnSuccessfully registerd", "status":"unsuccess"})
        
def Men_login():
    if request.method == "POST":
        try :
            conn = get_db()
            cursor = conn.cursor()
            content = request.json
            Men_email = str(content["email"])
            Men_pass = str(content["pass"])

            cursor.execute("SELECT * from Mentors WHERE Men_email = %s AND Men_pass = %s", (Men_email , Men_pass))
            myresult = cursor.fetchone()
            cursor.close()
            if myresult:
                vals = userdata = dict(id = myresult[0] , dateTime = myresult[1] , name = myresult[2] , address = myresult[3] , score = myresult[4] , phone = myresult[5] , email = myresult[6] , qual = myresult[8] , mlink = myresult[9])            
                conn.commit()               
                cursor.close()
                return jsonify({"msg":"Successfull Login", "status":"success" , "vals": vals})
               
            else:
                return jsonify({"msg":"Account Does not exists.", "status":"unsuccess"})

        except Exception as e:
            return jsonify({"Msg":str(e), "status":"unsuccess"})

def personalDetails():
    if request.method == "POST":
        try :
            conn = get_db()
            cursor = conn.cursor()
            content = request.json
            mid = content["mid"]
            print(mid)
            cursor.execute("select * from Mentors where Men_id = %s", (int(mid)))
            personalData = cursor.fetchone()
            print(personalData)
            res = {"paDetails":{}, "subjects":[], "weekdays":[]}
            if personalData == None:
                return jsonify(res)
            res["paDetails"]["name"] = personalData[2]
            res["paDetails"]["add"] = personalData[3]
            res["paDetails"]["phone"] = personalData[5]
            res["paDetails"]["email"] = personalData[6]
            cursor.execute("select * from mentors_subjects where mid = %s", (int(mid)))
            subjectsDetails = cursor.fetchall()
            if subjectsDetails != None:
                res["subjects"] = [i[2] for i in subjectsDetails]
            cursor.execute("select * from mentors_weekdays where mid = %s", (int(mid)))
            weekDaysAvail = cursor.fetchall()
            if weekDaysAvail != None:
                res["weekdays"] = [i[2] for i in weekDaysAvail]
            return jsonify(res)
        except Exception as e:
            print(e)
            return jsonify({"Msg":str(e), "status":"unsuccess"})

def Men_CreateClass():
    if request.method == "POST":
        try :
            conn = get_db()
            cursor = conn.cursor()
            content = request.json
            Men_id = str(content["Men_id"])
            Class_title = str(content["Class_title"])
            Start_dateTime = str(content["Start_dateTime"])
            End_dateTime = str(content["End_dateTime"])
            flag = ClassValidTime( Start_dateTime , End_dateTime )
            if flag[0] :
                cursor.execute("insert into Classes (Men_id , Start_dateTime , End_dateTime , Class_title ) values (%s,%s,%s,%s);", (str(Men_id) , Start_dateTime , End_dateTime , Class_title))
                conn.commit()               
                cursor.close()
                return jsonify({"msg":"Successfully Class created", "status":"success"})

            else:
                return jsonify({"msg":"Class creation timings were not valid.", "status":"Unsuccess"})
        
        except Exception as e:
            return jsonify({"msg":str(e), "status":"unsuccess"})

def Men_CreateBlog():
    if request.method == "POST":
        try :
            conn = get_db()
            cursor = conn.cursor()
            content = request.json
            Men_id = str(content["mentorId"])
            b_title = str(content["title"])
            b_contents = str(content["contents"])

            cursor.execute("insert into Blogs (b_title,b_contents,Men_id) values (%s,%s,%s);", (str(b_title),str(b_contents),str(Men_id)))
           
            conn.commit()               
            cursor.close()
            return jsonify({"msg":"Successfully Blog created", "status":"success"})

        except Exception as e:
            return jsonify({"msg":str(e), "status":"unsuccess"})

def mentorsAvailibityCreate():
    if request.method == "POST":
        try :
            conn = get_db()
            cursor = conn.cursor()    
            content = request.json
            mid = content["mid"]
            daysOfWeek = content["daysOfWeek"]
            startTime = content["startTime"]
            endTime = content["endTime"]   
            subjects = content["subjects"]
            cursor.execute("delete from mentors_subjects where mid = %s", ((int(mid))))
            cursor.execute("delete from mentors_weekdays where mid = %s", ((int(mid))))
            cursor.execute("update Mentors set starttime = %s, endtime = %s where Men_id = %s;", (str(startTime),str(endTime), int(mid)))
            for i in subjects:
                cursor.execute("insert into mentors_subjects (subjects, mid) values (%s, %s); ", (str(i), int(mid)))
            for i in daysOfWeek:
                cursor.execute("insert into mentors_weekdays (weekdays, mid) values (%s, %s); ", (str(i), int(mid)))
            conn.commit()               
            cursor.close()
            return jsonify({"msg":"Mentors Availibility recorded", "status":"success"})
        except Exception as e:
            print(e)
            return jsonify({"msg":str(e), "status":"unsuccess"})

def mappingStudentReq():
    if request.method == "POST":
        try:
            conn = get_db()
            cursor = conn.cursor()    
            content = request.json
            mid = content["mid"]
            sql = "select * from (select sr.id as sessid, Stud_id, Start_Datetime, endtime, weekdays, subjects, status from Session_Requests sr, student_weekdays sw, student_subjects ss where sr.id = sw.rid and sr.id = sw.rid) as d, (select Men_id, starttime, endtime, weekdays, subjects from Mentors m, mentors_subjects ms, mentors_weekdays mw where m.Men_id = ms.mid and m.Men_id  = mw.mid and m.Men_id = %s) as f where d.Start_Datetime = f.starttime and d.weekdays = f.weekdays and d.subjects = f.subjects and status = 0 group by sessid;"
            cursor.execute(sql, (int(mid)))
            myresult = cursor.fetchall()
            allSessionRequest = []
            for id in myresult:
                cursor.execute("select * from Session_Requests sr where sr.status = 0 and sr.id = %s", (int(id[0])))
                sessionResult = cursor.fetchall()
                for item in sessionResult:
                    individualReq = {}
                    individualReq["startTime"] = item[2]
                    individualReq["endTime"] = item[6]
                    individualReq["rid"] = item[0]
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
                print(myresult)
            cursor.close()
            return jsonify({"pendingReq":allSessionRequest, "status":"success"})
        except Exception as e:
            print(e)
            return jsonify({"msg":str(e), "status":"unsuccess"})


def AcceptingStudentReq():
    if request.method == "POST":
        try:
            conn = get_db()
            cursor = conn.cursor()    
            content = request.json
            print(content)
            Stud_id = content["sid"]
            mid = content["mid"]
            rid = content["rid"]
            sdate = str(content["sdate"])
            sql = 'UPDATE Session_Requests SET status = 1 , Men_id = %s, sdate = STR_TO_DATE("%s", \"%s\") WHERE id = %s'
            sql = sql % ((int(mid), str(sdate), str("%d-%m-%Y"), int(rid)))
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            return jsonify({"msg":"Session Confirmed", "status":"success"})
        except Exception as e:
            print(e)
            return jsonify({"msg":str(e), "status":"unsuccess"})

def showConfirmedMeet():
    if request.method == "POST":
        try:
            conn = get_db()
            cursor = conn.cursor()    
            content = request.json
            mid = content["mid"]
            print(mid)
            sql = "select sr.*,  DATE_FORMAT(sr.sdate, \"%s\") as strdate from Session_Requests sr where sr.Men_id = %d and sdate >= CURRENT_DATE()"
            sql = sql % (str("%d-%m-%Y"),int(mid))
            cursor.execute(sql)
            confirmReq = cursor.fetchall()
            print(confirmReq)
            allSessionRequest = []
            for item in confirmReq:
                individualReq = {}
                individualReq["startTime"] = item[2]
                individualReq["endTime"] = item[6]
                individualReq["rid"] = item[0]
                individualReq["sdate"] = str(item[8])
                cursor.execute("select Men_mlink from Mentors where Men_id = %s", (int(item[5])))
                meetLink = cursor.fetchone()
                print(meetLink)
                if meetLink[0] != "":
                    meetLink = eval(meetLink[0])
                    meetLink = meetLink[0]
                else:
                    meetLink = ""
                individualReq["meetlink"] = meetLink
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
            return jsonify({"confirmedReq":allSessionRequest, "status":"success"})              
        except Exception as e:    
            print(e)
            return jsonify({"msg":str(e), "status":"unsuccess"})

def Create_ClassAssignment():
    if request.method == "POST":
        try :
            conn = get_db()
            cursor = conn.cursor()
            content = request.json
            Men_id = str(content["Men_id"])
            Class_id = str(content["Class_id"])
            A_Title = str(content["A_Title"])
            Content = str(content["content"])
            cursor.execute("insert into Assignments (Men_id , Class_id , Content , A_Title ) values (%s,%s,%s,%s);", (str(Men_id) , Class_id , Content , A_Title))
            conn.commit()               
            cursor.close()
            return jsonify({"msg":"Successfully Class Assignment created", "status":"success"})
    
        except Exception as e:
            return jsonify({"msg":str(e), "status":"unsuccess"})

def showClasses():
    if request.method == "POST":
        try:
            conn = get_db()
            cursor = conn.cursor()
            content = request.json
            cursor.execute("select Men_mlink from Mentors where Men_id = %s", (int(content["mid"])))
            meetLink = cursor.fetchone()
            print(meetLink)
            if meetLink[0] != "":
                meetLink = eval(meetLink[0])
                meetLink = meetLink[0]
            else:
                meetLink = ""
            cursor.execute("select * from Classes where Men_id = %s" % (int(content["mid"])))
            res = cursor.fetchall()
            allClasses = []
            for item in res:
                individualClass = {}
                individualClass["startTime"] = item[1]
                individualClass["endTime"] = item[2]
                individualClass["title"] = item[7]
                individualClass["meetLink"] = meetLink
                allClasses.append(individualClass)
            cursor.close()
            return jsonify({"allClasses":allClasses, "status":"success"})
        except Exception as e:
            return jsonify({"msg":str(e), "status":"unsuccess"})