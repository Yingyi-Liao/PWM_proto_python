import pyodbc as odbc
from cryptography.fernet import Fernet
import datetime


loginAcc = 'test'
global getLogin_ID

DRIVER_NAME = 'SQL Server'
SERVER_NAME = 'middletohigh'
DATABASE_NAME = 'PasswordManager'
connection_string = f"DRIVER={DRIVER_NAME};\n" \
                    f"SERVER={SERVER_NAME};\n" \
                    f"DATABASE={DATABASE_NAME};\n" \
                    f"Trust_Connection=yes;"
conn = odbc.connect(connection_string)
cursor = conn.cursor()

query = f'SELECT Login_ID FROM Login WHERE (LoginAcc = \'{loginAcc}\')'
cursor.execute(query)
for z in cursor:
    getLogin_ID = z[0]


def query_from_date():
    while True:
        qDate = str(input('Please entry the date entry created(YYYY-MM-DD):'))
        try:
            datetime.date.fromisoformat(qDate)
            print(datetime.date.fromisoformat(qDate))
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

    query1 = f'SELECT COUNT(*) FROM Store WHERE (Time >= \'{qDate} 00:00:00.000\' and Time <= \'{qDate + 1} 00:00:00.000\' and Login_ID = {getLogin_ID})'
    cursor.execute(query1)
    for x in cursor:
        if x[0] == 0:
            print('This account user name does not exist!')
        else:
            query2 = (f'SELECT Store_ID, SourceName, UserAcc, UserPwd, StoreComm '
                      f'FROM Store '
                      f'LEFT JOIN Login on Store.Login_ID = Login.Login_ID '
                      f'LEFT JOIN Source on Store.Source_ID = Source.Source_ID '
                      f'WHERE Store.Login_ID = {getLogin_ID} and Store.Time = \'{qDate}\'')
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


query_from_date()