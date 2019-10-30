#!/bin/bash

# git pull origin master

python2 script/homepage.py

git add .
git commit -am 'auto commit'
git push origin master
