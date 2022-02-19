import os
import csv
import subprocess
import json
import xlwt
import re


# 统计文件夹下所有的java文件数量
def count_files(path: str):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.java'):
                count += 1
    return count

# def check_style(path: str, output_path: str):
#     subprocess.call('java -jar checkstylex.x.x -o ' + output_path + ' ' + path)


# 过滤任务
def filt(path: str):
    print('开始执行任务...')
    # 根据目录寻找所有目录，删除所有非Java文件，把所有Java文件放到该目录下
    for root, dirs, files in os.walk(path):
        for file in files:
            # print(os.path.join(root, file), file)
            if not file.endswith('.java'):
                os.remove(os.path.join(root, file))
            # else:
            #     check_style(os.path.join(root, file))   # 检查编写规范
    print('完成删除任务...')
    print('剩余文件: ')
    # for root, dirs, files in os.walk(path):
    #     for file in files:
    #         if file.endswith('.java') or file.endswith('.class'):
    #             print(os.path.join(file))


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

# def ini_to_list(ini_path):
#     startStr = 'org'
#     SmellyFile = {}
#     for filename in os.listdir(ini_path):
#         if filename.endswith('.ini'):
#             smellName = filename[:-4]
#             smellyFiles = []
#             with open(ini_path + filename) as f:
#                 for line in f:
#                     if startStr in line:
#                         index = line.index(startStr)
#                         smellyFile = line[index:-1]
#                         #if (not smellyFile.endswith('Test') and not smellyFile.endswith('TestCase')):
#                         if ('test' not in smellyFile.lower()):
#                             smellyFiles.append(smellyFile)
#             SmellyFile[smellName]=(smellyFiles)
#     return SmellyFile
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

# def get_project_versions(json_name):
#     with open(json_name) as file:
#         versions = json.load(file)
#     return versions

def get_project_names(root):
    return os.listdir(root)


if __name__ == "__main__":
    root = '/data01/ymz/ex/data_sets/'     # 数据集的路径

    # versions = get_project_versions('E:\Repository\Author_and_Smell\\' + project_name + '\\' + project_name + '.json')
    # versions = get_project_versions(root + '/' + project_name + '/' + project_name + '.json')
    # 获取企业名称
    enterprice_names = get_project_names(root)
    for enterprice_name in enterprice_names:

        # 获取项目名称
        project_names = get_project_names(root+ enterprice_name +'/') # 数据集下每个项目的文件名
        print(project_names)

        for name in project_names:  # 每一个项目分别求坏味

            if 'smellyFile' in name:    
                continue

            print(name)
            filt_path = root+enterprice_name+'/'+name
            filt(filt_path) # 过滤非java文件
            count = count_files(filt_path)

            All_Smelly_Files = {}   # 坏味共十三种，value是产生坏味的文件
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

            # 避免Test文件
            pahts = Scan_Version(filt_path)
            for path in pahts:
                print("===========================================================================================")
                subprocess.call('java -jar /data01/ymz/ex/smellspace/SmellMining/SmellMining_fat1.jar ' + str(path) , shell=True)   # 调用DECOR

                smellyFile = ini_to_list('/data01/ymz/ex/smellspace/Temp/')
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

            save_path = name
            print(save_path)
            print(All_Smelly_Files)

            file = xlwt.Workbook()
            sheet = file.add_sheet('sheet1')
            keys = All_Smelly_Files.keys()
            i = 1
            j = 0
            # for key in keys:
            #     i = 1
            #     sheet.write(0, j, key)
            #     if len(All_Smelly_Files[key]) == 0:
            #         sheet.write(1, j, 'null')
            #     else:
            #         for s in All_Smelly_Files[key]:
            #             sheet.write(i, j, s)
            #             i = i + 1
            #     j += 1
                
            for key in keys:
                i = 1
                sheet.write(j, 0, key)
                sheet.write(j, 1, len(All_Smelly_Files[key])) # 每个文件
                sheet.write(j, 2, len(All_Smelly_Files[key])/count) # 每个文件
                j += 1

            sheet.write(j+1, 0, '文件总数')
            sheet.write(j+1, 1, count)


            if not os.path.exists('/data01/ymz/ex/smellyFile/' + enterprice_name +'/' + save_path + '.xlsx'):
                f1 = open('/data01/ymz/ex/smellyFile/' + enterprice_name +'/' + save_path + '.xlsx', 'w')
            file.save('/data01/ymz/ex/smellyFile/' + enterprice_name +'/' + save_path + '.xlsx')
            print('finished...')
            print()
        
    print('all finished')
