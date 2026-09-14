# Password Manager queries
# Author: Yingyi Liao
# For private use only

import pyodbc as odbc
from cryptography.fernet import Fernet
import datetime
from prettytable import PrettyTable

loginAcc = 'test'
getLogin_ID = 1


def query_from_source():
    while True:
        qSource = str(input('Please entry the query source:'))
        if len(qSource) == 0 or len(qSource.strip(' ')) == 0:
            print('Source can not be blank or contains while space only!\n Please try again')
        else:
            break

    DRIVER_NAME = 'SQL Server'
    SERVER_NAME = 'middletohigh'
    DATABASE_NAME = 'PasswordManager'
    connection_string = f"DRIVER={DRIVER_NAME};\n" \
                        f"SERVER={SERVER_NAME};\n" \
                        f"DATABASE={DATABASE_NAME};\n" \
                        f"Trust_Connection=yes;"
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()

    query1 = f'SELECT COUNT(*) FROM Source WHERE (SourceName = \'{qSource}\')'
    cursor.execute(query1)
    for x in cursor:
        if x[0] == 0:
            print('This source does not exist!')
        else:
            query2 = f'SELECT Source_ID FROM Source WHERE (SourceName = \'{qSource}\')'
            cursor.execute(query2)
            for y in cursor:
                getSource_ID = y[0]

            query3 = f'SELECT COUNT(*) FROM Store WHERE (Login_ID = {getLogin_ID} and Source_ID = {getSource_ID})'
            cursor.execute(query3)
            for p in cursor:
                if p[0] == 0:
                    print('This source does not exist!')
                else:
                    query4 = (f'SELECT Store_ID, SourceName, UserAcc, UserPwd, StoreComm, Time '
                              f'FROM Store '
                              f'LEFT JOIN Login on Store.Login_ID = Login.Login_ID '
                              f'LEFT JOIN Source on Store.Source_ID = Source.Source_ID '
                              f'WHERE Store.Login_ID = {getLogin_ID} and Store.Source_ID = {getSource_ID}')
                    cursor.execute(query4)
                    for u in cursor:
                        getStore_ID = u[0]
                        token = u[3]
                        with open(f'{loginAcc}.key', 'r') as g:
                            a = g.readlines()
                            for b in a:
                                c = b.split(':divider:')
                                if getStore_ID == int(c[1]):
                                    key = c[0]
                                    decryptPwd = Fernet(key).decrypt(token)

                        print(f'{u[1]}, {u[2]}, {decryptPwd.decode()}, {u[4]}')


def query_from_acc_name():
    while True:
        qAccName = str(input('Please entry the account user name:'))
        if len(qAccName) == 0 or len(qAccName.strip(' ')) == 0:
            print('Account user name can not be blank or contains while space only!\n Please try again')
        else:
            break

    DRIVER_NAME = 'SQL Server'
    SERVER_NAME = 'middletohigh'
    DATABASE_NAME = 'PasswordManager'
    connection_string = f"DRIVER={DRIVER_NAME};\n" \
                        f"SERVER={SERVER_NAME};\n" \
                        f"DATABASE={DATABASE_NAME};\n" \
                        f"Trust_Connection=yes;"
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()

    query1 = f'SELECT COUNT(*) FROM Store WHERE (UserAcc = \'{qAccName}\' and Login_ID = {getLogin_ID})'
    cursor.execute(query1)
    for x in cursor:
        if x[0] == 0:
            print('This account user name does not exist!')
        else:
            query2 = (f'SELECT Store_ID, SourceName, UserAcc, UserPwd, StoreComm, Time '
                      f'FROM Store '
                      f'LEFT JOIN Login on Store.Login_ID = Login.Login_ID '
                      f'LEFT JOIN Source on Store.Source_ID = Source.Source_ID '
                      f'WHERE Store.Login_ID = {getLogin_ID} and Store.UserAcc = \'{qAccName}\'')
            cursor.execute(query2)
            for u in cursor:
                getStore_ID = u[0]
                token = u[3]
                with open(f'{loginAcc}.key', 'r') as g:
                    a = g.readlines()
                    for b in a:
                        c = b.split(':divider:')
                        if getStore_ID == int(c[1]):
                            key = c[0]
                            decryptPwd = Fernet(key).decrypt(token)

                print(f'{u[1]}, {u[2]}, {decryptPwd.decode()}, {u[4]}')


def query_from_date():
    while True:
        qDate = str(input('Please entry the date entry created(YYYY-MM-DD):'))
        try:
            d = datetime.date.fromisoformat(qDate)
            e = d + datetime.timedelta(days=1)
            break
        except ValueError:
            print('Please enter in correct date format!')

    DRIVER_NAME = 'SQL Server'
    SERVER_NAME = 'middletohigh'
    DATABASE_NAME = 'PasswordManager'
    connection_string = f"DRIVER={DRIVER_NAME};\n" \
                        f"SERVER={SERVER_NAME};\n" \
                        f"DATABASE={DATABASE_NAME};\n" \
                        f"Trust_Connection=yes;"
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()

    query1 = f'SELECT COUNT(*) FROM Store WHERE (Time >= \'{d} 00:00:00.000\' and Time <= \'{e} 00:00:00.000\' and Login_ID = {getLogin_ID})'
    cursor.execute(query1)
    for x in cursor:
        if x[0] == 0:
            print('This date does not exist!')
        else:
            query2 = (f'SELECT Store_ID, SourceName, UserAcc, UserPwd, StoreComm '
                      f'FROM Store '
                      f'LEFT JOIN Login on Store.Login_ID = Login.Login_ID '
                      f'LEFT JOIN Source on Store.Source_ID = Source.Source_ID '
                      f'WHERE Store.Login_ID = {getLogin_ID} and Store.Time >= \'{d} 00:00:00.000\' and Time <= \'{e} 00:00:00.000\'')
            cursor.execute(query2)
            for u in cursor:
                getStore_ID = u[0]
                token = u[3]
                with open(f'{loginAcc}.key', 'r') as g:
                    a = g.readlines()
                    for b in a:
                        c = b.split(':divider:')
                        if getStore_ID == int(c[1]):
                            key = c[0]
                            decryptPwd = Fernet(key).decrypt(token)

                print(f'{u[1]}, {u[2]}, {decryptPwd.decode()}, {u[4]}')


def query_from_all():
    DRIVER_NAME = 'SQL Server'
    SERVER_NAME = 'middletohigh'
    DATABASE_NAME = 'PasswordManager'
    connection_string = f"DRIVER={DRIVER_NAME};\n" \
                        f"SERVER={SERVER_NAME};\n" \
                        f"DATABASE={DATABASE_NAME};\n" \
                        f"Trust_Connection=yes;"
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()

    query2 = (f'SELECT Store_ID, SourceName, UserAcc, UserPwd, StoreComm, Time '
              f'FROM Store '
              f'LEFT JOIN Login on Store.Login_ID = Login.Login_ID '
              f'LEFT JOIN Source on Store.Source_ID = Source.Source_ID '
              f'WHERE Store.Login_ID = {getLogin_ID}')
    cursor.execute(query2)
    table = PrettyTable()
    table.field_names = ['Source Name', 'User Account', 'User Password', 'Comment', 'Time']
    t = 0
    for u in cursor:
        getStore_ID = u[0]
        token = u[3]
        with open(f'{loginAcc}.key', 'r') as g:
            a = g.readlines()
            for b in a:
                c = b.split(':divider:')
                if getStore_ID == int(c[1]):
                    key = c[0]
                    decryptPwd = Fernet(key).decrypt(token)
                table.add_row([u[1], u[2], decryptPwd.decode(), u[4], u[5]])
                print(f'{u[1]}, {u[2]}, {decryptPwd.decode()}, {u[4]}, {u[5]}')
                t += 1
    print(table)
    print(t)


def decrypt_pwd():
    for u in cursor:
        getStore_ID = u[0]
        token = u[3]
        with open(f'{loginAcc}.key', 'r') as g:
            a = g.readlines()
            for b in a:
                c = b.split(':divider:')
                if getStore_ID == int(c[1]):
                    key = c[0]
                    decryptPwd = Fernet(key).decrypt(token)

        print(f'{u[1]}, {u[2]}, {decryptPwd.decode()}, {u[4]}, {u[5]}')


query_from_all()
