#!/usr/bin/python2
# -*- coding:utf-8 -*-

import os

rootDir = os.getcwd() + '/docs'

def buildHomepage():
    f = open(rootDir + '/homepage.md', 'w')
    dirList = [''] * 13
    dirs = os.listdir(rootDir)
    for dir in dirs:
        dirPath = rootDir + '/' + dir
        if os.path.isdir(dirPath):
            # print dirPath
            if dir.find('-') > -1:
                pair = dir.split('-', 1)
                # print pair[0]
                dirList[int(pair[0]) - 1] = pair[1]

    for index, dir in enumerate(dirList):
        dirName = str(index + 1) + '-' + dir
        writeLine(f, '#### ' + str(index + 1) + '. ' + dir)
        mds = os.listdir(rootDir + '/' + dirName)
        writeLine(f, '')
        for md in mds:
            if md.find('.') > -1:
                pair = md.split('.', 1)
                writeLine(f, '* ' + '[' + pair[0] + '](' + dirName + '/' + md + ')')
        writeLine(f, '')

def writeLine(f, line):
    f.write(line + '\n')

def main():
    buildHomepage()

main()
