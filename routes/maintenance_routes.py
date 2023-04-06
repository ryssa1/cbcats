
#   Programmer Name: Oey Ching Yi (TP 061246), Student, APU 
#   Program Name: CBCATS application
#   File Name: maintenance_routes.py
#   First Written on: Saturday, 11th February 2023
#   Edited On: Monday, 3rd April 2023 

from flask import Blueprint,Flask, render_template,render_template_string,jsonify,request,flash,redirect,url_for,session
import sqlalchemy.types as types
from app import app
from models.supplier import Supplier
from models.company import Company
from models.asset import Asset
from models.employee import Employee
from models.status import Status
from models.maintenance import Maintenance  # configure model
from app import db
from datafunc import get_record

data_table = "maintenance" # configure model
maintenance_bp = Blueprint(data_table, __name__)

table_title = "MAINTENANCE INFO" # configure model
hide_columns = ['id']
tmp_titles = ['Maintenance ID',
              'Asset ID',
               'Employee ID',
               'Asset Type',
               'Company ID',
               'Location Name',
               'Date',
               'Status ID',
               'Description',
               'Inspected By',
               'Inpection Date',
               'Supplier ID']

searchable_col = ['maintenance_id',
'asset_id',
'employee_id',
'asset_type',
'company_ID',
'location_name',
'date',
'status_id',
'description',
'inspected_by',
'inspect_date',
'supplier_id']
 # configure model

column_titles = dict(zip(searchable_col, tmp_titles))


orderable_col = ['maintenance_id',
'asset_id'
'status_id',
'employee_id',
'asset_type',
'company_ID',
'location_name',
'date',
'status_id',
'description',
'inspected_by',
'inspect_date',
'supplier_id']
 # configure model

edit_flds = ['maintenance_id',
'asset_id'
'status_id',
'employee_id',
'asset_type',
'company_ID',
'location_name',
'date',
'status_id',
'description',
'inspected_by',
'inspect_date',
'supplier_id']
 # configure model

reqd_flds = ['maintenance_id',
'asset_id',
'status_id',
'employee_id',
'asset_type',
'company_ID',
'location_name',
'date',
'status_id']
 # configure model







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
def maintenance_table():

    session["HTML_TABLE"] = data_table + "_table.html"
    session["TABLE"] = data_table+"_data"
    session["UPDATE_URL"] ="update_"+data_table
    session["NEW_URL"] ="new_"+data_table
    session["DELETE_URL"] ="delete_"+data_table
    error_messages = {}
    all_columns = [column.key for column in Maintenance.__table__.columns]
    hide_columns = ['id']
    # columns = [col for col in all_columns if col not in hide_columns]
    columns = [col for col in all_columns]
    searchable_columns = searchable_col
    orderable_columns = orderable_col
    date_fields = ["date", "inspect_date"]
    edit_fields = edit_flds
    number_fields = []
    suppliers = Supplier.query.all()
    assets = Asset.query.all()
    companies = Company.query.all()
    employees = Employee.query.all()
    statuses = Status.query.all()
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
column_titles = column_titles, table_title=table_title, suppliers=suppliers, companies=companies, assets = assets, employees = employees, statuses=statuses, date_fields = date_fields)


@app.route('/update_'+data_table, methods=['POST'])
def update_maintenance(): # configure model
    print('UPDATE eeeeeeeeeeeeeeeeeeeeeeeeeee')
    session["HTML_TABLE"] = data_table + "_table.html"
    session["TABLE"] = data_table+"_data"
    session["UPDATE_URL"] ="update_"+data_table
    session["NEW_URL"] ="new_"+data_table
    session["DELETE_URL"] ="delete_"+data_table
    error_messages = {}
    all_columns = [column.key for column in Maintenance.__table__.columns]
    hide_columns = ['id']
    # columns = [col for col in all_columns if col not in hide_columns]
    columns = [col for col in all_columns]
    searchable_columns = searchable_col
    orderable_columns = orderable_col
    date_fields = ["date", "inspect_date"]
    edit_fields = edit_flds
    number_fields = []
    suppliers = Supplier.query.all()
    assets = Asset.query.all()
    companies = Company.query.all()
    employees = Employee.query.all()
    statuses = Status.query.all()
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
    chg_maintenance_id = data.get('maintenance_id').strip()
    ori_maintenance_id = ori_data['maintenance_id']
    print(chg_maintenance_id,ori_maintenance_id)
    if chg_maintenance_id != ori_maintenance_id and chg_maintenance_id.strip()!="":
        # check whether the new maintenance_id is being used by others
        chk_maintenance_id = get_record(data_table,"maintenance_id='"+chg_maintenance_id.strip()+"'")
        if chk_maintenance_id:
            error_messages['maintenance_id'] = "maintenance_id address not allowed. It is being used by others!"
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
          column_titles = column_titles, table_title=table_title, suppliers=suppliers, companies=companies, assets = assets, employees = employees, statuses=statuses, date_fields = date_fields)


@app.route('/new_'+data_table, methods=['POST'])
def add_maintenance(): # configure model
    print('NEWWWWWWWWWWWWWWWWWW')
    date_fields = ["date", "inspect_date"]
    data = request.form.to_dict()
    new_maintenance_id = data.get('maintenance_id').strip()
    # user = User.query.filter_by(maintenance_id=user_maintenance_id).first()
    new_acc = get_record(data_table,"maintenance_id='"+new_maintenance_id+"'")
    required_flds = reqd_flds
    error_messages = {}
    print('mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
    for itm in required_flds:
        info = data.get(itm)
        if info is None or info.strip() == "":
            error_messages[itm] = 'ERROR! {} is required'.format(itm)
    if new_acc:
        print("ERROR",data['maintenance_id'])
        error_messages['maintenance_id'] = 'ERROR! This maintenance_id already exist.'
    session['ERR_MSGS'] = error_messages
    print(error_messages)
    if new_acc is None and len(error_messages) == 0:
        newrec = Maintenance() # CONFIGURE model
        if ( data['supplier_id'] == None ):
            del data['supplier_id']
        if ( not data['inspect_date']):
            print('date!!!!!!!!!!!!!!!!!!!!!!!')
            del data['inspect_date']
        for key, value in data.items():
            if key != 'id':
                setattr(newrec, key, value)
        db.session.add(newrec)
        db.session.commit()
    succ = (len(session['ERR_MSGS']) == 0)
    return jsonify(success=succ)


@app.route('/delete_'+data_table+'/<int:id>', methods=['DELETE'])
def delete_maintenance(id): # configure model
    print('ddddddddddddddddddd')
    data = get_record(data_table,"id="+str(id))
    if data:
        db.session.delete(data)
        db.session.commit()
        return jsonify({'message': 'Record deleted successfully!'})
    else:
        return jsonify({'error': 'Record not found!'}), 404


@app.route('/supplierListM')
def supplierListM():
    suppliers = Supplier.query.all()
    print('uuuuuu', suppliers)
    return render_template(data_table+'_table.html', suppliers=suppliers)

@app.route('/companyListM')
def companyListM():
    companies = Company.query.all()
    print('uuuuuu', companies)
    return render_template(data_table+'_table.html', companies=companies)

@app.route('/assetListingM')
def assetListingM():
    assets = Asset.query.all()
    print('uuuuuu', assets)
    return render_template(data_table+'_table.html', assets=assets)

@app.route('/employeeListingM')
def employeeListingM():
    employees = Employee.query.all()
    print('uuuuuu', employees)
    return render_template(data_table+'_table.html', employees=employees)

@app.route('/statusListM')
def statusListingM():
    statuses = Status.query.all()
    print('uuuuuu', statuses)
    return render_template(data_table+'_table.html', statuses=statuses)


@app.route('/api/'+data_table+'_data')
def maintenance_data():
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