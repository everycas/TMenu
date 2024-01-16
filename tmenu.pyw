# MAIN PROGRAM LOGIC
# my modules
import _constants as c
import _utils as u
import _rk7sql as q
import _telegram as t
from _iface import TMenuApp
import tkinter as tk
from tkinter import messagebox
import _lic as lic


def get_data_button():
    func_name = u.get_func_name()
    if u.is_directory_empty(c.DOCS) and u.is_directory_empty(c.HISTORY):
        try:
            connection = q.connect_server(c.SRV_NAME, c.DB_NAME, c.USR_NAME, c.DECODED_PSW)
            rows = q.get_data(connection, c.RK7QUERY)
            q.write_data(rows, c.RK7GROUPS, c.DOCS, c.IMAGES, c.NOIMAGE)
            q.close_connection(connection)
        except Exception as e:
            u.log_msg(func_name, True, e)
            tk.messagebox.showerror('Get Data - Error!', 'Something went wrong.\nCheck log-file for details.')
        else:
            tk.messagebox.showinfo('Get Data - Ok!', 'Done! Now you can send it to Telegram Channel.')
            q.close_connection(connection)
    else:
        tk.messagebox.showerror("Get Data - Error!", "Looks like the Data folder/Channel is not empty.\n"
                                "Please, run first - 'Clear Data' function.")


def send_data_button():
    func_name = u.get_func_name()
    firstmsg = u.read_text_from_file(c.FIRSTMSG)
    try:
        t.send_firstmsg_to_channel(firstmsg, c.RK7GROUPS, c.DECODED_BOTTOKEN, c.CHANNELID, c.HISTORY)
        t.send_docs_to_channel(c.DOCS, c.CURRENCY, c.OPERATOR, c.DECODED_BOTTOKEN, c.CHANNELID, c.HISTORY)
    except Exception as e:
        u.log_msg(func_name, True, e)
        tk.messagebox.showerror('Send Data - Error!', 'Something went wrong.\nCheck log-file for details.')
    else:
        tk.messagebox.showinfo('Send Data - Ok!', 'Done! Check your Telegram Channel.')


def clear_data_button():
    func_name = u.get_func_name()
    try:
        t.clear_channel_history(c.DOCS, c.DECODED_BOTTOKEN, c.CHANNELID, c.HISTORY)
    except Exception as e:
        u.log_msg(func_name, True, e)
        tk.messagebox.showerror('Clear Data - Error!', 'Something went wrong.\nCheck log-file for details.')
    else:
        tk.messagebox.showinfo('Send Data - Ok!', 'Done! Telegram Channel is cleared.')


def run_tmenu():
    """Run program."""
    # Objects
    func_name = u.get_func_name()

    lc = lic.License()
    licensed = lc.chk_lic_file()

    if licensed:
        # Starting operations
        q.write_new_rk7query(c.RK7QUERY, c.RK7QUERY_CONTENT)  # if first run or not exist rk7query-file.
        t.write_new_firstmsg(c.FIRSTMSG, c.FIRSTMSG_CONTENT)  # if first run or not exist firstmsg-file.

        u.log_msg(func_name, False, f"License validation status: '{licensed}'.")
        u.log_msg(func_name, False, "Start program.")

        # Run interface
        root = tk.Tk()
        TMenuApp(master=root, get_data_button=get_data_button, send_data_button=send_data_button,
                 clear_data_button=clear_data_button)
        root.mainloop()
    else:
        u.log_msg(func_name, True, f"License validation status: '{licensed}'.\n"
                                   f"LICENSE REQUEST CODE: {lc.gen_lic_rcode()} (copied to clipboard).")
        tk.messagebox.showerror("License - Error!", f"License is expired. For new license, please,\n"
                                                    f"send request code to rodikov.pro@gmail.com\n\n"
                                                    f"{lc.gen_lic_rcode()}\nalredy copied to clipboard...\n")

    # DEBUG main program actions ------------------------------------------------------------------------------

    # # Getting SQL data & write to json
    # connection = q.connect_server(c.SRV_NAME, c.DB_NAME, c.USR_NAME, c.DECODED_PSW)
    # rows = q.get_data(connection, c.QUERY_NAME)
    # q.write_data(rows, c.RK7GROUPS, c.DOCS, c.IMAGES, c.NOIMAGE)
    # q.close_connection(connection)
    #
    # # Telegram operations
    # t.send_welcome_msg_to_channel(c.FIRST_MSG, c.RK7GROUPS, c.DECODED_BOTTOKEN, c.CHANNELID, c.HISTORY)
    # t.send_docs_to_channel(c.DOCS, c.CURRENCY, c.OPERATOR, c.DECODED_BOTTOKEN, c.CHANNELID, c.HISTORY)
    # t.clear_channel_history(c.DOCS, c.DECODED_BOTTOKEN, c.CHANNELID, c.HISTORY)
    # u.write_text_to_file(c.MANUAL, c.MANUAL_CONTENT)


run_tmenu()
