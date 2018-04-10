#!/usr/bin/env python  
# -*- coding:utf-8 -*- 

""" 
@version: v1.0 
@author: Harp
@contact: liutao25@baidu.com 
@software: PyCharm 
@file: better_print.py 
@time: 2018/4/8 0008 22:27 
"""

from prettytable import PrettyTable
from colorama import Fore, init
# import sys

init()
# print = sys.stdout.write


def print_info(doc):
    print()
    print(' ------- ' + Fore.CYAN + 'BeiJing Real Bus' + Fore.RESET + ' -------')
    print('|                                |')
    print('|      Author: Harpsichord       |')
    print('|   Contact: ' + Fore.BLUE + 'liutao25@baidu.com' + Fore.RESET + '  |')
    print(' --------------------------------')
    print(doc)


def print_direction_and_station(data0, data1, time0, time1):
    pt = PrettyTable()
    pt.field_names = ['#0', 'UP:' + time0, 'Bus0', '   ', '#1', 'DOWN:' + time1, 'Bus1']
    for i in range(max(len(data0), len(data1))):
        if i >= len(data0):
            r0 = [' '] * 3
        else:
            r0 = data0[i]
            if r0[2] == 'B':
                r0[1] = Fore.RED + r0[1]
                r0[2] = r0[2] + Fore.RESET
        if i >= len(data1):
            r1 = [' '] * 3
        else:
            r1 = data1[i]
            if r1[2] == 'B':
                r1[1] = Fore.RED + r1[1]
                r1[2] = r1[2] + Fore.RESET
        pt.add_row(r0 + ['   '] + r1)
    print(pt)


if __name__ == "__main__":
    pass
