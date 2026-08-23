import math
import random
import uuid
import secrets
import string

# --
# ...
# --


class RandomExpertion:
    # --
    # ...
    # --

    @staticmethod
    def get_uuid(prefix="", postfix="") -> str:
        return f"{prefix}{uuid.uuid4().hex}{postfix}"

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
    # --

    @staticmethod
    def password_maker():
        chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
        password = "".join(secrets.choice(chars) for _ in range(30))

        return password
