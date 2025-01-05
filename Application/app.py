# --- Imports --- #
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


# --- App Initialization --- #
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
Database = SQLAlchemy(app)


# --- Database Models --- #
class User(Database.Model):
    UserName = Database.Column(Database.String(200), primary_key=True)
    Name = Database.Column(Database.String(200), nullable=False)
    Email = Database.Column(Database.String(400), unique=True, nullable=False)
    Password = Database.Column(Database.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.UserName}>"

class Report(Database.Model):
    Id = Database.Column(Database.Integer, primary_key=True)
    Title = Database.Column(Database.String(200), nullable=False)
    Description = Database.Column(Database.String(2000), nullable=False)
    Type = Database.Column(Database.String(200), nullable=False)
    DateTime = Database.Column(Database.String(200), nullable=False)
    Location = Database.Column(Database.String(600), nullable=False)
    PostedBy = Database.Column(Database.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.Id}>"

class Knowledgehub(Database.Model):
    Id = Database.Column(Database.Integer, primary_key=True)
    Title = Database.Column(Database.String(200), nullable=False)
    Description = Database.Column(Database.String(1000), nullable=False)
    Content = Database.Column(Database.String(4000), nullable=False)

    def __repr__(self):
        return f"<KnowledgeHub {self.Id}>"


# --- Creating Database Instance --- #
with app.app_context():
    Database.create_all()


# --- Variable --- #
global ActiveUser


# --- Routes --- #
@app.route('/')
def Index():
    return render_template("Index.html")

@app.route('/SignUp/', methods=['GET', 'POST'])
def SignUp():

    if request.method == 'POST':
        UserName = request.form['UserName']
        Name = request.form['Name']
        Email = request.form['Email']
        Password = request.form['Password']
        RePassword = request.form['RepeatPassword']

        if Password != RePassword:
            return render_template("SignUp.html", error="Passwords don't match")

        if User.query.filter_by(UserName=UserName).first():
            return render_template("SignUp.html", error="Username already in use")

        Data = User(UserName=UserName, Name=Name, Email=Email, Password=Password)


        try:
            Database.session.add(Data)
            Database.session.commit()
            return redirect('/SignIn/')
        except Exception as e:
            print(f"Error: {e}")
            return render_template('SignUp.html', error="Error")
    else:
        return render_template("SignUp.html")

@app.route('/SignIn/', methods=['GET', 'POST'])
def SignIn():

    global ActiveUser

    if request.method == 'POST':
        UserName = request.form['UserName']
        Password = request.form['Password']

        try:
            Users = User.query.order_by(User.UserName).all()
            for user in Users:
                if (user.UserName == UserName) and (user.Password == Password):
                    ActiveUser = UserName
                    return redirect('/Home/')
                else:
                    return render_template('SignIn.html', error="Incorrect Password")
        except Exception as e:
            print(f"Error: {e}")
            return render_template('SignIn.html', error="Error")

    else:
        return render_template("SignIn.html")

@app.route('/Home/', methods=['GET', 'POST'])
def Home():
    return render_template("Home.html")

@app.route('/Reports/', methods=['GET', 'POST'])
def Reports():

    Reports = Report.query.order_by(Report.DateTime).all()
    return render_template("Reports.html", Reports=Reports)

@app.route('/Reports/CreateReport/', methods=['GET', 'POST'])
def CreateReport():

    global ActiveUser

    if request.method == 'POST':
        Title = request.form['ReportTitle']
        Description = request.form['ReportDescription']
        Type = request.form['ReportType']
        DateTime = request.form['DateTime']
        Location = request.form['ReportLocation']

        Data = Report(Title=Title, Description=Description, Type=Type, DateTime=DateTime, Location=Location, PostedBy=ActiveUser)

        try:
            Database.session.add(Data)
            Database.session.commit()
            return redirect('/Reports/')

        except Exception as e:
            print(f"Error: {e}")
            return render_template('CreateReport.html', error="Error")

    else:
        return render_template("CreateReport.html")

@app.route('/Reports/ViewReport/', methods=['GET', 'POST'])
def ViewReport():

    global ActiveUser

    return render_template("ViewReport.html", Reports=Reports)

@app.route('/KnowledgeHub/', methods=['GET', 'POST'])
def KnowledgeHub():

    Info = Knowledgehub.query.order_by(Knowledgehub.Id).all()
    return render_template("KnowledgeHub.html", Info=Info)

@app.route('/KnowledgeHub/AddInfo/', methods=['GET', 'POST'])
def AddInfo():

    if request.method == 'POST':
        Title = request.form['Title']
        Description = request.form['Description']
        Content = request.form['Content']

        Data = Knowledgehub(Title=Title, Description=Description, Content=Content)

        try:
            Database.session.add(Data)
            Database.session.commit()
            return redirect('/KnowledgeHub/')

        except Exception as e:
            print(f"Error: {e}")
            return render_template('AddInfo.html', error="Error")

    else:
        return render_template("AddInfo.html")


