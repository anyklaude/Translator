import requests
import sqlite3
import creating_table


def get_translation(txt, lng):
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20190423T190040Z.697d4ef188750baf.65f665b5bb9' \
          '06c53747e64b89b18344475f5a71d'
    r = requests.post(url, data={'key': key, 'text': txt, 'lang': lng})
    return eval(r.text)


with sqlite3.connect('TypingExchange.db') as conn:
    creating_table.create_table(conn.cursor())
    creating_table.insert_codes(conn.cursor())

while True:
    text = input('Your text: ')
    string = input('Translate to: ')
    with sqlite3.connect('TypingExchange.db') as conn:
        cur = conn.cursor()
        cur.execute('''
        SELECT code
        FROM TypingExchange
        WHERE natural_language = '{}'
        '''.format(string))
        try:
            code = cur.fetchone()[0]
        except:
            print("Language is not found, try again!")
            continue
    print(*get_translation(text, code)['text'])
    answer = input('One more? ')
    if answer != "Yes":
        print('See you soon!')
        break
