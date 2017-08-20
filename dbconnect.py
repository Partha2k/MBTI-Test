import MySQLdb
import os

print "Enter Hostname for Database(MySQL-Only)"
hst= raw_input()
print "Enter Database User"
usr = raw_input()
print "Enter password"
passd = raw_input()





conn = MySQLdb.connect(host = hst, user = usr, passwd = passd )
curs = conn.cursor()


curs.execute("SET sql_notes = 0;")
curs.execute("create database IF NOT EXISTS MBTI_QUESTIONS")
curs.execute("SET sql_notes = 0;")
curs.execute("create table IF NOT EXISTS MBTI_QUESTIONS.RegTab (user_id VARCHAR(20) NOT NULL, email_id  VARCHAR(50) NOT NULL, password VARCHAR(100) NOT NULL, PRIMARY KEY(email_id))ENGINE = InnoDB DEFAULT CHARSET = latin1")
curs.execute("create table IF NOT EXISTS MBTI_QUESTIONS.mbtiQuestionTab (Q_Nos INT NOT NULL AUTO_INCREMENT,Module VARCHAR(10) NOT NULL, Section VARCHAR(10) NOT NULL, Questions VARCHAR(500) NOT NULL, Q_Attribute VARCHAR(200) NOT NULL, Q_weight_A INTEGER(2) NOT NULL, Opt_A VARCHAR(200) NOT NULL, Q_weight_B INTEGER(2) NOT NULL, Opt_B VARCHAR(200) NOT NULL, PRIMARY KEY(Q_Nos))ENGINE = InnoDB DEFAULT CHARSET = latin1")
curs.execute("create table IF NOT EXISTS MBTI_QUESTIONS.responseTab (R_Nos INT NOT NULL AUTO_INCREMENT, reg_id VARCHAR(16) NOT NULL,R_Attribute VARCHAR(200) NOT NULL, Res_A VARCHAR(200) NOT NULL, Res_B VARCHAR(200) NOT NULL, KEY(R_Nos))ENGINE = InnoDB DEFAULT CHARSET = latin1")
curs.execute("SET sql_notes =1;")
