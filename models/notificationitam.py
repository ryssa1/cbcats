
#   Programmer Name: Oey Ching Yi (TP 061246), Student, APU 
#   Program Name: CBCATS application
#   File Name: notificationitam.py
#   First Written on: Saturday, 11th February 2023
#   Edited On: Monday, 3rd April 2023 

from app import db

class Notificationitam(db.Model):
    __tablename__ = 'notificationitam'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.String(30))
    full_name = db.Column(db.String(120))
    start_date = db.Column(db.Date)
    status = db.Column(db.String(10))
    asset_id = db.Column(db.String(30))
    contact_no = db.Column(db.String(20))
    email = db.Column(db.String(100))


    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'full_name': self.full_name,
            'start_date': self.date.date() if self.date else None,
            'status': self.status,
            'asset_id': self.asset_id,
            'contact_no': self.contact_no,
            'email': self.email,
        }

    def __repr__(self):
        return f"<Notificationitam {self.id}>"