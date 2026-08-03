import CONSTS
from services.logging.config.log_config import LogConfig
from services.logging.core.base_log import BaseLog
from services.logging.templates.log_template_dictionary import LogTemplateDictionary

# --
# ...
# --


class Logging(BaseLog):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        try:
            self.info_message = ["\n"]

            # aliance for short writing
            self.info = self.error = self.set_information_for_log_file

            # create instance for file operation
            self.file_manager = kwargs.get("file_manager_class")

            # set template and config
            if template := kwargs.get("template"):
                self.instance.log_template = self.instance.template_dictionary[template]
            else:
                self.instance.log_template = ""

            if config := kwargs.get("config"):
                self.instance.config_dictionary = self.instance.config_dictionary[
                    __name__
                ][config]
                self.log_file = f"{CONSTS.ROOT_DIR}{self.config_dictionary['directory_address']}{self.config_dictionary['filename']}"
                self.number_of_log_in_batch = int(
                    self.config_dictionary["number_of_log_in_batch"]
                )
                self.is_show_in_console = self.config_dictionary["is_show_in_console"]

        except Exception as exp:
            print(f"{__file__}--->{__name__} : + {exp!s}")

    # --
    # ...
    # --

    @classmethod
    def get_template_dictionary(cls):
        return LogTemplateDictionary()()

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return LogConfig().get_dictionary()

    # --
    # ...
    # --

    def set_information_for_log_file(self, message, is_force_write=False):

        try:
            # remove color from template
            log_template_for_show_in_screen = self.log_template

            log_template_for_write_in_file = self.log_template
            log_template_for_write_in_file = log_template_for_write_in_file.replace(
                """f"{CONSTS.COLORS.LOG_PROMPT.value}",""", ""
            )
            log_template_for_write_in_file = log_template_for_write_in_file.replace(
                """f"{CONSTS.COLORS.ERROR_PROMPT.value}",""", ""
            )
            log_template_for_write_in_file = log_template_for_write_in_file.replace(
                """, f"{CONSTS.COLORS.ENDC.value}" """, ""
            )

            # print message on screen
            if self.is_show_in_console:
                temp = f"import colorama\ncolorama.init()\nimport CONSTS\nimport datetime\nprint({log_template_for_show_in_screen})"
                exec(temp, {"message": message})

            # compile message and template
            temp = f"""import datetime;temp ={log_template_for_write_in_file}; f = open("temp.txt", "w"); f.write(str(temp[0] + temp[1]))"""
            exec(temp, {"message": message})

            # prepaire message
            message = self.file_manager.operation("r", "temp.txt")

            # send message to write in file
            self.info_message.append(message)
            if len(self.info_message) > self.number_of_log_in_batch or is_force_write:
                self.__write_in_log_file()

        except Exception as exp:
            print(f"{__file__}--->{__name__} : + {exp!s}")

    # --
    # ...
    # --

    def __write_in_log_file(self):

        try:
            self.file_manager.operation(
                "a", self.log_file, "\n".join(self.info_message)
            )
            self.info_message.clear()
            self.info_message.append("\n")

        except Exception as exp:
            print(f"{__file__}--->{__name__} : + {exp!s}")
