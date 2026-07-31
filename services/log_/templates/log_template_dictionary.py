class LogTemplateDictionary():

    def __call__(self) -> dict:
        self.dictionary = {
            'Pipeline': """ f"{CONSTS.COLORS.LOG_PROMPT.value}",str(datetime.datetime.now().strftime("%m-%d-%Y, %H:%M:%S")), f" {message}".ljust(8, ' '), f"{CONSTS.COLORS.ENDC.value}" """,
            'Error': """ f"{CONSTS.COLORS.ERROR_PROMPT.value}",str(datetime.datetime.now().strftime("%m-%d-%Y, %H:%M:%S")), f" {message}".ljust(8, ' '), f"{CONSTS.COLORS.ENDC.value}" """,
        }

        return self.dictionary