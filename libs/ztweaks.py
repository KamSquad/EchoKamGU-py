"""
Tweak library with global vars and some useful functions
by ZeD!
"""


def GetRemoteServerCredentials():
    """
    Function to get needed server's info for connection
    :return:
    """
    try:
        from pbwrap import Pastebin
        pastebin = Pastebin(api_dev_key=GlobalVars().pb_dev_key)
        user_id = pastebin.authenticate(username=GlobalVars().pb_user, password=GlobalVars().pb_pass)
        pb_pastes = pastebin.get_user_pastes()

        def FilterPastes():
            #  filter by name
            for paste in pb_pastes:
                if '#fizkam#' == paste.title:
                    return paste

        def ReturnConfigFromPaste(paste):
            net_str = pastebin.get_raw_paste(paste.key)
            return net_str.split("\r\n")

        pb_latest_paste = FilterPastes()
        configs = ReturnConfigFromPaste(paste=pb_latest_paste)
        return configs  # [ip, db_name, http_port, local_db_name]
    except:
        return False, False, False, False


class GlobalVars:
    debug_mode = False  # debug program's variable
    meme_mode = False
    #  \/\/\/ SERVER CONFIG
    remote_server_ip = '80.211.50.225'
    remote_server_db = 'kamgu'
    remote_server_http_port = '4141'
    #  /\/\/\
    local_db_name = 'local.db'  # name of local db based on sqlite

    user_role = ''

    def Update_local_db_InitScript(self):
        new_remote_server_ip, new_remote_server_db, new_remote_server_http_port, new_local_db_name = GetRemoteServerCredentials()
        if new_remote_server_ip:
            self.remote_server_ip = new_remote_server_ip
            self.remote_server_db = new_remote_server_db
            self.remote_server_http_port = new_remote_server_http_port
            self.local_db_name = new_local_db_name

    def local_db_SaveLoginScript(self, user_card):
        return ("""
                INSERT INTO config (id_key, value) VALUES ('user_login', '"""+user_card[1]+"""');
                INSERT INTO config (id_key, value) VALUES ('login_pass', '"""+user_card[2]+"""');
                """)

    def local_db_InitScript_AutoStartUpdate(self):
        try:
            self.Update_local_db_InitScript()
        except:
            print('[!] [ERROR]	[local_db_InitScript_AutoStartUpdate] : Failed')
        return ("""-- init tables
                UPDATE config SET value='"""+self.remote_server_ip+"""' WHERE id_key='remote_server_ip';
                UPDATE config SET value='"""+self.remote_server_db+"""' WHERE id_key='remote_server_db';
                UPDATE config SET value='"""+self.remote_server_http_port+"""' WHERE id_key='remote_server_http_port';
                UPDATE config SET value='"""+self.local_db_name+"""' WHERE id_key='local_db_name';
                """)

    def local_db_InitScript(self):
        self.Update_local_db_InitScript()
        return("""-- init tables
                     drop table if exists config;
                     drop table if exists settings;
                     drop table if exists news;
                     drop table if exists media;
                     CREATE TABLE config
                     (id_key text, value text);
                     CREATE TABLE settings
                     (id_key text, value text);
                     CREATE TABLE news
                     (id_key text, time text, title text, head_photo text, content text);
                     CREATE TABLE media
                     (id_key text, type text, path text, is_avatar text);
                     -- init default values
                     INSERT INTO config (id_key, value) VALUES ('first_run', '0');
                     INSERT INTO config (id_key, value) VALUES ('remote_server_ip', '"""+self.remote_server_ip+"""');
                     INSERT INTO config (id_key, value) VALUES ('remote_server_db', '"""+self.remote_server_db+"""');
                     INSERT INTO config (id_key, value) VALUES ('remote_server_http_port', '"""+self.remote_server_http_port+"""');
                     INSERT INTO config (id_key, value) VALUES ('local_db_name', '"""+self.local_db_name+"""');
                     
                  """)
    pb_user = 'zedcode505'
    pb_pass = 'cH8A$up4F4'
    pb_dev_key = '39b012db3b59aa64b4b01e268ae29aae'


def DefineRunningOS():
    """
    Function of detection OS
    :return: <str> ('android', 'ios', 'win', 'macos', 'linux')
    """
    if not GlobalVars().debug_mode:
        from kivy.utils import platform
        return platform
    else:
        return 'android'


def ProjectFolder(path):
    """
    Addressing project folder for working in it according to running OS
    :input: <str> path - path to file/folder for working with it
    :return: full path for kivy
    """
    from kivymd.app import MDApp
    from os.path import join
    user_data_dir = MDApp.get_running_app().user_data_dir
    full_path = join(user_data_dir, path)  # CHECK WORKING ON ANDROID/LINUX
    return full_path


def ReturnLocalDBPath():
    if GlobalVars().debug_mode:
        #  WARNING NEED CHECK OS FOR DIFFERENT RETURNS
        #  (ex: WIN - \\FOLDER\\FOLDER, ANDROID - ./FOLDER/FOLDER)
        return '.\\data\\' + GlobalVars().local_db_name
    else:
        return ProjectFolder(GlobalVars().local_db_name)


def nointernet_notify():
    from kivymd.toast import toast
    toast('Ошибка соединения с сервером. Проверьте интернет соединение')


def invalidlogin_notify():
    from kivymd.toast import toast
    toast('Неправильный логин или пароль, повторите попытку')


def checkinternet_and_notify():
    import libs.database as db
    if not db.check_internet_connection():
        nointernet_notify()
        return False
    else:
        return True


if __name__ == "__main__":
    # print(ProjectFolder(path='local.db'))
    # print(DefineRunningOS())
    # print(ReturnLocalDBPath())
    GetRemoteServerCredentials()
