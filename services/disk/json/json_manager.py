import json
from typing import Any
from services.core.singleton_meta import SingletonMeta
# --
# ...
# --

# convert json-data-file to Python object using the json.
# json.load()

# parse the JSON string and convert it to Python object
# json.loads()

# This function serializes a Python object (like a dict) to a JSON formatted file object.
# json.dump()

# This function serializes a Python object (like a dict) to a JSON formatted string.
# json.dumps()


class JSONManager(metaclass=SingletonMeta):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    # --
    # ...
    # --

    def operation(
        self,
        address="",
        context="",
        mode="",
        dele="",
        is_get_dictionary=True,
        is_convert_context_to_json=False,
        is_json_data_has_unexpected_char=False,
        is_fix_json_error=True,
    ) -> Any:

        try:
            json_data = None

            if address[-1] == "c":
                address = address[:-1]

            if context == "":
                with open(address, "r", encoding="utf8") as file:
                    readed_file = file.read()

                    if is_fix_json_error:
                        corrected_file_string = self.__fix_json_error(readed_file)
                    else:
                        corrected_file_string = readed_file

                    try:
                        json_data = json.loads(corrected_file_string)

                    except ValueError:
                        file.close()
                        with open(address, "r", encoding="utf8") as file:
                            json_data = json.load(file)

                    finally:
                        ...

                    if is_get_dictionary:
                        if not isinstance(json_data, dict):
                            json_data = eval(json_data)

                        json_data = dict(json_data)

                    if is_json_data_has_unexpected_char:
                        for key, value_dictionary in json_data.items():
                            for key_, value_ in value_dictionary.items():
                                value_ = value_.replace("*******", '"')
                                value_ = dict({key_: value_})
                            json_data[key] = value_

            elif is_convert_context_to_json:
                json_data = json.loads(context)

                if is_get_dictionary:
                    if not isinstance(json_data, dict):
                        json_data = eval(json_data)

                    json_data = dict(json_data)

            elif mode == "append_or_replace":
                dict_readed_file = {}

                try:
                    with open(address, "r", encoding="utf8") as file:
                        readed_file = file.read(file)
                        json_readed_file = json.dumps(readed_file)
                        dict_readed_file = json.loads(json_readed_file)

                except TypeError:
                    with open(address, "r", encoding="utf8") as file:
                        dict_readed_file = json.load(file)

                except FileNotFoundError:
                    print(repr(f"JSON file will created: {address}"))

                finally:
                    if isinstance(context, str):
                        context = json.dumps(context)

                    if isinstance(context, dict):
                        dict_context = context

                    else:
                        # with pprint can see maybe it is not dict but is list or string therefor two times loads
                        dict_context = json.loads(json.loads(context))

                    dict_readed_file.update(dict_context)

                    with open(address, "w") as file:
                        json.dump(dict_readed_file, file, indent=4)
                        json_data = True

                    dict_readed_file = {}

            elif mode == "append":
                with open(address, "a") as file:
                    if is_fix_json_error:
                        corrected_file_string = self.__fix_json_error(context)
                    else:
                        corrected_file_string = context

                    corrected_file_string = (
                        json.dumps(corrected_file_string, indent=4) + dele
                    )
                    file.write(corrected_file_string)
                    json_data = True

            else:
                with open(address, "w") as file:
                    if is_fix_json_error:
                        corrected_file_string = self.__fix_json_error(context)
                    else:
                        corrected_file_string = context

                    corrected_file_string = json.dumps(corrected_file_string, indent=4)
                    file.write(corrected_file_string)
                    json_data = True

            return json_data

        except Exception as exp:
            print(repr(f"{exp} -> {address}"))

    # --
    # ...
    # --

    def __fix_json_error(self, context="") -> str:

        try:
            if isinstance(context, dict):
                return context

            context = context.replace(chr(92), chr(47))
            context = context.replace(chr(39), chr(34))
            context = context.replace('/"', "*******")

            return context

        except Exception as exp:
            print(repr(exp))
