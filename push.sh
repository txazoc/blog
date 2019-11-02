#!/bin/bash

# git pull origin master

python2 script/homepage.py
# python2 script/config_replace.py

git add .
git commit -am 'auto commit'
git push origin master
