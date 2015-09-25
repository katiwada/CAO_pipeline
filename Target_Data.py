import numpy as np


class TargetData:

    # target_data provides a list of targets used to specify RA and Dec for a given .fits file's target object.
    target_data = np.loadtxt(fname='/Users/jaredhand/Documents/Automation Project/Automation_Project/target_data.txt',
                             dtype=bytes,
                             delimiter=',')

    def __init__(self):
        pass

    def bytes_to_str(self, list_input):
        """
        Converts data type of imported array elements from
        bytes to string.
        :type list_input: list
        """
        for i in range(len(list_input)):
            x = list_input[i].decode('utf-8')
            list_input[i] = x
        return list_input

    target_name = target_data[:, 0].tolist()
    target_RA = target_data[:, 1].tolist()
    target_dec = target_data[:, 2].tolist()

    target_name = bytes_to_str(target_name)
    target_RA = bytes_to_str(target_RA)
    target_dec = bytes_to_str(target_dec)

    def target_dict(self, name_list, val_list):
        """
        Takes list of names and list of values and returns a
        dictionary

        :type name_list: list used for dictionary key
        :type val_list: list used for dictionary value for each key
        """
        result = dict(zip(name_list, val_list))
        return result

    RA_dict = target_dict(target_name,
                          target_RA)
    dec_dict = target_dict(target_name,
                           target_dec)

    def coord_lookup(self, file1, dict1):
        """
        Used in script_loop() to relate parsed file name to a given coordinate. Filename is split according to conditional
        below.

        :type file1: string representing filename that will be compared to keys of dict1
        :type dict1: dictionary that is used to lookup coordinates via the keyvalue to file1

        """

        if 'B_' in file1:
            i = file1.split('B_', 1)[0]
        elif 'V_' in file1:
            i = file1.split('V_', 1)[0]
        elif 'I_' in file1:
            i = file1.split('I_', 1)[0]
        elif 'R_' in file1:
            i = file1.split('R_', 1)[0]
        elif '-' in file1:
            i = file1.split('-', 1)[0]
        elif '_' in file1:
            i = file1.split('_', 1)[0]
        else:
            return False

        no_whitespace = i.replace(' ', '')
        if no_whitespace in dict1.keys():
            try:
                print(no_whitespace)
                coord = dict1.get(no_whitespace)
                print(coord)
                return coord
            except:
                raise
                # return False
        elif no_whitespace.upper() in dict1.keys():
            try:
                print(no_whitespace.upper())
                coord = dict1.get(no_whitespace.upper())
                print(coord)
                return coord
            except:
                raise
                # return False
        elif no_whitespace.lower() in dict1.keys():
            try:
                print(no_whitespace.lower())
                coord = dict1.get(no_whitespace.lower())
                print(coord)
                return coord
            except:
                raise
                # return False

        else:
            return False
