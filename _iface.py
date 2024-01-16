import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
import _constants as c
import _utils as u
# import Pillow
from PIL import Image, ImageTk  # Предварительно убедитесь, что у вас установлен пакет Pillow


class TMenuApp:

    def __init__(self, master=None, get_data_button=None, send_data_button=None, clear_data_button=None):
        self.master = master
        if self.master:
            self.master.title("TMenu")
            self.master.geometry("500x500")  # set size
            self.master.minsize(500, 500)
            self.master.maxsize(500, 500)
            self.master.iconbitmap('_logo.ico')  # set ico

            self.saved_password = c.ENCODED_LOGIN  # Закодированный и сохраненный в ини пароль входа
            self.get_data_command = get_data_button  # Комманда кнопки
            self.send_data_command = send_data_button  # Комманда кнопки
            self.clear_data_command = clear_data_button  # Комманда кнопки

            # Create task menu
            self.menu_bar = tk.Menu(self.master)
            self.master.config(menu=self.menu_bar)

            # Add tab "File" to Task Menu
            self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
            self.menu_bar.add_cascade(label="File", menu=self.file_menu)
            self.file_menu.add_command(label="LogIn", command=self.check_password)
            self.file_menu.add_command(label="Settings", state=tk.DISABLED, command=self.open_settings_window)
            self.file_menu.add_separator()
            self.file_menu.add_command(label="Close", command=self.exit_program)

            # Add tab "Commands" to Task Menu
            self.import_menu = tk.Menu(self.menu_bar, tearoff=0)
            self.menu_bar.add_cascade(label="Import", menu=self.import_menu)
            self.import_menu.add_command(label="Clear Data", state=tk.DISABLED, command=clear_data_button)
            self.import_menu.add_separator()
            self.import_menu.add_command(label="Get Data", state=tk.DISABLED, command=get_data_button)
            self.import_menu.add_command(label="Send Data", state=tk.DISABLED, command=send_data_button)

            # Add tab "Help" to Task Menu
            self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
            self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
            self.help_menu.add_command(label="About", command=self.open_about_window)

            # Load Image
            image_path = c.BACGROUND_PIC  # Укажите путь к вашему изображению
            image = Image.open(image_path)
            self.photo = ImageTk.PhotoImage(image)

            # Create Label for display img in the center of the window
            self.label = tk.Label(self.master, image=self.photo)
            self.label.pack(pady=10)

    def check_password(self):
        user_password = simpledialog.askstring("Login", "Enter password:", show='*')
        if user_password is not None:
            if user_password == c.DECODED_LOGIN:
                self.activate_user_tabs()
            elif user_password == c.ADMIN_LOGIN:
                self.activate_all_tabs()
            else:
                tk.messagebox.showerror("Login Failed", "Incorrect password")

    def activate_all_tabs(self):
        """Login as Admin. Can make Settings."""
        self.file_menu.entryconfig(0, state=tk.DISABLED)  # Disable "Login"
        self.file_menu.entryconfig(1, state=tk.NORMAL)  # Enable "Settings"
        self.import_menu.entryconfig(0, state=tk.NORMAL)  # Enabele "Clear Channel"
        self.import_menu.entryconfig(2, state=tk.NORMAL)  # Enable "Get Data"
        self.import_menu.entryconfig(3, state=tk.NORMAL)  # Enabele "Send to Channel"

    def activate_user_tabs(self):
        """Login as User. Can not make Settings."""
        self.file_menu.entryconfig(0, state=tk.DISABLED)  # Disable "Login"
        # self.file_menu.entryconfig(1, state=tk.NORMAL)  # Enable "Settings"
        self.import_menu.entryconfig(0, state=tk.NORMAL)  # Enabele "Clear Channel"
        self.import_menu.entryconfig(2, state=tk.NORMAL)  # Enable "Get Data"
        self.import_menu.entryconfig(3, state=tk.NORMAL)  # Enabele "Send to Channel"

    @staticmethod
    def save_settings(settings_window, entries):
        func_name = u.get_func_name()

        sections = {
            'SQL': ['server', 'db', 'usr'],
            'DATA': ['docs', 'images', 'history', 'noimage'],
            'RK7': ['groups', 'query'],
            'TELEGRAM': ['channelid', 'operator', 'currency']
        }

        for section, keys in sections.items():
            for key in keys:
                value = entries[key].get()
                u.getset_iniparam(section, key, value)

        # Insert encoded usr login to ini
        login = entries['login'].get()
        encoded_login = u.encode_text(login)
        u.getset_iniparam('MAIN', 'login', encoded_login)

        # Insert encoded sql psw to ini
        psw = entries['psw'].get()
        encoded_psw = u.encode_text(psw)
        u.getset_iniparam('SQL', 'psw', encoded_psw)

        # Insert encoded bottoken to ini
        bttkn = entries['bottoken'].get()
        encoded_bttkn = u.encode_text(bttkn)
        u.getset_iniparam('TELEGRAM', 'bottoken', encoded_bttkn)

        u.log_msg(func_name, False, 'Settings is saved.')

        # Закрываем окно настроек
        settings_window.destroy()

    def open_settings_window(self):
        """Settings window options."""

        settings_window = tk.Toplevel(self.master)
        settings_window.title("TMenu - Settings")

        # Добавьте элементы управления и функциональность для настроек
        settings_window.geometry("300x650")  # set size
        settings_window.minsize(300, 650)
        settings_window.maxsize(300, 650)
        settings_window.iconbitmap('_logo.ico')  # set ico

        # [MAIN] Section

        main_frame = ttk.LabelFrame(settings_window, text="[MAIN]", padding=10)
        main_frame.pack(padx=10, pady=5, anchor='w')

        main_login_label = tk.Label(main_frame, text="login: ")
        main_login_label.grid(row=1, column=0, sticky='nw')
        main_login_entry = tk.Entry(main_frame, width=30)
        main_login_entry.insert(0, c.DECODED_LOGIN)
        main_login_entry.grid(row=1, column=1)

        # [SQL] Section

        sql_frame = ttk.LabelFrame(settings_window, text="[SQL]", padding=10)
        sql_frame.pack(padx=10, pady=5, anchor='w')

        sql_server_label = tk.Label(sql_frame, text="server: ")
        sql_server_label.grid(row=1, column=0, sticky='nw')
        sql_server_entry = tk.Entry(sql_frame, width=30)
        sql_server_entry.insert(0, c.SRV_NAME)
        sql_server_entry.grid(row=1, column=1)

        sql_db_label = tk.Label(sql_frame, text="db: ")
        sql_db_label.grid(row=2, column=0, sticky="nw")
        sql_db_entry = tk.Entry(sql_frame, width=30)
        sql_db_entry.insert(0, c.DB_NAME)
        sql_db_entry.grid(row=2, column=1)

        sql_usr_label = tk.Label(sql_frame, text="usr: ")
        sql_usr_label.grid(row=3, column=0, sticky="nw")
        sql_usr_entry = tk.Entry(sql_frame, width=30)
        sql_usr_entry.insert(0, c.USR_NAME)
        sql_usr_entry.grid(row=3, column=1)

        sql_psw_label = tk.Label(sql_frame, text="pass: ")
        sql_psw_label.grid(row=4, column=0, sticky="nw")
        sql_psw_entry = tk.Entry(sql_frame, width=30)
        sql_psw_entry.insert(0, c.DECODED_PSW)
        sql_psw_entry.grid(row=4, column=1)

        # [DATA] Section

        data_frame = ttk.LabelFrame(settings_window, text="[DATA]", padding=10)
        data_frame.pack(padx=10, pady=5, anchor='w')

        data_docs_label = tk.Label(data_frame, text="docs: ")
        data_docs_label.grid(row=1, column=0, sticky="nw")
        data_docs_entry = tk.Entry(data_frame, width=30)
        data_docs_entry.insert(0, c.DOCS)
        data_docs_entry.grid(row=1, column=1)

        data_images_label = tk.Label(data_frame, text="images: ")
        data_images_label.grid(row=2, column=0, sticky="nw")
        data_images_entry = tk.Entry(data_frame, width=30)
        data_images_entry.insert(0, c.IMAGES)
        data_images_entry.grid(row=2, column=1)

        data_history_label = tk.Label(data_frame, text="history: ")
        data_history_label.grid(row=3, column=0, sticky="nw")
        data_history_entry = tk.Entry(data_frame, width=30)
        data_history_entry.insert(0, c.HISTORY)
        data_history_entry.grid(row=3, column=1)

        data_noimage_label = tk.Label(data_frame, text="noimage: ")
        data_noimage_label.grid(row=4, column=0, sticky="nw")
        data_noimage_entry = tk.Entry(data_frame, width=30)
        data_noimage_entry.insert(0, c.NOIMAGE)
        data_noimage_entry.grid(row=4, column=1)

        # [RK7] Section

        rk7_frame = ttk.LabelFrame(settings_window, text="[RK7]", padding=10)
        rk7_frame.pack(padx=10, pady=5, anchor='w')

        rk7_groups_label = tk.Label(rk7_frame, text="groups: ")
        rk7_groups_label.grid(row=1, column=0, sticky="nw")
        rk7_groups_entry = tk.Entry(rk7_frame, width=30)
        rk7_groups_entry.insert(0, c.RK7GROUPS)
        rk7_groups_entry.grid(row=1, column=1)

        rk7_query_label = tk.Label(rk7_frame, text="query: ")
        rk7_query_label.grid(row=2, column=0, sticky="nw")
        rk7_query_entry = tk.Entry(rk7_frame, width=30)
        rk7_query_entry.insert(0, c.RK7QUERY)
        rk7_query_entry.grid(row=2, column=1)

        # [TELEGRAM] Section

        tlgrm_frame = ttk.LabelFrame(settings_window, text="[TELEGRAM]", padding=10)
        tlgrm_frame.pack(padx=10, pady=5, anchor='w')

        tlgrm_bottoken_label = tk.Label(tlgrm_frame, text="bottoken: ")
        tlgrm_bottoken_label.grid(row=1, column=0, sticky="nw")
        tlgrm_bottoken_entry = tk.Entry(tlgrm_frame, width=30)
        tlgrm_bottoken_entry.insert(0, c.DECODED_BOTTOKEN)
        tlgrm_bottoken_entry.grid(row=1, column=1)

        tlgrm_channelid_label = tk.Label(tlgrm_frame, text="channelid: ")
        tlgrm_channelid_label.grid(row=2, column=0, sticky="nw")
        tlgrm_channelid_entry = tk.Entry(tlgrm_frame, width=30)
        tlgrm_channelid_entry.insert(0, c.CHANNELID)
        tlgrm_channelid_entry.grid(row=2, column=1)

        tlgrm_operator_label = tk.Label(tlgrm_frame, text="operator: ")
        tlgrm_operator_label.grid(row=3, column=0, sticky="nw")
        tlgrm_operator_entry = tk.Entry(tlgrm_frame, width=30)
        tlgrm_operator_entry.insert(0, c.OPERATOR)
        tlgrm_operator_entry.grid(row=3, column=1)

        tlgrm_currency_label = tk.Label(tlgrm_frame, text="currency: ")
        tlgrm_currency_label.grid(row=4, column=0, sticky="nw")
        tlgrm_currency_entry = tk.Entry(tlgrm_frame, width=30)
        tlgrm_currency_entry.insert(0, c.CURRENCY)
        tlgrm_currency_entry.grid(row=4, column=1)

        # Фрейм для кнопок "ОК" и "Отмена"
        button_frame = tk.Frame(settings_window)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        # Получите значения Entry виджетов
        entries = {
            'login': main_login_entry,

            'server': sql_server_entry,
            'db': sql_db_entry,
            'usr': sql_usr_entry,
            'psw': sql_psw_entry,

            'docs': data_docs_entry,
            'images': data_images_entry,
            'history': data_history_entry,
            'noimage': data_noimage_entry,

            'groups': rk7_groups_entry,
            'query': rk7_query_entry,

            'bottoken': tlgrm_bottoken_entry,
            'channelid': tlgrm_channelid_entry,
            'operator': tlgrm_operator_entry,
            'currency': tlgrm_currency_entry
        }

        ok_button = tk.Button(button_frame, text="Save", padx=5,
                              command=lambda: self.save_settings(settings_window, entries))
        ok_button.grid(row=0, column=0, padx=3)

        cancel_button = tk.Button(button_frame, text="Cancel", padx=5, command=settings_window.destroy)
        cancel_button.grid(row=0, column=1, padx=3)

        # Дождаться закрытия окна
        settings_window.grab_set()
        settings_window.wait_window()

        # После закрытия окна, продолжить выполнение кода
        settings_window.grab_release()

    def exit_program(self):
        func_name = u.get_func_name()
        u.log_msg(func_name, False, 'Stop program.')
        self.master.destroy()

    @staticmethod
    def open_about_window():
        tk.messagebox.showinfo('Info - About', c.ABOUT_CONTENT)


def run():
    root = tk.Tk()
    app = TMenuApp(master=root)
    root.mainloop()


if __name__ == "__main__":
    run()


