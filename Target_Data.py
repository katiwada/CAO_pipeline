import numpy as np


class TargetData:

    # target_data provides a list of targets used to specify RA and Dec for a given .fits file's target object.
    # NOTE: data in this array is of type Byte.
    target_data = np.loadtxt(fname='/Users/jaredhand/Documents/Automation Project/Automation_Project/target_data.txt',
                             dtype=bytes,
                             delimiter=',')

    def __init__(self):
        """
        Initiates TargetData class
        """
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

    def target_dict(self, name_list, val_list):
        """
        Takes list of names and list of values and returns a
        dictionary

        :type name_list: list used for dictionary key
        :type val_list: list used for dictionary value for each key
        """
        result = dict(zip(name_list, val_list))
        return result

    def coord_lookup(self, file1, dict1):
        """
        Used in script_loop() to relate parsed file name to a given coordinate. Filename is split according to conditionals
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

        rm_underscore = i.replace('_', '')
        no_whitespace = rm_underscore.replace(' ', '')

        # This portion of code has a general except clause for each if/elif statement for debugging purposes.
        # Final code will take into consideration different error types and handle them accordingly.
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
