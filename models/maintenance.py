
#   Programmer Name: Oey Ching Yi (TP 061246), Student, APU 
#   Program Name: CBCATS application
#   File Name: maintenance.py
#   First Written on: Saturday, 11th February 2023
#   Edited On: Monday, 3rd April 2023 

from app import db


class Maintenance(db.Model):
    __tablename__ = 'maintenance'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    maintenance_id = db.Column(db.String(30), primary_key=True)
    asset_id = db.Column(db.String(30), db.ForeignKey('asset.asset_id'))
    employee_id = db.Column(db.String(30), db.ForeignKey('employee.employee_id'))
    asset_type = db.Column(db.String(60))
    company_ID = db.Column(db.String(30), db.ForeignKey('company.company_ID'))
    location_name = db.Column(db.String(30))
    date = db.Column(db.Date)
    status_id = db.Column(db.String(30), db.ForeignKey('status.status_id'))
    description = db.Column(db.String(120))
    inspected_by = db.Column(db.String(30))
    inspect_date = db.Column(db.Date)
    supplier_id = db.Column(db.String(30), db.ForeignKey('supplier.supplier_id'))


    def to_dict(self):
        return {
            'id': self.id,
            'maintenance_id': self.maintenance_id,
            'asset_id': self.asset_id,
            'employee_id': self.employee_id,
            'asset_type': self.asset_type,
            'company_ID': self.company_ID,
            'location_name': self.location_name,
            'date': self.date.date(),
            'status_id': self.status_id,
            'description':self.description,
            'inspected_by': self.inspected_by,
            'inspect_date': self.inspect_date.date() if self.inspect_date else None,
            'supplier_id': self.supplier_id
        }

    def __repr__(self):
        return f'<AssetStatus {self.id}>'
