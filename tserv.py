from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import threading
import json
import _constants as c
import requests


class MyHandler(SimpleHTTPRequestHandler):
    """Класс обработчика запросов."""
    def do_get(self):
        if self.path == '/shutdown':
            # Обрабатываем запрос на остановку сервера
            self.send_response(200)
            stop_server()  # Останавливаем сервер
        else:
            # Ваша пользовательская логика здесь
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=cp1251')
            self.end_headers()
            response = 'Привет от сервера!'.encode('cp1251')
            self.wfile.write(response)

            # DEBUG --
            print("Запрос обработан!")

    def do_post(self):
        content_length = int(self.headers['Content-Length'])
        raw_data = self.rfile.read(content_length)
        data = json.loads(raw_data.decode('utf-8'))

        if 'message' in data:
            # Проверяем, что запрос пришел от вашего бота
            if data['message']['from']['id'] == c.DECODED_BOTTOKEN:
                # Обрабатываем запрос
                self.process_message(data['message'])
            else:
                self.send_response(403)
                self.end_headers()
                return

        self.send_response(200)
        self.end_headers()

    def process_message(self, message):
        # Здесь можно обработать входящее сообщение от бота
        pass

    @staticmethod
    def process_callback_query(callback_query):
        user_id = callback_query['from']['id']
        print(f"User {user_id} pressed 'Add to Cart' button.")


def stop_server():
    """Stop server functionality."""
    print("Остановка сервера...")
    httpd.shutdown()
    server_thread.join()
    print("Сервер остановлен.")


# Создаем сервер с пользовательским обработчиком запросов
httpd = TCPServer((c.TSERV_DOMAIN_NAME, c.TSERV_PORT), MyHandler)
print(f"Сервер запущен на домене {c.TSERV_DOMAIN_NAME} и порту {c.TSERV_PORT}")

# Устанавливаем Webhook
webhook_url = (f'https://api.telegram.org/bot{c.DECODED_BOTTOKEN}/setWebhook?url=https://149.3.60.120:'
               f'{c.TSERV_PORT}{c.TSERV_WEBHOOK_PATH}')
response = requests.post(webhook_url)
print(response.text)

# Создаем и запускаем поток для сервера
server_thread = threading.Thread(target=httpd.serve_forever)
server_thread.start()

# DEBUG ----------------------------------------------------------

# Ожидаем ввода с консоли для остановки сервера
input("Нажмите Enter для остановки сервера...")

# Останавливаем сервер после ввода с консоли
stop_server()
