# Proces the LOS results for the Road user cost project
# Created by: Apoorba Bibeka
# Date: 10/24/18

rm(list=ls())
dir="D:/Dropbox/TTI_Projects/Road User Cost"
setwd(dir)
getwd()

require(xlsx)
require(data.table)
LosFun<-function(keyDat,DenDat,PceAM,PcePM,writeF,sheetO,append1=FALSE){
  # Do not use the year from the case name. NB has error. Case name for 2025 and 2045 scenarios are the
  # same. Just use the year column
  DenDat<-DenDat[SimRun=="AVG",.(SimRun,LinkEvlSeg,Density,Year,Time,Sen)]
  DenDat[,Year:=as.factor(Year)]
  DenDat[,Time:=as.factor(Time)]
  DenDat[,Sen:=as.factor(Sen)]
  DenDat<-DenDat[!(Sen %in% "5+1_Flared")]
  DenDat[,c("Link","St","End"):=tstrsplit(LinkEvlSeg,'-')]
  DenDat[,Link:=as.numeric(Link)]
  DenDat[,St:=as.numeric(St)]
  DenDat[,End:=as.numeric(End)]
  DenDat[,LinkSegLen:=End-St]
  DenDat[,LinkLenDen:=Density*LinkSegLen]
  summary(DenDat)
  DenDat[,Sen:=ifelse(Sen=="4+2_NoShared Ln R","4+2 NoShared Ln R",ifelse(Sen=="Base","Base","5+2 SharedLn R"))]
  
  FinDat<-merge(keyDat,DenDat,by.x=c("Scenario","Time","Link"),by.y=c("Sen","Time","Link"))
  sum(is.na(FinDat))
  FinDat<-na.omit(FinDat)
  FinDat[,Scenario:=as.factor(Scenario)]
  FinDat$Scenario=factor(FinDat$Scenario,levels(FinDat$Scenario)[c(3,1,2)])
  str(FinDat$NumLanes)
  FinDat[,LinkLenDenPerLn:=LinkLenDen/NumLanes]
  setorder(FinDat,Year,`Time`,Scenario,OrdR)
  FinDat<-FinDat[,.(Year,Time,Scenario,OrdR,Label,Link,Density,LinkSegLen,LinkLenDenPerLn)]
  FinDat[,Sumlen:=sum(LinkSegLen),by=list(Year,Time,Scenario,OrdR)]
  FinDat[,SumlenDen:=sum(LinkLenDenPerLn),by=list(Year,Time,Scenario,OrdR)]
  FinDat1<-unique(FinDat,by=c("Year","Time","Scenario","OrdR"))
  FinDat1[,FinDen:=round(SumlenDen/Sumlen,2)]
  FinDat1<-FinDat1[,.(Year,Time,Scenario,OrdR,Label,FinDen)]
  FinDat1[,FinDen:=ifelse(Time=="AM",round(FinDen*PceAM,2),round(FinDen*PcePM,2))]
  FinDat1[,LOS:=ifelse(FinDen>45,"F",ifelse(FinDen>35,"E",ifelse(FinDen>26,"D",ifelse(FinDen>18,"C",ifelse(FinDen>11,"B","A")))))]
  FinDat12<-dcast(FinDat1,Year+OrdR+Label~Time+Scenario,value.var = c("FinDen","LOS"))
  write.xlsx(FinDat12,writeF,sheetO,append=append1)
  NULL
}





LosFunSB<-function(keyDat,DenDat,PceAM,PcePM,writeF,sheetO,append1=FALSE){
  # Do not use the year from the case name. NB has error. Case name for 2025 and 2045 scenarios are the
  # same. Just use the year column
  DenDat<-DenDat[SimRun=="AVG",.(SimRun,LinkEvlSeg,Density,Year,Time,Sen)]
  DenDat[,Year:=as.factor(Year)]
  DenDat[,Time:=as.factor(Time)]
  DenDat[,Sen:=as.factor(Sen)]
  DenDat[,c("Link","St","End"):=tstrsplit(LinkEvlSeg,'-')]
  DenDat[,Link:=as.numeric(Link)]
  DenDat[,St:=as.numeric(St)]
  DenDat[,End:=as.numeric(End)]
  DenDat[,LinkSegLen:=End-St]
  DenDat[,LinkLenDen:=Density*LinkSegLen]
  DenDat<-DenDat[(Sen %in% c("Base","4+2_1500ft","4+2_No LnDrop"))]
  
  summary(DenDat)
  DenDat[,Sen:=ifelse(Sen=="4+2_1500ft","S4+2 1500",ifelse(Sen=="Base","Base","S4+2 NoDrop"))]
  
  FinDat<-merge(keyDat,DenDat,by.x=c("Scenario","Time","Link"),by.y=c("Sen","Time","Link"))
  FinDat<-na.omit(FinDat)
  FinDat[,Scenario:=as.factor(Scenario)]
  FinDat$Scenario=factor(FinDat$Scenario,levels(FinDat$Scenario)[c(1,2,3)])
  FinDat[,LinkLenDenPerLn:=LinkLenDen/NumLanes]
  setorder(FinDat,Year,`Time`,Scenario,OrdR)
  FinDat<-FinDat[,.(Year,Time,Scenario,OrdR,Label,Link,Density,LinkSegLen,LinkLenDenPerLn)]
  FinDat[,Sumlen:=sum(LinkSegLen),by=list(Year,Time,Scenario,OrdR)]
  FinDat[,SumlenDen:=sum(LinkLenDenPerLn),by=list(Year,Time,Scenario,OrdR)]
  FinDat1<-unique(FinDat,by=c("Year","Time","Scenario","OrdR"))
  FinDat1[,FinDen:=round(SumlenDen/Sumlen,2)]
  FinDat1<-FinDat1[,.(Year,Time,Scenario,OrdR,Label,FinDen)]
  FinDat1[,FinDen:=ifelse(Time=="AM",round(FinDen*PceAM,2),round(FinDen*PcePM,2))]
  FinDat1[,LOS:=ifelse(FinDen>45,"F",ifelse(FinDen>35,"E",ifelse(FinDen>26,"D",ifelse(FinDen>18,"C",ifelse(FinDen>11,"B","A")))))]
  FinDat12<-dcast(FinDat1,OrdR+Label+Time~Year+Scenario,value.var = c("FinDen","LOS"))
  setorder(FinDat12,Time,OrdR)
  
  write.xlsx(FinDat12,writeF,sheetO,append=append1)
  NULL
}


#Output file
Ofile =paste("Res_LOS", format(Sys.Date(),'%m-%d-%Y'),".xlsx",sep="")
#*******************************************************************************************
# NB IH 69
f1="LinkSectionKey.xlsx"
keyDat_<-read.xlsx(f1,"NB_IH69")
keyDat_<-as.data.table(keyDat_)
keyDat_[,Scenario:=as.factor(Scenario)]
PceAM= 1.034
PcePM=1.08

summary(keyDat_)
f2="NB_LinkEvalDat.csv"
DenDat_<-fread(f2)
colnames(DenDat_)
LosFun(keyDat=keyDat_,DenDat=DenDat_,PceAM,PcePM,Ofile,"IH69_NB")
#*******************************************************************************************
# NB Spur
f1="LinkSectionKey.xlsx"
keyDat_1<-read.xlsx(f1,"NB_Spur")
keyDat_1<-as.data.table(keyDat_1)
keyDat_1[,Scenario:=as.factor(Scenario)]
PceAM1= 1
PcePM1=1

summary(keyDat_1)
f2="NB_LinkEvalDat.csv"
DenDat_1<-fread(f2)
colnames(DenDat_1)
LosFun(keyDat_1,DenDat_1,PceAM1,PcePM1,Ofile,"NB_Spur",append1=TRUE)


#*******************************************************************************************
# SB IH 69
f1="LinkSectionKey.xlsx"
keyDat_<-read.xlsx(f1,"SB_IH69")
keyDat_<-as.data.table(keyDat_)
keyDat_[,Scenario:=as.factor(Scenario)]
PceAM= 1.028
PcePM=1.024

summary(keyDat_)
f2="SB_LinkEvalDat.csv"
DenDat_<-fread(f2)
colnames(DenDat_)
LosFunSB(keyDat=keyDat_,DenDat=DenDat_,PceAM,PcePM,Ofile,"IH69_SB",append1=TRUE)


#*******************************************************************************************
# SB_Spur
f1="LinkSectionKey.xlsx"
keyDat_<-read.xlsx(f1,"SB_Spur")
keyDat_<-as.data.table(keyDat_)
keyDat_[,Scenario:=as.factor(Scenario)]
PceAM= 1
PcePM=1

summary(keyDat_)
f2="SB_LinkEvalDat.csv"
DenDat_<-fread(f2)
colnames(DenDat_)
LosFunSB(keyDat_,DenDat_,PceAM,PcePM,Ofile,"SB_Spur",append1=TRUE)
