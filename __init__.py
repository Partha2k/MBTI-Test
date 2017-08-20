from flask import Flask, render_template, request, url_for,redirect, flash, session, g
from forms import ClientLogInForm, ClientReg, AdminForm, AdminPassChangeForm, QuestionForm, ResponseForm
import MySQLdb
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)

conn = MySQLdb.connect(host = 'localhost', user = 'root', passwd = '123', db = 'MBTI_QUESTIONS' )
curs = conn.cursor()

def insert_sec1(mod,sec,ques_1,q_type,wgt_a,op_a,wgt_b,op_b):
     curs.execute("ALTER TABLE `MBTI_QUESTIONS`.`mbtiQuestionTab` AUTO_INCREMENT=1")
     curs.execute("ALTER TABLE `MBTI_QUESTIONS`.`mbtiQuestionTab` ADD CONSTRAINT UNIQUE(`Q_Nos`, `Questions`, `Opt_A`, `Opt_B`)") 
     curs.execute("INSERT INTO `MBTI_QUESTIONS`.`mbtiQuestionTab`(`Q_Nos`, `Module`, `Section`, `Questions`, `Q_Attribute`, `Q_weight_A`, `Opt_A`, `Q_weight_B`, `Opt_B`) VALUES ('',%s,%s,%s,%s,%s,%s,%s,%s)", (mod,sec,ques_1,q_type,wgt_a,op_a,wgt_b,op_b))
     conn.commit()

def insert_sec2(mod,sec,q_type,wgt_a,op_a,wgt_b,op_b):
     curs.execute("ALTER TABLE `MBTI_QUESTIONS`.`mbtiQuestionTab` AUTO_INCREMENT=1")
     curs.execute("ALTER TABLE `MBTI_QUESTIONS`.`mbtiQuestionTab` ADD CONSTRAINT UNIQUE(`Q_Nos`, `Questions`, `Opt_A`, `Opt_B`)") 
     curs.execute("INSERT INTO `MBTI_QUESTIONS`.`mbtiQuestionTab`(`Q_Nos`, `Module`, `Section`, `Questions`, `Q_Attribute`, `Q_weight_A`, `Opt_A`, `Q_weight_B`, `Opt_B`) VALUES ('',%s,%s,'',%s,%s,%s,%s,%s)", (mod,sec,q_type,wgt_a,op_a,wgt_b,op_b))
     conn.commit()

def insert_response_store(res,attr,reg):
    if res == 'Opt_A':
       curs.execute("ALTER TABLE `MBTI_QUESTIONS`.`responseTab` AUTO_INCREMENT=1")
       curs.execute("INSERT INTO `MBTI_QUESTIONS`.`responseTab`(`reg_id`,`R_Attribute`,`Res_A`,`Res_B`) VALUES (%s,%s,'1','0')",(reg,attr))
       conn.commit()
    if res == 'Opt_B':
       curs.execute("ALTER TABLE `MBTI_QUESTIONS`.`responseTab` AUTO_INCREMENT=1")
       curs.execute("INSERT INTO `MBTI_QUESTIONS`.`responseTab`(`reg_id`,`R_Attribute`,`Res_A`,`Res_B`) VALUES (%s,%s,'0','1')",(reg,attr))
       conn.commit()

def calc_result_EI(name):
    p_type = ["Extraversion","Introversion","Sensing","Intuition","Thinking","feeling","Judging","Perceiving"]
    curs.execute("SELECT Q_weight_A FROM `MBTI_QUESTIONS`.`mbtiQuestionTab` WHERE Q_Attribute = 'E or I'")
    q_wgt_a = curs.fetchall()
    curs.execute("SELECT Res_A FROM `MBTI_QUESTIONS`.`responseTab` WHERE R_Attribute = 'E or I' AND reg_id= %s",(name))
    res_a = curs.fetchall()
    f_one_a=[]
    for i in range(len(res_a)):
        f_one_a.append(int(res_a[i][0]))
    sum_one_a = 0
    for i in range(len(q_wgt_a)):
        sum_one_a += f_one_a[i]*q_wgt_a[i][0]
    curs.execute("SELECT Q_weight_B FROM `MBTI_QUESTIONS`.`mbtiQuestionTab` WHERE Q_Attribute = 'E or I'")
    q_wgt_b = curs.fetchall()
    curs.execute("SELECT Res_B FROM `MBTI_QUESTIONS`.`responseTab` WHERE R_Attribute = 'E or I' AND reg_id= %s",(name))
    res_b = curs.fetchall()
    f_one_b=[]
    for i in range(len(res_b)):
        f_one_b.append(int(res_b[i][0]))
    sum_one_b = 0
    for i in range(len(q_wgt_b)):
        sum_one_b += f_one_b[i]*q_wgt_b[i][0]
    if sum_one_a > sum_one_b:
       return p_type[0]+" E score "+str(sum_one_a)+" I Score "+str(sum_one_b)
    else:
       return p_type[1]+" E score "+str(sum_one_a)+" I Score "+str(sum_one_b)
           
def calc_result_SN(name):
    p_type = ["Extraversion","Introversion","Sensing","Intuition","Thinking","feeling","Judging","Perceiving"]
    curs.execute("SELECT Q_weight_A FROM `MBTI_QUESTIONS`.`mbtiQuestionTab` WHERE Q_Attribute = 'S or N'")
    q_wgt_a = curs.fetchall()
    curs.execute("SELECT Res_A FROM `MBTI_QUESTIONS`.`responseTab` WHERE R_Attribute = 'S or N' AND reg_id= %s",(name))
    res_a = curs.fetchall()
    f_one_a=[]
    for i in range(len(res_a)):
        f_one_a.append(int(res_a[i][0]))
    sum_one_a = 0
    for i in range(len(q_wgt_a)):
        sum_one_a += f_one_a[i]*q_wgt_a[i][0]
    curs.execute("SELECT Q_weight_B FROM `MBTI_QUESTIONS`.`mbtiQuestionTab` WHERE Q_Attribute = 'S or N'")
    q_wgt_b = curs.fetchall()
    curs.execute("SELECT Res_B FROM `MBTI_QUESTIONS`.`responseTab` WHERE R_Attribute = 'S or N' AND reg_id= %s",(name))
    res_b = curs.fetchall()
    f_one_b=[]
    for i in range(len(res_b)):
        f_one_b.append(int(res_b[i][0]))
    sum_one_b = 0
    for i in range(len(q_wgt_b)):
        sum_one_b += f_one_b[i]*q_wgt_b[i][0]
    if sum_one_a > sum_one_b:
       return p_type[2]+" S score "+str(sum_one_a)+" N Score "+str(sum_one_b)
    else:
       return p_type[3]+" S score "+str(sum_one_a)+" N Score "+str(sum_one_b)

def calc_result_TF(name):
    p_type = ["Extraversion","Introversion","Sensing","Intuition","Thinking","feeling","Judging","Perceiving"]
    curs.execute("SELECT Q_weight_A FROM `MBTI_QUESTIONS`.`mbtiQuestionTab` WHERE Q_Attribute = 'T or F'")
    q_wgt_a = curs.fetchall()
    curs.execute("SELECT Res_A FROM `MBTI_QUESTIONS`.`responseTab` WHERE R_Attribute = 'T or F' AND reg_id= %s",(name))
    res_a = curs.fetchall()
    f_one_a=[]
    for i in range(len(res_a)):
        f_one_a.append(int(res_a[i][0]))
    sum_one_a = 0
    for i in range(len(q_wgt_a)):
        sum_one_a += f_one_a[i]*q_wgt_a[i][0]
    curs.execute("SELECT Q_weight_B FROM `MBTI_QUESTIONS`.`mbtiQuestionTab` WHERE Q_Attribute = 'T or F'")
    q_wgt_b = curs.fetchall()
    curs.execute("SELECT Res_B FROM `MBTI_QUESTIONS`.`responseTab` WHERE R_Attribute = 'T or F' AND reg_id= %s",(name))
    res_b = curs.fetchall()
    f_one_b=[]
    for i in range(len(res_b)):
        f_one_b.append(int(res_b[i][0]))
    sum_one_b = 0
    for i in range(len(q_wgt_b)):
        sum_one_b += f_one_b[i]*q_wgt_b[i][0]
    if sum_one_a > sum_one_b:
       return p_type[4]
    else:
       return p_type[5]

def calc_result_JP(name):
    p_type = ["Extraversion","Introversion","Sensing","Intuition","Thinking","feeling","Judging","Perceiving"]
    curs.execute("SELECT Q_weight_A FROM `MBTI_QUESTIONS`.`mbtiQuestionTab` WHERE Q_Attribute = 'J or P'")
    q_wgt_a = curs.fetchall()
    curs.execute("SELECT Res_A FROM `MBTI_QUESTIONS`.`responseTab` WHERE R_Attribute = 'J or P' AND reg_id= %s",(name))
    res_a = curs.fetchall()
    f_one_a=[]
    for i in range(len(res_a)):
        f_one_a.append(int(res_a[i][0]))
    sum_one_a = 0
    for i in range(len(q_wgt_a)):
        sum_one_a += f_one_a[i]*q_wgt_a[i][0]
    curs.execute("SELECT Q_weight_B FROM `MBTI_QUESTIONS`.`mbtiQuestionTab` WHERE Q_Attribute = 'J or P'")
    q_wgt_b = curs.fetchall()
    curs.execute("SELECT Res_B FROM `MBTI_QUESTIONS`.`responseTab` WHERE R_Attribute = 'J or P' AND reg_id= %s",(name))
    res_b = curs.fetchall()
    f_one_b=[]
    for i in range(len(res_b)):
        f_one_b.append(int(res_b[i][0]))
    sum_one_b = 0
    for i in range(len(q_wgt_b)):
        sum_one_b += f_one_b[i]*q_wgt_b[i][0]
    if sum_one_a > sum_one_b:
       return p_type[6]
    else:
       return p_type[7]
        
@app.route('/', methods = ['POST','GET'])
def index():
    form = ClientLogInForm()
    if request.method == 'POST':
       session.pop('user',None)
       if request.form['password'] == 'richardking':
          session['user'] = request.form['username']
          return redirect(url_for('mbti_start'))
    return render_template("clientlogin.html", form = form)
    
@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
       g.user = session['user']

@app.route('/mbti')
def mbti_start():
    if g.user:
      if 'user' in session:
         return render_template('clientDashboard.html')
      else:
         flash("You are not looged in.")
         return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/startTest/<i>')
def begin_test(i):
    form = ResponseForm()
    curs.execute("SELECT Questions,Opt_A,Opt_B,Q_Attribute FROM `MBTI_QUESTIONS`.`mbtiQuestionTab` WHERE Q_Nos = 1")
    opt=curs.fetchone()
    ques = opt[0]
    form.option.choices = [('Opt_A',opt[1]),('Opt_B',opt[2])]
    form.type.data = opt[3]
    k = int(i)
    k += 1
    j = str(k)
    return render_template('response.html',form = form, ini = j ,question = ques)
   
   
@app.route('/contTest/<ini>', methods = ['GET','POST'])
def cont_test(ini):
    ina = int(ini)
    ina += 1
    form = ResponseForm()
    curs.execute("SELECT max(Q_Nos) FROM `MBTI_QUESTIONS`.`mbtiQuestionTab`")
    max_q = curs.fetchone()
    if request.method == 'POST':
       if 'user' in session:
          resp = request.form['option']
          q_type = request.form['type']
          insert_response_store(resp,q_type,g.user)  
          while ina < max_q[0]+1:
            curs.execute("SELECT Questions,Opt_A,Opt_B,Q_Attribute FROM `MBTI_QUESTIONS`.`mbtiQuestionTab` WHERE Q_Nos = %s",(ina))
            opt=curs.fetchone()
            ques = opt[0]
            form.option.choices = [('Opt_A',opt[1]),('Opt_B',opt[2])]
            form.type.data = opt[3]
            j = str(ina)
            return render_template('response.html',form = form, ini = j ,question = ques)
       else:
            flash("You are not logged in")
            return redirect(url_for('index'))
       if ina == max_q[0]+1:
          if 'user' in session:
             session.pop('user',None)
             flash("You have successfully finished your test")
             return redirect(url_for('index'))
            

@app.route('/showTestResult')
def test_result():
    if 'user' in session:
       if curs.execute("SELECT R_Attribute FROM `MBTI_QUESTIONS`.`responseTab` WHERE R_Attribute = 'E or I' AND reg_id = %s",(session['user'])") > 0:
          type_one = calc_result_EI(session['user'])
       else:
          type_one = 'Score Not Found'
       if curs.execute("SELECT R_Attribute FROM `MBTI_QUESTIONS`.`responseTab` WHERE R_Attribute = 'S or N' AND reg_id = %s",(session['user'])") > 0:
          type_two = calc_result_SN(session['user'])
       else:
          type_two = 'Score Not Found'
       if curs.execute("SELECT R_Attribute FROM `MBTI_QUESTIONS`.`responseTab` WHERE R_Attribute = 'T or F' AND reg_id = %s",(session['user'])") > 0:
          type_three = calc_result_TF(session['user'])
       else:
          print 'No Questions Found'
       if curs.execute("SELECT R_Attribute FROM `MBTI_QUESTIONS`.`responseTab` WHERE R_Attribute = 'J or P' AND reg_id = %s",(session['user'])") > 0:
          type_four = calc_result_JP(session['user'])
       else:
          print 'No Questions Found'
       print 10*'#'
       print type_one 
       print 10*'#'
       print type_two
       print 10*'#'
       return render_template('result.html', EorI = type_one, SorN = type_two)
    else:
       flash("You are not logged in.")
       return redirect(url_for('index'))


@app.route('/admin')
def login_admin():
    form = AdminForm()
    return render_template('admin.html', form = form)

@app.route('/admin/adminDashboard', methods=['POST','GET'])
def admin_dBoard():
    form = AdminForm(request.form)
    if request.method == 'POST':
       name = request.form['username']
       passwd = request.form['password']
       chk = curs.execute("SELECT user_id,password FROM `MBTI_QUESTIONS`.`RegTab` WHERE user_id = %s AND password = %s",(name,passwd))
       if chk == 1:
          return render_template('admin_dashboard.html')
       else:
          flash('Incorrect Username or Password')
          return redirect(url_for('login_admin'))
    else:
       return render_template('admin.html', form = form)

@app.route('/admin/changepassword')
def passchange_admin():
    form = AdminPassChangeForm()
    return render_template('adminpass.html', form = form)

@app.route('/admin/createTest')
def newTest():
    form = QuestionForm()
    return render_template('new_test.html', form = form)

@app.route('/admin/createTest/continue', methods =['POST','GET'])
def contTest():
    form = QuestionForm()
    if request.method == 'POST':
       if form.validate() == False:
          return render_template('new_test.html', form =form)
       else:
          module,section,question,type= request.form['moduleNum'],request.form['sectionNum'],request.form['questions'],request.form['questionType']
          weightA,optA,weightB,optB= request.form['weight_A'], request.form['optionA'], request.form['weight_B'], request.form['optionB']
          if question =='':
             insert_sec2(module,section,type,weightA,optA,weightB,optB)
          else:
             insert_sec1(module,section,question,type,weightA,optA,weightB,optB)
      
    return redirect(url_for('newTest'))

@app.route('/admin/success')
def complete():
     flash('Test created successfully')
     return redirect(url_for('admin_dBoard'))
     return render_template('upload_success.html')

       
       

if __name__=='__main__':
   app.run(host='0.0.0.0',port = 80, debug= True,use_reloader = False)






         
         

