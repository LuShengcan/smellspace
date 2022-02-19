import os
import csv
import subprocess
import json
import xlwt

def Scan_Version(Version_Path):
    paths = Version_Path
    F = []
    for root, dirs, files in os.walk(paths):
        if ('src/main') in root and 'test' not in root.lower():
            #F.append(root)
            #print(root)
            index = root.index('src/main')
            tmp = root[:index] + 'src/main/'
            if tmp not in F:
                F.append(tmp)
    # for f in F:
    #     print(f)
    print("F:",F)
    return F

def ini_to_list(ini_path):
    startStr = 'org'
    SmellyFile = {}
    for filename in os.listdir(ini_path):
        if filename.endswith('.ini'):
            smellName = filename[:-4]
            smellyFiles = []
            with open(ini_path + filename) as f:
                for line in f:
                    if startStr in line:
                        index = line.index(startStr)
                        smellyFile = line[index:-1]
                        #if (not smellyFile.endswith('Test') and not smellyFile.endswith('TestCase')):
                        if ('test' not in smellyFile.lower()):
                            smellyFiles.append(smellyFile)
            SmellyFile[smellName]=(smellyFiles)
    return SmellyFile

def create_folder(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print('create new folder')
    else:
        print('folder is already exist')

def write_to_csv(datalist ,target_file):
    with open(target_file, 'w') as csvfile:
        fieldnames = ['AntiSingleton', 'Blob','ClassDataShouldBePrivate','ComplexClass','LargeClass','LazyClass','LongMethod','LongParameterList','MessageChains','RefusedParentBequest','SpaghettiCode','SpeculativeGenerality','SwissArmyKnife']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        for data in datalist:
            writer.writerow(data)

def get_project_versions(json_name):
    with open(json_name) as file:
        versions = json.load(file)
    return versions

if __name__ == "__main__":
    project_name = 'spring-security'
    code_version = 'code_version1'
    root = '/data01/ymz/code_smell/jiangjunpeng/' 

    # versions = get_project_versions('E:\Repository\Author_and_Smell\\' + project_name + '\\' + project_name + '.json')
    versions = get_project_versions(root + code_version + '/' + project_name + '/' + project_name + '.json')

    for version in versions :
        print(version)
        Main_Path = Scan_Version(root + code_version + '/' + project_name + '/' + version['name'])
        #print(type(Main_Path))
        All_Smelly_Files = {}
        All_Smelly_Files['AntiSingleton'] = []
        All_Smelly_Files['Blob'] = []
        All_Smelly_Files['ClassDataShouldBePrivate'] = []
        All_Smelly_Files['ComplexClass'] = []
        All_Smelly_Files['LargeClass'] = []
        All_Smelly_Files['LazyClass'] = []
        All_Smelly_Files['LongMethod'] = []
        All_Smelly_Files['LongParameterList'] = []
        All_Smelly_Files['MessageChains'] = []
        All_Smelly_Files['RefusedParentBequest'] = []
        All_Smelly_Files['SpaghettiCode'] = []
        All_Smelly_Files['SpeculativeGenerality'] = []
        All_Smelly_Files['SwissArmyKnife'] = []
        print(All_Smelly_Files)
        for path in Main_Path:
            print("===================================")
            subprocess.call('java -jar '+ root + code_version + '/' + 'smellspace/SmellMining/SmellMining_fat1.jar ' + str(path) , shell=True)
            # print('java -jar E:\Repository\smellspace\SmellMining\SmellMining_fat1.jar ' + str(path))
            smellyFile = ini_to_list(root + code_version + '/smellspace/Temp/')
            print(smellyFile)
            All_Smelly_Files['AntiSingleton'].extend(smellyFile['AntiSingleton'])
            All_Smelly_Files['Blob'].extend(smellyFile['Blob'])
            All_Smelly_Files['ClassDataShouldBePrivate'].extend(smellyFile['ClassDataShouldBePrivate'])
            All_Smelly_Files['ComplexClass'].extend(smellyFile['ComplexClass'])
            All_Smelly_Files['LargeClass'].extend(smellyFile['LargeClass'])
            All_Smelly_Files['LazyClass'].extend(smellyFile['LazyClass'])
            All_Smelly_Files['LongMethod'].extend(smellyFile['LongMethod'])
            All_Smelly_Files['LongParameterList'].extend(smellyFile['LongParameterList'])
            All_Smelly_Files['MessageChains'].extend(smellyFile['MessageChains'])
            All_Smelly_Files['RefusedParentBequest'].extend(smellyFile['RefusedParentBequest'])
            All_Smelly_Files['SpaghettiCode'].extend(smellyFile['SpaghettiCode'])
            All_Smelly_Files['SpeculativeGenerality'].extend(smellyFile['SpeculativeGenerality'])
            All_Smelly_Files['SwissArmyKnife'].extend(smellyFile['SwissArmyKnife'])

        save_path = version['name']
        #save_path = path[save_index:].replace('\\','.')
        print(save_path)
        #print(folder + '\\' + save_path + '.xlsx')
        print(All_Smelly_Files)

        file = xlwt.Workbook()
        sheet = file.add_sheet('sheet1')
        keys = All_Smelly_Files.keys()
        i = 1
        j = 0
        for key in keys:
            i=1
            sheet.write(0,j,key)
            if len(All_Smelly_Files[key]) == 0:
                sheet.write(1, j, 'null')
            else:
                for s in All_Smelly_Files[key]:
                    sheet.write(i, j, s)
                    i = i + 1
            j += 1
        if not os.path.exists(root + code_version + '/' + project_name + '/smellyFile/' + save_path + '.xlsx'):
            f1 = open(root + code_version + '/' + project_name + '/smellyFile/' + save_path + '.xlsx', 'w')
        file.save(root + code_version + '/' + project_name + '/smellyFile/' + save_path + '.xlsx')
        print('finished...')
        #write_to_csv(All_Smelly_Files ,'E:\Repository\smellspace\Temp\spring-framework\\' + save_path + '.csv')
