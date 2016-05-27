import os
import glob
import subprocess as sp
from astropy.io import fits


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
        if glob.glob('*.gz*'):
            try:
                sp.check_call('gunzip *.gz', shell=True)
            except sp.CalledProcessError:
                # this exception is raised if gunzip has no files to unzip.  As a result, it is ignored.
                pass
        for files in file_ext:
            data_files += glob.glob(files)
        if not data_files:
            print('Input directory contains no .fit(s) or .FIT(S) files.  Please enter another directory.')
            return False
        print(data_files)
        return data_files
    else:
        print('Invalid directory. Please try again.')
        return False


def rm_spaces(list1):
    """
    Removes all whitespace from members of a list (assuming list contains only str objects).

    :param list1: input list where are whitespace is replaced with '_'
    :return: modified list1
    """
    if len(list1) > 0:
        for i in range(len(list1)):
            if ' ' in list1[i]:
                j = list1[i].replace(' ', '_')
                os.rename(list1[i], j)
                list1.pop(i)
                list1.insert(i, j)
        return list1
    else:
        print('Directory contains no .fit(s) or .FIT(s) files.')
        return False


def get_files():
    """
    Decompress all FIT.gz files is they exists and returns list of all fit/FIT files in active directory.

    :return: fits+FITS as a list
    """
    try:
        if glob.glob('*.gz*'):
            sp.check_call('gunzip *FIT.gz', shell=True)
            sp.check_call('gunzip *fit.gz', shell=True)
            fits = glob.glob('*.fit*')
            FITS = glob.glob('*.FIT*')
            no_space = rm_spaces(list1=fits + FITS)
            return no_space
    except sp.CalledProcessError:
        raise
    try:
        if glob.glob('*.fit*') or glob.glob('*FIT'):
            fits = glob.glob('*.fit*')
            FITS = glob.glob('*.FIT*')
            no_space = rm_spaces(list1=fits + FITS)
            return no_space
    except sp.CalledProcessError:
        raise


def subdir_adddate(dir):
    """
    This is a script to take 'DATE-OBS' from fit file header and tack it onto the end of the file name.
    The script will recursively go through subdirectories of directory 'dir' from the top down.

    :param dir: directory where script is to be run
    :return:
    """
    if not os.path.isdir(dir):
        print('Directory parameter is not a directory.')
        return False
    for root, dirs, files in os.walk(dir):
        for directory in dirs:
            os.chdir(root + '/' + directory + '/')
            for f in glob.glob('*.fit*'):
                try:
                    data = fits.open(f)
                    date_time_obs = data[0].header['DATE-OBS']
                    date_obs = date_time_obs.split('T', 1)[0]
                    fname1 = f.split('.', 1)[0]
                    fname2 = f.split('.', 1)[1]
                    newfilename = fname1 + '_' + date_obs + '.' + fname2
                    os.rename(root + directory + '/' + f,
                              root + directory + '/' + newfilename)
                except:
                    raise
            for f in glob.glob('*.FIT*'):
                try:
                    data = fits.open(f)
                    date_time_obs = data[0].header['DATE-OBS']
                    date_obs = date_time_obs.split('T', 1)[0]
                    fname1 = f.split('.', 1)[0]
                    fname2 = f.split('.', 1)[1]
                    newfilename = fname1 + '_' + date_obs + '.' + fname2
                    os.rename(root + directory + '/' + f,
                              root + directory + '/' + newfilename)
                except:
                    raise
    return True


def subdir_chgname(dir, old, new):
    """
    This script checks to see if the string 'old' is in a filename in given directory.  If so, old is replaced
    with new.  Recursively checks subdirectories of 'dir' from the top down.

    :param dir: Directory where script is to be run
    :param old: old character string in file name
    :param new: character string to replace old in file name
    :return:
    """
    oldstr = str(old)
    newstr = str(new)
    if not os.path.isdir(dir):
        print('Directory parameter is not a directory.')
        return False
    for root, dirs, files in os.walk(dir):
        for directory in dirs:
            os.chdir(root + '/' + directory + '/')
            for f in glob.glob('*.fit*'):
                try:
                    if oldstr in f:
                        newfilename = f.replace(oldstr, newstr)
                        os.rename(root + directory + '/' + f,
                                  root + directory + '/' + newfilename)

                except:
                    raise
            for f in glob.glob('*.FIT*'):
                try:
                    if oldstr in f:
                        newfilename = f.replace(oldstr, newstr)
                        os.rename(root + directory + '/' + f,
                                  root + directory + '/' + newfilename)
                except:
                    raise
    return True


def get_name(list1):
    list1_len = len(list1)
    new_list = []
    for f in range(list1_len):
        old = list1[f]
        new = old.split('.', 1)[0]
        new_list.append(new)
    return new_list


# subdir_chgname(dir='/Users/jaredhand/Documents/sources/3c454dot3/2014/', old='3C 454.3', new='3C_454dot3')
# subdir_adddate(dir='/Users/jaredhand/Documents/sources/bllac/2012/')
