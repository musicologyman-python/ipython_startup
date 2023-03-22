#!/bin/bash

STARTUP_FILE=~/.ipython/profile_default/startup/startup.py 

if [ -e $STARTUP_FILE ]
then
  rm $STARTUP_FILE
fi

