from collections import namedtuple

from gettext import gettext as _


Line = namedtuple('Line', ('number', 'content'))


class Entry:
    """
    Manifest entry.
    Format: <path>, <size>, <digest>

    Lines beginning with `#` are ignored.

    Attributes:
        path (str): A relative path.
        size (int): The file size in bytes.
        digest (str): The file sha256 hex digest.
    """

    @staticmethod
    def parse(line):
        """
        Parse the specified line from the manifest into an Entry.

        Args:
            line (Line): A line from the manifest.

        Returns:
            Entry: An entry.

        Raises:
            ValueError: on parsing error.
        """
        part = [s.strip() for s in line.content.split(',')]
        if len(part) != 3:
            raise ValueError(
                _('Error: manifest line:{n}: '
                  'must be: <path>, <size>, <digest>').format(
                    n=line.number))
        return Entry(path=part[0],
                     size=int(part[1]),
                     digest=part[2])

    def __init__(self, path, size, digest):
        """
        Args:
            path (str): A relative path.
            size (int): The file size in bytes.
            digest (str): The file sha256 hex digest.
        """
        self.path = path
        self.size = size
        self.digest = digest


class Manifest:
    """
    A file manifest.
    Describes files contained within the directory.

    Attributes:
        path (str): An absolute path to the manifest.
    """

    def __init__(self, path):
        """
        Args:
            path (str): An absolute path to the manifest.
        """
        self.path = path

    def read(self):
        """
        Read the file at `path` and yield entries.

        Yields:
            Entry: for each line.
        """
        with open(self.path) as fp:
            n = 0
            for line in fp.readlines():
                n += 1
                line = line.strip()
                if not line:
                    continue
                if line.startswith('#'):
                    continue
                yield Entry.parse(Line(number=n, content=line))
