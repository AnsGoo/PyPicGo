from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from pypicgo.core.base.plugin import BeforePlugin
from pypicgo.core.base.file import UploadFile
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent


class WaterMarkPlugin(BeforePlugin):
    name = 'watermark'

    def __init__(self, mark: str, size:int=40, font:Optional[str]=None,**kwargs):
        super().__init__(**kwargs)
        self.size = size
        self.mark = mark
        if font:
            self.font = font
        else:
            self.font = str(BASE_DIR.joinpath('SourceHanSans-Light.otf').resolve())

    def execute(self, file: UploadFile) -> UploadFile:
        filepath = file.tempfile.resolve()
        filename = file.tempfile.name
        img = Image.open(filepath).convert('RGBA')
        width, height = img.size
        after_filepath = BASE_DIR.joinpath('temp')
        if not after_filepath.exists():
            after_filepath.mkdir(parents=True)
        after_filepath = after_filepath.joinpath(filename)
        mark_layer = Image.new('RGBA',img.size,(0,0,0,0))
        draw = ImageDraw.Draw(mark_layer)
        mark_length = len(self.mark) * self.size
        if mark_length > width:
            mark_length = width
        fnt = ImageFont.truetype(font=self.font, size=self.size)
        location = (width - mark_length, height - self.size * 2)

        draw.text(xy=location,text=self.mark, font=fnt)
        mark_img = Image.alpha_composite(img, mark_layer)
        mark_img = mark_img.convert('RGBA')
        
        mark_img.save(after_filepath.resolve())
        file.tempfile = after_filepath
        return file
