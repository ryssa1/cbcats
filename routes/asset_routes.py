
#   Programmer Name: Oey Ching Yi (TP 061246), Student, APU 
#   Program Name: CBCATS application
#   File Name: asset_routes.py
#   First Written on: Saturday, 11th February 2023
#   Edited On: Monday, 3rd April 2023 

from flask import Blueprint,Flask, render_template,render_template_string,jsonify,request,flash,redirect,url_for,session
import sqlalchemy.types as types
from app import app
from models.supplier import Supplier
from models.asset import Asset  # configure model
from app import db
from datafunc import get_record

data_table = "asset" # configure model
asset_bp = Blueprint(data_table, __name__)

table_title = "ASSET INFO" # configure model
hide_columns = ['id']
tmp_titles = ['Asset ID',
               'Supplier ID',
               'Brand',
               'Model',
               'Type',
               'Description',
               'Serial No']

searchable_col = ['asset_id',
'supplier_id',
'brand',
'model',
'type',
'description',
'serial_no'] # configure model

column_titles = dict(zip(searchable_col, tmp_titles))


orderable_col = ['asset_id',
'supplier_id',
'brand',
'model',
'type',
'description',
'serial_no'] # configure model

edit_flds = ['asset_id',
'supplier_id',
'brand',
'model',
'type',
'description',
'serial_no'] # configure model

reqd_flds = ['asset_id',
'supplier_id',
'brand',
'model',
'type',
'description',
'serial_no'] # configure model



@app.route('/'+data_table)
def asset_table():

    session["HTML_TABLE"] = data_table + "_table.html"
    session["TABLE"] = data_table+"_data"
    session["UPDATE_URL"] ="update_"+data_table
    session["NEW_URL"] ="new_"+data_table
    session["DELETE_URL"] ="delete_"+data_table
    error_messages = {}
    all_columns = [column.key for column in Asset.__table__.columns]
    hide_columns = ['id']
    # columns = [col for col in all_columns if col not in hide_columns]
    columns = [col for col in all_columns]
    searchable_columns = searchable_col
    orderable_columns = orderable_col
    date_fields = ["date"]
    suppliers = Supplier.query.all()
    edit_fields = edit_flds
    number_fields = []
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
column_titles = column_titles, table_title=table_title, suppliers=suppliers, date_fields = date_fields)


@app.route('/update_'+data_table, methods=['POST'])
def update_asset(): # configure model
    session["HTML_TABLE"] = data_table + "_table.html"
    session["TABLE"] = data_table+"_data"
    session["UPDATE_URL"] ="update_"+data_table
    session["NEW_URL"] ="new_"+data_table
    session["DELETE_URL"] ="delete_"+data_table
    error_messages = {}
    all_columns = [column.key for column in Asset.__table__.columns]
    hide_columns = ['id']
    # columns = [col for col in all_columns if col not in hide_columns]
    columns = [col for col in all_columns]
    searchable_columns = searchable_col
    orderable_columns = orderable_col
    date_fields = ["date"]
    edit_fields = edit_flds
    number_fields = []
    suppliers = Supplier.query.all()
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
    chg_asset_id = data.get('asset_id').strip()
    ori_asset_id = ori_data['asset_id']
    print(chg_asset_id,ori_asset_id)
    if chg_asset_id != ori_asset_id and chg_asset_id.strip()!="":
        # check whether the new asset_id is being used by others
        chk_asset_id = get_record(data_table,"asset_id='"+chg_asset_id.strip()+"'")
        if chk_asset_id:
            error_messages['asset_id'] = "asset_id address not allowed. It is being used by others!"
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
          column_titles = column_titles, table_title=table_title, suppliers=suppliers, date_fields = date_fields)


@app.route('/new_'+data_table, methods=['POST'])
def add_asset(): # configure model
    print('uuuuuuuuuuuuuuuu')
    date_fields = ["date"]
    data = request.form.to_dict()
    new_asset_id = data.get('asset_id').strip()
    # user = User.query.filter_by(asset_id=user_asset_id).first()
    new_acc = get_record(data_table,"asset_id='"+new_asset_id+"'")
    required_flds = reqd_flds
    error_messages = {}
    for itm in required_flds:
        info = data.get(itm)
        if info is None or info.strip() == "":
            error_messages[itm] = 'ERROR! {} is required'.format(itm)
    if new_acc:
        print("ERROR",data['asset_id'])
        error_messages['asset_id'] = 'ERROR! This asset_id already exist.'
    session['ERR_MSGS'] = error_messages
    print(error_messages)
    if new_acc is None and len(error_messages) == 0:
        newrec = Asset() # CONFIGURE model
        for key, value in data.items():
            if key != 'id':
                setattr(newrec, key, value)
        db.session.add(newrec)
        db.session.commit()
    succ = (len(session['ERR_MSGS']) == 0)
    return jsonify(success=succ)


@app.route('/delete_'+data_table+'/<int:id>', methods=['DELETE'])
def delete_asset(id): # configure model
    print('ddddddddddddddddddd')
    data = get_record(data_table,"id="+str(id))
    if data:
        db.session.delete(data)
        db.session.commit()
        return jsonify({'message': 'Record deleted successfully!'})
    else:
        return jsonify({'error': 'Record not found!'}), 404


@app.route('/supplierList_a')
def supplierList_a():
    suppliers = Supplier.query.all()
    print('uuuuuu', suppliers)
    return render_template(data_table+'_table.html', suppliers=suppliers)



@app.route('/api/'+data_table+'_data')
def asset_data():
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