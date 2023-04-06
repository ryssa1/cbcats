
#   Programmer Name: Oey Ching Yi (TP 061246), Student, APU 
#   Program Name: CBCATS application
#   File Name: employeestatus.py
#   First Written on: Saturday, 11th February 2023
#   Edited On: Monday, 3rd April 2023 


from app import db



class Employeestatus(db.Model):
    __tablename__ = 'employeestatus'
    id = db.Column(db.Integer, primary_key=True)
    emp_status_id = db.Column(db.String(6), primary_key=True)
    status_name = db.Column(db.String(10))


    def to_dict(self):
        return {
            'id': self.id,
            'emp_status_id': self.emp_status_id,
            'status_name':self.status_name,
        }
    
    def __repr__(self):
        return f"<Employeestatus(id={self.id}, emp_status_id='{self.emp_status_id}', status_name='{self.status_name}')>"
