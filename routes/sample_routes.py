from flask import Blueprint,Flask, render_template,render_template_string,jsonify,request,flash,redirect,url_for,session
import sqlalchemy.types as types
from app import app
from models.users import User
from app import db


user_bp = Blueprint('user', __name__)
data_table = "user"

def get_record(table_name, recid):
    table = db.metadata.tables[table_name]
    return db.session.query(table).get(recid)

@app.route('/user')
def grid():
    session["HTML_TABLE"] = data_table+"_table.html"
    session["TABLE"] = data_table + "_data"
    session["UPDATE_URL"] ="update_"+data_table
    session["NEW_URL"] ="new_"+data_table
    session['USERTYPE'] = "HR"
    error_messages = {}
    all_columns = [column.key for column in User.__table__.columns]
    hide_columns = ['id']
    # columns = [col for col in all_columns if col not in hide_columns]
    columns = [col for col in all_columns]
    searchable_columns = ['name','age','address', 'email']
    orderable_columns = ['name', 'age', 'email']
    edit_fields = ['name', 'age', 'address', 'email']
    dtitles=["EMP Name","EMP Age","Address","Email"]
    number_fields = []
    # Loop through each column in your model
    # for column in User.__table__.columns:
    print("TTTTTT",db.metadata.tables)
    table = db.metadata.tables[data_table]
    for column in table.columns:
    # for column in db.metadata.tables[data_table]:
        # Check the column data type and append to the list
        if isinstance(column.type, types.Integer) or isinstance(column.type, types.Float):
            number_fields.append(column.key)
    #
    # print("FIELD TYPE ",number_fields)
    return render_template(data_table+'_table.html', columns=columns, searchable_columns=searchable_columns, orderable_columns=orderable_columns,
          number_fields=number_fields,error_messages=error_messages,edit_fields=edit_fields,hide_columns=hide_columns, table_title='User Table')


@app.route('/update_'+data_table, methods=['POST'])
def update_user():
    print("UUUUUUUUUUUPDATE")
    data = request.form.to_dict() #edited data
    recid = data.get('id') #get id that is being edited
    ori_data =User.query.get(recid) # get the original data before being edited
    required_flds = ['name','email','age','address','phone']
    error_messages = {}
    session['ERR_MSGS'] = {}
    for itm in required_flds:   # required fields should not be empty
        info = data.get(itm)
        if info is None or info.strip() == "":
            error_messages[itm] = 'ERROR! {} is required'.format(itm)
    tage = data.get('age')
    if tage.isnumeric() and int(tage) == 0:
        error_messages['age'] = "ERROR! Age must be greater than zero."
    user_email = data.get('email')
    ori_email = ori_data.email
    if user_email != ori_email:
        # check whether the new email is being used by others
        chk_email = User.query.filter_by(email=user_email).first()
        if chk_email:
            error_messages['email'] = "Email address not allowed. It is being used by others!"
    session['ERR_MSGS'] = error_messages
    print("EEEEEEEEEEEE",error_messages)
    if not session['ERR_MSGS']:
        user = User.query.get(recid)
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
    return render_template('table.html', error_messages=error_messages)


@app.route('/new_'+data_table, methods=['POST'])
def add_user():
    print("IIIIINSERTTTTT")
    data = request.form.to_dict()
    user_email = data.get('email')
    user_age = data.get('age')
    user = User.query.filter_by(email=user_email).first()
    required_flds = ['name','email','age','address','phone']
    error_messages = {}
    for itm in required_flds:
        info = data.get(itm)
        if info is None or info.strip() == "":
            error_messages[itm] = 'ERROR! {} is required'.format(itm)
    if user:
        print("ERROR",data['email'])
        error_messages['email'] = 'ERROR! This email already exist.'
        flash('ERROR! This email already exist.', category='error')

    if not user_age.strip() == "" and not user_age.isnumeric():
        error_messages['age'] = 'ERROR! Age must be numeric'
        # return jsonify(success=False, message='ERROR! Age is required ')
    if data['email'].strip() == "":
        error_messages['email'] = 'ERROR! Email address is required.'
        # return jsonify(success=False, message='ERROR! Email address is required ')
    session['ERR_MSGS'] = error_messages
    if user is None and len(error_messages) == 0:
        newrec = User()
        for key, value in data.items():
            if key != 'id':
                setattr(newrec, key, value)
        db.session.add(newrec)
        db.session.commit()
        flash('Successfully saved,', 'success')
        # return jsonify(success=True)
    print("ERROR MSGSSS" ,error_messages)

    # if len(error_messages) > 0:
    #     session['ERR_MSGS'] = error_messages
    # else:
    #     session.pop('ERR_MSGS', None)
    succ = (len(session['ERR_MSGS']) == 0)
    return jsonify(success=succ)


@app.route('/delete_'+data_table+'/<int:id>', methods=['DELETE'])
def delete_users(id): # configure model
    data = get_record(data_table,"id="+str(id))
    if data:
        db.session.delete(data)
        db.session.commit()
        return jsonify({'message': 'Record deleted successfully!'})
    else:
        return jsonify({'error': 'Record not found!'}), 404

@app.route('/api/'+data_table+'_data')
def user_data():
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