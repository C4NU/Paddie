# Copyright 2023 Eugene Kim (komastar) komastar.photo@gmail.com

import csv
import os
import sys
import platform
from resource_path import resource_path

class ModelNameMapper:
    @staticmethod
    def replace_model_name(model_name) -> str:
        path = resource_path('resources/model_map.csv')

        try:
            with open(path, newline='', encoding='utf-8') as csv_file:
                map_reader = csv.DictReader(csv_file)
                for row in map_reader:
                    find_string = row['Find']
                    if find_string in model_name:
                        replace_string = row['Replace']
                        new_model_name = model_name.replace(find_string, replace_string)
                        print(f'{model_name} -> {new_model_name}')
                        return new_model_name
       
        except:
            path = os.path.join(os.getcwd(), '../resources/model_map.csv')
            with open(path, newline='', encoding='utf-8') as csv_file:
                map_reader = csv.DictReader(csv_file)
                for row in map_reader:
                    find_string = row['Find']
                    if find_string in model_name:
                        replace_string = row['Replace']
                        new_model_name = model_name.replace(find_string, replace_string)
                        print(f'{model_name} -> {new_model_name}')
                        return new_model_name

        return model_name

# ModelNameMapper.replace_model_name('ILCE-7RM3')
