from typing import Dict

class OnlineItem:
    """Class representing a muisc item that is not saved locally on the device.
    """
    def __init__(self, x: Dict[str, str]):
        self.from_dict(x)

    def from_dict(self, x: Dict[str,str]):
        """Convert a dictionary into OnlineItem object"""
        try:
            self.title = x['title']
            self.url = x['url']
            self.is_album = str(x['is_album']).lower() == 'true'
        except KeyError:
            raise Exception(f'Error. Could not parse dictionary {x}.')


class OfflineItem:
    """Class representing a muisc item that is not saved locally on the device.
    """
    def __init__(self, location: str, name: str, is_album: bool):
        self.location = location
        self.name = name
        self.is_album = is_album
