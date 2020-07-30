#!/usr/bin/python
# -*- encoding: utf-8 -*-

def getUserInfo():
    file = 'offer.log.20170526'
    userinfo = open('userinfo.txt','w')
    with open(file,'r') as f:
        for line in f.readlines():
            index = line.find('user_info')
            user_info = line[index:index+19]
            if user_info != '':
                userinfo.write(user_info)
                userinfo.write('\n')
    userinfo.close()

if __name__ == '__main__':
    getUserInfo()