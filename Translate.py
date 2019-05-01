import requests
import sqlite3
import creating_table
import telebot


token = '788927932:AAFhYxhg5aLYtgDlU11yW15-PDMjiysOjHI'
URL = 'https://api.telegram.org/bot' + token + '/'
bot = telebot.TeleBot(token)


def get_translation(text, lang):
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20190423T190040Z.697d4ef188750baf.65f665b5bb9' \
          '06c53747e64b89b18344475f5a71d'
    r = requests.post(url, data={'key': key, 'text': text, 'lang': lang})
    return eval(r.text)


with sqlite3.connect('TypingExchange.db') as conn:
    creating_table.create_table(conn.cursor())
    creating_table.insert_codes(conn.cursor())


def get_updates():
    url = URL + 'getupdates'
    r = requests.get(url)
    return r.json()


def get_message():
    data = get_updates()
    chat_id = data['result'][-1]['message']['chat']['id']
    message_text = data['result'][-1]['message']['text']
    message = {'chat_id': chat_id,
               'text': message_text}
    return message


def send_message(chat_id, text):
    url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
    requests.get(url)


@bot.message_handler(commands=['start'])
def welcome():
    return get_message()


def main():
    chat_id = welcome()['chat_id']
    send_message(welcome()['chat_id'],
                 'Type your language in English starting with a capital letter')
    update_id = get_updates()['result'][-1]['update_id']
    while True:
        send_message(chat_id, "Type your text, please")
        while update_id == get_updates()['result'][-1]['update_id']:
            pass
        user_text = get_message()['text']
        update_id = get_updates()['result'][-1]['update_id']

        send_message(chat_id, "Choose language")
        while update_id == get_updates()['result'][-1]['update_id']:
            pass
        user_language = get_message()['text']
        update_id = get_updates()['result'][-1]['update_id']

        with sqlite3.connect('TypingExchange.db') as conn:
            cur = conn.cursor()
            cur.execute('''
            SELECT code
            FROM TypingExchange
            WHERE natural_language = '{}'
            '''.format(user_language))
        try:
            code = cur.fetchone()[0]
            send_message(chat_id, *get_translation(user_text, code)['text'])
        except:
            send_message(chat_id, "Language is not found!")


if __name__ == '__main__':
    main()
