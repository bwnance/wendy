import sys
import os


#check for token.json in the ~/.config/tidal_dl_ng/ directory

playlist_url = os.getenv('PLAYLIST_URL')
if not playlist_url:
    print("Please set the PLAYLIST_URL environment variable.")
    sys.exit(1)
