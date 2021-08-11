import platform
import os
import time
try:
    from win10toast import ToastNotifier
except:
    pass
from core.logger import logger
class PyNotify():

    def __init__(self, title, message, filepath, timeout=10):
        self.message = message
        self.title = title
        self.timeout = timeout
        self.filepath = filepath

    def push(self):
        system_name = platform.system().lower()
        if system_name == 'darwin':
            command = f"osascript -e 'display notification \"{self.message}\" with title \"{self.title}\"'"
            os.system(command)

        elif system_name == 'linux':
            command = f'notify-send "{self.title}" "{self.message}" -t {self.timeout} -i {self.filepath}'
            os.system(command)

        # Displays an alertbox
        elif system_name == 'windows':
            toaster = ToastNotifier()
            toaster.show_toast(self.title,
                               self.message,
                               icon_path=self.filepath,
                               duration=self.timeout,
                               threaded=True)
            while toaster.notification_active():
                time.sleep(0.1)
        logger.info('send notify successfully')