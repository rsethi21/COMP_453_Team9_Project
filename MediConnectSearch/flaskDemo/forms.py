from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
# from flaskDemo.models import User, Department, getDepartment, getDepartmentFactory, Employee, Works_On, Project
from flaskDemo.models import Doctor, Patient
from wtforms.fields.html5 import DateField

# ssns = Department.query.with_entities(Department.mgr_ssn).distinct()
# #  or could have used ssns = db.session.query(Department.mgr_ssn).distinct()
# # for that way, we would have imported db from flaskDemo, see above
#
# myChoices2 = [(row[0],row[0]) for row in ssns]  # change
# results=list()
# for row in ssns:
#     rowDict=row._asdict()
#     results.append(rowDict)
# myChoices = [(row['mgr_ssn']) for row in results]
# regex1='^((((19|20)(([02468][048])|([13579][26]))-02-29))|((20[0-9][0-9])|(19[0-9][0-9]))-((((0[1-9])'
# regex2='|(1[0-2]))-((0[1-9])|(1\d)|(2[0-8])))|((((0[13578])|(1[02]))-31)|(((0[1,3-9])|(1[0-2]))-(29|30)))))$'
# regex=regex1 + regex2

# emp_ssns = Employee.query.with_entities(Employee.ssn)
# results2 = list()
# for row in emp_ssns:
#     rowDict = row._asdict()
#     results2.append(rowDict)
# emp_Choices =sorted( [(row['ssn']) for row in results2])
#
# projects = Project.query.with_entities(Project.pnumber)
# results3 = list()
# for row in projects:
#     rowDict = row._asdict()
#     results3.append(rowDict)
# project_Choices =sorted( [(row['pnumber'], row['pnumber']) for row in results3])

doctor_specialties = Doctor.query.with_entities(Doctor.specialty).distinct()
results = list()
for row in doctor_specialties:
    rowDict = row._asdict()
    results.append(rowDict)
specialty_Choices =sorted( [(row['specialty']) for row in results])

language = Doctor.query.with_entities(Doctor.language).distinct()
results = list()
for row in language:
    rowDict = row._asdict()
    results.append(rowDict)
language_Choices =sorted( [(row['specialty']) for row in results])

locations = Doctor.query.with_entities(Doctor.locations).distinct()
results = list()
for row in locations:
    rowDict = row._asdict()
    results.append(rowDict)
location_Choices =sorted( [(row['specialty']) for row in results])




class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')



class AssignmentUpdateForm(FlaskForm):

    essn = SelectField("Employee SSN", choices=emp_Choices)  # myChoices defined at top
    pno = SelectField("Project Number", choices= project_Choices, coerce=int)
    hours=IntegerField('Number of Hours Allocated', validators=[DataRequired()])
    submit = SubmitField('Update this assignment')

    def validate_pno(self, essn):    # apparently in the company DB, dname is specified as unique
         assignment = Works_On.query.filter_by(essn=essn.data)
         valid_pnos = list()
         for instance in assignment:
            valid_pnos.append(instance.pno)
         if (int(self.pno.data) not in valid_pnos):
             raise ValidationError('That project is already being assigned. Please choose a different project.')




    
class DeptUpdateForm(FlaskForm):

#    dnumber=IntegerField('Department Number', validators=[DataRequired()])
    dnumber = HiddenField("")

    dname=StringField('Department Name:', validators=[DataRequired(),Length(max=15)])
#  Commented out using a text field, validated with a Regexp.  That also works, but a hassle to enter ssn.
#    mgr_ssn = StringField("Manager's SSN", validators=[DataRequired(),Regexp('^(?!000|666)[0-8][0-9]{2}(?!00)[0-9]{2}(?!0000)[0-9]{4}$', message="Please enter 9 digits for a social security.")])

#  One of many ways to use SelectField or QuerySelectField.  Lots of issues using those fields!!
    mgr_ssn = SelectField("Manager's SSN", choices=myChoices)  # myChoices defined at top
    
# the regexp works, and even gives an error message
#    mgr_start=DateField("Manager's Start Date:  yyyy-mm-dd",validators=[Regexp(regex)])
#    mgr_start = DateField("Manager's Start Date")

#    mgr_start=DateField("Manager's Start Date", format='%Y-%m-%d')
    mgr_start = DateField("Manager's start date:", format='%Y-%m-%d')  # This is using the html5 date picker (imported)
    submit = SubmitField('Update this department')


# got rid of def validate_dnumber

    def validate_dname(self, dname):    # apparently in the company DB, dname is specified as unique
         dept = Department.query.filter_by(dname=dname.data).first()
         if dept and (str(dept.dnumber) != str(self.dnumber.data)):
             raise ValidationError('That department name is already being used. Please choose a different name.')


class AssignmentForm(FlaskForm):

    # essn = StringField("Employee SSN")  # myChoices defined at top
    essn = StringField("Employee SSN")  # myChoices defined at top
    pno = SelectField("Project Number", choices= project_Choices, coerce=int)
    hours=IntegerField('Number of Hours Allocated', validators=[DataRequired()])
    submit = SubmitField('Add this assignment')
    #def validate_assignment(self, essn, pno):    # apparently in the company DB, dname is specified as unique
        #assignment = Works_On.query.all()
        #for instance in assignment:
           #if (instance.pno == self.pno and instance.essn == self.essn) == False:
            #raise ValidationError('This assignment already exists. Please choose a different assignment.')
            
    def validate_assignment(self, essn):    #because dnumber is primary key and should be unique
        emp_assignments = Works_On.query.filter_by(essn=essn)
        for assignment in emp_assignments:
            if(str(self.pno.data) == str(assignment.pno)):
                raise ValidationError('That Assignment already exists. Please choose a different one.')
                return False


class SearchForm(FlaskForm):
    specialty = SelectField("Doctor Specialty", choices=specialty_Choices, validators=[DataRequired()])
    language = SelectField("Language", choices=language_Choices, validators=[DataRequired()])
    location = SelectField("Location", choices=location_Choices, validators=[DataRequired()])
    submit = SubmitField('Find a Doctor', choices=specialty_Choices, validators=[DataRequired()])


    # # essn = StringField("Employee SSN")  # myChoices defined at top
    # essn = StringField("Employee SSN")  # myChoices defined at top
    # pno = SelectField("Project Number", choices=project_Choices, coerce=int)
    # hours = IntegerField('Number of Hours Allocated', validators=[DataRequired()])
    # submit = SubmitField('Add this assignment')
    #
    # # def validate_assignment(self, essn, pno):    # apparently in the company DB, dname is specified as unique
    # # assignment = Works_On.query.all()
    # # for instance in assignment:
    # # if (instance.pno == self.pno and instance.essn == self.essn) == False:
    # # raise ValidationError('This assignment already exists. Please choose a different assignment.')
    #
    # def validate_assignment(self, essn):  # because dnumber is primary key and should be unique
    #     emp_assignments = Works_On.query.filter_by(essn=essn)
    #     for assignment in emp_assignments:
    #         if (str(self.pno.data) == str(assignment.pno)):
    #             raise ValidationError('That Assignment already exists. Please choose a different one.')
    #             return False

class DeptForm(DeptUpdateForm):

    dnumber=IntegerField('Department Number', validators=[DataRequired()])
    submit = SubmitField('Add this department')

    def validate_dnumber(self, dnumber):    #because dnumber is primary key and should be unique
        dept = Department.query.filter_by(dnumber=dnumber.data).first()
        if dept:
            raise ValidationError('That department number is taken. Please choose a different one.')

