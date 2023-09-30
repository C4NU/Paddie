# Copyright 2023 Hyo Jae Jeon (CANU) canu1832@gmail.com
import os
import sys
import platform

from PIL import Image, ImageDraw, ImageFont
import math

from model_name_mapper import ModelNameMapper


# 폰트 vs padding 비율은 1:4?
# 이미지파일 vs padding 비율은 10:1


class Exif:
    def __init__(self):
        # 폰트 사이즈 (초기)
        self.font_size = 50
        # 폰트 (초기)
        if platform.system() == "Windows":
            self.font = ImageFont.truetype(os.path.join(os.getcwd(), 'Resources/Barlow-Light.ttf'), self.font_size)
        else:
            try:
                self.font = ImageFont.truetype(os.path.join(os.path.dirname(sys.executable), "Resources/Barlow-Light.ttf"), self.font_size)
            except:
                self.font = ImageFont.truetype(os.path.join(os.getcwd(), 'Resources/Barlow-Light.ttf'), self.font_size)
        self.dump_data = "NONEDATA"

    def get_exif_data(self, image):
        exif_data = image._getexif()
        result_exif = None

        if exif_data is None:
            print('Sorry, image has no exif data.')
            return None, image
 
        else:
            # 데이터 읽어오기
            model = str(exif_data.get(272, self.dump_data))
            model = ModelNameMapper.replace_model_name(model)

            lens_model = str(exif_data.get(42036, self.dump_data))
            f_number = str(exif_data.get(33437, self.dump_data))
            focal_length = str(exif_data.get(41989, self.dump_data))
            iso = str(exif_data.get(34855, self.dump_data))

            shutter_speed_value = exif_data.get(33434, None)
            shutter_speed = self.dump_data
            if shutter_speed_value:
                if shutter_speed_value < 1.0:
                    # note(komastar) : 1/1000s, 1/4000s ...
                    shutter_speed = f'1/{int(round(1.0 / shutter_speed_value))}s'
                else:
                    # note(komastar) : 1.0s, 30.0s ...
                    # note(canu): ,2 형식으로 변환시 TypeError string to Fraction.__format__ 발생..?
                    shutter_speed = f'{format(round(shutter_speed_value), ".1f")}s'

            if lens_model is self.dump_data or 'iPhone' in model:
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
        
    def set_image_text(self, image, model_data, exif_data, length, font_path, color):
        draw = ImageDraw.Draw(image)
        x = image.width / 2
        y = image.height - (length / 2)

        self.font_size = length / 4.5
        self.font = ImageFont.truetype(font_path, self.font_size)

        draw.text(xy=(x, y - self.font_size / 2), text=model_data, font=self.font, fill=color, anchor="ms")
        draw.text(xy=(x, y + self.font_size), text=exif_data, font=self.font, fill=color, anchor="ms")

        return image   

    def set_line_text(self, image, model_data, exif_data, length, font_path, color):
        draw = ImageDraw.Draw(image)
        x = image.width / 2
        y = image.height - (length / 2)
        merged_text = model_data + " | " + exif_data

        self.font_size = length / 6
        self.font = ImageFont.truetype(font_path, self.font_size)

        draw.text(xy=(x, y), text=merged_text, font=self.font, fill=color, anchor="ms")

        return image

    @staticmethod            
    def set_square_padding(image, gap, color, horizontalImage):
        width, height = image.size
        instaSize = 1440
        ratio = width / height     

        newWidth = 0
        newHeight = 0
        newX = 0
        newY = 0

        if (horizontalImage) : 			
            newWidth = instaSize - 2*gap
            newHeight = math.floor(newWidth / ratio)
            
            if (newHeight>=instaSize-10*gap) :
                newHeight = instaSize-10*gap
                newWidth= math.floor(newHeight*ratio)
 
            newX = math.floor((instaSize - newWidth )/2) 
            newY = math.floor((instaSize - newHeight)/2)
		
        else :
            newHeight = instaSize - 2*gap
            newWidth = math.floor(newHeight*ratio)

            if (newWidth>=instaSize-10*gap) :
                newWidth = instaSize-10*gap
                newHeight= math.floor(newWidth/ratio)

            newX = math.floor((instaSize-newWidth)/2)
            newY = math.floor((instaSize-newHeight)/2)

        result = Image.new(image.mode, (instaSize, instaSize), color)		
        resizedImage = image.resize((newWidth,newHeight))		
        result.paste(resizedImage, (newX, newY))
        return result	

    def set_square_text(self, image, model_data, font_path, exif_data, color, horizontalImage):
        self.font_size = 46
        self.font = ImageFont.truetype(font_path, self.font_size)
        if(horizontalImage) : 
            rotateImage = image

        else :
            rotateImage = image.rotate(-90)

        draw = ImageDraw.Draw(rotateImage)
        x = image.width / 2
        y = image.height - self.font_size*3

        draw.text(xy = (x,y - self.font_size / 2), text = model_data,font=self.font, fill=color, anchor="ms")
        draw.text(xy = (x,y + self.font_size), text = exif_data,font=self.font, fill=color, anchor="ms")
        if(horizontalImage) : 
            image = rotateImage

        else :
            image = rotateImage.rotate(90)

        return image


def main():
    exif_test = Exif()

    img = Image.open("Error-Test/IMG_0058.jpeg")

    longer_length = img.width if img.width >= img.height else img.height
    padding = int(longer_length / 10)

    model_data, exif_data = exif_test.get_exif_data(img)
    img = Exif.set_image_padding2(img, top=int(padding / 2), side=int(padding / 2), bottom=padding,
                                  color=(255, 255, 255))
    img = exif_test.set_image_text(img, model_data=model_data, exif_data=exif_data, length=padding, font_path="Resources/Barlow-Light.ttf", color=(0,0,0))
    img.show()

    img.save("Test.jpg")


if __name__ == "__main__":
    main()
