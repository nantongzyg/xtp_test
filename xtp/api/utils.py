#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
from attribute import Attribute


def dump(obj, nested_level=0, output=sys.stdout):
    spacing = '   '
    if type(obj) == dict:
        print >> output, '%s{' % (nested_level * spacing)
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print >> output, '%s%s:' % ((nested_level + 1) * spacing, k)
                dump(v, nested_level + 1, output)
            else:
                print >> output, '%s%s: %s' % ((nested_level + 1) * spacing, k, v)
        print >> output, '%s}' % (nested_level * spacing)
    elif type(obj) == list:
        print >> output, '%s[' % (nested_level * spacing)
        for v in obj:
            if hasattr(v, '__iter__'):
                dump(v, nested_level + 1, output)
            else:
                print >> output, '%s%s' % ((nested_level + 1) * spacing, v)
        print >> output, '%s]' % (nested_level * spacing)
    else:
        print >> output, '%s%s' % (nested_level * spacing, obj)


def pretty_data(data):
    ret = Attribute()
    ret['data'] = {}
    for k in data:
        if type(data[k]) is dict:
            rows = data[k]
            if rows != {}:
                for p in rows:
                    item = rows[p]
                    if type(item) is dict:
                        for m in item:
                            if m == 'error_info':
                                ret['error'] = item[m]
                            elif m == k:
                                if 'ticker' in item[m]:
                                    ret['data'][item[m]['ticker']] = item
                            else:
                                ret['data'][p] = item[m]
                    else:
                        ret['data'][p] = rows[p]
        else:
            ret['data'][k] = data[k]

    return ret

def pretty_data_list(data):
    ret = []
    for k in data:
        if type(data[k]) is dict:
            rows = data[k]
            if rows != {}:
                for p in rows:
                    item = rows[p]
                    if type(item) is dict:
                        for m in item:
                            ret_temp = {}
                            if m == 'error_info':
                                ret_temp['error'] = item[m]
                            elif m == k:
                                if 'ticker' in item[m]:
                                    ret_temp[item[m]['ticker']] = item
                            else:
                                ret_temp[p] = item[m]

                            ret.append(ret_temp)
                    else:
                        ret_temp = {}
                        ret_temp[p] = rows[p]
                        ret.append(ret_temp)
        else:
            ret_temp = {}
            ret_temp[k] = data[k]

    return ret