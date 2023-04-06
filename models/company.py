
#   Programmer Name: Oey Ching Yi (TP 061246), Student, APU 
#   Program Name: CBCATS application
#   File Name: company.py
#   First Written on: Saturday, 11th February 2023
#   Edited On: Monday, 3rd April 2023 


from app import db


class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    company_ID = db.Column(db.String(30), index=True)
    name = db.Column(db.String(120))
    address = db.Column(db.String(200))
    postcode = db.Column(db.String(6))
    state = db.Column(db.String(30))
    country = db.Column(db.String(80))

    def to_dict(self):
        return {
            'id': self.id,
            'company_ID': self.company_ID,
            'name': self.name,
            'address': self.address,
            'postcode': self.postcode,
            'state': self.state,
            'country': self.country,
        }
    
    def __repr__(self):
        return f'<Company {self.company_ID}>'