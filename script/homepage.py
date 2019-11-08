#!/usr/bin/python2
# -*- coding:utf-8 -*-

import os
import sys
import re
import shutil

sourceDir = os.getcwd() + '/_docs'
destDir = os.getcwd() + '/docs'
encoding = sys.getfilesystemencoding()
regex_image = '!\[(.*)\]\((.*)\)\((.*)\)'

class Module:
    def __init__(self, srcPath, destPath, fileName, moduleName):
        self.srcPath = srcPath
        self.destPath = destPath
        self.fileName = fileName
        self.moduleName = moduleName

class Md:
    def __init__(self, srcPath, destPath, fileName, mdName, module):
        self.srcPath = srcPath
        self.destPath = destPath
        self.fileName = fileName
        self.mdName = mdName
        self.module = module

def buildHomepage(localDebug):
    f = open((sourceDir if localDebug == 'true' else destDir) + '/homepage.md', 'w')
    modules = [''] * 13
    dirs = os.listdir(sourceDir)
    for dir in dirs:
        srcPath = sourceDir + '/' + dir
        destPath = destDir + '/' + dir
        if os.path.isdir(srcPath):
            if dir.find('-') > -1:
                pair = dir.split('-', 1)
                modules[int(pair[0]) - 1] = Module(srcPath, destPath, dir, pair[1])

    for index, module in enumerate(modules):
        writeLine(f, '#### ' + str(index + 1) + '. ' + encode(module.moduleName))
        mds = os.listdir(module.srcPath)
        module.mds = [''] * len(mds)
        writeLine(f, '')
        for i, md in enumerate(mds):
            if md.find('.') > -1:
                pair = md.split('.', 1)
                module.mds[i] = Md(module.srcPath + '/' + md, module.destPath + '/' + md, md, pair[0], module)
                writeLine(f, '* ' + '[' + encode(pair[0]) + '](' + encode(module.fileName) + '/' + encode(md) + ')')
        writeLine(f, '')

    if localDebug == 'true':
        return

    for moduleIndex, module in enumerate(modules):
        if not os.path.exists(module.destPath):
            os.mkdir(module.destPath)
        for mdIndex, md in enumerate(module.mds):
            prevMd = getPrevMd(moduleIndex, mdIndex, module.mds, modules)
            nextMd = getNextMd(moduleIndex, mdIndex, module.mds, modules)
            copyAndRewrite(md.srcPath, md.destPath, prevMd, nextMd)

    print '[python] copy media begin.'
    copyMedia(sourceDir + '/_media', destDir + '/_media')
    print '[python] copy media begin.'

def copyMedia(sourcePath, destPath):
    childs = os.listdir(sourcePath)
    for child in childs:
        childPath = sourcePath + '/' +child
        if os.path.isdir(childPath):
            copyMedia(childPath, destPath + '/' +child)
        else:
            copyMediaImage(sourcePath, destPath, child)

def copyMediaImage(sourcePath, destPath, image):
    if not os.path.exists(destPath):
        os.mkdir(destPath)
    shutil.copy(sourcePath + '/' + image, destPath + '/' + image)

def getPrevMd(moduleIndex, mdIndex, mds, modules):
    if moduleIndex == 0 and mdIndex == 0:
        return ''
    elif mdIndex == 0:
        module = modules[moduleIndex - 1]
        return module.mds[len(module.mds) - 1]
    else:
        return mds[mdIndex - 1]

def getNextMd(moduleIndex, mdIndex, mds, modules):
    if moduleIndex == len(modules) - 1 and mdIndex == len(mds) - 1:
        return ''
    elif mdIndex == len(mds) - 1:
        module = modules[moduleIndex + 1]
        return module.mds[0]
    else:
        return mds[mdIndex + 1]

def copyAndRewrite(srcFile, destFile, prevMd, nextMd):
    f = open(destFile, 'w')
    for line in open(srcFile, 'r'):
        match = re.match(regex_image, line)
        if match:
            rewriteMdImage(f, match)
        else:
            f.write(line)

    writeLine(f, '')
    if prevMd != '':
        writeLine(f, '')
        writeLine(f, '[<< 上一篇: ' + encode(prevMd.mdName) + '](' + encode(prevMd.module.fileName) + '/' + encode(
                prevMd.fileName) + ')')
    if nextMd != '':
        writeLine(f, '')
        writeLine(f, '[>> 下一篇: ' + encode(nextMd.mdName) + '](' + encode(nextMd.module.fileName) + '/' + encode(
                nextMd.fileName) + ')')

def rewriteMdImage(f, match):
    uri = match.group(2)
    if uri.find('_media') > -1:
        uri = uri[uri.find('_media'):]
    f.write('<p style="text-align: center;"><img src="' + uri + '" alt="' + match.group(1) + '" style="width: ' + match.group(3) + '"></p>\n')

def writeLine(f, line):
    f.write(line + '\n')

def encode(str):
    return str.decode(encoding).encode('utf-8')

def main(localDebug):
    print '--------------------------------------------------'
    print '[python] build homepage begin.'
    buildHomepage(localDebug)
    print '[python] build homepage end.'
    print '--------------------------------------------------'

if __name__ == '__main__':
    localDebug = 'false'
    if len(sys.argv) > 1 and sys.argv[1] == 'true':
        localDebug = 'true'
    main(localDebug)
