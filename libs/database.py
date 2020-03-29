import pymysql
import sqlite3
import libs.ztweaks as ztweaks


# from libs import ztweaks


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

    def init_empty_db(self):
        """
        FUNCTION FOR FIRST INIT OF DB
        """
        self.db_cursor.executescript(ztweaks.GlobalVars().local_db_InitScript())
        self.db_connection.commit()  # save changes

    def local_db_is_empty(self):
        tables = ['config', 'news', 'media', 'settings']
        for table in tables:
            if not self.db_cursor.execute('SELECT COUNT(*) FROM ' + table).fetchone():
                return True

    def get_startscreen(self):
        return int(self.db_cursor.execute('SELECT value FROM config WHERE id_key="first_run"').fetchone()[0])

    def set_startscreen(self, value):
        """
        0 - greetings
        1 - login
        2 - news
        :param value: on what to switch start screen
        """
        self.db_cursor.executescript('UPDATE config SET value="' + str(value) + '" WHERE id_key="first_run"')
        self.db_connection.commit()  # save changes

    def save_usertoken(self, login_hash, pass_hash):
        user_token = login_hash + '-' + pass_hash
        self.db_cursor.executescript(
            '''INSERT OR IGNORE INTO config (id_key, value) VALUES ('user_token', "''' + user_token + '''");
                                        UPDATE config SET value = "''' + user_token + '''" WHERE id_key='user_token';
                                        ''')
        self.db_connection.commit()  # save changes

    def get_usertoken(self):
        return self.db_cursor.execute('SELECT value FROM config WHERE id_key="user_token"').fetchone()
        print()

    def __init__(self):
        try:
            """
            CONNECT TO DB
            """
            # print(ztweaks.ReturnLocalDBPath())
            self.db_connection = sqlite3.connect(ztweaks.ReturnLocalDBPath())
            self.db_cursor = self.db_connection.cursor()
            if LocalDB.local_db_is_empty(self):
                LocalDB.init_empty_db(self)
        except Exception as ex:
            print('[!] Error:\t' + str(ex))
            print('[!] Debug Warning:\tlocal db connection failed, running first init...')
            LocalDB.init_empty_db(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._close()

    def _close(self):
        self.db_connection.close()


def GetNewsByUser(user='student', password='kamgustudent'):
    db_ip = ztweaks.GlobalVars().remote_server_ip
    db_name = ztweaks.GlobalVars().remote_server_db
    with RemoteDB(db_ip=db_ip, db_login=user, db_pass=password, db_name=db_name) as rserv:
        res = rserv._cmd_get_all('SELECT * FROM kamgu.news;')
        return res  # print(res)


def LoginFunc(login, password):
    login_result = CheckUserLoginPass(login, password)
    if login_result:
        return login_result[0], login_result[1]
    else:
        return False


def check_usertoken():
    """
    verify user_token validation with remote server
    :return: 
    """

    def return_fail_result():
        """
        reset token and return to login form
        :return:
        """
        return False

    try:
        with LocalDB() as ldb:
            login_hash, pass_hash = ldb.get_usertoken()[0].split('-')
        if login_hash:
            with RemoteDB(db_ip=ztweaks.GlobalVars().remote_server_ip, db_login='student',
                          db_pass='kamgustudent', db_name=ztweaks.GlobalVars().remote_server_db) as rdb:
                return rdb._cmd_get_one(
                    "SELECT id, type FROM users_login WHERE md5(username)='" + login_hash +
                    "' AND md5(password)='" + pass_hash + "'")
        else:
            return_fail_result()
    except:
        return_fail_result()


def check_internet_connection():
    try:
        rdb = RemoteDB(ztweaks.GlobalVars().remote_server_ip, 'student', 'kamgustudent',
                  ztweaks.GlobalVars().remote_server_db)
        print('[+] [INFO]	[check_internet_connection] : Success')
        return True
    except:
        print('[!] [ERROR]	[check_internet_connection] : Failed')
        return False

def check_on_init():
    """
    to call when app starts
    fail => drop to login and reset 'user_token'
    :return:
    """
    if check_usertoken():
        print('[+] [INFO]\t[check_usertoken] : Success')
        return True
    else:
        print('[!] [ERROR]\t[check_usertoken] : Failed')
        return False


def CheckUserLoginPass(login, password):
    db_ip = ztweaks.GlobalVars().remote_server_ip
    db_name = ztweaks.GlobalVars().remote_server_db
    with RemoteDB(db_ip=db_ip, db_login='guest', db_pass='kamguguest', db_name=db_name) as rserv:
        try:
            # hash_pass = ''
            import hashlib
            hashed_login = hashlib.md5(login.encode('utf-8')).hexdigest()
            hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()
            # print(hashed_login, hashed_password)
            res = rserv._cmd_get_one(
                "SELECT id, type FROM users_login WHERE md5(username)='" + hashed_login + "' AND md5(password)='" + hashed_password + "'")
            if res:
                hashed_role = hashlib.md5(str(res[1]).encode('utf-8')).hexdigest()
                # save hash of password in local db
                # SaveUserToken(hashed_password, hashed_role)
                return hashed_login, hashed_password
        except Exception as ex:
            print('[!] [ERROR]\t[CheckUserLoginPass]', ex)
            return None


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

    # print( CheckUserLoginPass('student_fmf', 'password') )

    # DownloadPictureByHTTP(server_ip=server_ip)  # TEST HTTP DOWNLOAD
    # KamGUServer = RemoteDB(db_ip=server_ip, db_login='student', db_pass='kamgustudent', db_name='kamgu')
    # print(GetNewsByUser())
    # local_db = LocalDB()
    # SaveUserToken('student_fmf', 'password')
    # SaveUserToken('aa', 'gg')
    # LoginFunc('student_ffimk', 'password')
    # print( CheckUserLoginPass('student_fmf', 'password') )
