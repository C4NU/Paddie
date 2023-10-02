# Copyright 2023 Hyo Jae Jeon (CANU) canu1832@gmail.com

from PIL import Image, ImageDraw, ImageFont, ImageOps, ExifTags

import os
import subprocess
import platform

# import Watermark_module
import exif_module
import resize_module


class Converter:
    FILE_FORMAT_EXTENSION = {0: 'jpeg', 1: 'png', 2: 'webp'}
    FILE_FORMAT_QUALITY_PRESET = {0: 100, 1: 100, 2: 92}

    def __init__(self) -> None:
        # self.watermark = Watermark_module.Watermark()
        self.exif = exif_module.Exif()
        self.resize = resize_module.Resize()

    @staticmethod
    def fix_orientation(image):
        exif = image.getexif()
        print(type(exif))
        new_image = None
        
        try:
            if exif != {}:
                orientation = exif.get(274)

                print(orientation)

                if orientation == 3:
                    new_image = image.rotate(180, expand=True)
                    exif[274] = 1
                elif orientation == 6:
                    new_image = image.rotate(270, expand=True)
                    exif[274] = 1
                elif orientation == 8:
                    new_image = image.rotate(90, expand=True)
                    exif[274] = 1
                else:
                    new_image = image.rotate(0, expand=True)

                    return exif, new_image

        except Exception as e:
            print(e)
            return None, new_image

    def convert_image_to_webp(self, file_path, save_path, save_name, loseless_option, image_quality_option,
                              exif_option, icc_profile_option, exact_option, watermark_text, exif_view_option,
                              conversion_option, resize_option, width_option, height_option, resize_value):
        file_format = Converter.search_file_format(file_path)
        # note(komastar) : file_format : 'jpg', 'png'...
        
        # 01 일반 WebP 형식 Image로 변환할 때
        if conversion_option:
            image = Image.open(file_path)
            dest = save_path + save_name + ".webp"

            model_data, exif_data = self.exif.get_exif_data(image)

            if model_data == None:
                exif_option = False
                new_exif_data = None

            else:
                new_exif_data, image = Converter.fix_orientation(image)

            # Reize 하기
            if resize_option:
                image = self.resize.resize(image, 
                                    width_option,
                                    height_option,
                                    resize_value)

            # Exif Option 데이터 읽어오기 / 오류시 except
            if new_exif_data is not None:
                try:
                    exif_data = new_exif_data
                    print(f"Get Exif Data: {exif_data}")
                except:
                    print(f'No exif data:{save_name}')
                    exif_option = False
                    exif_data = None
            else:
                print("NO new exif data")
                exif_option = False
                exif_data = None

            # Icc profile 데이터 읽어오기 / 오류시 Except
            try:
                icc_profile = image.info['icc_profile']
                print("Get ICC Profile")
            except:
                print(f'No ICC Profile Data: {save_name}')
                icc_profile = None
                icc_profile_option = False

            if exif_option:
                if icc_profile_option:
                    image.save(dest, format="webp", loseless=loseless_option, quality=image_quality_option,
                                exif=exif_data, exact=exact_option, icc_profile=icc_profile)
                else:
                    image.save(dest, format="webp", loseless=loseless_option, quality=image_quality_option,
                                exif=exif_data, exact=exact_option)
            else:
                if icc_profile_option:
                    image.save(dest, format="webp", loseless=loseless_option, quality=image_quality_option,
                                   exact=exact_option, icc_profile=icc_profile)
                else:
                    image.save(dest, format="webp", loseless=loseless_option, quality=image_quality_option,
                                exact=exact_option)

    def convert_exif_image(self, file_path, save_path, save_name, file_format_option, font_path, 
                            bg_color, square_padding_option, dark_theme_option, exif_padding_option,
                            one_line_option, save_exif_data_option, resize_option, width_option, height_option, resize_value):
        
        file_format = Converter.search_file_format(file_path)

        if file_format == '':
            print("잘못된 파일 형식 입니다.")
            return

        # 02 EXIF Padding Image로 변환할 때
        image = Image.open(file_path)

        font_color = (0,0,0)
        background_color = (bg_color.red(), bg_color.green(), bg_color.blue())
        
        if dark_theme_option == True:
            font_color=(255,255,255)
            
        longer_length = image.width if image.width >= image.height else image.height
        padding = int(longer_length / 10)
        half_padding = int(padding * 0.5)

        model_data, exif_data = self.exif.get_exif_data(image)
        
        horizontalImage = True if image.width>=image.height else False
        
        if model_data == None:
            return

        else:
            new_exif_data, image = Converter.fix_orientation(image)

        if square_padding_option==True:
            image = self.exif.set_square_padding(image, gap = 60, color=background_color, horizontalImage= horizontalImage)
            image = self.exif.set_square_text(image, model_data=model_data, exif_data=exif_data, font_path=font_path, color = font_color, horizontalImage= horizontalImage)

        elif exif_padding_option==False:
            if one_line_option==True:
                print("oneline")
                image = self.exif.set_line_text(image,model_data=model_data, exif_data=exif_data, length=padding, font_path=font_path, color = font_color)
            else:
                image = self.exif.set_image_text(image,model_data=model_data, exif_data=exif_data, length=padding, font_path=font_path, color = font_color)

        else : 
            image = self.exif.set_image_padding2(image, top=half_padding, side=half_padding, bottom=padding, color=background_color)
            if one_line_option==True:
                print("oneline")
                image = self.exif.set_line_text(image,model_data=model_data, exif_data=exif_data, length=padding, font_path=font_path, color = font_color)
            else:
                image = self.exif.set_image_text(image,model_data=model_data, exif_data=exif_data, length=padding, font_path=font_path, color = font_color)

        # Resize 하기
        if resize_option:
            image = self.resize.resize(image, 
                                width_option,
                                height_option,
                                resize_value)
        # 파일 형식 선택
        export_extension = Converter.FILE_FORMAT_EXTENSION[file_format_option]
        export_quality = Converter.FILE_FORMAT_QUALITY_PRESET[file_format_option]
        fullpath = os.path.join(save_path, save_name) + '.' + export_extension

        if save_exif_data_option is True:
            image.save(fullpath, format=export_extension, quality=export_quality, exif=new_exif_data)
        else:
            image.save(fullpath, format=export_extension, quality=export_quality)

    def show_sample_exif_frame_image(self, file_path, file_name,font_path, 
                            bg_color, square_padding_option, dark_theme_option, exif_padding_option,
                            one_line_option):
        
        file_format = Converter.search_file_format(file_path+file_name)

        print(file_path)

        if file_format == '':
            print("잘못된 파일 형식 입니다.")
            return

        # 02 EXIF Padding Image로 변환할 때
        image = Image.open(file_path+file_name)

        font_color = (0,0,0)
        background_color = (bg_color.red(), bg_color.green(), bg_color.blue())
        
        if dark_theme_option == True:
            font_color=(255,255,255)
            
        longer_length = image.width if image.width >= image.height else image.height
        padding = int(longer_length / 10)
        half_padding = int(padding * 0.5)

        model_data, exif_data = self.exif.get_exif_data(image)
        
        horizontalImage = True if image.width>=image.height else False
        
        new_exif_data, image = Converter.fix_orientation(image)

        if square_padding_option==True:
            image = self.exif.set_square_padding(image, gap = 60, color=background_color, horizontalImage= horizontalImage)
            image = self.exif.set_square_text(image, model_data=model_data, exif_data=exif_data, font_path=font_path, color = font_color, horizontalImage= horizontalImage)

        elif exif_padding_option==False:
            if one_line_option==True:
                print("oneline")
                image = self.exif.set_line_text(image,model_data=model_data, exif_data=exif_data, length=padding, font_path=font_path, color = font_color)
            else:
                image = self.exif.set_image_text(image,model_data=model_data, exif_data=exif_data, length=padding, font_path=font_path, color = font_color)

        else : 
            image = self.exif.set_image_padding2(image, top=half_padding, side=half_padding, bottom=padding, color=background_color)
            if one_line_option==True:
                print("oneline")
                image = self.exif.set_line_text(image,model_data=model_data, exif_data=exif_data, length=padding, font_path=font_path, color = font_color)
            else:
                image = self.exif.set_image_text(image,model_data=model_data, exif_data=exif_data, length=padding, font_path=font_path, color = font_color)

        if platform.system() == "Darwin":
            save_path = file_path+"Sample_result.jpg"
            image.save(save_path)
            subprocess.run(["open", "-a", "Preview", save_path])
        else:
            image.show()

    @staticmethod
    def search_file_format(file_path) -> str:
        file_format = os.path.splitext(file_path)[1][1:]
        file_format = file_format.lower()

        support_format = {'jpg', 'jpeg', 'png', 'tiff', 'webp'}
        if file_format in support_format:
            return file_format
        return ''