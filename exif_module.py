# Copyright 2023 Hyo Jae Jeon (CANU) canu1832@gmail.com

from PIL import Image, ImageDraw, ImageFont

from fractions import Fraction


# 폰트 vs padding 비율은 1:4?
# 이미지파일 vs padding 비율은 10:1


class Exif:
    def __init__(self):
        # 폰트 사이즈 (초기)
        self.font_size = 50
        # 폰트 (초기)
        self.font = ImageFont.truetype("Barlow-Light.ttf", self.font_size)
        self.dump_data = "NONEDATA"

    def debugger(self, debug_type):
        pass

    def get_exif_data(self, image):
        exif_data = image._getexif()
        result_exif = None

        if exif_data is None:
            print('Sorry, image has no exif data.')
        else:
            # 데이터 읽어오기
            model = str(exif_data[272]) if 272 in exif_data else self.dump_data
            lens_model = str(exif_data[42036]) if 42036 in exif_data else self.dump_data
            f_number = str(exif_data[33437]) if 33437 in exif_data else self.dump_data
            focal_length = str(exif_data[41989]) if 41989 in exif_data else self.dump_data
            iso = str(exif_data[34855]) if 34855 in exif_data else self.dump_data
            shutter_speed_value = exif_data.get(33434, None)
            shutter_speed = self.dump_data
            if shutter_speed_value:
                shutter_speed = f"1/{int(round(1.0 / shutter_speed_value))}s"

            if lens_model is self.dump_data:
                print("Model: " + model)
                result_model = model
            else:
                print("Model: " + model)
                print("Lens: " + lens_model)
                result_model = model + " | " + lens_model

            if focal_length is self.dump_data:
                try:
                    focal_length = str(exif_data[37386])  # 소수점
                except KeyError:
                    print("Focal Length 데이터가 없습니다.")
                    focal_length = self.dump_data
            else:
                pass

            if f_number is self.dump_data:
                print("조리개 데이터가 없습니다.")

            if iso is self.dump_data:
                print("ISO 데이터가 없습니다.")

            if shutter_speed is self.dump_data:
                print("셔터스피드 데이터가 없습니다.")

            print("FocalLength: " + focal_length)
            print("fNumber: " + f_number)
            print("ISO: " + iso)
            print("ShutterSpeed: " + shutter_speed)

            try:
                result_exif = focal_length + "mm | F/" + f_number + " | " + "ISO " + iso + " | " + shutter_speed
            except:
                print("데이터 불량, 콘솔 창의 기록을 댓글로 남겨주세요.")

            return result_model, result_exif

    @staticmethod
    def set_image_padding(image, length, color):
        width, height = image.size
        new_width = width + 2 * length
        new_height = height + 2 * length

        result = Image.new(image.mode, (new_width, new_height), color)
        result.paste(image, (length, length))

        return result

    @staticmethod
    def set_image_padding2(image, top, side, bottom, color):
        width, height = image.size

        new_width = width + 2 * side
        new_height = height + 2 + top + bottom

        result = Image.new(image.mode, (new_width, new_height), color)
        result.paste(image, (side, top))

        return result

    def set_image_text(self, image, model_data, exif_data, length):
        draw = ImageDraw.Draw(image)
        x = image.width / 2
        y = image.height - (length / 2)

        self.font_size = length / 4.5
        self.font = ImageFont.truetype("Barlow-Light.ttf", self.font_size)

        draw.text(xy=(x, y - self.font_size / 2), text=model_data, font=self.font, fill=(0, 0, 0), anchor="ms")
        draw.text(xy=(x, y + self.font_size), text=exif_data, font=self.font, fill=(0, 0, 0), anchor="ms")

        return image


def main():
    exif_test = Exif()

    img = Image.open("Error-Test/M10R-02.jpg")

    longer_length = img.width if img.width >= img.height else img.height
    padding = int(longer_length / 10)

    model_data, exif_data = exif_test.get_exif_data(img)
    img = Exif.set_image_padding2(img, top=int(padding / 2), side=int(padding / 2), bottom=padding,
                                  color=(255, 255, 255))
    img = exif_test.set_image_text(img, model_data=model_data, exif_data=exif_data, length=padding)
    img.show()

    img.save("M10R-02.jpg")


if __name__ == "__main__":
    main()
