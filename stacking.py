import subprocess as sp
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
script = 'swarp -IMAGEOUT_NAME %s -WEIGHTOUT_NAME %s @%s'
# grab all astrometretized files
astro_files = glob.glob('*.new')

# empty lists that will be populated with file names that share filters
b_filt = []
v_filt = []
r_filt = []
i_filt = []

# put respective astrometretized files into lists based on filter type
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

# list of filter lists
filt_list = [b_filt, v_filt, r_filt, i_filt]

# run Swarp on a list of fits with corresponding filter types
for filt in filt_list:
    cat_name = ''
    try:
        if filt == b_filt:
            cat_name = b_filt[0].split('.', 1)[0]
        elif filt == v_filt:
            cat_name = v_filt[0].split('.', 1)[0]
        elif filt == r_filt:
            cat_name = r_filt[0].split('.', 1)[0]
        elif filt == i_filt:
            cat_name = i_filt[0].split('.', 1)[0]
        fits_list = open(cat_name + '_list.txt', 'a')
        # create list used by swarp
        for file in filt:
            fits_list.write(file)
            fits_list.write('\n')
        fits_list.close()
        j_script = script % (cat_name + '.fits', cat_name + '.weight.fits', cat_name + '_list.txt')
        sp.check_call(args=j_script, shell=True)
    except:
        raise

# move stacked fits and weights to respective directories
for stacked in glob.glob('*.fit*'):
    if stacked in glob.glob('*.weight.fit*'):
        shutil.move(config.stacking_directory + stacked,
                    config.stacking_directory + '/weights/' + stacked)
    else:
        shutil.move(config.stacking_directory + stacked,
                    config.sex_directory + stacked)

# remove lists used by swarp
for file in glob.glob('*._list.txt*'):
    os.remove(config.stacking_directory + file)
