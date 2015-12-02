import subprocess as sp
import os
import glob
import shutil

import Get_files

import config

# Set current working directory to /Users/jaredhand/Documents/photometry/data_in/
os.chdir(config.sex_directory)
# str for sextractor script
script = 'sex -CATALOG_NAME %s %s'
files = Get_files.get_files()


def sex_call(list1):
    """
    Runs sextractor on all members of input list1.

    :param list1: list of fits/FITS files in cwd
    :return: False if subprocess fails, otherwise returns True
    """

    if os.getcwd() != '/Users/jaredhand/Documents/photometry/data_in':
        print('Check current directory.')
        return False
    elif not list1:
        print('No .fit or .FIT files in /data_in folder.')
        return False

    for i in list1:
        cat_name = i.split('.')[0] + '.cat'
        try:
            sp.check_call(script % (cat_name, i), shell=True)
        except:
            raise
    return True

# sex fits in cwd
sex_call(list1=files)

# move catalogs to catalog directory
for sexed in glob.glob('*.cat'):
    shutil.move(config.sex_directory + sexed,
                config.finished_catalogs + sexed)

# move stacked fits to finished stacked directory
for stacked in glob.glob('*'):
    shutil.move(config.sex_directory + stacked,
                config.finished_stacked + stacked)

