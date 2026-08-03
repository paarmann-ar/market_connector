from services.mail.email.email import EMail
from services.core.singleton_meta import SingletonMeta
# --
# ...
# --


class EMailProvider(metaclass= SingletonMeta):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.email = EMail()
