#!/usr/bin/python2
# -*- coding:utf-8 -*-

import os

sourceDir = os.getcwd() + '/_docs'
destDir = os.getcwd() + '/docs'

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

def buildHomepage():
    f = open(destDir + '/homepage.md', 'w')
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
        writeLine(f, '#### ' + str(index + 1) + '. ' + module.moduleName)
        mds = os.listdir(module.srcPath)
        module.mds = [''] * len(mds)
        writeLine(f, '')
        for i, md in enumerate(mds):
            if md.find('.') > -1:
                pair = md.split('.', 1)
                module.mds[i] = Md(module.srcPath + '/' + md, module.destPath + '/' + md, md, pair[0], module)
                writeLine(f, '* ' + '[' + pair[0] + '](' + module.fileName + '/' + md + ')')
        writeLine(f, '')

    for moduleIndex, module in enumerate(modules):
        if not os.path.exists(module.destPath):
            os.mkdir(module.destPath)
        for mdIndex, md in enumerate(module.mds):
            prevMd = getPrevMd(moduleIndex, mdIndex, module.mds, modules)
            nextMd = getNextMd(moduleIndex, mdIndex, module.mds, modules)
            copyAndRewrite(md.srcPath, md.destPath, prevMd, nextMd)

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
        f.write(line)

    writeLine(f, '')
    if prevMd != '':
        writeLine(f, '')
        writeLine(f, '[上一篇 ' + prevMd.mdName + '](' + prevMd.module.fileName + '/' + prevMd.fileName + ')')
    if nextMd != '':
        writeLine(f, '')
        writeLine(f, '[下一篇 ' + nextMd.mdName + '](' + nextMd.module.fileName + '/' + nextMd.fileName + ')')

def writeLine(f, line):
    f.write(line + '\n')

def main():
    print '--------------------------------------------------'
    print '[python] build homepage begin.'
    buildHomepage()
    print '[python] build homepage end.'
    print '--------------------------------------------------'

main()
