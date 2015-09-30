from subprocess import check_call

from Get_files import check_files
# import SQL_connection
"""
This is incomplete.  Eventually this portion of the data pipeline will use a sql connection to store photometry results
from SExtractor.  Results will be be logged in a sql database.  LDAC type catalogs from SExtracting will likely be used
to determine if a file meets requirements to be used in astrometry.net to determine coordinates of said file.
"""

while True:
    cwd = input('Enter Directory:')
    file_list = check_files(cwd)
    print(file_list)
    if file_list != False:
        break


def sex_files(list1):
    """
    Runs SExtractor on each .fit or .fits file in the directory 'cwd' defined above

    :param list1: list containing file names of files to be SExtracted
    :return returns True if successful
    """
    for i in list1:
        try:
            check_call('sex ' + i, shell=True)
            return True
        except:
            raise










