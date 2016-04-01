import numpy as np
import os
import glob
from astropy.io import fits

import Target_Data
import config
import read_fits

td = Target_Data.TargetData()

# All values from target_data are Byte data type.
target_name = td.target_data[:, 0].tolist()
target_RA = td.target_data[:, 1].tolist()
target_dec = td.target_data[:, 2].tolist()

# Converts Byte data in each list to string data type.
target_name = td.bytes_to_str(target_name)
target_RA = td.bytes_to_str(target_RA)
target_dec = td.bytes_to_str(target_dec)

RA_dict = td.target_dict(target_name, target_RA)
dec_dict = td.target_dict(target_name, target_dec)

# 0:UID 1:ra, 2:dec, 3:b, 4:b_err, 5:v, 6:v_err, 7:r, 8:r_err, 9:i, 10:i_err
bllac_ref = np.array([[0, 330.689384, 42.276598, 14.52, 0.04, 12.78, 0.04, 11.93, 0.05, 11.09, 0.06],
                      [1, 330.666992, 42.286056, 15.09, 0.03, 14.19, 0.03, 13.69, 0.03, 13.23, 0.04],
                      [2, 330.636125, 42.279881, 15.68, 0.03, 14.31, 0.05, 13.60, 0.03, 12.93, 0.04],
                      [3, 330.650184, 42.281650, 16.26, 0.05, 15.44, 0.03, 14.88, 0.05, 14.34, 0.10]],
                     dtype=float)

mrk501_ref = np.array([[0, 253.441109, 39.735895, 13.55, 0.03, 12.61, 0.02, 12.11, 0.02, 1., 0.01],
                       [1, 253.368909, 39.783250, 14.10, 0.03, 13.23, 0.02, 12.79, 0.02, 999., 999.],
                       [2, 253.381853, 39.788248, 15.98, 0.04, 15.24, 0.02, 14.80, 0.02, 999., 999.],
                       [3, 253.445300, 39.719267, 16.05, 0.05, 15.30, 0.02, 14.96, 0.02, 999., 999.],
                       [4, 253.493675, 39.800534, 16.27, 0.04, 15.51, 0.02, 15.08, 0.02, 999., 999.],
                       [5, 253.487848, 39.759787, 16.82, 0.05, 15.67, 0.04, 14.99, 0.04, 999., 999.]],
                      dtype=float)


def haversine(ra1, dec1, ra2, dec2, radius=1):
    """
    Haversine formula used to calculate great circle distance (geodesic between two sources on celestial sphere).
    :param ra1: right ascension of first object in degrees
    :param dec1: declination of first object in degrees
    :param ra2: right ascension of second object in degrees
    :param dec2: declination of second object in degrees
    :param radius: Default to unity.  Distance from origin to spherical surface
    :return: distance in degrees
    """
    # Convert all necessary input parameters to radians
    rad_ra1 = np.pi * ra1 / 180
    rad_ra2 = np.pi * ra2 / 180
    rad_dec1 = np.pi * dec1 / 180
    rad_dec2 = np.pi * dec2 / 180

    delta_ra = abs(rad_ra2 - rad_ra1)
    delta_dec = abs(rad_dec2 - rad_dec1)
    value = np.sqrt((np.sin(delta_dec / 2) ** 2) + np.cos(rad_ra1) * np.cos(rad_ra2) * (np.sin(delta_ra / 2) ** 2))
    return np.arcsin(value) * 2 * radius


def find_ref(ref_source, cat):
    """
    Returns list of reference stars in catalog using coordinates of reference stars in source_ref.
    :param ref_source: first column must be right ascension, second column must be declination (both in degrees)
    :param cat: input catalog from pipeline. Must be 'B', 'V', 'R' or 'I'.
    :return: [[row number, distance in degrees],...]
    """
    os.chdir(config.blazar_photometry)
    try:
        cat_data = fits.open(cat)
    except:
        raise
    cat_len = len(cat_data[2].data)
    ref_list = []
    for ref_star in range(len(ref_source)):
        closest = 1e10
        uid = float(np.copy(ref_source[ref_star][0]))
        ref_ra = np.copy(ref_source[ref_star][1])
        ref_dec = np.copy(ref_source[ref_star][2])
        # print(ref_ra, ref_dec)
        for i in range(cat_len):
            cat_ra = np.copy(cat_data[2].data[i][34])
            cat_dec = np.copy(cat_data[2].data[i][35])
            delta = haversine(ref_ra, ref_dec, cat_ra, cat_dec)
            if delta < closest:
                closest = delta
                closest_source = i + 1
        ref_flux = float(np.copy(cat_data[2].data[closest_source - 1][6]))
        ref_fluxerr = float(np.copy(cat_data[2].data[closest_source - 1][7]))
        ref_data = [uid, closest_source, ref_flux, ref_fluxerr]
        ref_list.append(ref_data)
    return ref_list


def find_source(cat):
    """
    Uses methods from target_data class to determine actual source in input catalog.
    :param cat: Input catalog from pipeline
    :return:
    """
    source_ra = float(td.coord_lookup(cat, RA_dict)) * 15.0
    source_dec = float(td.coord_lookup(cat, dec_dict))
    os.chdir(config.blazar_photometry)
    try:
        cat_data = fits.open(cat)
    except:
        raise
    cat_len = len(cat_data[2].data)
    closest = 1e10
    for k in range(cat_len):
        cat_ra = np.copy(cat_data[2].data[k][34])
        cat_dec = np.copy(cat_data[2].data[k][35])
        # print(k, cat_ra, cat_dec)
        delta = haversine(source_ra, source_dec, cat_ra, cat_dec)
        if delta < closest:
            # print(k, delta)
            closest = delta
            closest_source = k + 1
    source_flux = float(np.copy(cat_data[2].data[closest_source - 1][6]))
    source_fluxerr = float(np.copy(cat_data[2].data[closest_source - 1][7]))
    return [closest_source, source_flux, source_fluxerr]


def mag_fit(ref_source, cat, filt):
    """
    Uses find_ref and find_source to create a best fit line for x-axis being flux and y-axis being magnitude.
    :param ref_source: array containing reference stars
    :param cat: Input catalog from pipeline
    :param filt: Filter of stacked file.  Must be 'B', 'V', 'R' or 'I'.
    :return: [catalog name, source information, reference star information, linear fit coefficients,
              reference aperture flux, reference magnitude, flux error, magnitude error]
    """
    ref_list = find_ref(ref_source=ref_source, cat=cat)
    os.chdir(config.blazar_photometry)
    ref_flux = []
    ref_fluxerr = []
    source = find_source(cat=cat)

    if filt == 'B':
        ref_mag = ref_source[:, 3].tolist()
        ref_magerr = ref_source[:, 4].tolist()
    elif filt == 'V':
        ref_mag = ref_source[:, 5].tolist()
        ref_magerr = ref_source[:, 6].tolist()
    elif filt == 'R':
        ref_mag = ref_source[:, 7].tolist()
        ref_magerr = ref_source[:, 8].tolist()
    elif filt == 'I':
        ref_mag = ref_source[:, 9].tolist()
        ref_magerr = ref_source[:, 10].tolist()
    else:
        print('Invalid filter.  Must be B, V, R or I.')
        return False

    # Remove all values of 999.0 in ref_mag and ref_magerr
    while 999. in ref_mag:
        ref_mag.remove(999.)
    while 999. in ref_magerr:
        ref_magerr.remove(999.)
    # Uses uid to populate correct flux for each ref source whose mag or magerr is not 999.0
    for s in ref_mag:
        for t in ref_list:
            if s == t[0]:
                ref_flux.append(t[2])
                ref_fluxerr.append((t[3]))
    lin_fit = np.polyfit(x=ref_flux, y=ref_mag, deg=1)
    return [cat, source, ref_list, lin_fit, ref_flux, ref_mag, ref_fluxerr, ref_magerr]


# User specifies filename information
os.chdir(config.blazar_photometry)
cat_list = glob.glob('*.cat')
ref_source_input = input('Enter ref_source: ')
year_input = input('Enter year: ')

# determine which array to use as reference source
global ref_source_data
if ref_source_input == 'bllac_ref':
    ref_source_data = np.copy(bllac_ref)
elif ref_source_input == 'mrk501_ref':
    ref_source_data = np.copy(mrk501_ref)

# loop to create .txt files containing all data(verbose_file) and data for plotting(data_file)
for catalog in cat_list:
    os.chdir(config.blazar_photometry)
    head_info = read_fits.decode_fitshead(filt1=catalog)
    filter_input = read_fits.get_filter(head_info)
    # dateobs = read_fits.get_dateobs(head_info)
    # mjd_date = read_fits.get_mjd(head_info)
    verbose_file = open(ref_source_input + '_' + filter_input + '_' + year_input + '_verbose.txt', 'a')
    data_file = open(ref_source_input + '_' + filter_input + '_' + year_input + '.txt', 'a')
    cat_data_list = mag_fit(ref_source=ref_source_data, cat=catalog, filt=filter_input)

    for x in cat_data_list:
        verbose_file.write(str(x))
        verbose_file.write(',')
    verbose_file.write('\n')
    verbose_file.close()

    cat_name = cat_data_list[0]
    source_info = cat_data_list[1]
    source_position = source_info[0]
    source_flux_data = source_info[1]
    source_fluxerr_data = source_info[2]
    linear_fit = cat_data_list[3]
    source_mag = linear_fit[0] * source_flux_data + linear_fit[1]
    source_magerr = linear_fit[0] * source_fluxerr_data
    data_file.write(cat_name + ',' + str(filter_input) + ',' + str(source_mag) + ',' + str(source_magerr) + ',')
    data_file.write('\n')
    data_file.close()
