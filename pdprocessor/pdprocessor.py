

class PDProcessorError(Exception):
    """A PDProcessor Error."""

    def __init__(self, message):
        self.message = message
