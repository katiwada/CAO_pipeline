import decimal
import target_data
import subprocess as sp
import psutil as ps
import get_files
import config
import glob
from astropy.io import fits


def kill_old():
    """
    Checks to see if there is an astrometry-engine process still running.  If there is, it is terminated.
    :return: True unless unhandled exception is raised
    """
    try:
        for p in ps.pids():
            if ps.Process(p).name() == 'astrometry-engine':
                ps.Process(p).terminate()
                break
    except ps.ZombieProcess:
        pass
    except ps.NoSuchProcess:
        pass
    except:
        raise
    return True


def find_failed():
    """
    Finds all fits files in astrometry_directory that do not have corresponding .new files from astrometry.net.
    :return: list of failed fits files
    """
    fits = get_files.check_files(config.astrometry_directory)
    new = glob.glob('*.new')
    fits_names = set(get_files.get_name(list1=fits))
    new_names = set(get_files.get_name(list1=new))
    failed = fits_names.difference(new_names)
    return list(failed)


def astro_pipe(files, dict1, dict2):
    """
    Runs astrometry.net on input file.  ra and dec are modified to be used in check_call method that
    runs astrometry.net with the following arguments:

        solve-field --use-sextractor --overwrite --downsample <int> --ra <degrees>
        --dec <degrees> --radius <arcminutes> 'filename'

    :param files: input files in which to run astrometry.net on
    :param dict1: used as a dictionary to determine ra from some file
    :param dict2: used as a dictionary to determine dec from some file
    """
    # set precision for decimal objects to 2 decimal points.
    decimal.getcontext().prec = 2

    # Script used in check_call to run astrometry.net as a process.
    script1 = 'solve-field --use-sextractor --overwrite --no-plots --no-remove-lines --ra %s --dec %s --radius 5 "%s"'

    # these following list is used to populate timed out and fail logs along with fail_list defined below.
    timeout_list = []

    # instantiate TargetData class
    td = target_data.TargetData()

    timeout_time = 20
    for i in files:
        try:
            # note that ra is returned in hour angles.
            ra = td.coord_lookup(i, dict1)
            dec = td.coord_lookup(i, dict2)
            if ra == False or dec == False:
                print('Coordinate lookup error.  Check to see if target exists in target_data.txt.')
            # Convert ra from str to Decimal and multiply by 15 to give angles in degrees as opposed to hour angles.
            # ra_angles is cast back to str during assignment for consistency with dec_int.
            ra_decimal = decimal.Decimal(ra)
            ra_angle = str(ra_decimal * 15)

            sp.run(script1 % (ra_angle, dec, i), shell=True, timeout=timeout_time)

        except KeyboardInterrupt:
            print('Halted')
        except sp.TimeoutExpired:
            timeout_list.append(i)
            kill_old()
        except:
            print('File name: ' + i + '  ra: ' + ra_angle + '  dec: ' + dec)
            raise

    # Used along with timeout_list to log all files that failed/timed out during astrometrization
    fail_list = find_failed()

    # a function will be added here that will create a timeout and failed file log.  Kati is working on this.
    # @edit Kati Wada working progress...
    hdulist = fits.open('input.fits')
    fheader = hdulist[0].header['targname']
    
    complete_fails = list(find_failed() - timeout_list) #separating out the complete files
    
    file = open('failntime.rtf', 'w') #creating a text file for lists
    
    name = timeout_time + date_obs + fheader + newfilename
    for i in timeout_list:
        file.write('timeout' + name)#writing in the file
    for i in complete_fails:
        file.write('Complete Fail' + name)#writing in the file 
    file.close()
    hdulist.close()

def wcs_header_merge(files, wcs):
    """
    Merges wcs solution from astrometry.net with old fits file to create new fits file
    :param files: list of fits files
    :param wcs: list of wcs solutions from astrometry.net
    :return: True unless unhandled exception is raised
    """
    script = 'new-wcs -i %s -w %s -o %s -d'
    for file in files:
        f_name = file.split('.', 1)[0]
        for w in wcs:
            w_name = w.split('.', 1)[0]
            if f_name == w_name:
                new_file = f_name + '_wcs.fits'
                try:
                    subprocess.run(script % (file, w, new_file), shell=True)
                except:
                    raise
    return True

