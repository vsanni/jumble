#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 18:23:32 2018

@author: vsanni
"""

import argparse
from jumble.text_manipulation import Camel2snake, tag_find_chunks, read_text_file

Parser = argparse.ArgumentParser()

Parser.add_argument("filename", type = str, help="input filename" )

try   : Args = Parser.parse_args()
except: Parser.exit(1)

s = read_text_file(Args.filename)

N0, N1, StringFlag = tag_find_chunks(s)

for n0, n1, sFlag in zip(N0, N1,StringFlag):
    if sFlag: print(s[n0:n1], end ="")
    else    : print(Camel2snake(s[n0:n1]), end="")
