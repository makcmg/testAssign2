from sqlalchemy import func

from database.model import session, Journal, engine


def get_db_chart_data():
    data = session.query(Journal.delivery_date,
                         func.sum(Journal.price_usd)).group_by(Journal.delivery_date).\
        order_by(Journal.delivery_date).all()
    return data


def get_db_table_data():
    data = session.query(Journal).all()
    return data


def get_total_data():
    data = session.query(func.sum(Journal.price_usd)).first()
    return data


def cleaner_table():
    session.query(Journal).delete()
    session.commit()


def insert_data(data):
    session.bulk_insert_mappings(Journal, data)
    session.commit()


# def updata_data(data):
#     session.bulk_update_mappings(Journal, data)
#     session.commit()
#
#
# def delete_data(data):
#     session.query(Journal).filter(Journal.id.in_([id_r.id for id_r in data])).delete()
#     session.commit()
