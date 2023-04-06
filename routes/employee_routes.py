
#   Programmer Name: Oey Ching Yi (TP 061246), Student, APU 
#   Program Name: CBCATS application
#   File Name: employee_routes.py
#   First Written on: Saturday, 11th February 2023
#   Edited On: Monday, 3rd April 2023 


from flask import Blueprint,Flask, render_template,render_template_string,jsonify,request,flash,redirect,url_for,session
import sqlalchemy.types as types
from app import app
from models.usertype import UserType
from models.employeestatus import Employeestatus
from models.employee import Employee  # configure model
from app import db
from datafunc import get_record


data_table = "employee" # configure model
employee_bp = Blueprint(data_table, __name__)

table_title = "EMPLOYEE INFO" # configure model
hide_columns = ['id','password']
tmp_titles = ['Employee ID',
'Email',
'Full Name',
'User Type',
'Position',
'Status',
'Gender',
'Date Of Birth',
'Contact No',
'Address',
'State',
'Postcode',
'Country',
'Department',
'Start Date',
'End Date'] 

searchable_col = ['employee_id',
'email',
'full_name',
'user_type',
'position',
'status',
'gender',
'dob',
'contact_no',
'address',
'state',
'postcode',
'country',
'department',
'start_date',
'end_date'] # configure model

column_titles = dict(zip(searchable_col, tmp_titles))

orderable_col = ['employee_id',
'email',
'full_name',
'password',
'user_type',
'position',
'status',
'gender',
'dob',
'contact_no',
'address',
'state',
'postcode',
'country',
'department',
'start_date',
'end_date']
 # configure model

edit_flds = ['employee_id',
'email',
'full_name',
'password',
'user_type',
'position',
'status',
'gender',
'dob',
'contact_no',
'address',
'state',
'postcode',
'country',
'department',
'start_date',
'end_date'] # configure model

reqd_flds = ['employee_id',
'email',
'full_name',
'position',
'status',
'gender',
'dob',
'contact_no',
'address',
'state',
'postcode',
'country',
'department',
'start_date'] # configure model







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
def employee_table():

    session["HTML_TABLE"] = data_table + "_table.html"
    session["TABLE"] = data_table+"_data"
    session["UPDATE_URL"] ="update_"+data_table
    session["NEW_URL"] ="new_"+data_table
    session["DELETE_URL"] = "delete_"+data_table
    error_messages = {}
    all_columns = [column.key for column in Employee.__table__.columns]

    # columns = [col for col in all_columns if col not in hide_columns]
    columns = [col for col in all_columns]
    searchable_columns = searchable_col
    orderable_columns = orderable_col
    date_fields = ["dob","start_date","end_date"]
    if session["usertype"] == "HR":
        edit_fields = edit_flds
        hide_columns = ['id','user_type', 'password'] 

    else:
        edit_fields = ["user_type"] 
        hide_columns = ['id','status', 'gender', 'dob', 'contact_no', 'address', 'postcode', 'country', 'department', 'start_date', 'end_date']


    number_fields = []
    user_types = UserType.query.all()
    employee_statuses = Employeestatus.query.all()
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
          column_titles = column_titles, table_title=table_title, user_types=user_types, employee_statuses = employee_statuses, date_fields = date_fields)



@app.route('/update_'+data_table, methods=['POST'])
def update_employee(): # configure model
    print('UPDATEEEEEE')
    session["HTML_TABLE"] = data_table + "_table.html"
    session["TABLE"] = data_table+"_data"
    session["UPDATE_URL"] ="update_"+data_table
    session["NEW_URL"] ="new_"+data_table
    error_messages = {}
    all_columns = [column.key for column in Employee.__table__.columns]

    # columns = [col for col in all_columns if col not in hide_columns]
    columns = [col for col in all_columns]
    searchable_columns = searchable_col
    orderable_columns = orderable_col
    required_flds = ['employee_id',
                    'email',
                    'full_name',
                    'position',
                    'status',
                    'gender',
                    'dob',
                    'contact_no',
                    'address',
                    'state',
                    'postcode',
                    'country',
                    'department',
                    'start_date']
    date_fields = ["dob","start_date","end_date"]
    if session["usertype"] == "HR":
        edit_fields = edit_flds
        hide_columns = ['id','user_type', 'password'] 

    else:
        edit_fields = ["user_type"] 
        hide_columns = ['id','status', 'gender', 'dob', 'contact_no', 'address', 'postcode', 'country', 'department', 'start_date', 'end_date']
        required_flds = ['employee_id',
                    'email',
                    'full_name',
                    'department']

    number_fields = []
    user_types = UserType.query.all()
    employee_statuses = Employeestatus.query.all()
    data = request.form.to_dict() #edited data
    recid = data.get('id') #get id that is being edited
    ori_data = get_record(data_table,'id='+recid,1) # get the original data before being edited
    error_messages = {}
    session['ERR_MSGS'] = {}
    for itm in required_flds:   # required fields should not be empty
        if ( itm == 'status' ):
            info = data.get('emp_status_id')
        else:
            info = data.get(itm)
        if info is None or info.strip() == "":
            error_messages[itm] = 'ERROR! {} is required'.format(itm)
    chg_employee_id = data.get('employee_id')
    ori_employee_id = ori_data['employee_id']
    if chg_employee_id != ori_employee_id and chg_employee_id.strip()!="":
        # check whether the new employee_id is being used by others
        chk_employee_id = get_record(data_table,"employee_id='"+chg_employee_id.strip()+"'")
        if chk_employee_id:
            error_messages['employee_id'] = "employee_id address not allowed. It is being used by others!"
    session['ERR_MSGS'] = error_messages
    print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',error_messages )
    if len(session['ERR_MSGS']) == 0:
        acc = get_record(data_table,"id="+recid)
        if(not data["end_date"]):
            del data["end_date"]
        # if (session["usertype"] == "ITAM"):
        #     for dt in date_fields:
        #         del data[dt]
        for key, value in data.items():
            if key != "id":
                print('KEY VALUE',key, value)
                if ( key == 'emp_status_id' ):
                    setattr(acc, 'status', value)    
                else:
                    setattr(acc, key, value)
        db.session.commit()
    return render_template(data_table+'_table.html', columns=columns, searchable_columns=searchable_columns, orderable_columns=orderable_columns,
          number_fields=number_fields,error_messages=error_messages,edit_fields=edit_fields,hide_columns=hide_columns,
          column_titles = column_titles, table_title=table_title, user_types=user_types, employee_statuses = employee_statuses, date_fields = date_fields)
    # return render_template(data_table+'_table.html', error_messages=error_messages)


@app.route('/new_'+data_table, methods=['POST'])
def add_employee(): # configure model
    print('ADDDINGGGG')
    data = request.form.to_dict()
    new_employee_id = data.get('employee_id').strip()
    # user = User.query.filter_by(employee_id=user_employee_id).first()
    new_acc = get_record(data_table,"employee_id='"+new_employee_id+"'")
    required_flds = reqd_flds
    error_messages = {}
    for itm in required_flds:   # required fields should not be empty
        if ( itm == 'status' ):
            info = data.get('emp_status_id')
        else:
            info = data.get(itm)
        if info is None or info.strip() == "":
            error_messages[itm] = 'ERROR! {} is required'.format(itm)
    if new_acc:
        print("ERROR",data['employee_id'])
        error_messages['employee_id'] = 'ERROR! This employee_id already exist.'
    session['ERR_MSGS'] = error_messages
    print(error_messages)
    if new_acc is None and len(error_messages) == 0:
        newrec = Employee() # CONFIGURE model
        if(not data["end_date"]):
            del data["end_date"]
        for key, value in data.items():
           if key != "id":
                print('KEY VALUE',key, value)
                if ( key == 'emp_status_id' ):
                    setattr(newrec, 'status', value)    
                else:
                    setattr(newrec, key, value)
        db.session.add(newrec)
        db.session.commit()
    succ = (len(session['ERR_MSGS']) == 0)
    return jsonify(success=succ)


@app.route('/delete_'+data_table+'/<int:id>', methods=['DELETE'])
def delete_employee(id): # configure model
    data = get_record(data_table,"id="+str(id))
    if data:
        db.session.delete(data)
        db.session.commit()
        return jsonify({'message': 'Record deleted successfully!'})
    else:
        return jsonify({'error': 'Record not found!'}), 404


@app.route('/usertypeList')
def usertypeList():
    # fetch user types from the database
    user_types = UserType.query.all()
    return render_template(data_table+'_table.html', user_types=user_types)

@app.route('/empstatusList')
def empstatusList():
    # fetch user types from the database
    employee_statuses = Employeestatus.query.all()
    return render_template(data_table+'_table.html', employee_statuses=employee_statuses)


@app.route('/api/'+data_table+'_data')
def employee_data():
    table = db.metadata.tables[data_table]
    if ( session['usertype'] == 'HR'):
        query = db.session.query(table).all()
    else:
        query = db.session.query(table).filter(table.c.status == 'ES01').all()
    return {'data': [row._asdict() for row in query]}





