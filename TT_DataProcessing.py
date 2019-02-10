# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 10:09:49 2019

@author: A-Bibeka
Read data from travel time files
"""

import os
import pandas as pd
import numpy as np
import glob
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import datetime

os.chdir("D:/Dropbox/TTI_Projects/Road User Cost")
os.getcwd()
########################################################################################################################
# Get results directory
ListFiles=glob.glob('D:/Dropbox/TTI_Projects/Road User Cost/VISSIM AM Peak V14/NB/NB 2045/*Vehicle Travel Time Results.att')
Lfs2=glob.glob("D:/Dropbox/TTI_Projects/Road User Cost/VISSIM PM Peak V14/NB/NB 2045/*Vehicle Travel Time Results.att")
Lfs3=glob.glob("D:/Dropbox/TTI_Projects/Road User Cost/VISSIM AM Peak V14/NB/NB 2025/*Vehicle Travel Time Results.att")
Lfs4=glob.glob("D:/Dropbox/TTI_Projects/Road User Cost/VISSIM PM Peak V14/NB/NB 2025/*Vehicle Travel Time Results.att")

ListFiles=ListFiles+Lfs2+Lfs3+Lfs4
#file = ListFiles[1]
#file = "AM 2045 NB Base_Vehicle Travel Time Results.att"
def TTSegName(x):
    if(x==1):Nm="69_SB"
    elif(x==2):Nm="69_NB"
    elif(x==3):Nm="Spur_SB"
    else:Nm="Spur_NB"
    return Nm
Findat= pd.DataFrame()
for file_Fu in ListFiles:
    file=file_Fu.split("\\")[1]
    desc1= file[0:10]
    Time,Year, SenDir=desc1.split(" ")
    Scenario=file[11:].split("_Vehicle Travel Time Results.att")[0]
    Scenario=Scenario.split(" Cor2")[0]
    dat=pd.read_csv(file_Fu,sep =';',skiprows=17)
    mask=dat["$VEHICLETRAVELTIMEMEASUREMENTEVALUATION:SIMRUN"]=="AVG"
    dat["TTSegNm"]=dat['VEHICLETRAVELTIMEMEASUREMENT'].apply(TTSegName)
    mask2=(dat["TTSegNm"]=="69_NB")|(dat["TTSegNm"]=="Spur_NB")
    dat = dat[mask & mask2]
    dat
    dat["Scenario"] = Scenario
    dat["Time"]= Time
    dat["Year"] = np.int(Year)
    dat["SenDir"]= SenDir
    Findat=Findat.append(dat)
    Findat["Delay"]= Findat["VEHS(ALL)"]*(Findat["TRAVTM(ALL)"]-(Findat["DISTTRAV(ALL)"]/(1.47*65)))/3600
    Findat["Delay"]=np.round( Findat["Delay"])
Findat["SMS"] =np.round(Findat["DISTTRAV(ALL)"]/Findat["TRAVTM(ALL)"]/1.47,1)



RdFl1= os.path.join("D:/Dropbox/TTI_Projects/Road User Cost","InpVolKey.csv")
InputVolDat=pd.read_csv(RdFl1)
InputVolDat=InputVolDat.drop("Scenario2",axis=1)
Findat=Findat.merge(InputVolDat,how='inner',on=["Scenario","Year","Time","TTSegNm"])
Findat["LatentDelay"]=(Findat["InpVol"]-Findat["VEHS(ALL)"])*(Findat["TRAVTM(ALL)"]-(Findat["DISTTRAV(ALL)"]/(1.47*65)))/3600
Findat["LatentDelay"]=np.round(Findat["LatentDelay"],1)
Findat["TotalDelay"] = np.round(Findat["Delay"]+Findat["LatentDelay"],1)
Findat["Sen"]=Findat["Scenario"].apply(lambda x: str.split(x,"_")[0])
Findat["LaneDrLoc"]=Findat["Scenario"].apply(lambda x: str.split(x," ")[-1])
Findat["LaneDrLoc"]=Findat["LaneDrLoc"].apply(lambda x: "L" if x=="Ln" else x)
########################################################################################################################
Findat_NB_69= Findat[Findat["TTSegNm"]=="69_NB"]
Findat_NB_Spur= Findat[Findat["TTSegNm"]=="Spur_NB"]

# SB IH 69 Plots
def NB_plots(x1="Sen",y1="SMS",ylim1=(0,65),xlab="",ylab="IH 69 NB Average Speed in 2025",title_AB="IH 69 NB Average Speed in 2025",data1=Findat_NB_69[Findat_NB_69["Year"]==2025],saveNm="NB69_2025.png"):
    sns.set(style="whitegrid", color_codes=True)
    sns.palplot(sns.color_palette("Greys"))
    AB_palette= ["white",sns.xkcd_rgb["cool grey"],sns.xkcd_rgb["charcoal grey"]]
    g=sns.catplot(x=x1,y=y1,col="Time",hue="LaneDrLoc",
                  data=data1,
                  order=["Base","4+2","5+1","5+2"],kind="bar",
                  hue_order=["Base","L","R"],palette=AB_palette,
                  sharex=True,sharey=True,legend=False,
                  edgecolor="black")
    g.set(ylim=ylim1)
    g.set_axis_labels(xlab,ylab)
    g.fig.subplots_adjust(top=0.85)
    g.fig.suptitle(title_AB,fontsize=16) # can also get the figure from plt.gcf()
    g.set_titles("{col_name}",fontsize=12)
    
    #g._legend.set_title("Lane Drop")
    #new_labels = ['Base', 'Add Lane to the Left','Add Lane to the Right']
    #for t, l in zip(g._legend.texts, new_labels): t.set_text(l)
    
    # Put the legend out of the figure
    cool_grey = mpatches.Patch(color=sns.xkcd_rgb["cool grey"], label='Add Lane to the Left')
    charcoal_grey = mpatches.Patch(color=sns.xkcd_rgb["charcoal grey"], label='Add Lane to the Right')
    plt.legend(handles=[cool_grey,charcoal_grey],
               loc="lower center",ncol=4,bbox_to_anchor=(-0.3,-0.2,0.5,0.5))
    g.savefig(saveNm)

NB_plots(x1="Sen",y1="SMS",xlab="",ylab="Average Speed (mph)",title_AB="IH 69 NB Average Speed in 2025",data1=Findat_NB_69[Findat_NB_69["Year"]==2025],saveNm="NB69_2025.png")
NB_plots(x1="Sen",y1="SMS",xlab="",ylab="Average Speed (mph)",title_AB="Spur 527 NB Average Speed in 2025",data1=Findat_NB_Spur[Findat_NB_Spur["Year"]==2025],saveNm="NB_Spur_2025.png")
NB_plots(x1="Sen",y1="SMS",xlab="",ylab="Average Speed (mph)",title_AB="IH 69 NB Average Speed in 2045",data1=Findat_NB_69[Findat_NB_69["Year"]==2045],saveNm="NB69_2045.png")
NB_plots(x1="Sen",y1="SMS",xlab="",ylab="Average Speed (mph)",title_AB="Spur 527 NB Average Speed in 2045",data1=Findat_NB_Spur[Findat_NB_Spur["Year"]==2045],saveNm="NB_Spur_2045.png")

NB_plots(x1="Sen",y1="TotalDelay",ylim1=(0,900),xlab="",ylab="Total Delay (hr)",title_AB="IH 69 NB Total Delay in 2025",data1=Findat_NB_69[Findat_NB_69["Year"]==2025],saveNm="Del_NB69_2025.png")
NB_plots(x1="Sen",y1="TotalDelay",ylim1=(0,900),xlab="",ylab="Total Delay (hr)",title_AB="Spur 527 NB Total Delay in 2025",data1=Findat_NB_Spur[Findat_NB_Spur["Year"]==2025],saveNm="Del_NB_Spur_2025.png")
NB_plots(x1="Sen",y1="TotalDelay",ylim1=(0,900),xlab="",ylab="Total Delay (hr)",title_AB="IH 69 NB Total Delay in 2045",data1=Findat_NB_69[Findat_NB_69["Year"]==2045],saveNm="Del_NB69_2045.png")
NB_plots(x1="Sen",y1="TotalDelay",ylim1=(0,900),xlab="",ylab="Total Delay (hr)",title_AB="Spur 527 NB Total Delay in 2045",data1=Findat_NB_Spur[Findat_NB_Spur["Year"]==2045],saveNm="Del_NB_Spur_2045.png")


# Put a legend to the right s
Findat_Wd=pd.pivot_table(Findat_NB_69,index="Scenario",columns=["Time","Year"],values =["SMS","VEHS(ALL)","Delay","LatentDelay","TotalDelay"])
new_index=['Base','4+2_NoShared Ln R','4+2_NoShared Ln','5+1_Flared Ln R','5+1_Flared Ln','5+2_Shared Ln R','5+2_Shared Ln']
Findat_Wd=Findat_Wd.reindex(new_index)

Findat_Wd

########################################################################################################################
# SB Data Processing
ListFiles=glob.glob('D:/Dropbox/TTI_Projects/Road User Cost/VISSIM AM Peak V14/SB/SB 2045/*Vehicle Travel Time Results.att')
Lfs2=glob.glob("D:/Dropbox/TTI_Projects/Road User Cost/VISSIM PM Peak V14/SB/SB 2045/*Vehicle Travel Time Results.att")
Lfs3=glob.glob("D:/Dropbox/TTI_Projects/Road User Cost/VISSIM AM Peak V14/SB/SB 2025/*Vehicle Travel Time Results.att")
Lfs4=glob.glob("D:/Dropbox/TTI_Projects/Road User Cost/VISSIM PM Peak V14/SB/SB 2025/*Vehicle Travel Time Results.att")

ListFiles=ListFiles+Lfs2+Lfs3+Lfs4#file = ListFiles[1]
#file = "AM 2045 NB Base_Vehicle Travel Time Results.att"
def TTSegName(x):
    if(x==1):Nm="69_SB"
    elif(x==2):Nm="69_NB"
    elif(x==3):Nm="Spur_SB"
    else:Nm="Spur_NB"
    return Nm
Findat= pd.DataFrame()
for file_Fu in ListFiles:
    file=file_Fu.split("\\")[1]
    desc1= file[0:10]
    Time,Year, SenDir=desc1.split(" ")
    Scenario2=file[11:].split("_Vehicle Travel Time Results.att")[0]
    Scenario2=Scenario2.split(" Cor2")[0]
    dat=pd.read_csv(file_Fu,sep =';',skiprows=17)
    mask=dat["$VEHICLETRAVELTIMEMEASUREMENTEVALUATION:SIMRUN"]=="AVG"
    dat["TTSegNm"]=dat['VEHICLETRAVELTIMEMEASUREMENT'].apply(TTSegName)
    mask2=(dat["TTSegNm"]=="69_SB")|(dat["TTSegNm"]=="Spur_SB")
    dat = dat[mask & mask2]
    dat
    dat["Scenario2"] = Scenario2
    dat["Time"]= Time
    dat["Year"] = np.int(Year)
    dat["SenDir"]= SenDir
    Findat=Findat.append(dat)
    Findat["Delay"]= Findat["VEHS(ALL)"]*(Findat["TRAVTM(ALL)"]-(Findat["DISTTRAV(ALL)"]/(1.47*65)))/3600
    Findat["Delay"]=np.round( Findat["Delay"])
Findat["SMS"] =np.round(Findat["DISTTRAV(ALL)"]/Findat["TRAVTM(ALL)"]/1.47,1)



RdFl1= os.path.join("D:/Dropbox/TTI_Projects/Road User Cost","InpVolKey.csv")
InputVolDat=pd.read_csv(RdFl1)
InputVolDat=InputVolDat.drop("Scenario",axis=1)
Findat=Findat.merge(InputVolDat,how='inner',on=["Scenario2","Year","Time","TTSegNm"])
Findat["LatentDelay"]=(Findat["InpVol"]-Findat["VEHS(ALL)"])*(Findat["TRAVTM(ALL)"]-(Findat["DISTTRAV(ALL)"]/(1.47*65)))/3600
Findat["LatentDelay"]=np.round(Findat["LatentDelay"],1)
Findat["TotalDelay"] = np.round(Findat["Delay"]+Findat["LatentDelay"],1)
Findat["Sen"]=Findat["Scenario2"].apply(lambda x: str.split(x,"_")[0])
Findat["LaneDrLoc"]=Findat["Scenario2"].apply(lambda x: str.split(x,"_")[-1])

########################################################################################################################
# Get the Data for SB 69 and Spur
Findat_SB_69= Findat[Findat["TTSegNm"]=="69_SB"]
Findat_SB_Spur= Findat[Findat["TTSegNm"]=="Spur_SB"]

########################################################################################################################
# SB IH 69 Plots
sns.set(style="whitegrid", color_codes=True)

# SB IH 69 Plots
def SB_plots(x1="Sen",y1="SMS",ylim1=(0,65),xlab="",ylab="IH 69 SB Average Speed in 2025",title_AB="IH 69 SB Average Speed in 2025",data1=Findat_SB_69[Findat_SB_69["Year"]==2025],saveNm="SB69_2025.png"):
    sns.set(style="whitegrid", color_codes=True)
    sns.palplot(sns.color_palette("Greys"))
    AB_palette1= ["white",sns.xkcd_rgb["light grey"],sns.xkcd_rgb["cool grey"],sns.xkcd_rgb["charcoal grey"]]
    g3=sns.catplot(x=x1,y=y1,col="Time",hue="LaneDrLoc",
                  data=data1,
                  order=["Base","4+2","5+1"],kind="bar",
                  hue_order=["Base","1500ft","2500ft","No LnDrop"],palette=AB_palette1,
                  sharex=True,sharey=True,legend=False,
                  edgecolor="black")
    g3.set(ylim=ylim1)
    g3.set_axis_labels(xlab,ylab)
    g3.fig.subplots_adjust(top=0.85)
    g3.fig.suptitle(title_AB,fontsize=16) # can also get the figure from plt.gcf()
    g3.set_titles("{col_name}",fontsize=12)
    
    #g._legend.set_title("Lane Drop")
    #new_labels = ['Base', 'Add Lane to the Left','Add Lane to the Right']
    #for t, l in zip(g._legend.texts, new_labels): t.set_text(l)
    
    # Put the legend out of the figure
    # Put the legend out of the figure
    #white = mpatches.Patch(color="white", label='Base')
    Lt_grey = mpatches.Patch(color=sns.xkcd_rgb["light grey"], label='Lane Drop at 1500 ft.')
    cool_grey = mpatches.Patch(color=sns.xkcd_rgb["cool grey"], label='Lane Drop at 2500 ft.')
    charcoal_grey = mpatches.Patch(color=sns.xkcd_rgb["charcoal grey"], label='No Lane Drop')
    
    plt.legend(handles=[Lt_grey,cool_grey,charcoal_grey],
               loc="lower center",ncol=4,bbox_to_anchor=(-0.3,-0.2,0.5,0.5))
    g3.savefig(saveNm)

SB_plots(x1="Sen",y1="SMS",xlab="",ylab="Average Speed (mph)",title_AB="IH 69 SB Average Speed in 2025",data1=Findat_SB_69[Findat_SB_69["Year"]==2025],saveNm="SB69_2025.png")
SB_plots(x1="Sen",y1="SMS",xlab="",ylab="Average Speed (mph)",title_AB="Spur 527 SB Average Speed in 2025",data1=Findat_SB_Spur[Findat_SB_Spur["Year"]==2025],saveNm="SB_Spur_2025.png")
SB_plots(x1="Sen",y1="SMS",xlab="",ylab="Average Speed (mph)",title_AB="IH 69 SB Average Speed in 2045",data1=Findat_SB_69[Findat_SB_69["Year"]==2045],saveNm="SB69_2045.png")
SB_plots(x1="Sen",y1="SMS",xlab="",ylab="Average Speed (mph)",title_AB="Spur 527 SB Average Speed in 2045",data1=Findat_SB_Spur[Findat_SB_Spur["Year"]==2045],saveNm="SB_Spur_2045.png")

SB_plots(x1="Sen",y1="TotalDelay",ylim1=(0,900),xlab="",ylab="Total Delay (hr)",title_AB="IH 69 SB Total Delay in 2025",data1=Findat_SB_69[Findat_SB_69["Year"]==2025],saveNm="Del_SB69_2025.png")
SB_plots(x1="Sen",y1="TotalDelay",ylim1=(0,900),xlab="",ylab="Total Delay (hr)",title_AB="Spur 527 SB Total Delay in 2025",data1=Findat_SB_Spur[Findat_SB_Spur["Year"]==2025],saveNm="Del_SB_Spur_2025.png")
SB_plots(x1="Sen",y1="TotalDelay",ylim1=(0,900),xlab="",ylab="Total Delay (hr)",title_AB="IH 69 SB Total Delay in 2045",data1=Findat_SB_69[Findat_SB_69["Year"]==2045],saveNm="Del_SB69_2045.png")
SB_plots(x1="Sen",y1="TotalDelay",ylim1=(0,900),xlab="",ylab="Total Delay (hr)",title_AB="Spur 527 SB Total Delay in 2045",data1=Findat_SB_Spur[Findat_SB_Spur["Year"]==2045],saveNm="Del_SB_Spur_2045.png")

Findat_Wd_SB=pd.pivot_table(Findat_SB_69,index="Scenario2",columns=["Time","Year"],values =["SMS","VEHS(ALL)","Delay","LatentDelay","TotalDelay"])
new_index=['Base','4+2_1500ft','4+2_2500ft','4+2_No LnDrop','5+1_1500ft','5+1_2500ft','5+1_No LnDrop']
Findat_Wd_SB=Findat_Wd_SB.reindex(new_index)


########################################################################################################################
# Tech Memo Tables
# Undertand the data format before merging

[Findat_NB_69.columns,Findat_NB_69.shape]
[Findat_NB_Spur.columns,Findat_NB_Spur.shape]
[Findat_SB_69.columns,Findat_SB_69.shape]
[Findat_SB_Spur.columns,Findat_SB_Spur.shape]

Mer_Dat= pd.DataFrame()

d1=Findat_NB_69.loc[:,["Sen","SenDir","Year","Time","TTSegNm","TotalDelay","SMS","VEHS(ALL)","LaneDrLoc"]].copy()
d2=Findat_NB_Spur.loc[:,["Sen","SenDir","Year","Time","TTSegNm","TotalDelay","SMS","VEHS(ALL)","LaneDrLoc"]].copy()
d3=Findat_SB_69.loc[:,["Sen","SenDir","Year","Time","TTSegNm","TotalDelay","SMS","VEHS(ALL)","LaneDrLoc"]].copy()
d4=Findat_SB_Spur.loc[:,["Sen","SenDir","Year","Time","TTSegNm","SMS","VEHS(ALL)","TotalDelay","LaneDrLoc"]].copy()
Mer_Dat=pd.concat([d1,d2,d3,d4])
Mer_Dat.loc[:,"TotalDelay"]=np.round(Mer_Dat.loc[:,"TotalDelay"],0)
Mer_Dat.loc[:,"TotalDelay"]=Mer_Dat.loc[:,"TotalDelay"].apply(np.int)
Mer_Dat.loc[:,"SMS"]=np.round(Mer_Dat.loc[:,"SMS"],0)
Mer_Dat.loc[:,"SMS"]=Mer_Dat.loc[:,"SMS"].apply(np.int)
Mer_Dat.loc[:,"TTSegNm"]=Mer_Dat.loc[:,"TTSegNm"].apply(lambda x: str.split(x,"_")[0])
Mer_Dat.loc[:,"TTSegNm"]=Mer_Dat.loc[:,"TTSegNm"].apply(lambda x:"IH 69" if x=="69" else "Spur 527")

def tempfun(x):
    y=""
    if x=="Base":
        y="Base Conditions"
    elif x=="L":
        y="Add Lane to Left"
    elif x=="R":
        y="Add Lane to Right"
    elif x=="1500ft":
        y="Lane Drop at 1500 ft"
    elif x=="2500ft":
        y="Lane Drop at 2500 ft"
    elif x=="No LnDrop":
        y="No Lane Drop"
    else:
        y="nan"
    return y;

Mer_Dat.loc[:,"LaneDrLoc"]=Mer_Dat.loc[:,"LaneDrLoc"].apply(tempfun)


def PivFun(Dat,PivVal="TotalDelay"):
    PivDat =pd.pivot_table(Dat,index=["SenDir","Sen","LaneDrLoc"],columns=["TTSegNm","Time"],values =[PivVal])
    new_index = pd.MultiIndex(levels=[['NB','SB'],["Base","4+2","5+1","5+2"], ['Base Conditions', "Add Lane to Left", "Add Lane to Right","Lane Drop at 1500 ft","Lane Drop at 2500 ft","No Lane Drop"]], 
                              labels=[[0,0,0,0,0,0,0,1,1,1,1,1,1,1],[0,1,1,2,2,3,3,0,1,1,1,2,2,2],[0,1,2,1,2,1,2,0,3,4,5,3,4,5]],names=['SenDir', 'Sen',"LaneDrLoc"]
                              )
    PivDat=PivDat.reindex(new_index)
    return PivDat;
def PivFun1(Dat,PivVal="TotalDelay"):
    PivDat =pd.pivot_table(Dat,index=["SenDir","Sen","LaneDrLoc"],columns=["Time","Year"],values =[PivVal],aggfunc='sum')
    new_index = pd.MultiIndex(levels=[['NB','SB'],["Base","4+2","5+1","5+2"], ['Base Conditions', "Add Lane to Left", "Add Lane to Right","Lane Drop at 1500 ft","Lane Drop at 2500 ft","No Lane Drop"]], 
                              labels=[[0,0,0,0,0,0,0,1,1,1,1,1,1,1],[0,1,1,2,2,3,3,0,1,1,1,2,2,2],[0,1,2,1,2,1,2,0,3,4,5,3,4,5]],names=['SenDir', 'Sen',"LaneDrLoc"]
                              )
    PivDat=PivDat.reindex(new_index)
    return PivDat;

dt_buf=datetime.datetime.now()
dt_buf1=dt_buf.strftime("%m-%d-%Y")
writer=pd.ExcelWriter("Res"+dt_buf1+".xlsx")
PivFun(Mer_Dat[Mer_Dat["Year"]==2045],"SMS").to_excel(writer,"SMS2045")
PivFun(Mer_Dat[Mer_Dat["Year"]==2025],"TotalDelay").to_excel(writer,"TotDelay2025")
PivFun(Mer_Dat[Mer_Dat["Year"]==2025],"VEHS(ALL)").to_excel(writer,"Throughput")
PivFun(Mer_Dat[Mer_Dat["Year"]==2045],"SMS").to_excel(writer,"AuxDocSMS2045")
PivFun1(Mer_Dat,"TotalDelay").to_excel(writer,"AuxDocTDelay")

writer.save()