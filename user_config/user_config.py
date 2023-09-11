# Copyright 2023 Eugene Kim (komastar) komastar.photo@gmail.com

import json
import os.path

from PyQt5.QtGui import QColor


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
