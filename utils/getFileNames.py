# -*- encoding: utf-8 -*-

import os

def getFileNames():
    dir_list = ['/home/yhl2/workspace/xtp_test/Autocase_Result/Quote18']
    name_list = ['redemption_ha_qw']
    for index,dir in enumerate(dir_list):
        file_list = os.listdir(dir)
        file_list.sort()
        name_file_dir = '/home/yhl2/workspace/xtp_test/Autocase_Result/Quote18/run.sh'
        for file in file_list:
            if file.endswith('.py') and file != '__init__.py':
                file_index = file.endswith('.py')
                file_num = file[file_index-3:file_index]
                with open(name_file_dir,'a') as f:
                    if file_num != -1:
                        f.write('python ' + file)
                        f.write("\n")

getFileNames()