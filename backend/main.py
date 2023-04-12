import json

import flask
from flask import Flask

from database.db_manager import get_db_chart_data, get_db_table_data, get_total_data

app = Flask(__name__)


# Создание json файла, на основе которого строится график на фронте
def make_json_chart_data():
    db_data = get_db_chart_data()
    result = []
    for row in db_data:
        result.append({
            'year': row[0].strftime('%m/%d/%Y'),
            'sum_order': row[1],
        })

    with open('./backend/static/data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


# Создание json файла, на основе которого строится таблица на фронте
def make_json_table_data():
    db_data = get_db_table_data()
    result = []
    for row in db_data:
        result.append({
            'id_row': row.id_row,
            'id_order': row.id_order,
            'price_usd': row.price_usd,
            'year': row.delivery_date.strftime('%m/%d/%Y'),
        })

    with open('./backend/static/table_data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


@app.route('/')
def my_index():
    make_json_chart_data()
    make_json_table_data()
    # Получение общей суммы стоимости заказов
    total_price = get_total_data()
    return flask.render_template('index.html', token=total_price[0])


if __name__ == '__main__':
    app.run(debug=True)
