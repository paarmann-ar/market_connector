import math
import random
from pathlib import Path
import sys
import os
from datetime import datetime
import CONSTS

# --
# ...
# --


class FileAndFolderOperation:

    # --
    # ...
    # --

    @staticmethod
    def get_all_file_address(address=""):

        try:

            file_address_list = []

            if address == "":
                address = CONSTS.ROOT_DIR

            for folder_adress, sub_folders, files in os.walk(address):
                folder_adress = folder_adress.replace("\\", "/")
                for file in files:
                    file_address_list.append(f"{folder_adress}/{file}")

            return file_address_list

        except Exception as exp:
            print(repr(exp))

    # --
    # ...
    # --

    @staticmethod
    def remove_pycache():

        try:

            file_address_list = FileAndFolderOperation().get_all_file_address()

            for file in file_address_list:
                file_list = file.split("/")

                file_list = filter(lambda x: x=="__pycache__", file_list)
                for item in file_list:
                    os.remove(file)
                    print(f"I remove: {file}")

        except Exception as exp:
            print(repr(exp))

    # --
    # ...
    # --

    @staticmethod
    def remove_file(file_address):

        try:

            candidate_filename = file_address.split('/')[-1]
            dir_address = file_address.split('/')[:-1]
            dir_address = '/'.join(dir_address)

            for filename in os.listdir(dir_address):
                if filename.upper()==candidate_filename.upper():
                    os.remove(file_address)
                    print(f"I remove: {file_address}")
                    return True
                
            print(f"I remove nothing: {file_address}")
            return False
                    
        except Exception as exp:
            print(repr(exp))