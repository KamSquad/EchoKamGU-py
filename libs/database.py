import pymysql
import sqlite3
import libs.ztweaks as ztweaks
from libs import ztweaks


class RemoteDB:
    """
    CLASS FOR WORKING WITH REMOTE DB BASED ON MYSQL
    """

    def __init__(self, db_ip, db_login, db_pass, db_name):
        self.db_connection = pymysql.connect(db_ip, db_login, db_pass, db_name)
        self.db_cursor = self.db_connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._close()

    def _cmd_get_one(self, cmd_str):
        self.db_cursor.execute(cmd_str)
        return self.db_cursor.fetchone()

    def _cmd_get_all(self, cmd_str, cursor=None):
        self.db_cursor.execute(cmd_str)
        return self.db_cursor.fetchall()

    def _close(self):
        self.db_connection.close()


class LocalDB:
    """
    CLASS FOR WORKING WITH LOCAL DB BASED ON SQLITE
    """

    local_db_name = ztweaks.GlobalVars.local_db_name

    def __init__(self, update=True):
        def init_empty_db():
            """
            FUNCTION FOR FIRST INIT OF DB
            """
            self.db_cursor.executescript(ztweaks.GlobalVars().local_db_InitScript())
            self.db_connection.commit()  # save changes

        def local_bd_is_empty():
            tables = ['config', 'news', 'media', 'settings']
            for table in tables:
                if not self.db_cursor.execute('SELECT COUNT(*) FROM ' + table).fetchone():
                    return True

        def local_db_update():
            """
            FUNCTION TO UPDATE REMOTE CREDENTIALS IN LOCAL DB
            """
            self.db_cursor.executescript(ztweaks.GlobalVars().local_db_InitScript_AutoStartUpdate())
            self.db_connection.commit()  # save changes

        try:
            """
            CONNECT TO DB
            """
            # print(ztweaks.ReturnLocalDBPath())
            self.db_connection = sqlite3.connect(ztweaks.ReturnLocalDBPath())
            self.db_cursor = self.db_connection.cursor()
            if local_bd_is_empty():
                init_empty_db()
            else:
                local_db_update()

        except Exception as ex:
            print('[!] Error:\t' + str(ex))
            print('[!] Debug Warning:\tlocal db connection failed, running first init...')
            init_empty_db()

    def __enter__(self):
        return self

    def __exit__(self):
        self.db_connection.close()


def GetNewsByUser(user='student', password='kamgustudent'):
    db_ip = ztweaks.GlobalVars().remote_server_ip
    db_name = ztweaks.GlobalVars().remote_server_db
    with RemoteDB(db_ip=db_ip, db_login=user, db_pass=password, db_name=db_name) as rserv:
        res = rserv._cmd_get_all('SELECT * FROM kamgu.news;')
        return res  # print(res)


def LoginFunc(login, password):
    from kivymd.toast.kivytoast.kivytoast import toast
    toast('running auth..')
    user_card = CheckUserLoginPass(login, password)
    if user_card:
        SaveUserLoginPass(user_card)
        toast('Auth success')
    else:
        toast('Auth failed')


def SaveUserLoginPass(user_card):
    with LocalDB(update=False) as ldb:
        ldb.db_cursor.executescript(ztweaks.GlobalVars().local_db_SaveLoginScript(user_card))
        ldb.db_connection.commit()  # save changes


def CheckUserLoginPass(login, password):
    db_ip = ztweaks.GlobalVars().remote_server_ip
    db_name = ztweaks.GlobalVars().remote_server_db
    with RemoteDB(db_ip=db_ip, db_login='guest', db_pass='kamguguest', db_name=db_name) as rserv:
        try:
            #hash_pass = ''
            import hashlib
            hashed_password = hashlib.md5(password)
            print(hashed_password)
            res = rserv._cmd_get_one(
                "SELECT id, username, password, type FROM kamgu.users_login WHERE password='" + password + "' AND username='" + login + "';")
            if res:
                return res  # print(res)
        except:
            return False


def DownloadPictureByHTTP(server_ip, server_port='4141', file_name='logo.png'):
    import urllib3
    import shutil
    http = urllib3.PoolManager()
    url = 'http://' + server_ip + ':' + server_port + '/' + file_name
    with http.request('GET', url, preload_content=False) as resp, open('./data/pics/' + file_name, 'wb') as out_file:
        shutil.copyfileobj(resp, out_file)


if __name__ == '__main__':
    server_ip = ztweaks.GlobalVars.remote_server_ip
    server_port = ztweaks.GlobalVars().remote_server_http_port  # SERVER PORT BY DEFAULT
    # DownloadPictureByHTTP(server_ip=server_ip)  # TEST HTTP DOWNLOAD
    # KamGUServer = RemoteDB(db_ip=server_ip, db_login='student', db_pass='kamgustudent', db_name='kamgu')
    # print(GetNewsByUser())
    # local_db = LocalDB()
    LoginFunc('student_ffimk', 'password')
    # print( CheckUserLoginPass('student_fmf', 'password') )
