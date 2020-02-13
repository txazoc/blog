#!/bin/bash

python2 script/homepage.py
# python2 script/homepage.py true
# python2 script/config_replace.py true

open -g http://localhost:3000/#/homepage

docsify serve docs
