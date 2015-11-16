import subprocess as sp
import os
import glob
import shutil

import Get_files

# Set current working directory to /Users/jaredhand/Documents/photometry/data_in/
os.chdir('/Users/jaredhand/Documents/photometry/data_in/')
# str for sextractor script
script = 'sex -CATALOG_NAME %s %s'
files = Get_files.get_files()


def sex_call(list1):
    """
    Runs sextractor on all members of input list1.

    :param list1: list of fits/FITS files in cwd
    :return: False if subprocess fails, otherwise returns True
    """
    print(os.getcwd())
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

print(os.getcwd())
sex_call(list1=files)
for i in glob.glob('*.cat'):
    shutil.move('/Users/jaredhand/Documents/photometry/data_in/' + i,
                '/Users/jaredhand/Documents/photometry/catalogs/' + i)


"""
def get_files():

    fits = []
    FITS = []
    try:
        for file in Path('/Users/jaredhand/Documents/photometry/data_in/').glob('/**/*.FIT*'):
            if 'FIT.gz' in file:
                sp.check_call('gunzip ' + file, shell=True)
            FITS.append(file)

        for file in Path('/Users/jaredhand/Documents/photometry/data_in/').glob('/**/*.fit*'):
            if 'fit.gz' in file:
                sp.check_call('gunzip ' + file, shell=True)
            fits.append(file)

    except sp.CalledProcessError:
        raise

    return fits + FITS
"""




