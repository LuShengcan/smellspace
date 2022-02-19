import os
import re

def ini_to_list(ini_path):
    smell_file = {}
    # print(os.listdir(ini_path))
    for filename in os.listdir(ini_path):
        # print(filename)
        if filename.endswith('.ini'):
            smellname = filename[:-4]
            smell_file[smellname] = []
            f = open(ini_path+'/'+filename, 'r')
            lines = f.readlines()
            for line in lines:
                if '100' in line and '=' in line:
                    start = line.index('=') + 1
                    s = line[start:]
                    if '.' in s and not '=' in s:
                        if re.search(r'[0-9]+', s) is None:
                        # if s[:-2].isalpha():
                            smell_file[smellname].append(s[:-1])
    # print(smell_file.values())
    return smell_file


if __name__ == '__main__':
    ini_to_list('/data01/ymz/ex/smellspace/Temp')
