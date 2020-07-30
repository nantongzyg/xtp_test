# -*- coding:UTF-8 -*-
__author__ = "Snow"
import os

def traverseFiles(file_dir):
    L=[]
    for root,dirs,files in os.walk(file_dir):
        for file in files:
            if file.startswith("YW_"):
                L.append(os.path.join(root, file))
    return L

def replaceErrMsg(file_name):
    try:
        with open(file_name) as fp:
            lines = []
            # errmsg_num = 0
            # num = 0
            for one in fp:
                # num +=1
                if one.strip().startswith("'errorID'"):
                    errid= one.split(':')[1].split(',')[0].strip()
                    lines.append(one)
                    # errmsg_num = num
                elif one.strip().startswith("'errorMSG'") and errid != '0':
                    ori_str = one.split(':')[1].split(',')[0].strip()
                    if "\"'\" " + "+" + " queryOrderErrorMsg(" + errid + ") +" + " \"'\"" == ori_str:
                        rep_str = "queryOrderErrorMsg(" + errid + ")"
                        lines.append(one.replace(ori_str, rep_str))
                elif one.strip().startswith("case_goal['errorID']"):
                    case_errid= one.split('=')[1].strip()
                    lines.append(one)
                    # errmsg_num = num
                elif one.strip().startswith("case_goal['errorMSG']") and case_errid != '0':
                    ori_str = one.split('=')[1].strip()
                    if "\"'\" " + "+" + " queryOrderErrorMsg(" + case_errid + ") +" + " \"'\""==ori_str:
                        rep_str="queryOrderErrorMsg("+ case_errid + ")"
                        lines.append(one.replace(ori_str, rep_str))
                else:
                    lines.append(one)

            content = ''.join(tuple(lines))
        with open(file_name,'w') as fp:
            fp.write(content)
    except Exception as e:
        print e

if __name__ == '__main__':

    fileList = traverseFiles("/home/yhl2/workspace/xtp_test/autocase_by_hand")
    for file in fileList:
        replaceErrMsg(file)

    # replaceErrMsg("YW_ETFMM_SZXJ_109_K.py")

