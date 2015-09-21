from Get_files import check_files


while True:
    cwd = input('Enter Directory:')
    file_list = check_files(cwd)
    print(file_list)
    if file_list != False:
        break
# check_call('sex ' + filename, shell=True)










