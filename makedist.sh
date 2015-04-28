#!/bin/bash
#make tar
if  ! [ -d dist ]; then
 mkdir ./dist
fi
if [ -f ./dist/bvccli.tar ]; then
 rm ./dist/bvccli.tar
fi
tar -cf bvccli.tar bvccli/ setup.py  -C ./dist
