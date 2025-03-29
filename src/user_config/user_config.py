# Copyright 2023 Eugene Kim (komastar) komastar.photo@gmail.com

import json
import os.path
import platform
import sys

print("User_Config Python Package Loaded")

from PyQt6 import QtGui
from PyQt6.QtGui import QColor
print("PyQt6 QColor Loaded") 

from resource_path import resource_path

RESOURCE_USER_DATA = "resources/user_data.json"

class UserConfig:
    # setting value is default value
    language = None
    latest_load_path = None
    latest_save_path = None
    save_original_path = False

    resize_options = False
    resize_axis = 2 # 0:Width, 1:Height, 2:Longest, 3:Shortest
    resize_size = 3000

    conversion_options = True
    conversion_loseless = False
    conversion_exif = False
    conversion_icc = False
    conversion_transparent = False
    conversion_quality = 92
    
    exif_options = False
    exif_show_preview = False
    exif_padding_mode = 0 # 0:None, 1:Under, 2:Frame
    exif_save_exifdata = False
    exif_quality = 92
    exif_ratio = 0 # 0:Original, 1:Square, 2:4:5, replacement of Square Mode
    exif_type = 2 # 0:JPEG, 1:PNG, 2:WebP, name changed from format
    exif_text_color = QColor(0, 0, 0) # replacement of white text
    exif_bg_color = QColor(255, 255, 255)
    exif_easymode_options = True
    exif_easymode_oneline = False
    exif_format = "{body} | {lens}\n{focal_f} | {aper} | {iso} | {ss}" # replacement of 1 line text
    exif_font_index = 1 # index of font list
    exif_format_alignment = 0 # 0:Center, 1:Left, 2:Right
    exif_auto_hide_nonedata = False

    @staticmethod
    def save():
        save_data = open(resource_path(RESOURCE_USER_DATA), 'w')

        #with open('resources/user_data.json', 'w') as save_data:
        data = {key: getattr(UserConfig, key) for key in UserConfig.__dict__.keys() if not key.startswith("__") and not callable(getattr(UserConfig, key)) and "_color" not in key}

        # Special handling for QColor
        data['exif_text_color'] = [UserConfig.exif_text_color.red(), UserConfig.exif_text_color.green(), UserConfig.exif_text_color.blue()]
        data['exif_bg_color'] = [UserConfig.exif_bg_color.red(), UserConfig.exif_bg_color.green(), UserConfig.exif_bg_color.blue()]

        json.dump(data, save_data, indent=4)

    @staticmethod
    def load():
        load_data = open(resource_path(RESOURCE_USER_DATA), 'r')

        if not load_data:
            print("User Data Not loaded")
            return

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
