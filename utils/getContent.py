# -*- encoding: utf-8 -*-

filename = raw_input("Enter file name:")
fobj = open(filename)
for eachline in fobj:
    print eachline,
fobj.close()