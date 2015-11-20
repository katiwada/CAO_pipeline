import subprocess as sp
import threading
import os
import glob

from astropy.io import fits

from Get_files import check_files, rm_spaces

directory = input('Enter directory')
os.chdir(directory)

script = 'swarp s%'
astro_files = glob.glob('*.new')

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
    swarp = threading.thread(target=sp.check_call, args=([script, j], None, None, None, True))
    swarp.start()





