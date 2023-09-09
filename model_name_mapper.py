# Copyright 2023 Eugene Kim (komastar) komastar.photo@gmail.com

import csv
from utils import resource_path


class ModelNameMapper:
    @staticmethod
    def replace_model_name(model_name) -> str:
        path = resource_path('Resources/model_map.csv')
        with open(path, newline='') as csv_file:
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
