# cleanup.py - removing old audio & JSON files

import shared as sh

file_dir = 'audio/'
delete_hours = 48

sh.cleanup(file_dir,delete_hours)

