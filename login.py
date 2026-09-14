# Password Manager login
# Author: Yingyi Liao
# For private use only
# ref: https://www.youtube.com/watch?v=3NEzo3CfbPg Secure Login System in Python

import pyodbc as odbc
import hashlib
import stdiomask

login_successful = False
global getLogin_ID
global loginAcc


def login():
    global login_successful, loginAcc, getLogin_ID
    while not login_successful:
        loginAcc = str(input('Please enter your login account:'))
        loginPwd = hashlib.sha256(stdiomask.getpass(prompt='Please enter your login password:', mask='*').encode()).hexdigest()

        DRIVER_NAME = 'SQL Server'
        SERVER_NAME = 'MIDDLETOHIGH'
        DATABASE_NAME = 'PasswordManager'
        connection_string = f"DRIVER={DRIVER_NAME};\n" \
                            f"SERVER={SERVER_NAME};\n" \
                            f"DATABASE={DATABASE_NAME};\n" \
                            f"Trust_Connection=yes;"

        conn = odbc.connect(connection_string)
        cursor = conn.cursor()

        query = f'SELECT COUNT(*) FROM Login WHERE (LoginAcc = \'{loginAcc}\' and LoginPwd = \'{loginPwd}\')'

        cursor.execute(query)
        for x in cursor:
            y = list(x)
            if y[0] == 1:
                login_successful = True

        if login_successful:
            print(f'Login successful, welcome {loginAcc}')
            query3 = f'SELECT Login_ID FROM Login WHERE (LoginAcc = \'{loginAcc}\')'
            cursor.execute(query3)
            for z in cursor:
                getLogin_ID = z[0]
            break
        else:
            print('Incorrect login account or password')


login()
