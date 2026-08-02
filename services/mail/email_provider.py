from services.mail.email.email import EMail
from toolboxs.decorators import singleton

# --
# ...
# --


@singleton
class EMailProvider:
    def __init__(self, **kwargs):
        self.email = EMail().instance
