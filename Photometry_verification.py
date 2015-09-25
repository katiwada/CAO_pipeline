from subprocess import check_call

from Get_files import check_files
# import SQL_connection


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
    :return:
    """
    for i in list1:
        try:
            check_call('sex ' + i, shell=True)
            return True
        except:
            raise










