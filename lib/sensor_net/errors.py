class BackendError(Exception):
    """Backend Error"""
    def __init__(self, backend_name: str, message: str, *args):
        super().__init__(backend_name + ":" + message, *args)
        self.backend_name = backend_name
        self.message = message


class BackendWriteError(BackendError):
    """Backend Write Error"""
    pass
