# Copyright 2023 Hyo Jae Jeon (CANU) canu1832@gmail.com
import os
import sys
import platform

from PIL import Image, ImageDraw, ImageFont
import math

from caption_format_converter import CaptionFormatConverter

# 폰트 vs padding 비율은 1:4?
# 이미지파일 vs padding 비율은 10:1

class Exif:
    def __init__(self):
        # 폰트 사이즈 (초기)
        self.font_size = 50
        self.ratio_image_gap = 60
        self.side_padding_45 = 50
        # 폰트 (초기)
        if platform.system() == "Windows":
            self.font = ImageFont.truetype(os.path.join(os.getcwd(), 'Resources/Barlow-Light.ttf'), self.font_size)
        else:
            try:
                self.font = ImageFont.truetype(os.path.join(os.path.dirname(sys.executable), "Resources/Barlow-Light.ttf"), self.font_size)
            except:
                self.font = ImageFont.truetype(os.path.join(os.getcwd(), 'Resources/Barlow-Light.ttf'), self.font_size)

    def set_image_padding(self, image, top, side, bottom, color):
        width, height = image.size

        new_width = width + 2 * side
        new_height = height + top + bottom

        result = Image.new(image.mode, (new_width, new_height), color)
        result.paste(image, (side, top))

        return result
        
    def set_image_text(self, image, text, length, font_path, color, alignment):
        draw = ImageDraw.Draw(image)

        x = image.width / 2
        y = image.height - (length / 2)
        anchor = "ms"
        align = "center"

        if alignment is 1:
            x = length / 2
            anchor = "ls"
            align = "left"
        elif alignment is 2:
            x = image.width - (length / 2)
            anchor = "rs"
            align = "right"

        self.font_size = length / 6

        line_count = len(text.splitlines())
        if line_count == 1:
            y += math.floor(self.font_size / 3)
        elif line_count == 2:
            self.font_size *= 4 / 3
            y -= math.floor(self.font_size / 2)
        else: #line_count == 3, 4 and more is not regarded
            y -= math.floor(self.font_size)

        self.font = ImageFont.truetype(font_path, self.font_size)
        draw.text(xy=(x, y), text=text, font=self.font, fill=color, anchor=anchor, align=align, spacing=math.floor(self.font_size / 2))
        return image

    def set_square_padding(self, image, gap, color, horizontalImage):
        width, height = image.size
        instaSize = 1440
        ratio = width / height     

        newWidth = 0
        newHeight = 0
        newX = 0
        newY = 0

        self.ratio_image_gap = gap

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
    
    def set_square_text(self, image, text, font_path, color, horizontalImage, alignment):
        self.font_size = 46
        if(horizontalImage) : 
            rotateImage = image
        else :
            rotateImage = image.rotate(-90)

        draw = ImageDraw.Draw(rotateImage)
        x = image.width / 2
        y = image.height - self.font_size * 3
        anchor = "ms"
        align = "center"

        if alignment is 1:
            x = self.ratio_image_gap
            anchor = "ls"
            align = "left"
        elif alignment is 2:
            x = image.width - self.ratio_image_gap
            anchor = "rs"
            align = "right"

        line_count = len(text.splitlines())
        if line_count == 1:
            self.font_size /= 1.15
            y += math.floor(self.font_size / 3)
        elif line_count == 2:
            y -= math.floor(self.font_size / 2)
        else: #line_count == 3, 4 and more is not regarded
            y -= math.floor(self.font_size)

        self.font = ImageFont.truetype(font_path, self.font_size)
        draw.text(xy = (x,y), text = text,font=self.font, fill=color, anchor=anchor, align=align, spacing=math.floor(self.font_size / 2))
        if(horizontalImage) : 
            image = rotateImage

        else :
            image = rotateImage.rotate(90)

        return image
    
    def set_45_padding(self, image, gap, color):
        #instagram 4:5 image size
        width = 1080
        height = 1350

        self.ratio_image_gap = gap

        width_actual = width - gap * 2
        height_actual = height - gap * 3

        image_width = width
        image_height = height
        image_x = 0
        image_y = 0

        image_raw_width, image_raw_height = image.size

        horizontal_image = image_raw_width / image_raw_height > width_actual / height_actual

        if horizontal_image:
            image_width = width_actual
            image_height = math.floor(image_width * image_raw_height / image_raw_width)
            image_x = gap
            image_y = gap + math.floor((height_actual - image_height) / 2)
        else:
            image_height = height_actual
            image_width = math.floor(image_height * image_raw_width / image_raw_height)
            image_y = gap
            image_x = gap + math.floor((width_actual - image_width) / 2)
            
        self.side_padding_45 = image_x

        result = Image.new(image.mode, (width, height), color)
        resized_image = image.resize((image_width, image_height))
        result.paste(resized_image, (image_x, image_y))
        return result
        
    def set_45_text(self, image, text, font_path, color, alignment):
        self.font_size = self.ratio_image_gap / 2

        x = image.width / 2
        y = image.height - self.ratio_image_gap
        anchor = "ms"
        align = "center"

        if alignment is 1:
            x = self.side_padding_45
            anchor = "ls"
            align = "left"
        elif alignment is 2:
            x = image.width - self.side_padding_45
            anchor = "rs"
            align = "right"

        line_count = len(text.splitlines())
        if line_count == 1:
            self.font_size /= 1.15
            y += math.floor(self.font_size / 2)
        elif line_count == 2:
            y -= math.floor(self.font_size / 2.125)
        else: #line_count == 3, 4 and more is not regarded
            self.font_size /= 1.15
            y -= math.floor(self.font_size)

        self.font = ImageFont.truetype(font_path, self.font_size)
        draw = ImageDraw.Draw(image)
        draw.text(xy=(x, y), text=text, font=self.font, fill=color, anchor=anchor, align=align, spacing=math.floor(self.font_size / 2))
        return image


def main():
    exif_test = Exif()

    img = Image.open("Error-Test/IMG_0058.jpeg")

    longer_length = img.width if img.width >= img.height else img.height
    padding = int(longer_length / 10)

    text = CaptionFormatConverter.convert("{body} | {lens}\n{focal_f} | {aper} | {iso} | {ss}", img._getexif())
    img = Exif.set_image_padding2(img, top=int(padding / 2), side=int(padding / 2), bottom=padding,
                                  color=(255, 255, 255))
    img = exif_test.set_image_text(img, text=text, length=padding, font_path="Resources/Barlow-Light.ttf", color=(0,0,0), alignment=0)
    img.show()

    img.save("Test.jpg")


if __name__ == "__main__":
    main()
