import decimal
import Target_Data
import subprocess
import psutil as ps
import Get_files
import config
import glob


def kill_old():
    """
    Checks to see if there is an astrometry-engine process still running.  If there is, it is terminated.
    :return:
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
    fits = Get_files.check_files(config.astrometry_directory)
    new = glob.glob('*.new')
    fits_names = set(Get_files.get_name(list1=fits))
    new_names = set(Get_files.get_name(list1=new))
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

    # instantiate TargetData class
    td = Target_Data.TargetData()

    script_len = len(script1)
    timeoutlist_file = open(files[0].split('.', 1)[0] + '_timeout.txt', 'a')
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

            subprocess.run(script1 % (ra_angle, dec, i), shell=True, timeout=timeout_time)

        except KeyboardInterrupt:
            print('Halted')
        except subprocess.TimeoutExpired:
            # populate timeout list with file names of files that timed out during astrometrization
            timeoutlist_file.write(i + ' terminated after ' + str(timeout_time) + ' seconds.')
            timeoutlist_file.write('\n')
            kill_old()
        except:
            print('File name: ' + i + '  ra: ' + ra_angle + '  dec: ' + dec)
            timeoutlist_file.close()
            raise

    failed_files = find_failed()
    for failed in failed_files:
        timeoutlist_file.write((failed + ' did not succeed'))
        timeoutlist_file.write('\n')
    timeoutlist_file.close()


def wcs_header_merge(files, wcs):
    """
    Merges wcs solution from astrometry.net with old fits file to create new fits file
    :param files: list of fits files
    :param wcs: list of wcs solutions from astrometry.net
    :return:
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

