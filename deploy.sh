#!/bin/bash

STARTUP_FILE=~/.ipython/profile_default/startup/startup.py 

if [ -e $STARTUP_FILE ]
then
  exit
fi

ln $(pwd)/startup.py $STARTUP_FILE
