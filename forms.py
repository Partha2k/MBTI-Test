from flask_wtf import FlaskForm
from wtforms import TextField, HiddenField, TextAreaField, StringField, RadioField, IntegerField, TextAreaField, SubmitField, SelectField, PasswordField
from wtforms import validators, ValidationError

class ResponseForm(FlaskForm):
   type = HiddenField()
   option = RadioField('Please select an option')
   submit = SubmitField("Confirm Answer")
class QuestionForm(FlaskForm):
   moduleNum = StringField('Enter Module Name',[validators.Required('Please Enter module')])
   sectionNum = SelectField('Section entry point (Four Section Max)',choices = [('sec-1','Section 1'),('sec-2','Section 2'),('sec-3','Section 3'),('sec-4','Section 4')])
   questions = TextAreaField('Question entry point')
   questionType = SelectField('Question Type Indicator',choices = [('E or I','Extraversion or Introversion'),('S or N','Sensing or Intuition'),('T or F','Thinking or feeling'),('J or P','Judging or Perceiving')])
   weight_A = IntegerField('Score for Option A',[validators.Required('Please enter score A')])
   optionA = TextField('Option A',[validators.Required('Please enter option A')])
   weight_B = IntegerField('Score for Option B',[validators.Required('Please enter score B')])
   optionB = TextField('Option B',[validators.Required('Please enter option B')])
   submit = SubmitField("Upload")
class ClientLogInForm(FlaskForm):
   username = StringField('Username',[validators.Length(min = 4, max =16), validators.Required('Please enter admin username')])
   password = PasswordField('Password',[validators.DataRequired()])
   submit = SubmitField("Log In")
class AdminForm(FlaskForm):
   username = StringField('Admin Username',[validators.Length(min = 4, max =16), validators.Required('Please enter admin username')])
   password = PasswordField('Admin Password',[validators.DataRequired()])
   submit = SubmitField("Log In")
class AdminPassChangeForm(FlaskForm):
   old_password = PasswordField('Old Password',[validators.DataRequired()])
   new_password = PasswordField('New Password',[validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
   confirm = PasswordField('Repeat Password')
   submit = SubmitField("Confirm")
class ClientReg(FlaskForm):      
   username = StringField('Username', [validators.Length(min=4, max=25),validators.Required('Username Required')])
   email = StringField('Email Address', [validators.Length(min=6, max=35),validators.Required('Email Required')])
   password = PasswordField('New Password', [validators.Required('Enter Password'), validators.EqualTo('confirm', message='Passwords must match')])
   confirm = PasswordField('Repeat Password',[validators.Required()])
   submit = SubmitField("Sign Up")
class ContactForm(FlaskForm):
   name = TextField("Name Of Student",[validators.Required("Please enter your name.")])
   Gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])
   Address = TextAreaField("Address")
   
   email = TextField("Email",[validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
   
   Age = IntegerField("age")
   language = SelectField('Languages', choices = [('cpp', 'C++'), ('py', 'Python')])
   submit = SubmitField("Send")
      
