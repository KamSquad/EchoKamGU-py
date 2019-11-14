import mysql.connector


def read_cursor(mycursor):
    for x in mycursor:
        print(x)


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="SQLpythonkivy",
    database='test'
)

mycursor = mydb.cursor()

mycursor.execute("select * from test")
read_cursor(mycursor)

# mycursor.execute("insert into test values ('some more text', NOW(), 'third')")
# mycursor.execute("select * from test")
# read_cursor(mycursor)
#
# mydb.commit()
