import numpy as np
import os
from astropy.io import fits
import matplotlib.pyplot as plt

import Target_Data
import config

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

# 0:ra, 1:dec, 2:b, 3:b_err, 4:v, 5:v_err, 6:r, 7:r_err, 8:i, 9:i_err
bllac_ref = np.array([[330.689384, 42.276598, 14.52, 0.04, 12.78, 0.04, 11.93, 0.05, 11.09, 0.06],
                      [330.666992, 42.286056, 15.09, 0.03, 14.19, 0.03, 13.69, 0.03, 13.23, 0.04],
                      [330.636125, 42.279881, 15.68, 0.03, 14.31, 0.05, 13.60, 0.03, 12.93, 0.04],
                      [330.650184, 42.281650, 16.26, 0.05, 15.44, 0.03, 14.88, 0.05, 14.34, 0.10]],
                     dtype=float)

mrk501_ref = np.array([[253.441109, 39.735895, 13.55, 0.03, 12.61, 0.02, 12.11, 0.02, 0, 0],
                       [253.368909, 39.783250, 14.10, 0.03, 13.23, 0.02, 12.79, 0.02, 0, 0],
                       [253.381853, 39.788248, 15.98, 0.04, 15.24, 0.02, 14.80, 0.02, 0, 0],
                       [253.445300, 39.719267, 16.05, 0.05, 15.30, 0.02, 14.96, 0.02, 0, 0],
                       [253.493675, 39.800534, 16.27, 0.04, 15.51, 0.02, 15.08, 0.02, 0, 0],
                       [253.487848, 39.759787, 16.82, 0.05, 15.67, 0.04, 14.99, 0.04, 0, 0]],
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
    x = np.sqrt((np.sin(delta_dec / 2)**2) + np.cos(rad_ra1) * np.cos(rad_ra2) * (np.sin(delta_ra / 2)**2))
    return np.arcsin(x) * 2 * radius


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
        ref_ra = np.copy(ref_source[ref_star][0])
        ref_dec = np.copy(ref_source[ref_star][1])
        # print(ref_star, source_ra, source_dec)
        for i in range(cat_len):
            cat_ra = np.copy(cat_data[2].data[i][34])
            cat_dec = np.copy(cat_data[2].data[i][35])
            # print(i, cat_ra, cat_dec)
            delta = haversine(ref_ra, ref_dec, cat_ra, cat_dec)
            if delta < closest:
                # print(i, delta)
                closest = delta
                closest_source = i + 1
        ref_flux = float(np.copy(cat_data[2].data[closest_source - 1][6]))
        ref_data = [closest_source, ref_flux]
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
    print(source_ra, source_dec)
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
        # print(i, cat_ra, cat_dec)
        delta = haversine(source_ra, source_dec, cat_ra, cat_dec)
        if delta < closest:
            # print(k, delta)
            closest = delta
            closest_source = k + 1
    source_flux = float(np.copy(cat_data[2].data[closest_source - 1][6]))
    return [closest_source, source_flux]


def mag_fit(ref_source, cat, filt):
    """
    Uses find_ref and find_source to create a best fit line for x-axis being flux and y-axis being magnitude.
    :param ref_source: array containing reference stars
    :param cat: Input catalog from pipeline
    :param filt: Filter of stacked file.  Must be 'B', 'V', 'R' or 'I'.
    :return: [linear fit coefficients, reference aperture flux, reference magnitude, flux error, magnitude error]
    """
    ref_list = find_ref(ref_source=ref_source, cat=cat)
    os.chdir(config.blazar_photometry)
    ref_flux = []
    ref_fluxerr = []
    source = find_source(cat=cat)

    if filt == 'B':
        ref_mag = ref_source[:, 2]
        ref_magerr = ref_source[:, 3]
    elif filt == 'V':
        ref_mag = ref_source[:, 4]
        ref_magerr = ref_source[:, 5]
    elif filt == 'R':
        ref_mag = ref_source[:, 6]
        ref_magerr = ref_source[:, 7]
    elif filt == 'I':
        ref_mag = ref_source[:, 8]
        ref_magerr = ref_source[:, 9]
    else:
        print('Invalid filter.  Must be B, V, R or I.')
        return False
    try:
        cat_data = fits.open(cat)
    except:
        raise
    for j in range(len(ref_list)):
        ref_number = ref_list[j][0]
        ref_flux.append(cat_data[2].data[ref_number - 1][6])
        ref_fluxerr.append(cat_data[2].data[ref_number - 1][7])
    cat_data.close()

    linear_fit = np.polyfit(x=ref_flux, y=ref_mag, deg=1)
    return [[cat, source, ref_list], [linear_fit, ref_flux, ref_mag, ref_fluxerr, ref_magerr]]


best_fit = mag_fit(ref_source=bllac_ref, cat='BL_Lac-001B_2010-11-02_2010-11-02.cat', filt='B')
print(best_fit)

x_list = np.linspace(0, 5000, 10000)
y_list = []
stuff = best_fit[1]
line_fit = stuff[0]
for i in x_list:
    y_list.append(i * line_fit[0] + line_fit[1])

thing = best_fit[0]
that = thing[1]
source_flux = that[1]
source_mag = source_flux*line_fit[0] + line_fit[1]

plt.scatter(stuff[1], stuff[2], c='r')
plt.scatter(source_flux, source_mag, c='g')
plt.plot(x_list, y_list)
plt.show()
