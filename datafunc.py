from app import db
from sqlalchemy.orm import class_mapper
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.sql import text


# search the table for a specific field name with a given value
def get_record(data_table, where_clause,type=None):
    # table = db.metadata.tables[data_table]
    # get the declarative base class
    Base = automap_base()
    Base.prepare(db.engine, reflect=True)
    # get the class corresponding to the table
    cls = Base.classes[data_table]
    # build the query based on the where clause
    query = db.session.query(cls).filter(text(where_clause)).first()
    # execute the query and return the first record
    if type != None: # return dictionary otherwise query object
        # convert the result to a dictionary
        query = query.__dict__
        # remove unwanted keys from the dictionary
        del query['_sa_instance_state']
    return query



def update_record(data_table, updates, where_clause):
    # get the declarative base class
    Base = automap_base()
    Base.prepare(db.engine, reflect=True)
    # get the class corresponding to the table
    cls = Base.classes[data_table]
    # build the query based on the where clause
    query = db.session.query(cls).filter(text(where_clause))
    # execute the query and update the record
    query.update(updates)
    db.session.commit()
    # retrieve the updated record and return as a dictionary
    updated_record = query.first().__dict__
    # remove unwanted keys from the dictionary
    del updated_record['_sa_instance_state']
    return updated_record




# def update_record(data_table, data, field_name, field_value):
#     # table = db.metadata.tables[data_table]
#     # get the declarative base class
#     Base = automap_base()
#     Base.prepare(db.engine, reflect=True)
#     # get the class corresponding to the table
#     cls = Base.classes[data_table]
#     # get the row to update
#     row = db.session.query(cls).filter(getattr(cls, field_name) == field_value).first()
#     if row:
#         # update the attributes of the row
#         for key, value in data.items():
#             setattr(row, key, value)
#         db.session.commit()
#         return True
#     else:
#         return False



