import subprocess as sp
import threading
import os
import glob
import shutil

from astropy.io import fits

import config

#
for new in glob.glob('*.new'):
    shutil.move(config.astrometry_directory + new,
                config.stacking_directory + new)

os.chdir(config.stacking_directory)

# script for swarp
script = 'swarp -IMAGEOUT_NAME s% s%'
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

for filt in filt_list:
    if filt == b_filt:
        for k in filt:
            b += k
    if filt == v_filt:
        for k in filt:
            v += k
    if filt == r_filt:
        for k in filt:
            r += k
    if filt == i_filt:
        for k in filt:
            i += k

files_for_script = [b, v, r, i]

for j in files_for_script:
    cat_name = files_for_script[0]
    swarp = threading.Thread(target=sp.check_call,
                             args=([script % (cat_name, j)], None, None, None, True))
    swarp.start()

for stacked in glob.glob('*.fit*'):
    shutil.move(config.stacking_directory + stacked,
                config.sex_directory + stacked)
