import mysql.connector
from mysql.connector import errorcode

# PASSWORD TO SQL
password = input('haslo:')

# CONNECT WITH MyDataBase WITH CATCHING ERRORS
try:
    mybd = mysql.connector.connect(host='localhost',
                                   user='root',
                                   passwd=str(password),
                                   # database='test_database')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Something wrong with your user name or password')
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print('Database does not exist')
    else:
        print(err)
else:

    DB_NAME = 'matches'

    TABLES = {}
    TABLES['Matches'] = (
        "CREATE TABLE 'matches' ("
        "   'Country'                   varchar(100),"
        "   'Leaggue'                   varchar(100),"
        "   'Years of League'           varchar(20),"
        "   'Month'                     int(3),"
        "   'Year'                      int(5),"
        "   'Hosts name'                varchar(100),"
        "   'Guests name'               varchar(100),"
        "   'Together matchs played'    int(10),"
        "   'Number of Together breaks' int(10),"
        "   'Number of breaks Hosts'    int(10),"
        "   'Number of breaks Guests'   int(10),"
        "   'Pre Odds Hosts'            int(5),"
        "   'Pre Odds Draw'             int(5),"
        "   'Pre Odds Guests'           int(5),"
        "   'HT Odds Hosts'             int(10),"
        "   'HT Odds Draw'              int(10),"
        "   'HT Odds Guests'            int(10),"
        "   'HT Score Hosts'            int(2),"
        "   'HT Score Guests'           int(2),"
        "   'HT Ball possession ratio'  int(10),"
        "   'HT Goal situations Hosts'  int(10),"
        "   'HT Goal situations Guests' int(10),"
        "   'HT Shots on goal Hosts'    int(10),"
        "   'HT Shots on goal Guests'   int(10),"
        "   'HT Missed shots Hosts'     int(10),"
        "   'HT Missed shots Guests'    int(10),"
        "   'HT Red Cards Hosts'        int(2),"
        "   'HT Red Cards Guests'       int(2),"
        "   '# standing Host'           int(3),"
        "   '# standing Guest'          int(3),"
        "   'Full time score Hosts'     int(2),"
        "   'Full time score Guests'    int(2),"
    )
    mybd.close()