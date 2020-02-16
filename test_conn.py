import pymysql
from sshtunnel import SSHTunnelForwarder
from time import sleep

server = SSHTunnelForwarder(
    '80.211.50.225',
    ssh_username="sql",
    ssh_password="%Z9Bo@E3#k",
    remote_bind_address=('127.0.0.1', 3306)
)

server.start()
sleep(1)

conn = pymysql.connect(
        host='127.0.0.1', port=server.local_bind_port, database='kamgu', user='student',
        password='kamgustudent', charset='utf8')

cur = conn.cursor()
cur.execute('select * from news')

res = ['Title: {}\nContent: {}'.format(row[1], row[3]) for row in cur]

print(*res, sep='\n\n')

conn.close()
server.stop()
