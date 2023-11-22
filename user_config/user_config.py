# Copyright 2023 Eugene Kim (komastar) komastar.photo@gmail.com

import json
import os.path

print("User_Config Python Package Loaded")
# comment (CANU): 호호 맥에서 패키지가 어디갓징
from PyQt6 import QtGui
from PyQt6.QtGui import QColor
print("PyQt6 QColor Loaded")


class UserConfig:
    # setting value is default value
    latest_load_path = None
    latest_save_path = None

    resize_options = False
    resize_axis = 2 # 0:Width, 1:Height, 2:Longest, 3:Shortest
    resize_size = 3000

    conversion_options = True
    conversion_loseless = False
    conversion_exif = False
    conversion_icc = False
    conversion_transparent = False
    conversion_quality = 80
    
    exif_options = False
    exif_padding = False
    exif_save_exifdata = False
    exif_quality = 80
    exif_ratio = 0 # 0:Original, 1:Square, 2:4:5, replacement of Square Mode
    exif_type = 2 # 0:JPEG, 1:PNG, 2:WebP, name changed from format
    exif_text_color = QColor(0, 0, 0) # replacement of white text
    exif_bg_color = QColor(255, 255, 255)
    exif_format = "{body} | {lens}\n{focal_length_ff} | {aperture} | {iso} | {shutter_speed}" # replacement of 1 line text
    exif_font = 1 # index of font list
    exif_format_alignment = 0 # 0:Center, 1:Left, 2:Right

    @staticmethod
    def save():
        with open('user_data.json', 'w') as save_data:
            data = {key: getattr(UserConfig, key) for key in UserConfig.__dict__.keys() if not key.startswith("__") and not callable(getattr(UserConfig, key)) and "_color" not in key}

            # Special handling for QColor
            data['exif_text_color'] = [UserConfig.exif_text_color.red(), UserConfig.exif_text_color.green(), UserConfig.exif_text_color.blue()]
            data['exif_bg_color'] = [UserConfig.exif_bg_color.red(), UserConfig.exif_bg_color.green(), UserConfig.exif_bg_color.blue()]

            json.dump(data, save_data, indent=4)

    @staticmethod
    def load():
        if not os.path.exists('user_data.json'):
            print("User Data Not loaded")
            return

        with open('user_data.json', 'r') as load_data:
            try:
                data = json.load(load_data)

                for key, value in data.items():
                    # Special handling for QColor
                    if key == 'exif_text_color' or key == 'exif_bg_color':
                        setattr(UserConfig, key, QColor(value[0], value[1], value[2]))
                    else:
                        setattr(UserConfig, key, value)

            except json.decoder.JSONDecodeError:
                print('json decode error')
