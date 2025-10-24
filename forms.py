from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length, Regexp

class RegistrationForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField("Phone", validators=[
        DataRequired(),
        Regexp(r"^[0-9+\-() ]{7,20}$", message="Enter a valid phone number")
    ])
    dob = DateField("Date of Birth", validators=[DataRequired()], format="%Y-%m-%d")
    address = TextAreaField("Address", validators=[DataRequired(), Length(max=1000)])

    course = SelectField(
        "Course Applying For",
        choices=[
            ("", "Select a course"),
            ("Python Full Stack", "Python Full Stack"),
            ("MERN Stack", "MERN Stack"),
            ("Java Full Stack", "Java Full Stack"),
            ("Data Science", "Data Science"),
            ("AI & ML", "AI & ML"),
            ("Digital Marketing", "Digital Marketing"),
        ],
        validators=[DataRequired(message="Please select a course.")],
    )

    statement = TextAreaField("Statement of Purpose", validators=[Length(max=2000)])
    submit = SubmitField("Submit Application")


class AdminLoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
