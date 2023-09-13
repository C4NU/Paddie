# Copyright 2023 Eugene Kim (komastar) komastar.photo@gmail.com

import json
import os.path

print("User_Config Python Package Loaded")
# comment (CANU): 호호 맥에서 패키지가 어디갓징
from PyQt6 import QtGui
from PyQt6.QtGui import QColor
print("PyQt6 QColor Loaded")


class UserConfigKey:
    LATEST_SAVE_PATH = 'latest_save_path'
    BACKGROUND_PATH = 'background_path'


class UserConfig:
    latest_save_path = None
    background_color: QColor
    background_color = None

    @staticmethod
    def save():
        with open('user_data.json', 'w') as save_data:
            data = dict()
            data[UserConfigKey.LATEST_SAVE_PATH] = UserConfig.latest_save_path
            if UserConfig.background_color:
                color = UserConfig.background_color
                data[UserConfigKey.BACKGROUND_PATH] = [color.red(), color.green(), color.blue()]

            json.dump(data, save_data, indent=4)

    @staticmethod
    def load():
        if not os.path.exists('user_data.json'):
            print("User Data Not loaded")
            return

        with open('user_data.json', 'r') as load_data:
            try:
                data: dict
                data = json.load(load_data)
                UserConfig.latest_save_path = data.get(UserConfigKey.LATEST_SAVE_PATH)
                color = data.get(UserConfigKey.BACKGROUND_PATH)
                if color:
                    UserConfig.background_color = QColor(color[0], color[1], color[2])
            except json.decoder.JSONDecodeError:
                print('json decode error')
