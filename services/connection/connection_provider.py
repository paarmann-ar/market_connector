from services.connection.request.request import Request
from services.logging.log_provider import LogProvider
from services.core.singleton_meta import SingletonMeta

# --
# ...
# --


class ConnectionProvider(metaclass=SingletonMeta):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        log_info_class = LogProvider().info
        log_error_class = LogProvider().error

        self.request = Request(log_info_class=log_info_class, log_error_class=log_error_class, **kwargs)
