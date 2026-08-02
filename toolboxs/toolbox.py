import math
import os
import random
import sys
from datetime import datetime
from pathlib import Path

# --
# ...
# --


class Toolbox:
    @staticmethod
    def str_(input_):

        try:
            if isinstance(input_, str):
                return input_

            elif isinstance(input_, float) or isinstance(input_, int):
                return str(input_)

        except Exception as exp:
            print(repr(exp))

    # --
    # ...
    # --

    @staticmethod
    def get_random(start_string="RND ", type="string", limit=1000000, delemeter="_"):

        try:
            result = 0

            if start_string is tuple:
                start_string, _ = start_string

            if type == "string":
                rand_ = math.ceil(random.random() * limit)
                if rand_ < 10:
                    rand_ += 10
                result = f"{start_string}{delemeter}{rand_!s}"

            elif type == "int":
                result = math.ceil(random.random() * limit)
                if result < 10:
                    result += 10

            return result

        except Exception as exp:
            print(repr(exp))

    # --
    # ...
    # --bundan qiziq vidy

    @staticmethod
    def get_root_path() -> str:

        try:
            return str(Path(__file__).parent.parent)

        except Exception as exp:
            print(repr(exp))

    # --
    # ...
    # --

    @staticmethod
    def get_import_moduls() -> str:

        try:
            modules = []
            sys_modules_keys = sys.modules.keys()
            for module in sys_modules_keys:
                if module[:48] == "d_365.main.finance_chapter":
                    modules.append(module)

            with open(
                f"{Toolbox().get_root_path().replace('\\', '/')}/.external_files/temp/temp_import_moluls.txt",
                "w",
            ) as temp_import_moluls:
                moduls_text = ""
                for m in modules:
                    moduls_text = f"{moduls_text} {m} \n"

                print(moduls_text, file=temp_import_moluls)

            temp_import_moluls.close()

            return modules

        except Exception as exp:
            print(repr(exp))

    # --
    # ...
    # --

    @staticmethod
    def get_all_file_name_with_length(app_dir="", len_condition=255):

        if app_dir == "":
            app_dir = f"{Toolbox().get_root_path()}/app".replace("\\", "/")

        file_name_with_length = []

        for folder_adress, sub_folders, files in os.walk(app_dir):
            for file in files:
                file_name_with_length.append(f"{folder_adress.replace('\\', '/')}/{file}")

        file_name_with_length.sort(key=lambda k: len(k), reverse=True)
        file_name_len_list = [
            f"{file}: {len(file)}" for file in file_name_with_length if len(file) > len_condition
        ]

        print(len(file_name_len_list))
        print(f"{'\n'.join(file_name_len_list)}")

    # Toolbox().get_all_file_name_with_length(app_dir="C:/Users/mpaarmann/Projects/rdp_bot", len_condition=155)

    # --
    # ...
    # --

    @staticmethod
    def get_first_day_of_month(input_):

        try:
            today = datetime.today()
            return datetime(today.year, today.month, 1)

        except Exception as exp:
            print(repr(exp))
