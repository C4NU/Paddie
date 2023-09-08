# Copyright 2023 Hyo Jae Jeon (CANU) canu1832@gmail.com

from PIL import Image, ImageDraw, ImageFont

import os
# import Watermark_module
import exif_module


class Converter:
    def __init__(self) -> None:
        # self.watermark = Watermark_module.Watermark()
        self.exif = exif_module.Exif()

    def convert_image(self, file_path, save_path, save_name, loseless_opt, image_quality_opt, exif_opt, icc_profile_opt,
                      transparent_rgb,
                      watermark_text, exif_view_opt, conversion_opt):
        # 확장자명 탐색
        condition, file_format = Converter.search_file_format(file_path)

        if condition:
            image = Image.open(file_path)

            if exif_view_opt:
                longer_length = image.width if image.width >= image.height else image.height
                padding = int(longer_length / 10)

                model_data, exif_data = self.exif.get_exif_data(image)
                image = self.exif.set_image_padding2(image, top=int(padding / 2), side=int(padding / 2), bottom=padding,
                                                     color=(255, 255, 255))
                image = self.exif.set_image_text(image, modelData=model_data, exifData=exif_data, length=padding)
            # jpg, jpeg, png, tiff 등 지원하는 파일 형식일 때

            if conversion_opt:
                image_data = Image.open(file_path).convert('RGB')
                dest = save_path + save_name + ".webp"

                exif_data = getattr(image_data.info, 'exif', None)
                if not exif_data:
                    print(f'no exif data {save_name}')
                    exif_opt = False

                icc_profile = image_data.info['icc_profile']

                # image = self.watermark.InsertWatermark(image=image, fontColor=watermarkColor, watermarkText=watermarkText)

                if exif_opt:
                    if icc_profile_opt:
                        image.save(dest, format="webp", loseless=loseless_opt, quality=image_quality_opt,
                                   exif=exif_data,
                                   exact=transparent_rgb, icc_profile=icc_profile)
                    else:
                        image.save(dest, format="webp", loseless=loseless_opt, quality=image_quality_opt,
                                   exif=exif_data,
                                   exact=transparent_rgb)

                else:
                    if icc_profile_opt:
                        image.save(dest, format="webp", loseless=loseless_opt, quality=image_quality_opt,
                                   exact=transparent_rgb,
                                   icc_profile=icc_profile)
                    else:
                        image.save(dest, format="webp", loseless=loseless_opt, quality=image_quality_opt,
                                   exact=transparent_rgb)
            else:
                # webp 변환 말고 확장자 그대로
                image_data = Image.open(file_path).convert('RGB')
                dest = save_path + save_name + ".png"
                exif_data = image_data.info['exif']
                icc_profile = image_data.info['icc_profile']

                # image = self.watermark.InsertWatermark(image=image, fontColor=watermarkColor, watermarkText=watermarkText)

                if exif_opt:
                    if icc_profile_opt:
                        image.save(dest, format="png", loseless=loseless_opt, quality=image_quality_opt, exif=exif_data,
                                   exact=transparent_rgb, icc_profile=icc_profile)
                    else:
                        image.save(dest, format="png", loseless=loseless_opt, quality=image_quality_opt, exif=exif_data,
                                   exact=transparent_rgb)

                else:
                    if icc_profile_opt:
                        image.save(dest, format="png", loseless=loseless_opt, quality=image_quality_opt,
                                   exact=transparent_rgb,
                                   icc_profile=icc_profile)
                    else:
                        image.save(dest, format="png", loseless=loseless_opt, quality=image_quality_opt,
                                   exact=transparent_rgb)

    @staticmethod
    def search_file_format(file_path):
        file_format: str
        file_format = os.path.splitext(file_path)[1][1:]

        file_ext_set = {"jpg", "jpeg", "png", "tiff"}
        if file_format in file_ext_set:
            return True, file_format
        else:
            return False, None
