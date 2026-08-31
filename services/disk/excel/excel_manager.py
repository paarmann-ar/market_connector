import random

import xlsxwriter
import xlwings

import CONSTS
from services.core.base import Base
from services.disk.excel.config.excel_config import excelConfig

# --
# ...
# --


class ExcelManager(Base):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.mode = kwargs.get("mode", self.config_dictionary["default_mode"])
        self.address = kwargs.get(
            "address",
            f"{CONSTS.ROOT_DIR}/{self.config_dictionary['default_address']}",
        )

        #  self.workbook = [
        #      {
        #          "worksheet_1": [
        #              [
        #                  {
        #                      (0, 0): "Set name",
        #                  },
        #                  {(0, 1): "Tax Exempt Number"},
        #              ],
        #              [{(1, 0): "country"}, {(1, 1): "ITA"}],
        #              [{(2, 0): "tax_exempt_number"}, {(2, 1): "47510326"}],
        #          ]
        #      }
        #  ]

        self.workbook = []
        self.worksheet = None
        self.worksheets_dictionary = {}

    #  --
    #  ...
    #  --

    @classmethod
    def get_config_dictionary(cls):
        return excelConfig().get_dictionary()

    #  --
    #  ...
    #  --

    def operation(self, mode="", address="", file_name="", range="A1", is_print_worksheets=True) -> str:

        try:
            if mode == "":
                mode = self.mode

            if address == "":
                address = self.address

                if file_name:
                    address = address.replace(address[address.rfind("/") :], file_name)

            if mode == "w":
                with xlsxwriter.Workbook(address) as workbook:
                    format_first_row = workbook.add_format({"bg_color": "#c6e2ff", "border": 1})
                    format_rest_rows = workbook.add_format({"bg_color": "#ffefd5", "border": 1})
                    format_first_row.set_center_across()
                    format_rest_rows.set_center_across()

                    temp_list_worksheet_name = []

                    for index, worksheet in enumerate(self.workbook):
                        temp_worksheet_name = list(worksheet.keys())[0]

                        if temp_worksheet_name in temp_list_worksheet_name:
                            temp_new_worksheet_name = f"{temp_worksheet_name}_{random.randint(1, 10000)}"

                            temp = self.workbook.pop(index)
                            temp[temp_new_worksheet_name] = temp.pop(temp_worksheet_name)
                            self.workbook.insert(index, temp)

                        temp_list_worksheet_name.append(temp_worksheet_name)

                    for worksheet in self.workbook:
                        for worksheet_name, worksheet_value in worksheet.items():
                            worksheet = workbook.add_worksheet(worksheet_name)

                            for row_data in worksheet_value:
                                for data in row_data:
                                    for item, value in data.items():
                                        try:
                                            row_format = format_rest_rows if item[0] != 0 else format_first_row

                                            worksheet.write(item[0], item[1], value, row_format)
                                        #  I have change this exp to bestimmt exception
                                        except Exception as exp:
                                            self.error(repr(exp))

                        worksheet.autofit()

            elif mode == "r":
                worksheets = []
                workbook = xlwings.Book(address)

                if self.worksheet:
                    worksheets = workbook.sheets[self.worksheet].range(range).expand().value

                else:
                    worksheet_data = []
                    for worksheet in workbook.sheets:
                        worksheet_data = worksheet.used_range.value

                        temp_workdata = []
                        for item in worksheet_data:
                            item = list(map(lambda x: str(x), item))
                            temp_workdata.append(item)

                        worksheet_data.clear()
                        worksheet_data = temp_workdata

                        worksheets.append(worksheet_data)
                        self.worksheets_dictionary.update({worksheet.name: worksheet_data})

                if is_print_worksheets:
                    self.info(worksheets)

                return worksheets

        except Exception as exp:
            self.error(repr(exp))
            return False
