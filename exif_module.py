# Copyright 2023 Hyo Jae Jeon (CANU) canu1832@gmail.com

from PIL import Image, ImageDraw, ImageFont


# 폰트 vs padding 비율은 1:4?
# 이미지파일 vs padding 비율은 10:1
class Exif():
    def __init__(self):
        # 폰트 사이즈 (초기)
        self.__font_size = 50
        # 폰트 (초기)
        self.__font = ImageFont.truetype("Barlow-Light.ttf", self.__font_size)

    def get_exif_data(self, image):
        exif_data = image._getexif()

        if exif_data is None:
            print('Sorry, image has no exif data.')
        else:
            model = str(exif_data[272]) if 272 in exif_data else None
            lens_model = str(exif_data[42036]) if 42036 in exif_data else None
            f_number = str(exif_data[33437]) if 33437 in exif_data else None
            focal_length = str(exif_data[41989]) if 41989 in exif_data else None
            iso = str(exif_data[34855]) if 34855 in exif_data else None

            try:
                shutter_speed_value = 1 / (2 ** exif_data[37377])
                shutter_speed = f"1/{int(round(1 / shutter_speed_value))}s"

            except KeyError:
                shutter_speed = " "

            if lens_model is None:
                result_model = model
            else:
                result_model = model + " | " + lens_model

            if focal_length is None:
                focal_length = exif_data[37386]

                if model.find("X100") != -1:
                    focal_length = round(focal_length * 1.5 + 0.1)
                    focal_length = str(focal_length)
            else:
                pass

            result_exif = focal_length + "mm | F/" + f_number + " | " + "ISO " + iso + " | " + shutter_speed

            print(result_exif)

            return result_model, result_exif

    def set_image_padding(self, image, length, color):
        width, height = image.size
        new_width = width + 2 * length
        new_height = height + 2 * length

        result = Image.new(image.mode, (new_width, new_height), color)
        result.paste(image, (length, length))

        return result

    def set_image_padding2(self, image, top, side, bottom, color):
        width, height = image.size

        new_width = width + 2 * side
        new_height = height + 2 + top + bottom

        result = Image.new(image.mode, (new_width, new_height), color)
        result.paste(image, (side, top))

        return result

    def set_image_text(self, image, modelData, exifData, length):
        draw = ImageDraw.Draw(image)
        x = image.width / 2
        y = image.height - (length / 2)

        self.__font_size = length / 4.5
        self.__font = ImageFont.truetype("Barlow-Light.ttf", self.__font_size)

        draw.text(xy=(x, y - self.__font_size / 2), text=modelData, font=self.__font, fill=(0, 0, 0), anchor="ms")
        draw.text(xy=(x, y + self.__font_size), text=exifData, font=self.__font, fill=(0, 0, 0), anchor="ms")

        return image


def main():
    exif_test = Exif()

    img = Image.open("Error-Test/01.jpg")

    longerLength = img.width if img.width >= img.height else img.height
    padding = int(longerLength / 10)

    model_data, exif_data = exif_test.get_exif_data(img)
    img = exif_test.set_image_padding2(img, top=int(padding / 2), side=int(padding / 2), bottom=padding, color=(255, 255, 255))
    img = exif_test.set_image_text(img, modelData=model_data, exifData=exif_data, length=padding)
    img.show()

    img.save("01_a.jpg")


if __name__ == "__main__":
    main()
