from PIL import Image, ImageTk
from tkinter import Tk, Label, LEFT, Canvas, X, Y, TOP
import time
import platform


class TkinterNotice:
    _window = None
    sucess_color = '#67C23A'
    warn_color = '#F56C6C'
    major_color = '#45898A'
    background_color = '#C6E2FF'
    width = 300
    height = 100

    def __init__(self):
        self._window = Tk()
        screen_width = self._window.winfo_screenwidth()
        screen_height = self._window.winfo_screenheight()
        geometry = self._get_geometry(screen_width, screen_height)
        self._window.geometry(geometry)
        self._window.configure(bg=self.background_color)
        self._window.overrideredirect(True)

    def _get_geometry(self, width: int, height: int):
        system_name = platform.system().lower()
        if system_name == 'linux':
            return f'{self.width}x{self.height}+{(width - self.width) // 2}+0'
        elif system_name == 'windows':
            return f'{self.width}x{self.height}+{width - self.width - 10}+{height - self.height - 110}'
        elif system_name == 'darwin':
            return f'{self.width}x{self.height}+{(width - self.width) // 2}+0'
        else:
            return f'{self.width}x{self.height}+{(width - self.width) // 2}+0'

    def send(self, is_success: bool, result: str, filepath: str):
        # 创建550 * 300的画布
        canvas = Canvas(self._window, bg=self.background_color, width=100, height=100)
        # 在画布上创建图像，放置导入图片
        img = Image.open(filepath)
        width, height = img.size
        width = width * self.height // height
        # 以通知窗体的高度为基准，等比例缩放图片生成缩略图
        img.thumbnail((width, self.height), Image.ANTIALIAS)
        small = 100
        # 去出来的部分为中心部分的矩形（如300*100取的是(100,0,200,100)）
        box = ((img.size[0] - small) / 2, (img.size[1] - small), (img.size[0] - small) / 2 + small,
               (img.size[1] - small) / 2 + small)
        # 裁切缩略图片
        img = img.crop(box)
        width = img.size[0]
        # 生成图片数据
        image = ImageTk.PhotoImage(img)

        # 向画布绘图
        canvas.create_image(width // 2, 0, anchor='n', image=image)
        canvas.configure(highlightthickness=0)
        title = 'PyPicGo上传成功'
        msg = f'返回信息为：{result}'
        color = self.sucess_color
        if not is_success:
            color = self.warn_color
            title = 'PyPicGo上传失败'

        label_tiitle = Label(
            master=self._window,
            text=title,
            wraplength=240,
            bg=self.background_color,
            font=(None, 15),
            fg=color)
        label_body = Label(
            master=self._window,
            text=msg,
            wraplength=240,
            bg=self.background_color,
            fg=self.major_color,
            )
        canvas.pack(fill=Y, side=LEFT)  # #相对布局
        label_tiitle.pack(fill=X, side=TOP)
        label_body.pack()

        self._window.after(1000, self.destroy)
        self._window.mainloop()

    def destroy(self):
        for i in range(100, 0, 5):  # 这里不会生成775，要使用比750大25的数字结尾
            self._window.attributes('-alpha', i / 100.0)
            time.sleep(0.01)

        self._window.after(1, self._window.destroy)
