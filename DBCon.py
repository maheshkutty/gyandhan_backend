from pickle import FALSE, TRUE
import pymysql
import config
from flask import g
from datetime import datetime 

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(host=config.MYSQL_HOST,
        port=config.MYSQL_PORT,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        db=config.MYSQL_DB
        )
        print("Connection established")
    return g.db
    
def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()    

def validDate( startDate , endDate ):

    st_d = datetime.strptime( startDate ,  '%Y-%m-%dT%H:%M' )
    en_d = datetime.strptime( endDate ,  '%Y-%m-%dT%H:%M' )
    # 2022-01-22T01:00  2022-01-22T03:00
    # print("StartDate : ", st_d , type(st_d))
    # print("EndDate : ", en_d , type(en_d) )
    duration  = en_d - st_d
    now  = datetime.now()
    print("Now : ", now , type(now) )
    # print(  duration , type(duration))
    # print(  duration.days  , duration.seconds)

    if( st_d < now and en_d > now ):
        # if( en_d > now ):
        print("valid")
        return [ 1 , duration ]
        # else:
        #     print("Not Valid")
        #     return [False , 'In Valid timings']
    else:
        print("Not Valid")
        return [ 0 , 'In Valid timings']

def ClassValidTime( startDate , endDate ):

    st_d = datetime.strptime( startDate ,  '%Y-%m-%dT%H:%M' )
    en_d = datetime.strptime( endDate ,  '%Y-%m-%dT%H:%M' )
   
    duration  = en_d - st_d
    now  = datetime.now()
    print("Now : ", now , type(now) )
  
    if( st_d > now ):
        if( en_d > st_d ):
            print("valid")
            return [ 1 , duration ]
    else:
        print("Not Valid")
        return [0 , 'In Valid timings']