
#   Programmer Name: Oey Ching Yi (TP 061246), Student, APU 
#   Program Name: CBCATS application
#   File Name: notificationhr_routes.py
#   First Written on: Saturday, 11th February 2023
#   Edited On: Monday, 3rd April 2023 


from flask import Blueprint,Flask, render_template,render_template_string,jsonify,request,flash,redirect,url_for,session
import sqlalchemy.types as types
from app import app
from models.notificationhr import Notificationhr  # configure model
from app import db
from datafunc import get_record

data_table = "notificationhr" # configure model
notificationhr_bp = Blueprint(data_table, __name__)

table_title = "NOTIFICATION INFO" # configure model
hide_columns = ['id']
tmp_titles = ['Employee ID',
 'Full name',
 'Email',
 'Contact number',
 'Status',
 'Position',
 'Department',
 'Start_date',
 'End_date']

searchable_col = ['employee_id',
 'full_name',
 'email',
 'contact_no',
 'status',
 'position',
 'department',
 'start_date',
 'end_date'] # configure model

column_titles = dict(zip(searchable_col, tmp_titles))


orderable_col = ['employee_id',
 'full_name',
 'email',
 'contact_no',
 'status',
 'position',
 'department',
 'start_date',
 'end_date'] # configure model

# edit_flds = ['employee_id',
#             'full_name',
#             'start_date',
#             'asset_id',
#             'contact_no',
#             'email' ] # configure model

# reqd_flds = ['employee_id',
#             'full_name',
#             'start_date',
#             'asset_id',
#             'contact_no',
#             'email' ] # configure model



@app.route('/'+data_table)
def notificationhr_table():

    session["HTML_TABLE"] = data_table + "_table.html"
    session["TABLE"] = data_table+"_data"
    error_messages = {}
    all_columns = [column.key for column in Notificationhr.__table__.columns]
    hide_columns = ['id']
    columns = [col for col in all_columns]
    searchable_columns = searchable_col
    orderable_columns = orderable_col
    date_fields = ["start_date", "end_date"]  # Add end_date to date_fields
    number_fields = []
    # Loop through each column in your model
    # for column in User.__table__.columns:
    table = db.metadata.tables[data_table]
    for column in table.columns:
    # for column in db.metadata.tables[data_table]:
        # Check the column data type and append to the list
        if isinstance(column.type, types.Integer) or isinstance(column.type, types.Float):
            number_fields.append(column.key)

    return render_template('dashboardHR.html', columns=columns, searchable_columns=searchable_columns, orderable_columns=orderable_columns,
          number_fields=number_fields,error_messages=error_messages, hide_columns=hide_columns, 
column_titles = column_titles, table_title=table_title, date_fields = date_fields)


@app.route('/api/'+data_table+'_data')
def notificationhr_data():
    table = db.metadata.tables[data_table]
    query = db.session.query(table).all()
    return {'data': [row._asdict() for row in query]}


@app.route('/api/notificationhr_items')
def get_notificationhr_items():
    notificationhr_items = Notificationhr.query.all()
    results = []
    for item in notificationhr_items:
        result = {
            'id': item.id,
            'employee_id': item.employee_id,
            'email': item.email,
            'full_name': item.full_name,
            'position': item.position,
            'status': item.status,
            'contact_no': item.contact_no,
            'department': item.department,
            'start_date': item.start_date,
            'end_date': item.end_date
        }
        results.append(result)
    return jsonify(results)


@app.route('/notificationhr')
def notifyhr_table():
    query = """
        SELECT 
          `employee`.`id` AS `id`,
          `employee`.`employee_id` AS `employee_id`,
          `employee`.`full_name` AS `full_name`,
          `employee`.`email` AS `email`,
          `employee`.`contact_no` AS `contact_no`,
          `employee`.`status` AS `status`,
          `employee`.`position` AS `position`,
          `employee`.`department` AS `department`,
          `employee`.`start_date` AS `start_date`,
          `employee`.`end_date` AS `end_date`
        FROM 
          `employee`
        WHERE 
          `employee`.`end_date` BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 2 WEEK)  # Add condition for end_date
        ORDER BY 
          `employee`.`end_date` ASC
    """
    results = db.engine.execute(query)
    columns = results.keys()
    rows = [dict(zip(columns, row)) for row in results]
    return {'data': rows}


# @app.route('/'+data_table)
# def notificationhr_table():

#     session["HTML_TABLE"] = data_table + "_table.html"
#     session["TABLE"] = data_table+"_data"
#     error_messages = {}
#     all_columns = [column.key for column in Notificationhr.__table__.columns]
#     hide_columns = ['id']
#     columns = [col for col in all_columns]
#     searchable_columns = searchable_col
#     orderable_columns = orderable_col
#     date_fields = ["start_date"]
#     number_fields = []
#     # Loop through each column in your model
#     # for column in User.__table__.columns:
#     table = db.metadata.tables[data_table]
#     for column in table.columns:
#     # for column in db.metadata.tables[data_table]:
#         # Check the column data type and append to the list
#         if isinstance(column.type, types.Integer) or isinstance(column.type, types.Float):
#             number_fields.append(column.key)

#     return render_template('DashboardHR.html', columns=columns, searchable_columns=searchable_columns, orderable_columns=orderable_columns,
#           number_fields=number_fields,error_messages=error_messages, hide_columns=hide_columns, 
# column_titles = column_titles, table_title=table_title, date_fields = date_fields)


# @app.route('/api/'+data_table+'_data')
# def notificationhr_data():
#     table = db.metadata.tables[data_table]
#     query = db.session.query(table).all()
#     return {'data': [row._asdict() for row in query]}


# @app.route('/api/notification_items')
# def get_notification_items():
#     notification_items = Notificationhr.query.all()
#     results = []
#     for item in notification_items:
#         result = {
#             'id': item.id,
#             'employee_id': item.employee_id,
#             'full_name': item.full_name,
#             'start_date': item.start_date,
#             'status': item.status,
#             'asset_id': item.asset_id,
#             'contact_no': item.contact_no,
#             'email': item.email
#         }
#         results.append(result)
#     return jsonify(results)


# @app.route('/notificationhr')
# def notifyhr_table():
#     query = """
#         SELECT ROW_NUMBER() OVER (ORDER BY 'employee'.'start_date' DESC) AS 'id',
#         'employee'.'employee_id' AS 'employee_id',
#         'employee'.'full_name' AS 'full_name',
#         'employee'.'start_date' AS 'start_date',
#         'employee'.'status' AS 'status',
#         'asset'.'asset_id' AS 'asset_id',
#         'employee'.'contact_no' AS 'contact_no',
#         'employee'.'email' AS 'email'
#         FROM 'employee'
#         LEFT JOIN 'assetlocation' ON 'employee'.'employee_id' = 'assetlocation'.'employee_id'
#         LEFT JOIN 'asset' ON 'assetlocation'.'asset_id' = 'asset'.'asset_id'
#         WHERE 'employee'.'status' IN ('ES01', 'ES02', 'ES03') AND
#         'employee'.'status' <> 'ES04' AND
#         'assetlocation'.'id' IS NULL
#         ORDER BY 'employee'.'start_date' DESC
#     """
#     print('TABLE TTTTTT')
#     results = db.engine.execute(query)
#     columns = results.keys()
#     rows = [dict(zip(columns, row)) for row in results]
#     return {'data': rows}






# @app.route('/notificationhr')
# def notifyitam_table():
#     query = """
#         SELECT employee.employee_id, employee.full_name, employee.start_date, asset.asset_id, employee.contact_no, employee.email
#         FROM employee
#         LEFT JOIN assetlocation ON employee.employee_id = assetlocation.employee_id
#         LEFT JOIN asset ON assetlocation.asset_id = asset.asset_id
#         WHERE employee.status != 'dismissed' AND assetlocation.id IS NULL
#         ORDER BY employee.start_date DESC
#     """
#     print('TABLE TTTTTT')
#     results = db.engine.execute(query)
#     columns = results.keys()
#     rows = [dict(zip(columns, row)) for row in results]
#     return {'data': rows}
