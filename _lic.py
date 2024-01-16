import _utils as u


class License:

    import datetime as dt
    import random
    import uuid
    import pyperclip

    def __init__(self):

        self.NOW = self.dt.datetime.now()  # now date & time
        self.FILE = 'lic.dat'

    def gen_lic_rcode(self):
        """ This function is a simple version for Code in place IDE. """
        func_name = u.get_func_name()

        num = str(self.random.randint(10000000, 99999999))
        guid_dict = {
            "date_time": self.NOW.strftime('%Y%m%d-'),  # year.month.day-
            "pc_uuid": str(self.uuid.getnode())[:8],  # PC UUID (unicum pc number)
            "random_num": '-' + str(num)
        }
        rcode = ""
        for key, value in guid_dict.items():
            rcode += value

        self.pyperclip.copy(rcode)  # copy request code to clipboard
        # print("License Request Code: " + rcode + " created and copied to clipboard.")
        # u.log_msg(func_name, False, f"REQUEST CODE: {rcode}")
        return rcode  # 20230609-24632113-82685405

    def gen_lic_file(self, rcode: str, expdate: str):
        """ This function could be using in License Generation Application to Create and write control lic file using
        control params from license request guid.

        rcode - license request code string;
        expdate - expire date string (YYYY.MM.DD).

        License Control String Params:
        - Control String size = 264 characters/bytes;
        - '1?' + License request code uuid part1 (6)
        - '2?' + License request code uuid part2 (6)
        - '3?' + License expiration date year (6)
        - '4?' + License expiration date month, day (6) """

        # Step 1 - Characters and params for creating license control string
        symbols = ('#', '$', '%', '&', '*', '+', '[', ']', ';', ':', '{', '}')
        letters = ('A', 'B', 'C', 'D', 'E', 'F')

        control_list = []
        for _ in range(40):  #
            control_list.append(str(self.random.randint(1000, 9999)))  # add random digit number to file_body_list
            control_list.append(self.random.choice(letters))  # add random letter
            control_list.append(self.random.choice(symbols))  # add random symbol
        # print(control_list)

        # Step 2 - Create License Control Params dict
        control_params = {
            'uuid1': '1?' + rcode[9:13],
            'uuid2': '2?' + rcode[13:17],
            'exp_year': '3?' + expdate[:4],
            'exp_mmdd': '4?' + expdate[5:7] + expdate[8:10]
        }
        # Step 3 - Insert control params to a list and shuffle it.
        ins_index = self.random.randint(1, len(control_list))
        for key, value in control_params.items():
            control_list.insert(ins_index, value)
        self.random.shuffle(control_list)  # shuffle list

        # Step 4 / Convert shuffled list to a control string.
        lic_string = ""
        for i in control_list:
            lic_string += i

        with open(self.FILE, 'w') as f:
            f.write(lic_string)

        return lic_string

    def chk_lic_file(self):
        """ Open License Control String, check file size (should be 264 byte), extract 4 Control Parameters
        and compare with PC system date and UUID num. If all 3 check-tests (string size, date, UUID) passed successfully
        return True. """
        func_name = u.get_func_name()
        try:
            with open(self.FILE) as file:
                f_string = file.read()

        except Exception as e:
            # print(f"File error: {e}")
            u.log_msg(func_name, True, e)
        else:
            c_str = f_string

            # Step 1 - Check string size (264)
            if len(c_str) == 264:
                # print("Step 1 Checking -> passed!")
                u.log_msg(func_name, False, "Step 1 Checking -> passed!")

                # Step 2 - Compare pc date with date in control string
                pc_date = self.NOW.strftime('%Y%m%d')  # pc system date : str
                c_date = c_str[c_str.find('3?') + 2: c_str.find('3?') + 6] + c_str[c_str.find('4?') + 2: c_str.find('4?') + 6]

                if int(c_date) > int(pc_date):  # Compare 2 dates:
                    # print("Step 2 Checking -> passed!")
                    u.log_msg(func_name, False, "Step 2 Checking -> passed!")

                    # Step 3 - Compare pc uuid[:8] with  uuid in control string
                    pc_uuid = str(self.uuid.getnode())[:8]  # pc uuid
                    c_uuid = c_str[c_str.find('1?') + 2: c_str.find('1?') + 6] + c_str[
                                                                                 c_str.find('2?') + 2: c_str.find('2?') + 6]

                    if c_uuid == pc_uuid:
                        # print("Step 3 Checking -> passed!")
                        u.log_msg(func_name, False, "Step 3 Checking -> passed!")
                        return True
                    else:
                        # print("Step 1 Checking -> failed!")
                        u.log_msg(func_name, True, "Step 1 Checking -> failed!")
                        return False
                else:
                    # print("Step 2 Checking -> failed!")
                    u.log_msg(func_name, True, "Step 2 Checking -> failed!")
                    return False

    def plus_month_date(self):

        yyyy = str(self.NOW.year)
        mm = str(self.NOW.month + 1)
        dd = str(self.NOW.day)

        if len(mm) != 2:
            mm = '0' + mm
        if len(dd) != 2:
            dd = '0' + dd

        return yyyy + '.' + mm + '.' + dd

    def run_console_user_interface(self):
        """ Console user interface to demonstrate generation license_request, license_file and
        license_checking functionality. admin psw : **** """

        admin_psw = 'ZzXx54321!'

        print(""" 
    * License Generator & Checking Utility, v0.4
    * Developed by rodikov.pro'
    * Support: rodikov.pro@gmail.com\n""")

        menu0 = input("For 'USER MENU' press 'Enter': ")

        if menu0 != admin_psw:  # USER MENU

            while True:
                print(""" 
    * USER MENU: 
    1 - Generate License Request code. 
    2 - Exit.""")
                menu = input('Select - 1, 2: ')

                if menu == '1':
                    # gen_license_request_guid()
                    self.gen_lic_rcode()
                    print("Now, you can paste and send this code to rodikov.pro@gmail.com > to get your license file.")
                else:
                    print("Bye!")
                    break

        else:  # ADMIN MENU
            while True:
                print(""" 
    * ADMIN MENU: 
    1 - Generate License String (using Request Code and Expiration Date).
    2 - Exit.""")
                menu = input('Select - 1, 2')
                if menu == '1':
                    # actions with request code
                    code = input("Enter License Request Code, or press 'Enter': ")
                    # Request Code params checking
                    if len(code) != 26 or code[8] != '-' or code[16] != '-':
                        print("Wrong License Request. Will be generated and used request for this PC.")
                        code = self.gen_lic_rcode()

                    date = input(f"Enter License Expiration Date YYYY.MM.DD, or 'Enter' for {self.plus_month_date()}: ")
                    # date params checking
                    if len(date) != 10 or date[4] != '.' or date[7] != '.':
                        date = self.plus_month_date()
                        print(f"Wrong date. Will be used maximum expiration date - {date}")

                    control_string = self.gen_lic_file(rcode=code, expdate=date)
                    print("License Control String\n" + control_string + "\n-generated successful.")

                else:

                    print("Bye!")
                    break

