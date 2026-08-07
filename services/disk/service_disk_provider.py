from services.disk.csv.csv_manager import CSVManager
from services.disk.excel.excel_manager import ExcelManager
from services.disk.file.file_manager import FileManager
from services.disk.json.json_manager import JSONManager
from services.disk.xml.xml_manager import XMLManager
from services.logging.log_provider import LogProvider
from services.core.singleton_meta import SingletonMeta

# --
# ...
# --


class ServiceDiskProvider(metaclass=SingletonMeta):
    def __init__(self, **kwargs):
        log_info_class = LogProvider().info
        log_error_class = LogProvider().error

        self.json = JSONManager(log_info_class=log_info_class, log_error_class=log_error_class, **kwargs)

        self.xml = XMLManager(log_info_class=log_info_class, log_error_class=log_error_class, **kwargs)

        self.file = FileManager(log_info_class=log_info_class, log_error_class=log_error_class, **kwargs)

        self.excel = ExcelManager(log_info_class=log_info_class, log_error_class=log_error_class, **kwargs)

        self.csv = CSVManager(log_info_class=log_info_class, log_error_class=log_error_class, **kwargs)
