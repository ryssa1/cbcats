from flask import Flask, render_template,render_template_string,jsonify,request,flash,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
# import sqlalchemy.types as types
from sqlalchemy import text
import datetime
import os
import re
# from werkzeug.security import check_password_hash, generate_password_hash

regex = re.compile(r"([-!#-'+/-9=?A-Z^-~]+(\.[-!#-'+/-9=?A-Z^-~]+)|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'+/-9=?A-Z^-~]+(\.[-!#-'+/-9=?A-Z^-~]+)|\[[\t -Z^-~]*])")

selected_row = 0


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:abc123456@cbcatsdb.cntx162waxib.us-east-1.rds.amazonaws.com/cbcats'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ftincgfdwbjgkkt3j7593hh3'
app.config['HTML_TABLE'] = ""
# app.config['selected_row'] = 0
db = SQLAlchemy(app)
app.jinja_env.globals.update(len=len)

def isValid(email):
    if re.fullmatch(regex, email):
        return True
    else:
        return False




# Import the models and routes for each table
from models.company import Company
from models.employee import Employee
from models.asset import Asset
from models.assetlocation import Assetlocation
from models.supplier import Supplier
from models.maintenance import Maintenance
from models.location import Location
from models.notificationitam import Notificationitam
from models.notificationhr import Notificationhr







from routes.company_routes import company_bp
from routes.employee_routes import employee_bp
from routes.asset_routes import asset_bp
from routes.assetlocation_routes import assetlocation_bp
from routes.supplier_routes import supplier_bp
from routes.maintenance_routes import maintenance_bp
from routes.location_routes import location_bp
from routes.notificationitam_routes import notificationitam_bp
from routes.notificationhr_routes import notificationhr_bp






# Register the Blueprints for each table's routes
app.register_blueprint(company_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(asset_bp)
app.register_blueprint(assetlocation_bp)
app.register_blueprint(supplier_bp)
app.register_blueprint(maintenance_bp)
app.register_blueprint(location_bp)
app.register_blueprint(notificationitam_bp)
app.register_blueprint(notificationhr_bp)














with app.app_context():
    db.create_all()



# @app.route('/')
# def index():
#     return render_template('Login.html')


@app.route('/reset_errors',methods=['GET'])
def reset_errors():
    if 'ERR_MSGS' in session:
        session.pop('ERR_MSGS', None)
    session['ERR_MSGS'] = {}
    return redirect(url_for(session["TABLE"]))



@app.route('/', methods=['GET', 'POST'])
def login():
    print("pppppppppppppppppppppppppppppppppppp")
    # all_users = Employee.query.all()
    # for user in all_users:
    #     user.set_password(user.emp_password)
    #     db.session.commit()
    if request.method == 'POST':
        print("logging in")
        emp_email = request.form.get('email')
        password = request.form.get('password')
        print("email : ", emp_email, "password : ", password)
        user = Employee.query.filter_by(email=emp_email).first()
        # if user is None or not user.check_password(password):
        if user is None or not user.password == password:
            print("error message")
            error = 'Invalid email or password'
            return render_template('login.html', error=error)
        else:
            print("else")
            session['userid'] = user.employee_id
            session['username'] = user.full_name
            session['usertype'] = user.user_type
            if user.user_type == 'ITAM':
                return redirect(url_for('dashboard'))
            elif user.user_type == 'HR':
                return redirect(url_for('dashboardHr'))
            else:
                print("error message")
                error = 'You are not allowed to access. Kindly refer to IT department for assistance.'
                return render_template('login.html', error=error)
    return render_template('Login.html')


@app.route('/addUsers')
def addUsers():
        return render_template('addUsers.html')


@app.route('/dashboard')
def dashboard():
    return render_template('Dashboard.html')

@app.route('/dashboardHr')
def dashboardHr():
    return render_template('DashboardHR.html')

@app.route('/employee')
def employeeListHR():
    return render_template('Employee_table.html')

@app.route('/employeeIT')
def employeeListIT():
    return render_template('IT_Employee_table.html')

@app.route('/assetMenu')
def assetMenu():
    return render_template('Asset-Menu.html')

@app.route('/asset')
def assetList():
    return render_template('Asset_table.html')

@app.route('/assetlocation')
def assetLocation():
    return render_template('AssetLocation_table.html')

@app.route('/supplier')
def supplier():
    return render_template('Supplier_table.html')


@app.route('/maintenance')
def maintenance():
    return render_template('Maintenance_table.html')

@app.route('/notificationitam')
def notificationitam():
    return render_template('Notificationitam_table.html')


@app.route('/about')
def about():
    return render_template('About.html')


@app.route('/logout')
def logout():
    session.pop('userid',None)
    session.pop('password',None)
    session.pop('username',None)
    session.pop('usertype',None)
    return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)
