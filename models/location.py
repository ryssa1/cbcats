
#   Programmer Name: Oey Ching Yi (TP 061246), Student, APU 
#   Program Name: CBCATS application
#   File Name: location.py
#   First Written on: Saturday, 11th February 2023
#   Edited On: Monday, 3rd April 2023 


from app import db

class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_id = db.Column(db.String(30))
    location_name = db.Column(db.String(45))

    def to_dict(self):
        return {
            'id': self.id,
            'location_id' : self.location_id, 
            'location_name' : self.location_name
        }
    
    def _repr_(self):
        return f'<Location {self.id}>'
