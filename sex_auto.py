import subprocess as sp
import os
import get_files
import config


def sex_call():
    """
    Runs sextractor on all members of input list1.

    :param list1: list of fits/FITS files in cwd
    :return: False if subprocess fails, otherwise returns True
    """
    # Set current working directory to /Users/jaredhand/Documents/photometry/data_in/
    os.chdir(config.sex_directory)
    # str for sextractor script
    script = 'sex -CATALOG_NAME %s %s'
    files = get_files.get_files()
    if not files:
        print('No .fit or .FIT files in /data_in folder.')
        return False

    for i in files:
        cat_name = i.split('.')[0] + '.cat'
        try:
            sp.check_call(script % (cat_name, i), shell=True)
        except:
            raise
    return True
