
#   Programmer Name: Oey Ching Yi (TP 061246), Student, APU 
#   Program Name: CBCATS application
#   File Name: employee.py
#   First Written on: Saturday, 11th February 2023
#   Edited On: Monday, 3rd April 2023 

from app import db
# from werkzeug.security import check_password_hash, generate_password_hash



class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(6), primary_key=True)
    email = db.Column(db.String(100))
    full_name = db.Column(db.String(120))
    password = db.Column(db.String(128))
    user_type = db.Column(db.String(50))
    position = db.Column(db.String(30))
    status = db.Column(db.String(10))
    gender = db.Column(db.String(1))
    dob = db.Column(db.Date)
    contact_no = db.Column(db.String(20))
    address = db.Column(db.String(200))
    state = db.Column(db.String(30))
    postcode = db.Column(db.String(10))
    country = db.Column(db.String(80))
    department = db.Column(db.String(120))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'email':self.email,
            'full_name': self.full_name,
            'password':self.password,
            'user_type': self.user_type,
            'position': self.position,
            'status': self.status,
            'gender': self.gender,
            'dob': self.dob.date() if self.dob else None,
            'contact_no': self.contact_no,
            'address': self.address,
            'state': self.state,
            'postcode': self.postcode,
            'country': self.country,
            'department': self.department,
            'start_date': self.start_date.date() if self.start_date else None,
            'end_date': self.end_date.date() if self.end_date else None,
        }
    
    def __repr__(self):
        return f"<Employee(id={self.id}, employee_id='{self.employee_id}', full_name='{self.full_name}')>"
    
    # def set_password(self, password):
    #     self.password = generate_password_hash(password)

    # def check_password(self, password):
    #     return check_password_hash(self.password, password)