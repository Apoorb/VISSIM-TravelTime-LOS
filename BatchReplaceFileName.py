# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 15:08:22 2018

@author: A-Bibeka
"""

import os
import shutil
import re

print('Current working directory ',os.getcwd())
os.chdir('D:/Dropbox/TTI_Projects/Road User Cost/VISSIM PM Peak V14/SB/SB 2025') 
print('Current working directory ',os.getcwd())
# Replace _ to - in a file name 
#[os.rename(f, f.replace('_', '-')) for f in os.listdir('.') if not f.startswith('.')]
# Replace the year from 2045 to 2025
[os.rename(f, f.replace('2045', '2025')) for f in os.listdir('.') if not f.startswith('.')]

#######################################################################################
#Copying files to a folder
path ="C:/Users/a-bibeka/Dropbox/TTI_Projects/Road User Cost/VISSIM PM Peak V10/NB/"
OriginPath =os.path.join(path,'NB 2045')
DestinPath=os.path.join(path,'NB 2025')
files= os.listdir(OriginPath)
files1 = [file for file in files if re.search(r'2045',file, re.I|re.M)]
files
len(files1)
#With rbc files 
#files1 = [file for file in files if re.search(r'Base|.rbc',file, re.I|re.M)]

for f in files1:
    shutil.copy(os.path.join(OriginPath,f), DestinPath)
    

################################################################################
# Deleting files
for f in files1:
    os.remove(os.path.join(DestinPath,f))