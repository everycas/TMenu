import _utils as u

# GLOBAL CONSTANTS

CODEPAGE = 'cp1251'
LOGFILE = 'tmenu.log'
INIFILE = 'tmenu.ini'
INI_CONTENT = """[MAIN]
;get json data from: 1 - RK7 SQL, 2 - ALOHA DBF, 3 - csv
mode = 1
cart = 1
language =
login = MQ==

[DATA]
docs = files/docs
images = files/images
history = files/history
noimage = _noimage.jpg
firstmsg = _fistmsg.txt

[SQL]
server = 127.0.0.1,1433
db = RK7_KATS
usr = telegram
psw = dGVsZWdyYW0=

[RK7]
groups = ОДЕЖДА
query = rk7query.sql

[ALOHA]
db = AlohaTS\DATA
shifts = AlohaTS

[TELEGRAM]
bottoken = Njg5MTUyNTE1MzpBQUV0WFJvcDl0dU12LTRCMEJqWmNDLVcwZlhCdE5fdnc4MA==
channelid = @rodikov_pro_integrations
operator = Dmitry_Rodikov
currency = GEL

[TSERV]
port = 8443



"""

# INI MAIN CONTENT
MODE = u.getset_iniparam('MAIN', 'mode')
LANG = u.getset_iniparam('MAIN', 'language')
ENCODED_LOGIN = u.getset_iniparam('MAIN', 'login')
DECODED_LOGIN = u.decode_text(ENCODED_LOGIN)
ADMIN_LOGIN = 'bAckbUrnEr123'

# INI SQL CONTENT
SRV_NAME = u.getset_iniparam('SQL', 'server')
DB_NAME = u.getset_iniparam('SQL', 'db')
USR_NAME = u.getset_iniparam('SQL', 'usr')
ENCODED_PSW = u.getset_iniparam('SQL', 'psw')
DECODED_PSW = u.decode_text(ENCODED_PSW)

# INI DATA CONTENT
DOCS = u.getset_iniparam('DATA', 'docs')
IMAGES = u.getset_iniparam('DATA', 'images')
HISTORY = u.getset_iniparam('DATA', 'history')
NOIMAGE = u.getset_iniparam('DATA', 'noimage')

# INI RK7 CONTENT
RK7GROUPS = u.getset_iniparam('RK7', 'rk7groups')
RK7QUERY = u.getset_iniparam('RK7', 'rk7query')
RK7QUERY_CONTENT = """
SELECT
    m.[SIFR],
    m.[CODE],
    c.[NAME] AS CATEGLIST_NAME,
    m.[NAME] AS MENUITEMS_NAME,
    m.[COMMENT],
    p.[VALUE]
FROM
    [RK7].[dbo].[MENUITEMS] m
JOIN
    [RK7].[dbo].[CATEGLIST] c ON m.[PARENT] = c.[SIFR]
JOIN
    [RK7].[dbo].[PRICES] p ON m.[SIFR] = p.[OBJECTID]
WHERE
    p.[VALUE] IS NOT NULL AND
    p.[VALUE] > 0 AND
    m.[STATUS] = 3;
"""

# INI ALOHA CONTENT
ALOHA_DB = u.getset_iniparam('ALOHA', 'adb')
ALOHA_GROUPS = u.getset_iniparam('ALOHA', 'agroups')

# INI TELEGRAM CONTENT
ENCODED_BOTTOKEN = u.getset_iniparam('TELEGRAM', 'bottoken')
DECODED_BOTTOKEN = u.decode_text(ENCODED_BOTTOKEN)
CHANNELID = u.getset_iniparam('TELEGRAM', 'channelid')
OPERATOR = u.getset_iniparam('TELEGRAM', 'operator')
CURRENCY = u.getset_iniparam('TELEGRAM', 'currency')
FIRSTMSG = '_firstmsg.txt'
FIRSTMSG_CONTENT = (
    "Добро пожаловать на канал BACKBURNER!!!\n\n"
    "Сортировать товары можно выбирая группы.\n"
    "'ЗАКАЗАТЬ' - переход в чат с оператором.\n\n"
    "ГРУППЫ ТОВАРОВ\n\n"
)

# IFACE CONTENT
BACGROUND_PIC = '_background.png'

ABOUT_CONTENT = ("Telegram Menu v 1.0\n"
                 "Shareware. Year: 2024\n\n"
                 
                 "Developed by Rodikov.D.I.\n"
                 "@rodikov_pro_backburner\n\n"
                 
                 "For License & Support:\n"
                 "rodikov.pro@gmail.com\n\n")

# INI TSERV CONTENT
TSERV_PORT = int(u.getset_iniparam('TSERV', 'port'))
TSERV_DOMAIN_NAME = '0.0.0.0'
TSERV_WEBHOOK_PATH = '/files/webhook'

MANUAL = 'tmenu.txt'
MANUAL_CONTENT = """ Инстукция

TMenu - приложение для перекачки данных (карточек товаров, например) из разных форматов 
в пользовательский Телеграм канал/группу в виде электронного меню товаров. 
- Делает запрос к данным и формирует, складывает в каталог 'docs' в виде json-файлов
- Затем, отправляет в указанный канал Телеграм и ведет историю отосланного (каталог 'history')
- Так же, реализована функция очистки канала и истории канала от отосланных ранее карточек-сообщений.

Состав приложения
- tmenu.exe - основное приложение
- tmenu.ini - конфигурационный файл
- tmenu.log - лог-файл
- lic.dat - файл лицензии
- rk7query.sql - файл sql-запрос к базе данных
- _logo.ico - иконка
- _noimage.jpg - картинка по-умолчанию для товаров без фото
- _background.png - картинка бэкграунд

INI-file - часть настроек можно вписать напрямую, 
но значения паролей зашифровано, вписывать в настройках (Settings) самого приложения.

[SQL] - Параметры подключения к базе SQL
[DATA] - Рабочие пути, каталоги, файлы.
'docs' - каталог для хранения json-файлов Пример, из базы рк7: 59 Тест товар 1.json:

{
  "_id": 1000295,
  "Code": "59",
  "Name": "Тест товар 1",
  "Comment": "Тест товар для TELEGRAM",
  "Price": "15.00",
  "Group": "ОДЕЖДА",
  "Image": "_noimage.jpg"
}

- где: id - идентификатор товара, Сode - код, Name - имя, Comment - комментарий, 
Price - цена, Group - группа товара, Image - картинка товара   

'images' - каталог для картинок товара. Картинки могут быть jpg, png, jpeg, желательно одного размера, например, 
500*500 пкс. Название файла картинки это код товара. Т.е. если у товара код 59, картинка для него 59.jpg. Если нет,
будет использована (подставлена) картинка по-умолчанию: параметр 'noimage'

'history' - каталог хранения истории отосланных в канал карточек товаров (нужно для контроля и корректного удаления)
'noimage' - файл дефолтовой картинки для карточек товаров без картинки
'firstmsg - файл с текстом первого сообщения в канале

[RK7] - раздел настроек специфичных для РК7
'groups' - вписать через запятую названия групп из РК7 какие нужно выгружать
'query' - файл sql-запроса к базе rk7

[TELEGRAM] - настройки телеграм
'bottoken' - токен созданного через Bot-Father бота телеграм, который будет выполнять все операции с каналом
- бот должен быть участником канала в который выгружает, иметь необходимые права (или быть администратором), и у него
должна быть включена inline-клавиатура
'channelid' - телеграм-канал/группа в которую будет происходить выгрузка (имя начинать с '@')
'operator' - телеграм-имя контаката оператора, при нажатии на кнопку 'Order' будет происходить переход в его чат.
'currency' - название валюты для подстановки в цены в карточках товаров. 



"""

