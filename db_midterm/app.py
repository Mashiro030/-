from flask import Flask,request,Response,redirect,render_template,request,url_for,session,flash,Blueprint, redirect
from flask_bootstrap import Bootstrap
from datetime import datetime,timedelta
from flask_mail import Mail,Message
from threading import Thread
# import cx_Oracle
# ========== for sqlite ==========
import sqlite3

from flask import g, current_app

DATABASE = './db.sqlite'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def parse_column_headers(res):
    return [r[0] for r in res.description]
# ========== for sqlite ==========

app=Flask(__name__) # 透過__name__確定app檔案位置，方便找到其他構成app的檔案
app.secret_key='hello' # session的key可隨意設定字串 
app.permanent_session_lifetime=timedelta(minutes=100) #設定session能夠被儲存在server上的時間

# conn=cx_Oracle.connect("Group6/Group666@140.117.69.58:1521/Group6",encoding="UTF-8")
# conn=cx_Oracle.connect('Group6', 'Group666', "140.117.69.58:1521/Group6",encoding="UTF-8")

# tns=cx_Oracle.makedsn('140.117.69.58',1521,'orcl')
# conn=cx_Oracle.connect('Group6','Group666',tns)
# conn = cx_Oracle.connect('Group6/Group666@140.117.69.58/Group6')

# ========== for sqlite ==========
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
# ========== for sqlite ==========

app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']='testcodepython1126@gmail.com'
app.config['MAIL_PASSWORD']='bhjagzxcrusbkdos'
mail=Mail(app) # 初始化flask-mail

def gen_search_flight(start_date, end_date, start, arrive):
    search_flight = 'SELECT * FROM FLIGHT'
    if start_date or end_date or start or arrive:
        search_flight += ' WHERE '
        where_query = []
        if start_date:
            where_query.append(''' datetime(departure_time) >= datetime('%s') '''.format(start_date))
        if end_date:
            where_query.append(''' datetime(departure_time) <= datetime('%s') '''.format(end_date))
        
        if start or arrive:
            in_query = 'FLIGHT_NUMBER IN ( SELECT FLIGHT_NUMBER FROM FLIGHT WHERE'
            loc_query = []
            if start:
                loc_query.append(''' DEPARTURE_AIRPORT LIKE '%{}%'  '''.format(start))
            if arrive:
                loc_query.append(''' ARRIVAL_AIRPORT LIKE '%{}%'  '''.format(arrive))
            
            in_query += ' AND '.join(loc_query)
            in_query += ')'

            where_query.append(in_query)
        search_flight += ' AND '.join(where_query)
    return search_flight

@app.route('/',methods=['POST','GET'])
def search():
    conn = get_db() # sqlite conn
    if request.method == 'POST':
        start=request.form['departure']
        arrive=request.form['destination']
        start_date=request.form['start_date']
        end_date=request.form['end_date']
        passenger_num=request.form['passenger_num']
        # if start and arrive and start_date and end_date and passenger_num:
        if True:
            cursor=conn.cursor()
            # search_flight='''
            # SELECT * FROM FLIGHT
            # WHERE TO_DATE(DEPARTURE_DATE,'YYYY-MM-DD HH24-MI') >= TO_DATE('%s','YYYY-MM-DD HH24-MI')
            # AND TO_DATE(DEPARTURE_DATE,'YYYY-MM-DD HH24-MI') <= TO_DATE('%s','YYYY-MM-DD HH24-MI')
            # AND FLIGHT_NUMBER IN (
            #     SELECT FLIGHT_NUMBER FROM FLIGHT
            #     WHERE DEPARTURE_AIRPORT LIKE '%%%s%%' 
            #     AND ARRIVAL_AIRPORT LIKE '%%%s%%'
            # )''' % (start_date,end_date,start,arrive)

            # search_flight='''
            # SELECT * FROM FLIGHT
            # WHERE datetime(departure_time) >= datetime('%s')
            # AND datetime(departure_time) <= datetime('%s')
            # AND FLIGHT_NUMBER IN (
            #     SELECT FLIGHT_NUMBER FROM FLIGHT
            #     WHERE DEPARTURE_AIRPORT LIKE '%%%s%%'  
            #     AND ARRIVAL_AIRPORT LIKE '%%%s%%'
            # )''' % (start_date,end_date,start,arrive)

            
            search_flight = gen_search_flight(start_date, end_date, start, arrive)

            
            # search_flight=''' SELECT * FROM FLIGHT WHERE DEPARTURE_AIRPORT LIKE '%%%s%%' 
            # AND ARRIVAL_AIRPORT LIKE '%%%s%%' ''' % (start,arrive)
            res = cursor.execute(search_flight)
            test=cursor.fetchall()
            # print('test', test)
            cursor.close()

            cols = parse_column_headers(res)
            test = [dict(zip(cols, t)) for t in test]
            print('test', test)


            if test:
                return render_template('homepage.html',test=test)
                # AND ARRIVAL_AIRPORT LIKE '%%%s%%' DEPARTURE_DATE LIKE '%%%s%%' AND END_DATE LIKE '%%%s%%' ,arrive,start_date,end_date
    return render_template('homepage.html')

@app.route('/login',methods=['POST','GET'])
def login():
    conn = get_db() # sqlite conn
    if request.method=='POST':
        email=request.form['email']
        pwd=request.form['pwd'] # 抓取form.html中input text的值
        if email and pwd: # 輸入欄位不可為空
            cursor=conn.cursor()
            check_user_db='''
                SELECT * FROM USER_INFO LEFT JOIN MANAGER ON USER_INFO.User_id = MANAGER.User_id
                WHERE EMAIL='%s' AND PASSWORD='%s'
            ''' % (email,pwd)
            res = cursor.execute(check_user_db)
            test=cursor.fetchall()
            print('test', test)
            cursor.close()
            if test:
                success_notify='用戶登入成功'
                session['user_email']=email # 運用session存值，代表該用戶確實存在於資料庫中
                session['user_pwd']=pwd

                cols = parse_column_headers(res)
                test_dict = dict(zip(cols, test[0]))
                print('dict', test_dict)

                # {'User_id': 1, 'USERNAME': 'dragon', 'EMAIL': 'ddd@gmail.com', 'PASSWORD': 'dragon123', 'PASSPORT': 'dragon123', 'PERMISSION': 10}
                
                if test_dict.get('PERMISSION', None):
                    session['manager_email'] = email # 運用session存值，代表該用戶確實存在於資料庫中
                    session['manager_pwd'] = pwd

                return render_template('login.html',success_notify=success_notify,failed_notify=None,test=test)
            else:
                failed_notify='查無此用戶資訊，請先註冊帳號'
                return render_template('login.html',success_notify=None,failed_notify=failed_notify,test=test)
    return render_template('login.html')

@app.route('/logout') # 清除session
def logout():
    session.pop('user_email',None)
    session.pop('user_pwd',None)
    session.pop('manager_email',None)
    session.pop('manager_pwd',None)
    return redirect(url_for('search')) # 清除完session導回登入頁面

@app.route('/flight')
def info():
    conn = get_db() # sqlite conn
    sess_user_email=session.get('user_email')
    sess_user_pwd=session.get('user_pwd')
    if sess_user_email and sess_user_pwd:
        cursor=conn.cursor()
        search_flight=''' SELECT * FROM FLIGHT '''
        cursor.execute(search_flight)
        result=cursor.fetchall()
        cursor.close()
        return render_template('flight_info.html',result=result)
    else:
        failed_notify='請先登入再做查詢'
        return render_template('login.html',failed_notify=failed_notify)

@app.route('/register',methods=['POST','GET'])
def regist():
    conn = get_db() # sqlite conn
    if request.method=='POST':
        cursor=conn.cursor()
        name=request.form['name']
        email=request.form['email']
        pwd=request.form['pwd']
        passport=request.form['passport']
        if name and email and passport:
            check_user=''' SELECT * FROM USER_INFO WHERE EMAIL='%s' and PASSPORT='%s' ''' % (email,passport)
            cursor.execute(check_user)
            result=cursor.fetchall()
            if result:
                failed_notify='此email已使用過，請重新註冊帳號'
                return render_template('regist.html',success_notify=None,failed_notify=failed_notify)
                
            else:
                insert_user=''' INSERT INTO USER_INFO (USERNAME,EMAIL,PASSWORD,PASSPORT) VALUES ('%s','%s','%s','%s') ''' % (name,email,pwd,passport)
                cursor.execute(insert_user)
                # cursor.close()
                conn.commit()

                success_notify='註冊成功，請前往信箱完成註冊驗證'
                session['user_name']=name # 運用session存值，代表該用戶確實存在於資料庫中
                session['user_email']=email
                msg_title='訂票系統用戶註冊'+' To: '+ name # 主旨
                msg_sender='testcodepython1126@gmail.com' # 寄件者
                msg_receiver=[email] # 收件者格式為list，否則報錯
                msg_content=f'{name} 恭喜您完成註冊!' # 郵件內容
                msg=Message(msg_title,sender=msg_sender,recipients=msg_receiver)
                msg.body=msg_content
                # mail.send(msg) 
                def send_async_email(app,msg): # 使用多線程寄信時減少卡頓loading time 
                    with app.app_context(): # with開啟時只有在這個with的範圍可以使用，離開這個範圍時自動關閉，回收相關的資源
                        mail.send(msg)
                # app_context詳細解說:https://www.jianshu.com/p/4548516ca896
                thr=Thread(target=send_async_email,args=[app, msg]) 
                thr.start()
                return render_template('regist.html',success_notify=success_notify,failed_notify=None)
                
    return render_template('regist.html')

@app.route('/manager',methods=['POST','GET'])
def manager_login():
    conn = get_db() # sqlite conn
    if request.method=='POST':
        email=request.form['email'] # 抓取form.html中input text的值
        pwd=request.form['pwd'] 
        if email and pwd: # 輸入欄位不可為空
            cursor=conn.cursor()
            check_manager_db = '''
                SELECT * FROM MANAGER NATURAL JOIN USER_INFO WHERE EMAIL='%s' AND PASSWORD='%s'
            ''' % (email, pwd)
            cursor.execute(check_manager_db)
            test=cursor.fetchall()
            cursor.close()
            if test:
                success_notify='管理員登入成功'
                session['manager_email']=email # 運用session存值，代表該用戶確實存在於資料庫中
                session['manager_pwd']=pwd
                return render_template('manager_login.html',success_notify=success_notify,failed_notify=None)
            else:
                failed_notify='查無此管理員資訊，權限不足'
                return render_template('manager_login.html',success_notify=None,failed_notify=failed_notify)
    return render_template('manager_login.html')

@app.route('/manager_login/manager_edit',methods=['POST','GET'])
def manager_edit():
    conn = get_db() # sqlite conn
    sess_manager_email=session.get('manager_email')
    sess_manager_pwd=session.get('manager_pwd')
    if sess_manager_email and sess_manager_pwd:
        if request.method == 'POST':
            start=request.form['departure']
            arrive=request.form['destination']
            start_date=request.form['start_date']
            end_date=request.form['end_date']

            flight_no=request.form['flight_no']
            edit_company=request.form['edit_company']
            edit_start_date=request.form['edit_start_date']
            edit_end_date=request.form['edit_end_date']
            edit_start=request.form['edit_start']
            edit_end=request.form['edit_end']
            price=request.form['price']

            # check_flight=''' select count(*) from FLIGHT where exists (SELECT * FROM FLIGHT where FLIGHT_NUMBER='%s') ''' % (flight_no)
            # check_flight_no=''' SELECT COUNT(*) FROM FLIGHT WHERE FLIGHT_NUMBER='%s' AND ROWNUM = 1 '''  % (str(flight_no))
            # cursor=conn.cursor()
            # cursor.execute(check_flight_no)
            # check=cursor.fetchall()
            # temp=check[0][0]

            if flight_no and edit_company=='':
                cursor=conn.cursor()
                delete_flight=''' DELETE FROM FLIGHT WHERE FLIGHT_NUMBER='%s' ''' % (flight_no)
                cursor.execute(delete_flight)
                conn.commit()
                cursor.close()
                return render_template('manager_edit.html')
            if flight_no and edit_company and edit_start_date and edit_end_date and edit_start and edit_end and price:
                flight_no=request.form['flight_no']
                check_flight_no=''' SELECT COUNT(*) FROM FLIGHT WHERE FLIGHT_NUMBER='%s' AND ROWNUM = 1 '''  % str(flight_no)
                cursor=conn.cursor()
                cursor.execute(check_flight_no)
                check=cursor.fetchall()
                if check[0][0]==1:
                    cursor=conn.cursor()              
                    update_flight=''' UPDATE FLIGHT SET COMPANY='%s',DEPARTURE_DATE='%s',ARRIVAL_DATE='%s',DEPARTURE_AIRPORT='%s',ARRIVAL_AIRPORT='%s',PRICE='%s' WHERE FLIGHT_NUMBER='%s' ''' % (edit_company,edit_start_date,edit_end_date,edit_start,edit_end,price,flight_no)
                    cursor.execute(update_flight)
                    conn.commit()
                    return render_template('manager_edit.html')
                # if flight_no and edit_company and edit_start_date and edit_end_date and edit_start and edit_end and price and check[0][0]==0:
                if check[0][0]==0:   
                    cursor=conn.cursor()
                    insert_flight=''' INSERT INTO FLIGHT(COMPANY,FLIGHT_NUMBER,DEPARTURE_DATE,DEPARTURE_AIRPORT,ARRIVAL_DATE,ARRIVAL_AIRPORT,PRICE) VALUES('%s','%s','%s','%s','%s','%s','%s') ''' % (edit_company,flight_no,edit_start_date,edit_start,edit_end_date,edit_end,price)
                    cursor.execute(insert_flight)
                    conn.commit()
                    return render_template('manager_edit.html')
            # if start or arrive or start_date or end_date:
            else:
                cursor=conn.cursor()
                search_flight = gen_search_flight(start_date, end_date, start,arrive)
                res = cursor.execute(search_flight)
                test=cursor.fetchall()
                cursor.close()

                cols = parse_column_headers(res)
                test = [dict(zip(cols, t)) for t in test]

                if test:
                    return render_template('manager_edit.html',test=test)
                
    else:
        failed_notify='請先登入管理員'
        return render_template('manager_login.html',failed_notify=failed_notify)
    return render_template('manager_edit.html')

@app.route('/boardingpass',methods=['POST','GET'])
def boarding_pass():
    conn = get_db() # sqlite conn
    if request.method == 'POST':
        time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        pid=request.form['check_in']
        query=''' SELECT * FROM BOARDINGPASS WHERE PID='%s' ''' % (pid)
        cursor=conn.cursor()
        cursor.execute(query)
        test=cursor.fetchall()
        cursor.close()
        if test:
            return render_template('boarding_pass.html',test=test,time=time)
    return render_template('boarding_pass.html')
    


@app.route('/login/booking',methods=['POST','GET'])
def booking():
    conn = get_db() # sqlite conn
    sess_user_email=session.get('user_email')
    sess_user_pwd=session.get('user_pwd')
    if sess_user_email and sess_user_pwd:
        if request.method == 'POST':
            first_name=request.form['first_name']
            last_name=request.form['last_name']
            birthdate=request.form['birthdate']
            passport=request.form['passport']
            nationality=request.form['nationality']
            exp_date=request.form['exp_date']
            sex=request.form.get('sex')
            flight_number=request.form['flight_number']
            amount=request.form.get('amount')
            p_class=request.form.get('class')
            ticket_type=request.form.get('ticket_type')
            time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            check_flight_no=''' SELECT * FROM FLIGHT WHERE FLIGHT_NUMBER='%s' ''' % (str(flight_number))
            cursor=conn.cursor()
            cursor.execute(check_flight_no)
            check=cursor.fetchall()

            get_user_id=''' SELECT USER_ID FROM USER_INFO WHERE EMAIL='%s' ''' % (sess_user_email)
            cursor.execute(get_user_id)
            temp_uid=cursor.fetchall()

            # get_pid=''' SELECT PID FROM BOOKING WHERE USER_ID='%s' ''' % (temp_uid[0][0])
            # cursor.execute(get_pid)
            # temp_pid=cursor.fetchall()
            temp_pid = [[1]]

            get_price=''' SELECT PRICE FROM FLIGHT WHERE FLIGHT_NUMBER='%s' ''' % (str(flight_number))
            cursor.execute(get_price)
            temp_price=cursor.fetchall()

            if first_name and last_name and sex and birthdate and passport and nationality and exp_date and ticket_type and amount and check:
                cursor=conn.cursor()
                update_flight=''' INSERT INTO BOOKING(P_FIRSTNAME,P_LASTNAME,COUNTRY,P_PASSPORT,P_CLASS,USER_ID,TICKET_TYPE,GENDER,BIRTHDATE,EXPDATE,FLIGHT_NUMBER) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') ''' % (first_name,last_name,nationality,passport,p_class,temp_uid[0][0],ticket_type,sex,birthdate,exp_date,flight_number)
                cursor.execute(update_flight)
                conn.commit()

                cursor=conn.cursor()
                insert_record=''' INSERT INTO RECORD(TRANSACTION_TIME,PID,SALE_PRICE) VALUES('%s','%s','%s') ''' % (time,temp_pid[0][0],temp_price[0][0])
                cursor.execute(insert_record)

                # add to boardingpass
                import random
                seat_number = random.sample(['1A', '1B', '46A'], 1)[0]
                terminal = random.sample(['T1', 'T2'], 1)[0]
                boarding_gate = random.sample(['D4/19', 'C7/19', 'B5'], 1)[0]
                print('check', check)
                boarding_time = check[0][3] # grab from FLIGHT table
                Pid = 1
                # flight_number = flight_number

                cursor=conn.cursor()
                insert_record='''
                INSERT INTO BOARDINGPASS (
                    seat_number, terminal, boarding_gate, boarding_time, Pid, flight_number
                ) VALUES('{}','{}','{}','{}','{}','{}') '''.format(
                    seat_number, terminal, boarding_gate, boarding_time, Pid, flight_number
                )
                print('SQL', insert_record)
                cursor.execute(insert_record)

                conn.commit()
                # cursor.close()

                success_notify='訂票成功，明細以寄送至信箱'
                temp_email=session.get('user_email')
                msg_title='訂票成功通知'+' To: '+last_name+' '+first_name  # 主旨
                msg_sender='testcodepython1126@gmail.com' # 寄件者
                msg_receiver=[temp_email] # 收件者格式為list，否則報錯
                msg_content=last_name+first_name+' ,恭喜您完成訂票，請享受旅程'+'\n'+'以下為您這次定的機票:'+'\n'+'航班編號: '+flight_number+'\n'+'票種: '+ticket_type+'\n'+'.............可因應需求再做調整' # 郵件內容
                msg=Message(msg_title,sender=msg_sender,recipients=msg_receiver)
                msg.body=msg_content
                # mail.send(msg) 
                def send_async_email(app,msg): # 使用多線程寄信時減少卡頓loading time 
                    with app.app_context(): # with開啟時只有在這個with的範圍可以使用，離開這個範圍時自動關閉，回收相關的資源
                        mail.send(msg)
                # app_context詳細解說:https://www.jianshu.com/p/4548516ca896
                thr=Thread(target=send_async_email,args=[app, msg]) 
                thr.start()
                return render_template('user_booking.html',success_notify=success_notify,temp_price=temp_price[0][0])
            else:
                failed_notify='航班編號輸入錯誤'
                return render_template('user_booking.html',failed_notify=failed_notify)       
    else:
        failed_notify='請先用戶登錄在進行訂票'
        # return render_template('login.html', failed_notify=failed_notify)
        # return render_template('login.html', failed_notify=failed_notify)
        return redirect('/login')
    return render_template('user_booking.html')

@app.errorhandler(404) # request錯誤的路徑
def page_not_found(error):
    return render_template('404.html'),404 

@app.errorhandler(500) # 未知的app錯誤
def interna_server_error(error):
    return render_template('500.html'),500

# pwa
@app.route('/manifest.json')
def manifest():
    return app.send_from_directory('static', 'manifest.json')

if __name__=='__main__':
    # app.run(debug=True, threaded=True)
    app.run(debug=True)