import os

class PDProcessorError(Exception):
    """A PDProcessor Error."""

    def __init__(self, message):
        self.message = message

class Path(object):
    """A path class."""

    def __init__(self, path_to_file):
        self.path = path_to_file




    


class PDProcessor(Path):
    """Base class for a pandas dataframe processor.

    A PDProcessor creates a dataframe from a delimited file such as csv or
    excel. The dataframe is manipulated by adding or formatting columns.
    """

    def process(self):
        """Process the file."""

        self.validate_path()

    def validate_path(self):
        """Validate the path point to a file."""

        if not os.path.isfile(self.path):
            message = "No file found at '{path}'.".format(path=self.path)
            raise PDProcessorError(message)

        
