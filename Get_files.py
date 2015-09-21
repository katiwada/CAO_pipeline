import os
import glob


def check_files(user_input):
    """
    Checks to make sure given directory is a valid directory.
    If directory exists, returns list of .fit or .fits files.
    """
    file_ext = ['*.fit*', '*.FIT*']
    data_files = []
    working_dir = os.path.exists(user_input)

    if working_dir:
        os.chdir(user_input)
        for files in file_ext:
            data_files += glob.glob(files)
        print(data_files)
        return data_files
    else:
        print('Invalid directory. Please try again.')
        return False
