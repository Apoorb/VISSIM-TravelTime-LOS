# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 10:09:49 2019

@author: A-Bibeka
Read data from link segment evaluation
"""

import os
import pandas as pd
import numpy as np
import glob



os.chdir("D:/Dropbox/TTI_Projects/Road User Cost")
os.getcwd()
########################################################################################################################
# Get results directory
ListFiles=glob.glob("D:/Dropbox/TTI_Projects/Road User Cost/VISSIM AM Peak V14/NB/NB 2025/*Link Segment Results.att")
Lfs2=glob.glob("D:/Dropbox/TTI_Projects/Road User Cost/VISSIM PM Peak V14/NB/NB 2025/*Link Segment Results.att")

ListFiles=ListFiles+Lfs2
file_Fu = ListFiles[0]
#file = "AM 2045 NB Base_Vehicle Travel Time Results.att"

Findat= pd.DataFrame()
for file_Fu in ListFiles:
    file=file_Fu.split("\\")[1]
    desc1= file[0:10]
    Time,Year, Dir=desc1.split(" ")
    Sen=file[11:].split("_Link Segment Results.att")[0]
    Sen=Sen.split(" Cor2")[0]
    dat=pd.read_csv(file_Fu,sep =';',skiprows=54)
    dat= dat.loc[:,['$LINKEVALSEGMENTEVALUATION:SIMRUN',"LINKEVALSEGMENT","DENSITY(ALL)"]]
    dat= dat.rename(index=str,columns={'$LINKEVALSEGMENTEVALUATION:SIMRUN':"SimRun","DENSITY(ALL)":"Density","LINKEVALSEGMENT":"LinkEvlSeg"})
    mask=dat["SimRun"]=="AVG"
    dat = dat[mask]
    dat["Sen"] = Sen
    dat["Time"]= Time
    dat["Year"] = np.int(Year)
    dat["Dir"]= Dir
    Findat=Findat.append(dat)




RdFl1= os.path.join("D:/Dropbox/TTI_Projects/Road User Cost","NB_LinkEvalDat.csv")
Findat.to_csv(RdFl1,index=False)

########################################################################################################################
# SB Data Processing
ListFiles=glob.glob("D:/Dropbox/TTI_Projects/Road User Cost/VISSIM AM Peak V14/SB/SB 2025/*Link Segment Results.att")
Lfs2=glob.glob("D:/Dropbox/TTI_Projects/Road User Cost/VISSIM PM Peak V14/SB/SB 2025/*Link Segment Results.att")

ListFiles=ListFiles+Lfs2
file_Fu = ListFiles[0]
#file = "AM 2045 NB Base_Vehicle Travel Time Results.att"

Findat= pd.DataFrame()
for file_Fu in ListFiles:
    file=file_Fu.split("\\")[1]
    desc1= file[0:10]
    Time,Year, Dir=desc1.split(" ")
    Sen=file[11:].split("_Link Segment Results.att")[0]
    Sen=Sen.split(" Cor2")[0]
    dat=pd.read_csv(file_Fu,sep =';',skiprows=54)
    dat= dat.loc[:,['$LINKEVALSEGMENTEVALUATION:SIMRUN',"LINKEVALSEGMENT","DENSITY(ALL)"]]
    dat= dat.rename(index=str,columns={'$LINKEVALSEGMENTEVALUATION:SIMRUN':"SimRun","DENSITY(ALL)":"Density","LINKEVALSEGMENT":"LinkEvlSeg"})
    mask=dat["SimRun"]=="AVG"
    dat = dat[mask]
    dat["Sen"] = Sen
    dat["Time"]= Time
    dat["Year"] = np.int(Year)
    dat["Dir"]= Dir
    Findat=Findat.append(dat)


RdFl1= os.path.join("D:/Dropbox/TTI_Projects/Road User Cost","SB_LinkEvalDat.csv")
Findat.to_csv(RdFl1,index=False)
