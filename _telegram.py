# TELEGRAM LOGIC
import _utils as u
import json as j  # work with json
import requests as r  # work with telegram requests
from urllib.parse import quote  # work with quotation
import os  # work with os


def write_new_firstmsg(file_path: str, query: str):
    """If sql-file not exist in folder, create new file."""
    func_name = u.get_func_name()
    if not os.path.exists(file_path):
        with open(file_path, 'w') as ini_file:
            ini_file.write(query)
        u.log_msg(func_name, True, f"New '{file_path}' file created.")


def send_firstmsg_to_channel(message: str, rk7groups: str, bottoken: str, channelid: str, history_path: str):
    """Send first/welcome message to telegram channel."""
    # Convert rk7groups string to list
    groups_list = [f"#{group.strip()}" for group in rk7groups.split(',')]
    # Header message text
    message_text = (message + ' '.join(groups_list))

    # Send message
    url = f'https://api.telegram.org/bot{bottoken}/sendMessage?chat_id={channelid}&text={quote(message_text)}'

    response = r.get(url)
    message_id = j.loads(response.text).get("result", {}).get("message_id")

    if message_id:
        # Pin message
        pin_url = f'https://api.telegram.org/bot{bottoken}/pinChatMessage?chat_id={channelid}&message_id={message_id}'
        r.get(pin_url)

        # Remove message "bot pin message"
        del_msg_url = f'https://api.telegram.org/bot{bottoken}/deleteMessage?chat_id={channelid}&message_id={message_id + 1}'
        r.get(del_msg_url)

        # Save answer to history
        history_filename = os.path.join(history_path, "group_list_response.json")
        with open(history_filename, "w", encoding="utf-8") as response_file:
            response_file.write(j.dumps(j.loads(response.text), indent=2, ensure_ascii=False))


def send_docs_to_channel(docs: str, currency: str, operator: str, bottoken: str, channelid: str, history_path: str):
    """Scan directory and send all json docs files to the Telegram channel."""

    for filename in os.listdir(docs):

        if filename.endswith(".json"):
            filepath = os.path.join(docs, filename)

            with open(filepath, "r", encoding="utf-8") as file:
                json_content = j.load(file)

                # Generate text message from json_content
                telegram_message = (
                    f"{json_content['Name']} - {json_content['Price']} {currency}\n\n"
                    f"{json_content['Comment']}\n\n"
                    f"Код товара {json_content['Code']}\n"
                    f"Группа {quote('#' + json_content['Group'])}"
                )
                # Inline keyboard markup with "Order" button
                inline_keyboard = [
                    [
                        {"text": "Order", "url": f't.me/{operator}'}
                    ]
                ]
                # send photo and message with inline keyboard
                files = {'photo': open(json_content['Image'], 'rb')}

                url = (f'https://api.telegram.org/bot{bottoken}'
                       f'/sendPhoto?chat_id={channelid}'
                       f'&caption={telegram_message}'
                       f'&reply_markup={j.dumps({"inline_keyboard": inline_keyboard})}')
                response = r.post(url, files=files)

                # Save response to history folder
                history_filename = os.path.join(history_path, f"{json_content['Code']}_response.json")

                with open(history_filename, "w", encoding="utf-8") as response_file:
                    response_file.write(j.dumps(j.loads(response.text), indent=2, ensure_ascii=False))


def clear_channel_history(docs_path: str, bot_token: str, channel_id: str, history_path: str):
    """Clear Telegram Channel history."""
    func_name = u.get_func_name()
    # Scan all files in history folder
    for filename in os.listdir(history_path):
        if filename.endswith("_response.json"):
            filepath = os.path.join(history_path, filename)

            with open(filepath, "r", encoding="utf-8") as file:
                response_data = j.load(file)
                # Get message_id from response_data
                message_id = response_data.get("result", {}).get("message_id")

                if message_id is not None:
                    # Delete message from telegram channel
                    url = (f'https://api.telegram.org/bot{bot_token}/deleteMessage?'
                           f'chat_id={channel_id}&message_id={message_id}')
                    response = r.get(url)

                    if response.status_code != 200:
                        u.log_msg(func_name, True, f"{message_id} delete error: {response.status_code}.")
    try:
        # Scan all files in files/history folder and remove it
        for filename in os.listdir(history_path):
            filepath = os.path.join(history_path, filename)
            os.remove(filepath)

        # Scan all files in files/docs folder and remove it
        for filename in os.listdir(docs_path):
            filepath = os.path.join(docs_path, filename)
            os.remove(filepath)
        u.log_msg(func_name, False, f"'Docs' and 'History' folders is clear.")

    except Exception as e:
        u.log_msg(func_name, True, e)
