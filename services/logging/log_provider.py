from services.disk.file.file_manager import FileManager
from services.logging.core.logging.logging import Logging
from services.logging.core.stack.stack_context import StackContext
from services.core.singleton_meta import SingletonMeta
# --
# ...
# --


class LogProvider(metaclass=SingletonMeta ):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        template = kwargs.get("template", "Pipeline")
        config = kwargs.get("config", "Pipeline")

        file_manager_class = FileManager()

        self.info = Logging(
            template=template, config=config, file_manager_class=file_manager_class
        ).info
        self.error = Logging(
            template="Error", config="Error", file_manager_class=file_manager_class
        ).error
        self.stack = StackContext().StackOperation
