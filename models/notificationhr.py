
#   Programmer Name: Oey Ching Yi (TP 061246), Student, APU 
#   Program Name: CBCATS application
#   File Name: notificationhr.py
#   First Written on: Saturday, 11th February 2023
#   Edited On: Monday, 3rd April 2023 


from app import db



class Notificationhr(db.Model):
    __tablename__ = 'notificationhr'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(6), primary_key=True)
    email = db.Column(db.String(100))
    full_name = db.Column(db.String(120))
    position = db.Column(db.String(30))
    status = db.Column(db.String(10))
    contact_no = db.Column(db.String(20))
    department = db.Column(db.String(120))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'email':self.email,
            'full_name': self.full_name,
            'position': self.position,
            'status': self.status,
            'contact_no': self.contact_no,
            'department': self.department,
            'start_date': self.start_date.date() if self.start_date else None,
            'end_date': self.end_date.date() if self.end_date else None,
        }
    
    def __repr__(self):
        return f"<Notificationhr(id={self.id}, employee_id='{self.employee_id}', full_name='{self.full_name}')>"
    
