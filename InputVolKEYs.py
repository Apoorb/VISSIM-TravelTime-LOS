# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 16:12:26 2019

@author: A-Bibeka
"""
import pandas as pd
import os

os.chdir("D:/Dropbox/TTI_Projects/Road User Cost")

InputVolDat =pd.DataFrame()
tempdat=pd.DataFrame()
for year in [2025,2045]:
    for tm in ["AM","PM"]:
        for TTSegNm in ["69_SB","69_NB","Spur_SB","Spur_NB"]:
            if year==2025:
                if tm=="AM":
                    if TTSegNm =="69_SB":
                        InpVol_B=0.95*0.94*(0.6*6458+0.78*1447) #4468
                        InpVol_Alt=0.95*0.94*(0.6*6458+0.45*2829) #4597
                    elif TTSegNm =="69_NB":
                        InpVol_B=0.9*0.47*(8855+620+0.05*558) #4020
                        InpVol_Alt=0.9*0.47*(8855+620+0.05*558) #4020
                    elif TTSegNm=="Spur_SB":
                        InpVol_B=2403
                        InpVol_Alt=2403
                    else:
                        InpVol_B=791
                        InpVol_Alt=791
                else:
                    if TTSegNm =="69_SB":
                        InpVol_B=0.9*0.95*(0.67*3578+0.67*2071) #3236
                        InpVol_Alt=0.9*0.95*(0.67*3578+0.51*2449) #3118
                    elif TTSegNm =="69_NB":
                        InpVol_B=0.39*0.89*(650+7338) #2773
                        InpVol_Alt=0.39*0.89*(650+7338) #2773
                    elif TTSegNm=="Spur_SB":
                        InpVol_B=1872
                        InpVol_Alt=1872
                    else:
                        InpVol_B=860
                        InpVol_Alt=860                    
    
            else:
                if tm=="AM":
                    if TTSegNm =="69_SB":
                        InpVol_B=0.95*0.94*(0.6*7968+0.78*1785) #5513
                        InpVol_Alt=0.95*0.94*(0.6*7968+0.45*3490) #5672
                    elif TTSegNm =="69_NB":
                        InpVol_B=0.9*0.47*(10925+765+0.05*688) #4959
                        InpVol_Alt=0.9*0.47*(10925+765+0.05*688) #4959
                    elif TTSegNm=="Spur_SB":
                        InpVol_B=2965
                        InpVol_Alt=2965
                    else:
                        InpVol_B=976
                        InpVol_Alt=976
                else:
                    if TTSegNm =="69_SB":
                        InpVol_B= 0.9*0.95*(0.67*4414+0.67*2555) #3992
                        InpVol_Alt=0.9*0.95*(0.67*4414+0.51*3021) #3849
                    elif TTSegNm =="69_NB":
                        InpVol_B=0.39*0.89*(802+9054) #3421
                        InpVol_Alt=0.39*0.89*(802+9054) #3421
                    elif TTSegNm=="Spur_SB":
                        InpVol_B=2309
                        InpVol_Alt=2309
                    else:
                        InpVol_B=1061
                        InpVol_Alt=1061
                        
            tempdat["Scenario"]=['Base','4+2_NoShared Ln R','4+2_NoShared Ln','5+1_Flared Ln R','5+1_Flared Ln','5+2_Shared Ln R','5+2_Shared Ln']
            tempdat["Scenario2"]=['Base','4+2_1500ft','4+2_2500ft','4+2_No LnDrop','5+1_1500ft','5+1_2500ft','5+1_No LnDrop']
            tempdat["Time"] =tm
            tempdat["Year"]=year
            tempdat["TTSegNm"]=TTSegNm
            tempdat["InpVol"] = tempdat["Scenario"].apply(lambda x: np.round(InpVol_B,0) if x=="Base" else np.round(InpVol_Alt,0))
            tempdat["InpVol"] = tempdat["Scenario"].apply(lambda x: np.round(InpVol_B,0) if x=="Base" else np.round(InpVol_Alt,0))

            InputVolDat=InputVolDat.append(tempdat)
InputVolDat.to_csv("InpVolKey.csv",index=False)