#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import json
import sys
if sys.version_info[0] < 3:
    path = raw_input('Enter your folder path: ').decode('utf-8')
else:
    path = input('Enter your folder path: ')
cwd = os.getcwd()
oldfile = None
deleted = []
created = []
if not os.path.isabs(path):
    path = os.path.abspath(path)+'/'
jsonfile = os.path.basename(os.path.dirname(path))+'.json'
if sys.version_info[0] < 3:
    if jsonfile in os.listdir(os.getcwd().decode('utf-8')):
        with open(jsonfile) as file:
            oldfile = json.load(file)
    pathlist = repr([x.encode(sys.stdout.encoding) for x in os.listdir(path)]).decode('string-escape')
    cwdlist = repr([x.encode(sys.stdout.encoding) for x in os.listdir(os.getcwd().decode('utf-8'))]).decode('string-escape')
else:
    if jsonfile in os.listdir(os.getcwd()):
        with open(jsonfile) as file:
            oldfile = json.load(file)
with open(jsonfile, 'w') as file:
    json.dump(os.listdir(path), file)
if oldfile is not None:
    for d in oldfile:
        if d not in oldfile:
            deleted.append(d)
        if d in oldfile:
            created.append(d)
    if sys.version_info[0] < 3:
        deleted = repr([x.encode(sys.stdout.encoding) for x in deleted]).decode('string-escape')
        created = repr([x.encode(sys.stdout.encoding) for x in created]).decode('string-escape')
    print('Deleted files from last request: ')
    print(deleted)
    print('Files created again: ')
    print(created)
if sys.version_info[0] < 3:
    pathlist = repr([x.encode(sys.stdout.encoding) for x in os.listdir(path)]).decode('string-escape')
    cwdlist = repr([x.encode(sys.stdout.encoding) for x in os.listdir(os.getcwd().decode('utf-8'))]).decode(
        'string-escape')
else:
    pathlist = os.listdir(path)
    cwdlist = os.listdir(os.getcwd())
if oldfile is None:
    print('Folder never registered before, therefore it was created now')
print('File data: ')
print(pathlist)
print('Json file named after last folder: {} of the request: {} '
      'is present'.format(jsonfile, path))
print('As can be seen in the script folder files list:')
print(cwdlist)
