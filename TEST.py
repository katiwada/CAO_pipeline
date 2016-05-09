import astrometry as a
import config
import os
import glob
import numpy as np
import sex_auto
import shutil

# initialize fits_files variable as a list of fits files at input directory.
"""
while True:
    cwd = config.astrometry_directory
    fits_files = Get_files.check_files(cwd)
    no_space = Get_files.rm_spaces(fits_files)
    if no_space:
        break

# Instantiate TargetData class.
td = Target_Data.TargetData()
# All values from target_data are Byte data type.
target_name = td.target_data[:, 0].tolist()
target_RA = td.target_data[:, 1].tolist()
target_dec = td.target_data[:, 2].tolist()
# Converts Byte data in each list to string data type.
target_name = td.bytes_to_str(target_name)
target_RA = td.bytes_to_str(target_RA)
target_dec = td.bytes_to_str(target_dec)
# create dictionaries of RA and dec for each respective target
RA_dict = td.target_dict(target_name, target_RA)
dec_dict = td.target_dict(target_name, target_dec)
"""

# a.astro_pipe(fits_files, RA_dict, dec_dict)

# a.wcs_header_merge(fits_files, glob.glob('*.wcs'))
# fit = fits.open('3C_279-001B_2011-03-29_wcs_2011-03-29_st.cat')
# fitio = fitsio.read('3C_279-001B_2011-03-29_wcs_2011-03-29_st.cat')
# print(fitio)
# decoded = read_fits.decode_fitshead('3C_279-001B_2011-03-29_wcs_2011-03-29_st.cat')
# print(decoded)
# print(read_fits.get_filter(decoded))

# run SExtractor on stacked files
sex_auto.sex_call()

# move catalogs to catalog directory
for sexed in glob.glob('*.cat'):
    shutil.move(config.sex_directory + sexed,
                config.finished_catalogs + sexed)
# move stacked fits to finished stacked directory
for stacked in glob.glob('*.fit*'):
    shutil.move(config.sex_directory + stacked,
                config.finished_stacked + stacked)






