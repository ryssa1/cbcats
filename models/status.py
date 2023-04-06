
#   Programmer Name: Oey Ching Yi (TP 061246), Student, APU 
#   Program Name: CBCATS application
#   File Name: status.py
#   First Written on: Saturday, 11th February 2023
#   Edited On: Monday, 3rd April 2023 



from app import db

class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status_id = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(40))


    def to_dict(self):
        return {
            'id': self.id,
            'status_id': self.status_id,
            'name': self.name,

        }

    def __repr__(self):
        return f"<Status {self.status_id}>"