from PIL import Image
from pathlib import Path
from pypicgo.core.base.plugin import BeforePlugin
from pypicgo.core.base.file import UploadFile

BASE_DIR = Path(__file__).resolve().parent


class Compress(BeforePlugin):
    name = 'compress'

    def __init__(self, ratio: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        self.ratio = ratio

    def execute(self, file: UploadFile) -> UploadFile:
        filepath = file.tempfile.resolve()
        filename = file.tempfile.name
        img = Image.open(filepath)
        width, height = img.size
        after_width = int(width * self.ratio)
        after_height = int(height * self.ratio)
        after_filepath = BASE_DIR.joinpath('temp')
        if not after_filepath.exists():
            after_filepath.mkdir(parents=True)
        after_filepath = after_filepath.joinpath(filename)

        img.resize((after_width, after_height), Image.ANTIALIAS)
        img.save(after_filepath.resolve(), quality=95)
        file.tempfile = after_filepath
        return file
