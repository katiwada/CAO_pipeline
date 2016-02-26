from decimal import *
from subprocess import CalledProcessError, check_call, TimeoutExpired
import Target_Data


def script_loop(files1, dict1, dict2):
    """
    Prints input list of files.  Loops through each i in files1 and performs coord_lookup with i
    with both dict1 and dict2.  Coord_lookup is a method in the Target_Data class.  Right ascension is determined
    by input dict1 and i and declination by dict2 and i.  ra and dec are modified to be used in check_call method that
    runs astrometry.net with the following arguments:
    
        solve-field --use-sextractor --overwrite --downsample <int> --ra <degrees>
        --dec <degrees> --radius <arcminutes> 'filename'

    :param files1: input list of all files in a directory in which to run astrometry.net
    :param dict1: used as a dictionary to determine ra from some file in files1
    :param dict2: used as a dictionary to determine dec from some file in files1
    """
    # set precision for decimal objects to 2 decimal points.
    getcontext().prec = 2
    # Script used in check_call to run astrometry.net as a process.
    script1 = 'solve-field --use-sextractor --overwrite --no-plots --ra %s --dec %s --radius 5 "%s"'
    # instantiate TargetData class
    td = Target_Data.TargetData()
    script_len = len(script1)
    timeoutlist_file = open(files1[0].split('.', 1)[0] + '_timeout.txt', 'a')
    timeout_time = 30

    # Following conditional determines whether script1 is a valid script for use in this program.
    if '--ra' not in script1:
        print('Input script string is invalid.  Please include parameter --ra in script string.')
        return False
    elif '--dec' not in script1:
        print('Input script string is invalid.  Please include parameter --dec in script string.')
        return False
    elif script1[script_len - 4: script_len] != '"%s"':
        print('Input script string is invalid.  Please include placeholder file name that will be used.')
        return False
    elif type(script1) != str:
        print('Input script must be a string.')
        return False

    for i in files1:
        try:
            # note that ra is returned in hour angles.
            ra = td.coord_lookup(i, dict1)
            dec = td.coord_lookup(i, dict2)
            if ra == False or dec == False:
                print('Coordinate lookup error.  Check to see if target exists in target_data.txt.')
                break
            # Convert ra from str to Decimal and multiply by 15 to give angles in degrees as opposed to hour angles.
            # ra_angles is cast back to str during assignment for consistency with dec_int.
            ra_decimal = Decimal(ra)
            ra_angle = str(ra_decimal * 15)

            check_call([script1 % (ra_angle, dec, i)], shell=True, timeout=timeout_time)
            print('Success for file ' + i)
        except AttributeError:
            print('AttributeError: Filename: ' + i + '. Check to see if target exists in target_data.txt')
            raise
        except KeyboardInterrupt:
            print('Halted')
            break
        except CalledProcessError:
            print('CallProcessError for File name: ' + i + '  ra: ' + ra_angle + '  dec: ' + dec +
                  '.  Please check installation of astrometry.net.')
        except TimeoutExpired:
            # populate timeout list with file names of files that timed out during astrometrization
            timeoutlist_file.write(i + ' terminated after ' + str(timeout_time) + ' seconds.')
            timeoutlist_file.write('\n')
        except:
            print('File name: ' + i + '  ra: ' + ra_angle + '  dec: ' + dec)
            raise
    timeoutlist_file.close()


