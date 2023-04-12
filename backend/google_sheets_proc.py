from datetime import datetime, timedelta

import pygsheets
import requests
import schedule as schedule
import telebot
import datetime as dt

from database.db_manager import cleaner_table, insert_data
from settings import AUTH_SERVICE_FILE, SHEETS_NAME, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

import xml.etree.ElementTree as ET


# Функция отправки сообщения в telegram
def send_telegram_message(message):
    bot = telebot.TeleBot(TELEGRAM_TOKEN)
    # Формируем сообщения для отправки на основе полученных данных
    text_message = (
        f'*Срок поставки заказа истек!*\n\n'
        f'Срок поставки: *{message["delivery_date"]}*\n'
        f'Заказ №*{message["id_order"]}*\n'
        f'Стоимость: {message["price_usd"]}$ / {message["price_rub"]}₽\n'
        )

    # Отправляем сообщение в заранее указанный чат
    bot.send_message(TELEGRAM_CHAT_ID, text=text_message, parse_mode='markdown')


# Функция получение текущего курса USD/RUB
def get_exchange_rate():
    # Переменная для хранения даты
    # Дата за предыдущий день, так как обновление информации на cbr.ru идет с задержкой
    now_day = datetime.utcnow()
    delta_day = datetime.utcnow() - timedelta(days=3)
    date_req = now_day.strftime('%d/%m/%Y')
    date_req1 = delta_day.strftime('%d/%m/%Y')

    url = f'https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={date_req1}&date_req2={date_req}&VAL_NM_RQ=R01235'
    # Делаем запрос к cbr.ru и получаем XML-файл
    response = requests.request('POST', url)
    if response.status_code == 200:
        # Разбираем полученный XML-файл
        root_node = ET.fromstring(response.text)
        value = root_node.find('Record').find('Value')
        return value.text


# Функция получения данных из google sheets
def get_sheet_data():
    # Авторизация в google sheets и получение данных из таблицы
    gc = pygsheets.authorize(service_file=AUTH_SERVICE_FILE)
    worksheet = gc.open(SHEETS_NAME).sheet1
    sheet_data = worksheet.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False)

    # Получение текущего курса USD/RUB
    exchange_rate = get_exchange_rate()
    # Список записей на добавление в БД
    insert_records = []
    # Проходим по всем записям из google_sheets, пропуская первую с заголовками
    for row in sheet_data[1:]:
        # Формируем дату корректную для добавления в БД
        delivery_date = datetime.strptime(row[3], '%d.%m.%Y').date()
        # Получаем стоимость заказа по курсу в рублях
        price_rub = int(row[2]) * float(exchange_rate.replace(',', '.'))
        # Формируем словарь на основе полученных данных
        sh_data = {
            'id_row': row[0],
            'id_order': row[1],
            'price_usd': float(row[2]),
            'delivery_date': delivery_date,
            'price_rub': round(price_rub, 2),
        }
        insert_records.append(sh_data)
        # Проверка даты поставки, если дата просрочена, то отправляем сообщение в телеграмм
        if dt.date.today() > delivery_date:
            send_telegram_message(sh_data)

    return insert_records


    #TODO Вариант с проверкой данных в таблице, тесты показали, что этот вариант в разы медленнее
    #
    # # Создание списка для хранения идентификаторов записей, которые были обработаны
    # processed_ids = []
    # # Создание списка для хранения записей на обновление в БД
    # update_records = []
    # # Создание списка для хранения записей на добавление в БД
    # insert_records = []
    #
    # # Обработка каждой записи из таблицы Google Sheets
    # for row in sheet_data[1:]:
    #     price_rub = int(row[2]) * float(exchange_rate.replace(',', '.'))
    #     delivery_date = datetime.strptime(row[3], '%d.%m.%Y')
    #     # Создание словаря для хранения данных записи
    #     sheet_data = {
    #         'id_row': row[0],
    #         'id_order': row[1],
    #         'price_usd': row[2],
    #         'delivery_date': delivery_date,
    #         'price_rub': str(round(price_rub, 2)),
    #     }
    #
    #     # Поиск записи в базе данных по ключевым полям
    #     record_id_order = session.query(Journal).filter(Journal.id_order == row[1]).first()
    #
    #     # Если запись существует, то проверяем на актуальность и если надо обновляем
    #     if record_id_order:
    #         db_data = {
    #             'id_row': record_id_order.id_row,
    #             'id_order': record_id_order.id_order,
    #             'price_usd': record_id_order.price_usd,
    #             'delivery_date': record_id_order.delivery_date,
    #             'price_rub': record_id_order.price_rub,
    #         }
    #         if sheet_data != db_data:
    #             sheet_data.update({'id': record_id_order.id})
    #             update_records.append(sheet_data)
    #         processed_ids.append(row[1])
    #     # Если запись не существует, то выполнить добавление данных
    #     else:
    #         insert_records.append(sheet_data)
    #
    # # Ищем записи в базе, которых уже нет в sheets и удаляем их
    # delete_records = session.query(Journal).filter(Journal.id_order.notin_([r for r in processed_ids])).all()
    #
    # if update_records:
    #     updata_data(update_records)
    #
    # if insert_records:
    #     insert_data(insert_records)
    #
    # if delete_records:
    #     delete_data(delete_records)


def google_sheets_saver():
    # Получаем данные из sheets
    insert_records = get_sheet_data()
    # Очищаем таблицу в БД
    cleaner_table()
    # Добавляем новые данные в БД
    insert_data(insert_records)


def main():
    google_sheets_saver()
    schedule.every(10).minutes.do(google_sheets_saver)

    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()
