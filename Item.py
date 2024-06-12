class Item:
    """
    A class that represents a single musical item (song or album)

    Attributes
    ----------
    location : str
        a path to directory in which this item is located
    name : str
        a name of this item (song title or album name)
    is_album : bool
        a value that tells us weather this item is and album or just a singular
        song
    """
    def __init__(self, location: str, name: str, is_album: bool):
        """
        Constructs an item.

        Parameters
        ----------
        location : str
            a path to directory in which this item is located
        name : str
            a name of this item (song title or album name)
        is_album : bool
            a value that tells us weather this item is and album or just a singular
            song
        """
        self.location = location
        self.name = name
        self.is_album = is_album
