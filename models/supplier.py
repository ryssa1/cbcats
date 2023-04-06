
#   Programmer Name: Oey Ching Yi (TP 061246), Student, APU 
#   Program Name: CBCATS application
#   File Name: supplier.py
#   First Written on: Saturday, 11th February 2023
#   Edited On: Monday, 3rd April 2023 

from app import db


class Supplier(db.Model):
    __tablename__ = 'supplier'
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.String(30), index=True)
    company = db.Column(db.String(120))
    address = db.Column(db.String(200))
    postcode = db.Column(db.String(10))
    state = db.Column(db.String(30))
    country = db.Column(db.String(80))
    contact_name = db.Column(db.String(100))
    contact_no = db.Column(db.String(20))

    def to_dict(self):
        return {
            'id': self.id,
            'supplier_id': self.supplier_id,
            'company': self.company,
            'address': self.address,
            'postcode': self.postcode,
            'state': self.state,
            'country': self.country,
            'contact_name': self.contact_name,
            'contact_no': self.contact_no
        }

    def __repr__(self):
        return f'<Supplier {self.id}>'