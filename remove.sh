#!/bin/bash
rm -rf /home/pi/Documents/*
cd /home/pi/Documents
git clone git@github.com:pavelmaks/JagerMachine.git
cd JagerMachine
mv * ../
rmdir JagerMachine


