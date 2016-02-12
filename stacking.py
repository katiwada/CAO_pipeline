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

# move timeout lists
for file in glob.glob('*_timeout.txt*'):
    shutil.move(config.astrometry_directory,
                config.pipeline_root + 'timeout_lists/')

# Remove clutter created by astrometry.net
new = glob.glob('*.new*')
for file in glob.glob('*'):
    if file in new:
        pass
    else:
        os.remove(config.astrometry_directory + file)

os.chdir(config.stacking_directory)

# script for swarp
script = 'swarp -COPY_KEYWORDS \'FILTER\',\'DATE-OBS\' -IMAGEOUT_NAME %s -WEIGHTOUT_NAME %s @%s'
# grab all astrometretized files
astro_files = glob.glob('*.new')

# empty dictionary that will be populated with file names that share filters
filt_dict = {}

# put respective astrometretized files into lists in filt_dict where key is filter type
for file in astro_files:
    data = fits.open(file)
    filter_type = data[0].header['FILTER']
    if filter_type not in filt_dict.keys():
        key = filter_type
        filt_dict[filter_type] = list()
        filt_dict[key].append(file)
    elif filter_type in filt_dict.keys():
        key = filter_type
        filt_dict[key].append(file)
    data.close()
print(filt_dict)

obs_dict = {}

# create dictionary with key values for dates of observation and values as files with corresponding date of observation
for filt in filt_dict.values():
    for file in filt:
        data = fits.open(file)
        date_time_obs = data[0].header['DATE-OBS']
        date_obs = date_time_obs.split('T', 1)[0]
        if date_obs not in obs_dict.keys():
            key = date_obs
            obs_dict[date_obs] = list()
            obs_dict[key].append(file)
        elif date_obs in obs_dict.keys():
            key = date_obs
            obs_dict[key].append(file)
        data.close()
print(obs_dict)

# Run swarp on sets corresponding to unique dates and filters for all files in astro_files
# empty_set = set()
for filt_files in filt_dict.values():
    for date_files in obs_dict.values():
        cat_name = ''
        filt_set = set(filt_files)
        date_set = set(date_files)
        stack_set = date_set.intersection(filt_set)
        if len(stack_set) == 0:
            pass
        else:
            try:
                stack_list = list(stack_set)
                data = fits.open(stack_list[0])
                obs_date_time = data[0].header['DATE-OBS']
                obs_date = obs_date_time.split('T', 1)[0]
                cat_name = stack_list[0].split('.', 1)[0] + '_' + obs_date
                data.close()

                # create list used by swarp
                fits_list = open(cat_name + '_list.txt', 'a')
                for file in stack_list:
                    fits_list.write(file)
                    fits_list.write('\n')
                fits_list.close()
                swarp_script = script % (cat_name + '.fits', cat_name + '.weight.fits', cat_name + '_list.txt')
                sp.check_call(args=swarp_script, shell=True)
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
for file in glob.glob('*_list.txt*'):
    os.remove(config.stacking_directory + file)

# remove *.new files created by astrometry.net
for file in glob.glob('*.new'):
    os.remove(config.stacking_directory + file)
