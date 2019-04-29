def create_table(cur):
    cur.execute('DROP TABLE IF EXISTS TypingExchange')
    cur.execute('''
        CREATE TABLE TypingExchange (
            code varchar(255),
            natural_language varchar(255)
        );''')


def insert_codes(cur):
    dictionary = {
        'be': 'Belarusian', 'bg': 'Bulgarian',
        'hu': 'Hungarian',  'vi': 'Vietnamese',
        'nl': 'Dutch',      'el': 'Greek',
        'da': 'Danish',     'ga': 'Irish',
        'it': 'Italian',    'is': 'Icelandic',
        'es': 'Spanish',    'kk': 'Kazakh',
        'ca': 'Catalan',    'zh': 'Chinese',
        'ko': 'Korean',     'lv': 'Latvian',
        'lt': 'Lithuanian', 'de': 'German',
        'no': 'Norwegian',  'pl': 'Polish',
        'pt': 'Portuguese', 'ro': 'Romanian',
        'ru': 'Russian',    'sr': 'Serbian',
        'sk': 'Slovakian',  'sl': 'Slovenian',
        'th': 'Thai',       'tr': 'Turkish',
        'uk': 'Ukrainian',  'fi': 'Finnish',
        'fr': 'French',     'hr': 'Croatian',
        'cs': 'Czech',      'sv': 'Swedish',
        'gd': 'Scottish',   'et': 'Estonian',
        'ja': 'Japanese'
    }
    for key in dictionary:
        cur.execute('''INSERT INTO TypingExchange (code, natural_language)
                    VALUES ('{}', '{}');'''.format(key, dictionary[key]))
