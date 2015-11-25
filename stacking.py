import subprocess as sp
import threading
import os
import glob
import shutil

from astropy.io import fits

import config

os.chdir(config.astrometry_directory)
for new in glob.glob('*.new'):
    shutil.move(config.astrometry_directory + new,
                config.stacking_directory + new)

os.chdir(config.stacking_directory)

# script for swarp
script = 'swarp -IMAGEOUT_NAME %s @%s'
# grab all astrometretized files
astro_files = glob.glob('*.new')

# empty lists that will be populated with file names that share filters
b_filt = []
v_filt = []
r_filt = []
i_filt = []

for file in astro_files:
    data = fits.open(file)
    filter_type = data[0].header['FILTER']
    if filter_type == 'B':
        b_filt.append(file)
    elif filter_type == 'V':
        v_filt.append(file)
    elif filter_type == 'R':
        r_filt.append(file)
    elif filter_type == 'I':
        i_filt.append(file)
    else:
        print('No filter type detected.')

filt_list = [b_filt, v_filt, r_filt, i_filt]
b = ''
v = ''
r = ''
i = ''
"""
for filt in filt_list:
    if filt == b_filt:
        for k in filt:
            b += ' ' + k
    if filt == v_filt:
        for k in filt:
            v += ' ' + k
    if filt == r_filt:
        for k in filt:
            r += ' ' + k
    if filt == i_filt:
        for k in filt:
            i += ' ' + k
"""
for filt in filt_list:
    cat_name = ''
    try:
        if filt == b_filt:
            cat_name = b_filt[0]
        elif filt == v_filt:
            cat_name = v_filt[0]
        elif filt == r_filt:
            cat_name = r_filt[0]
        elif filt == i_filt:
            cat_name = i_filt[0]

        fits_list = open(cat_name + '_list.txt', 'a')
        for file in filt:
            fits_list.write(file)
            fits_list.write('\n')
        fits_list.close()
        j_script = script % (cat_name, cat_name + '_list.txt')
        swarp = threading.Thread(target=sp.check_call,
                                 args=(j_script, None, None, None, True))
        swarp.start()
    except:
        raise
#iles_for_script = [b, v, r, i]
"""
for j in files_for_script:
    cat_name = ''
    try:
        if j == b:
            cat_name = b_filt[0]
        elif j == v:
            cat_name = v_filt[0]
        elif j == r:
            cat_name = r_filt[0]
        elif j == i:
            cat_name = i_filt[0]
        fits_list = open(cat_name, 'a')

        j_script = script % (cat_name, j)
        swarp = threading.Thread(target=sp.check_call,
                                 args=(j_script, None, None, None, True))
        swarp.start()
    except:
        raise
"""
for stacked in glob.glob('*.fit*'):
    shutil.move(config.stacking_directory + stacked,
                config.sex_directory + stacked)
