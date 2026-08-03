from services.db.sqlserver.sqlserver_provider import SqlserverProvider
from services.core.singleton_meta import SingletonMeta



# --
# ...
# --
class ServiceDBProvider(metaclass=SingletonMeta):
    def __init__(self, get_provider=[]):

        self.db_connection = SqlserverProvider().db_connection
        self.db_command_execute = SqlserverProvider().db_command_execute
        self.db_execute = SqlserverProvider().db_execute
