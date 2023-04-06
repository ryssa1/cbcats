
#   Programmer Name: Oey Ching Yi (TP 061246), Student, APU 
#   Program Name: CBCATS application
#   File Name: assetlocation_routes.py
#   First Written on: Saturday, 11th February 2023
#   Edited On: Monday, 3rd April 2023 

from flask import Blueprint,Flask, render_template,render_template_string,jsonify,request,flash,redirect,url_for,session
import sqlalchemy.types as types
from app import app
from models.supplier import Supplier
from models.company import Company
from models.asset import Asset
from models.employee import Employee
from models.location import Location
from models.assetlocation import Assetlocation  # configure model
from datetime import datetime
from app import db
from datafunc import get_record

data_table = "assetlocation" # configure model
assetlocation_bp = Blueprint(data_table, __name__)

table_title = "ASSET MOVEMENT INFO" # configure model
hide_columns = ['id']
tmp_titles = ['Location ID',
              'Asset ID',
               'Company ID',
               'Date',
               'Employee ID',
               'Supplier ID']
searchable_col = ['location_id',
'asset_id',
'company_ID',
'date',
'employee_id',
'supplier_id'] # configure model

column_titles = dict(zip(searchable_col, tmp_titles))


orderable_col = ['location_id',
'asset_id',
'company_ID',
'date',
'employee_id',
'supplier_id'] # configure model

edit_flds = ['location_id',
'asset_id',
'company_ID',
'date',
'employee_id',
'supplier_id'] # configure model

reqd_flds = ['location_id',
'asset_id',
'company_ID',
'date'] # configure model







# @app.route('/reset_errors',methods=['GET'])
# def reset_errors():
#     if 'ERR_MSGS' in session:
#         session.pop('ERR_MSGS', None)
#     session['ERR_MSGS'] = {}
#     # print('RESETTING session',session['ERR_MSGS'])
#     return redirect(url_for(session["HTML_TABLE"]))
#     # succ = (len(session['ERR_MSGS']) == 0)
#     # return jsonify(success=succ)
#
#
# @app.route('/get_errors',methods=['GET'])
# def get_errors():
#     print(session['ERR_MSGS'])
#     return redirect(url_for(session["HTML_TABLE"]))


@app.route('/'+data_table)
def assetlocation_table():

    session["HTML_TABLE"] = data_table + "_table.html"
    session["TABLE"] = data_table+"_data"
    session["UPDATE_URL"] ="update_"+data_table
    session["NEW_URL"] ="new_"+data_table
    session["DELETE_URL"] ="delete_"+data_table
    error_messages = {}
    all_columns = [column.key for column in Assetlocation.__table__.columns]
    hide_columns = ['id']
    # columns = [col for col in all_columns if col not in hide_columns]
    columns = [col for col in all_columns]
    searchable_columns = searchable_col
    orderable_columns = orderable_col
    date_fields = ["date"]
    edit_fields = edit_flds
    number_fields = []
    suppliers = Supplier.query.all()
    assets = Asset.query.all()
    companies = Company.query.all()
    employees = Employee.query.all()
    locations = Location.query.all()
    # Loop through each column in your model
    # for column in User.__table__.columns:
    table = db.metadata.tables[data_table]
    for column in table.columns:
    # for column in db.metadata.tables[data_table]:
        # Check the column data type and append to the list
        if isinstance(column.type, types.Integer) or isinstance(column.type, types.Float):
            number_fields.append(column.key)

    return render_template(data_table+'_table.html', columns=columns, searchable_columns=searchable_columns, orderable_columns=orderable_columns,
          number_fields=number_fields,error_messages=error_messages,edit_fields=edit_fields,hide_columns=hide_columns, 
column_titles = column_titles, table_title=table_title, suppliers=suppliers, companies=companies, assets = assets, employees = employees,locations=locations, date_fields = date_fields)


@app.route('/update_'+data_table, methods=['POST'])
def update_assetlocation(): # configure model
    session["HTML_TABLE"] = data_table + "_table.html"
    session["TABLE"] = data_table+"_data"
    session["UPDATE_URL"] ="update_"+data_table
    session["NEW_URL"] ="new_"+data_table
    session["DELETE_URL"] ="delete_"+data_table
    error_messages = {}
    all_columns = [column.key for column in Assetlocation.__table__.columns]
    hide_columns = ['id']
    # columns = [col for col in all_columns if col not in hide_columns]
    columns = [col for col in all_columns]
    searchable_columns = searchable_col
    orderable_columns = orderable_col
    date_fields = ["date"]
    edit_fields = edit_flds
    number_fields = []
    suppliers = Supplier.query.all()
    assets = Asset.query.all()
    companies = Company.query.all()
    employees = Employee.query.all()
    locations = Location.query.all()
    data = request.form.to_dict() #edited data
    recid = data.get('id') #get id that is being edited
    ori_data = get_record(data_table,'id='+recid,1) # get the original data before being edited
    required_flds = reqd_flds
    error_messages = {}
    session['ERR_MSGS'] = {}
    for itm in required_flds:   # required fields should not be empty
        info = data.get(itm)
        if info is None or info.strip() == "":
            error_messages[itm] = 'ERROR! {} is required'.format(itm)
    chg_asset_id = data.get('asset_id')
    ori_asset_id = ori_data['asset_id']
    chg_date = data.get('date')
    ori_date = ori_data['date']
    chg_location_id = data.get('location_id')
    ori_location_id = ori_data['location_id']
    print(chg_location_id,ori_location_id)
    if chg_location_id != ori_location_id or chg_asset_id != ori_asset_id or chg_date != ori_date:
        date_str = data["date"]
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
        # check if asset id, location id and date is the same as existing records
        chk_location_id = get_record(data_table,"location_id='"+chg_location_id+"' and date ='" + formatted_date +"' and asset_id ='" + data['asset_id']+"'")
        if chk_location_id:
            error_messages['location_id'] = "Location ID , Asset ID and Date already exist!"
    session['ERR_MSGS'] = error_messages
    print(error_messages)
    if len(session['ERR_MSGS']) == 0:
        acc = get_record(data_table,"id="+recid)
        for key, value in data.items():
            if key != "id":
                setattr(acc, key, value)
        db.session.commit()
    return render_template(data_table+'_table.html', columns=columns, searchable_columns=searchable_columns, orderable_columns=orderable_columns,
          number_fields=number_fields,error_messages=error_messages,edit_fields=edit_fields,hide_columns=hide_columns,
          column_titles = column_titles, table_title=table_title, suppliers=suppliers, companies=companies, assets = assets, employees = employees, locations=locations, date_fields = date_fields)


@app.route('/new_'+data_table, methods=['POST'])
def add_assetlocation(): # configure model
    print('uuuuuuuuuuuuuuuu')
    date_fields = ["date"]
    data = request.form.to_dict()
    new_location_id = data.get('location_id').strip()
    # user = User.query.filter_by(location_id=user_location_id).first()
    date_str = data["date"]
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')    
    new_acc = get_record(data_table,"date ='" + formatted_date +"' and asset_id ='" + data['asset_id']+"'")
    required_flds = reqd_flds
    error_messages = {}
    for itm in required_flds:
        info = data.get(itm)
        if info is None or info.strip() == "":
            error_messages[itm] = 'ERROR! {} is required'.format(itm)
    if new_acc:
        print("ERROR",data['location_id'])
        error_messages['location_id'] = 'ERROR! This asset ID  and date already exist.'
    session['ERR_MSGS'] = error_messages
    print(error_messages)
    if new_acc is None and len(error_messages) == 0:
        newrec = Assetlocation() # CONFIGURE model
        for key, value in data.items():
            if key != 'id':
                setattr(newrec, key, value)
        db.session.add(newrec)
        db.session.commit()
    succ = (len(session['ERR_MSGS']) == 0) 
    print("ADDINGGGGGG")
    return jsonify(success=succ)


@app.route('/delete_'+data_table+'/<int:id>', methods=['DELETE'])
def delete_assetlocation(id): # configure model
    print('ddddddddddddddddddd')
    data = get_record(data_table,"id="+str(id))
    if data:
        db.session.delete(data)
        db.session.commit()
        return jsonify({'message': 'Record deleted successfully!'})
    else:
        return jsonify({'error': 'Record not found!'}), 404


@app.route('/supplierList')
def supplierList():
    suppliers = Supplier.query.all()
    print('uuuuuu', suppliers)
    return render_template(data_table+'_table.html', suppliers=suppliers)

@app.route('/companyList')
def companyList():
    companies = Company.query.all()
    print('uuuuuu', companies)
    return render_template(data_table+'_table.html', companies=companies)

@app.route('/assetListing')
def assetListing():
    assets = Asset.query.all()
    print('uuuuuu', assets)
    return render_template(data_table+'_table.html', assets=assets)

@app.route('/employeeListing')
def employeeListing():
    employees = Employee.query.all()
    print('uuuuuu', employees)
    return render_template(data_table+'_table.html', employees=employees)

@app.route('/locationList')
def locationList():
    locations = Location.query.all()
    print('uuuuuu', locations)
    return render_template(data_table+'_table.html', locations=locations)


@app.route('/api/'+data_table+'_data')
def assetlocation_data():
    table = db.metadata.tables[data_table]
    query = db.session.query(table).all()
    return {'data': [row._asdict() for row in query]}

# def data():
#     return {'data': [user.to_dict() for user in User.query]}

# def data():
#     table_name = "User"
#     table = db.metadata.tables[table_name]
#     query = db.session.query(table).all()
#     return {'data': [row._asdict() for row in query]}