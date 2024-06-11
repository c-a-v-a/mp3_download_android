import os

# CONSTANTS
DATABASE_PATH = 'db.json'
MUSIC_LOCATIONS = ['music/']


def validate_paths():
    try:
        # make sure that database file exists
        f = open(DATABASE_PATH, 'a')
        f.close()

        # make sure that music directories exist
        for location in MUSIC_LOCATIONS:
            if not os.path.isdir(location):
                os.mkdir(location)
    except:
        raise Exception('Error. Could not validate paths.')
