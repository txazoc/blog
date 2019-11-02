#!/bin/bash

python2 script/homepage.py true
python2 script/config_replace.py true

# open -g http://127.0.0.1:3000

docsify serve _docs
