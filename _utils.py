# MAIN SERVICES UTILITY FUNCTIONS -------------------
import _constants as c
from datetime import datetime as dt  # datetime
import inspect
from configparser import ConfigParser  # ini config
import hashlib  # hash passwords
import os
import base64


def get_dtime(ru_fmt: bool) -> str:
    """Get formatted date & time string."""
    return dt.now().strftime('%d.%m.%Y | %H:%M:%S.%f') if ru_fmt else dt.now().strftime('%Y-%m-%d | %H:%M:%S.%f')


def get_func_name() -> str:
    """Get current function name."""
    return inspect.currentframe().f_back.f_code.co_name


def log_msg(func_name, is_err: bool, msg: str):
    """Write error or info message to log file."""
    d_t = get_dtime(False)
    msg_type = 'Error' if is_err else 'Info'
    msg_text = f"\n{d_t} | Function '{func_name}' >> \n{msg_type} message: {msg}"
    with open(c.LOGFILE, "a", encoding='cp1251') as log_file:
        log_file.write(msg_text)


def write_new_inifile(file_path: str, content: str):
    """Create & write to disc new ini-file."""
    func_name = get_func_name()
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='cp1251') as ini_file:
            ini_file.write(content)
        log_msg(func_name, True, f"New '{file_path}' file created.")


def getset_iniparam(section: str, param: str, data=None):
    """Get or set parameter from ini-file."""
    func_name = get_func_name()
    ini = ConfigParser()
    ini.read(c.INIFILE)

    if not data:  # get
        try:
            data = ini[section][param]
        except Exception as err_msg:
            log_msg(func_name, True, err_msg)
        else:
            return data
    else:  # set
        ini.set(section, param, data)
        with open(c.INIFILE, 'w') as ini_file:
            ini.write(ini_file)


def hash_text(text) -> str:
    hash_object = hashlib.sha256(text.hash_text())
    return hash_object.hexdigest()


def check_hashed(self, text, encoded_text) -> bool:
    input_hash = self.hash_text(text)
    return input_hash == encoded_text


def encode_text(text):
    """Encode text with base64-module."""

    encoded_bytes = base64.b64encode(text.encode('utf-8'))
    encoded_text = encoded_bytes.decode('utf-8')
    return encoded_text


def decode_text(encoded_text):
    """Decode text that was encoded with base64-module."""

    func_name = get_func_name()
    try:
        decoded_bytes = base64.b64decode(encoded_text.encode('utf-8'))
        decoded_text = decoded_bytes.decode('utf-8')
        return decoded_text
    except base64.binascii.Error as e:
        log_msg(func_name, True, e)
        return None


def read_text_from_file(file_path):
    """Read text from file."""
    try:
        with open(file_path, 'r', encoding='cp1251') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Файл '{file_path}' не найден.")
        return None


def write_text_to_file(file_path, text):
    """Write text to file."""
    try:
        with open(file_path, 'w', encoding='cp1251') as file:
            file.write(text)
            print(f"Текст успешно записан в файл: {file_path}")
    except Exception as e:
        print(f"Ошибка при записи текста в файл: {e}")


def is_directory_empty(path) -> bool:
    return not any(os.listdir(path))
