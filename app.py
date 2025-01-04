from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
db = SQLAlchemy(app)


class User(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=False)
    Email = db.Column(db.String(400), unique=True, nullable=False)
    Password = db.Column(db.String(200), nullable=False)

class Report(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(200), nullable=False)
    Description = db.Column(db.String(2000), nullable=False)
    Type = db.Column(db.String(200), nullable=False)
    DateTime = db.Column(db.String(200), nullable=False)
    Location = db.Column(db.String(600), nullable=False)
    PostedBy = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.Id}>"

UserId = 0

# Routes
@app.route('/')
def Index():
    return render_template("Index.html")

@app.route('/SignUp/', methods=['GET', 'POST'])
def SignUp():

    if request.method == 'POST':
        Name = request.form['Name']
        Email = request.form['Email']
        Password = request.form['Password']

        Data = User(Name=Name, Email=Email, Password=Password)

        try:
            db.session.add(Data)
            db.session.commit()
            return redirect('/SignIn/')
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
    else:
        return render_template("SignUp.html")

@app.route('/SignIn/', methods=['GET', 'POST'])
def SignIn():

    if request.method == 'POST':
        Email = request.form['Email']
        Password = request.form['Password']

        try:
            Users = User.query.order_by(User.Id).all()
            for user in Users:
                if (user.Email == Email) and (user.Password == Password):
                    return redirect('/Home/')
                else:
                    return render_template('SignIn.html')
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"

    else:
        return render_template("SignIn.html")

@app.route('/Home/', methods=['GET', 'POST'])
def Home():
    return render_template("Home.html")

@app.route('/Report/CreateReport/', methods=['GET', 'POST'])
def CreateReport():

    if request.method == 'POST':
        Title = request.form['ReportTitle']
        Description = request.form['ReportDescription']
        Type = request.form['ReportType']
        DateTime = request.form['DateTime']
        Location = request.form['ReportLocation']

        Data = Report(Title=Title, Description=Description, Type=Type, DateTime=DateTime, Location=Location, PostedBy=UserId)

        try:
            db.session.add(Data)
            db.session.commit()
            return redirect('/Report/ViewReport/')

        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"

    else:
        return render_template("CreateReport.html")

@app.route('/Report/ViewReport/', methods=['GET', 'POST'])
def ViewReport():

    Reports = Report.query.order_by(Report.DateTime).all()
    return render_template("ViewReport.html", Users=Users, Reports=Reports)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=8000)
