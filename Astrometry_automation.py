from decimal import *
from subprocess import check_call, CalledProcessError

import numpy as np
from Get_files import check_files
from Target_Data import TargetData
from astropy.table import Table




# initialize fits_files variable as a list of fits files at input directory.
while True:
    cwd = input('Enter Directory:')
    fits_files = check_files(cwd)
    print(fits_files)
    if fits_files != False:
        break


# set precision for decimals:
getcontext().prec = 2

script = 'solve-field --use-sextractor --overwrite --no-plots --ra %s --dec %s --radius 2 "%s"'

td = TargetData()


def script_loop(files1, dict1, dict2):
    """
    Prints input list of files.  Loops through reach i in files1 and performs coord_lookup with i 
    with both dict1 and dict2.  From there right ascension is determined by input dict1 and i and 
    declination by dict2 and i.  ra and dec are modified to be used in check_call method that runs 
    astrometry.net with given parameters:
    
        solve-field --use-sextractor --overwrite --downsample <int> --ra <degrees>
        --dec <degrees> --radius <arcminutes> 'filename'
        
    Parameters:
    
        files1: input list of all files in a directory in which to run astrometry.net
        dict1: used as a dictionary to determine ra a file in files1
        dict2: used as a dictionary to determine dec from a file files1
        
    """
    print(files1)
    for i in files1:
        """
        try:
            proc.communicate(timeout=5)
        except TimeoutExpired:
            proc.kill()
        """
        try:
            # note that ra is returned in hour angles.
            ra = td.coord_lookup(i,
                              dict1)

            dec = td.coord_lookup(i,
                               dict2)

            if ra == False or dec == False:
                print('Coordinate lookup error.  Check to see if target exists in target_data.txt.')
                break

            """
            Convert ra from str to Decimal and multiply by 15 to give angles in degrees as opposed to hour angles.
            ra_angles is cast back to str during assignment for consistency with dec_int.
            """
            ra_decimal = Decimal(ra)
            ra_angle = str(ra_decimal * 15)

            print(script % (ra_angle, dec, i))

            proc = check_call([script % (ra_angle, dec, i)],
                              shell=True)

            print('Success for file ' + i)
        except AttributeError:
            print('AttributeError: Filename: ' + i + '. Check to see if target exists in target_data.txt')
            raise
        except KeyboardInterrupt:
            print('Halted')
            break
        except CalledProcessError:
            print("CallProcessError for File name: " + i + "  ra: " + ra_angle + "  dec: " + dec +
                  ".  Please check installation of astrometry.net.")
        except:
            print("File name: " + i + "  ra: " + ra_angle + "  dec: " + dec)
            raise

"""
print(script_loop(fits_files, RA_dict, dec_dict))

target_table = Table([target_name, target_RA, target_dec],
                     names=('name', 'RA', 'dec'))
target_table.show_in_browser()
"""