import uuid
import random
import urllib
import libs.ztweaks as zt
import ftplib
import os


def get_password():
    """
    Password generator for FTP connection
    :return: key
    """
    key = tuple('4poknutKrovaviyShnurok')  # string to generate password
    key_size = 200  # size of result key

    def str_to_int(key_string):
        res = []
        for i in key_string:
            res.append(ord(i))
        res = ''.join(str(e) for e in res)
        return res

    key = str_to_int(key)
    rd = random.Random()
    rd.seed(key)
    key = str(rd.getrandbits(key_size))
    return key


class MediaServer:
    """
    Class for work with remote FTP server contains media files

    Specify dir/folder when downloading needed file:
    * pics/   - pictures
    * avatar/ - avatar pictures
    * music/  - music
    * video/  - video
    """
    ftp = None
    user = "kamgu"
    password = None
    pwd = '/home/kamgu/cloud-drive/KAMGU-MEDIA-FTP'

    def init_local_media(self):
        """
        initializing local folder's paths to media
        :return:
        """
        from pathlib import Path
        Path(zt.ProjectFolder("media/pics")).mkdir(parents=True, exist_ok=True)
        Path(zt.ProjectFolder("media/avatar")).mkdir(parents=True, exist_ok=True)
        Path(zt.ProjectFolder("media/music")).mkdir(parents=True, exist_ok=True)
        Path(zt.ProjectFolder("media/video")).mkdir(parents=True, exist_ok=True)

    def __init__(self):
        self.password = get_password()
        self.init_local_media()
        self.ftp = ftplib.FTP(zt.GlobalVars().remote_server_ip)
        self.ftp.login('kamgu', self.password)

    def download_file(self, file_path):
        """
        download file from remote media server (using FTP)
        :param file_path: string that consists of:
          folder + filename, ex: pics/picture.png

        :Example:
            import libs.media as md
            with md.MediaServer() as ms:
                ms.download_file('pics/koshak.jpg')

        :return: void
        """
        try:
            with open(zt.ProjectFolder('media/' + file_path), 'wb') as f:
                self.ftp.retrbinary('RETR ' + file_path, f.write)
                return True
        except ftplib.error_perm:
            print('[*] [ERROR]\t[Downloading file]\tFile "' + file_path + '" does not exist or no permission..')
            return 404
        except Exception as ex:
            print('[*] [ERROR]\t[Downloading file]\tError: ' + str(ex))
            return False

    def upload_file(self, file_folder, file_path):
        """
        upload files to remote media server (using FTP)
        :param file_folder: folder to send file to
                for folder names look at class description
        :param file_path: file path to upload on server

        :Example:
            import libs.media as md
            with md.MediaServer() as ms:
                ms.upload_file('pics', 'C:/Users/ZeD/Pictures/koshak.jpg')

        :return: void
        """
        file_name = os.path.split(file_path)[-1]
        print(file_name)
        upload_path = self.pwd + '/' + file_folder + '/' + file_name
        with open(file_path, 'rb') as fobj:
            self.ftp.storbinary('STOR ' + upload_path, fobj, 1024)

    def get_pwd(self):
        """
        Return the pathname of the current directory on the server.
        :return: string
        """
        return str(self.ftp.pwd())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass


if __name__ == '__main__':
    print(get_password())
    # ftp.download_file('pics/volk.jpg')

