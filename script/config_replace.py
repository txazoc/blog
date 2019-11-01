#!/usr/bin/python2
# -*- coding:utf-8 -*-

import os
import sys

configFile = os.getcwd() + '/docs/_coverpage.md'

def replace(localDebug):
    f = open(configFile, 'r')
    lines = f.readlines()
    f.close()

    f = open(configFile, 'w')
    for line in lines:
        if line.find('开始阅读') > -1:
            if localDebug == 'false':
                f.write('<a href="http://www.txazo.com/blog/#/homepage">开始阅读</a>')
            else:
                f.write('<a href="http://localhost:3000/#/homepage">开始阅读</a>')
        else:
            f.write(line)
    f.close()

def main(localDebug):
    print '--------------------------------------------------'
    print '[python] replace config begin.'
    replace(localDebug)
    print '[python] replace config success.'
    print '--------------------------------------------------'

if __name__ == '__main__':
    localDebug = 'false'
    if len(sys.argv) > 1 and sys.argv[1] == 'true':
        localDebug = 'true'
    main(localDebug)
