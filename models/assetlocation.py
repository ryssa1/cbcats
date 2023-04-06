
#   Programmer Name: Oey Ching Yi (TP 061246), Student, APU 
#   Program Name: CBCATS application
#   File Name: assetlocation.py
#   First Written on: Saturday, 11th February 2023
#   Edited On: Monday, 3rd April 2023 

from app import db

class Assetlocation(db.Model):
    __tablename__ = 'assetlocation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_id = db.Column(db.String(30))
    date = db.Column(db.Date)
    asset_id = db.Column(db.String(30), db.ForeignKey('asset.asset_id'))
    company_ID = db.Column(db.String(30), db.ForeignKey('company.company_ID'))
    employee_id = db.Column(db.String(30), db.ForeignKey('employee.employee_id'))
    supplier_id = db.Column(db.String(30), db.ForeignKey('supplier.supplier_id'))

    def to_dict(self):
        return {
            'id': self.id,
            'location_id' : self.location_id, 
            'date': self.date.date() if self.date else None,
            'asset_id': self.asset_id,
            'company_ID': self.company_ID,
            'employee_id': self.employee_id,
            'supplier_id': self.supplier_id
        }
    
    def _repr_(self):
        return f'<Assetlocation {self.id}>'
