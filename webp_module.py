# Copyright 2023 Hyo Jae Jeon (CANU) canu1832@gmail.com

from PIL import Image, ImageDraw, ImageFont, ImageOps, ExifTags

import os
# import Watermark_module
import exif_module


class Converter:
    FILE_FORMAT_EXTENSION = {0: 'jpeg', 1: 'png', 2: 'webp'}
    FILE_FORMAT_QUALITY_PRESET = {0: 100, 1: 100, 2: 92}

    def __init__(self) -> None:
        # self.watermark = Watermark_module.Watermark()
        self.exif = exif_module.Exif()

    @staticmethod
    def fix_orientation(image):
        exif = image.getexif()
        new_image = None
        try:
            if exif:
                orientation = exif.get(274)

                if orientation == 3:
                    new_image = image.rotate(180, expand=True)
                elif orientation == 6:
                    new_image = image.rotate(270, expand=True)
                elif orientation == 8:
                    new_image = image.rotate(90, expand=True)
                else:
                    new_image = image.rotate(0, expand=True)
        except Exception as e:
            print(e)

        return new_image

    @staticmethod
    def convert_image_to_webp(file_path, save_path, save_name, loseless_option, image_quality_option,
                              exif_option, icc_profile_option, exact_option, watermark_text, exif_view_option,
                              conversion_option):
        condition, file_format = Converter.search_file_format(file_path)
        # note(komastar) : file_format : 'jpg', 'png'...

        if condition:
            # 01 일반 WebP 형식 Image로 변환할 때
            if conversion_option:
                image = Image.open(file_path).convert("RGB")
                # image = self.FixOrientation(image)

                dest = save_path + save_name + ".webp"

                # 여기서 exif 데이터의 특정 값이 존재하지 않으면 바로 실패함 / 옵션을 선택하지 않아도 읽어오기에 무조건적으로 뻗음
                # exifData = getattr(image.info, 'exif', None)
                # if not exifData:
                #	print(f'no exif data {saveName}')
                #	exifOpt = False
                exif_option = False
                exif_data = None

                icc_profile = image.info['icc_profile']

                # image = self.watermark.InsertWatermark(image=image, fontColor=watermarkColor, watermarkText=watermarkText)

                image = image.convert("RGB")

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

    def convert_exif_image(self, file_path, save_path, save_name, file_format_option):
        file_format = Converter.search_file_format(file_path)

        if file_format == '':
            print("잘못된 파일 형식 입니다.")
            return

        # 02 EXIF Padding Image로 변환할 때
        image = Image.open(file_path)

        longer_length = image.width if image.width >= image.height else image.height
        padding = int(longer_length / 10)
        half_padding = int(padding * 0.5)

        model_data, exif_data = self.exif.get_exif_data(image)

        image = Converter.fix_orientation(image)
        image = self.exif.set_image_padding2(image, top=half_padding, side=half_padding, bottom=padding,
                                             color=(255, 255, 255))
        image = self.exif.set_image_text(image, model_data=model_data, exif_data=exif_data, length=padding)

        # 파일 형식 선택
        export_extension = Converter.FILE_FORMAT_EXTENSION[file_format_option]
        export_quality = Converter.FILE_FORMAT_QUALITY_PRESET[file_format_option]
        fullpath = os.path.join(save_path, save_name) + '.' + export_extension
        image.save(fullpath, format=export_extension, quality=export_quality)

    @staticmethod
    def search_file_format(file_path) -> str:
        file_format = os.path.splitext(file_path)[1][1:]
        file_format = file_format.lower()

        support_format = {'jpg', 'jpeg', 'png', 'tiff', 'webp'}
        if file_format in support_format:
            return file_format
        return ''
