
#   Programmer Name: Oey Ching Yi (TP 061246), Student, APU 
#   Program Name: CBCATS application
#   File Name: asset.py
#   First Written on: Saturday, 11th February 2023
#   Edited On: Monday, 3rd April 2023 



from app import db

class Asset(db.Model):
    __tablename__ = 'asset'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    asset_id = db.Column(db.String(30), primary_key=True)
    supplier_id = db.Column(db.String(30), db.ForeignKey('supplier.supplier_id'))
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    type = db.Column(db.String(60))
    description = db.Column(db.String(256))
    serial_no = db.Column(db.String(80))

    def to_dict(self):
        return {
            'id': self.id,
            'asset_id': self.asset_id,
            'supplier_id': self.supplier_id,
            'brand': self.brand,
            'model': self.model,
            'type': self.type,
            'description': self.description,
            'serial_no': self.serial_no
        }

    def __repr__(self):
        return f"<Asset {self.asset_id}>"