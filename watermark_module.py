from PIL import Image, ImageFont, ImageDraw


class Watermark:
    def __init__(self):
        # 변수 초기화

        # 폰트 사이즈 (초기
        self.__font_size = 30
        # 폰트 (초기)
        self.__font = ImageFont.truetype("Barlow-Light.ttf", self.__font_size)

    def insert_watermark(self, image, font_color, watermark_text):
        width, height = image.size

        draw = ImageDraw.Draw(image)
        x, y = int(width / 2), int(height / 2)

        self.__font = ImageFont.truetype("Barlow-Light.ttf", self.__font_size)

        if font_color:  # FontColor가
            draw.text(xy=(width / 2 - (self.__font_size * 2), height / 2), text=watermark_text, font=self.__font,
                      fill=(0, 0, 0))
        else:
            draw.text(xy=(width / 2 + (self.__font_size * 2), height / 2), text=watermark_text, font=self.__font,
                      fill=(255, 255, 255))

        return image

    def set_font_size(self, x, y):
        if x > y:
            self.__font_size = y
        elif y > x:
            self.__font_size = x
        else:
            self.__font_size = x

        self.__font_size = int(self.__font_size / 6)
