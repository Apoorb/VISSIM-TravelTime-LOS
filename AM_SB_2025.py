# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 11:18:23 2019

@author: A-Bibeka
"""

#==========================================================================
# Python-Script for PTV Vissim 6+
# Copyright (C) PTV AG, Jochen Lohmiller
# All rights reserved.
# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# Example of basic syntax - DO NOT MODIFY
#==========================================================================

# This script demonstrates how to use the COM interface in Python.
# Basic commands for loading a network and layout, reading and setting
# attributes of network objects, running a simulation and retrieving
# evaluations are shown. This example is also available for the programming
# languages VBA, VBS Matlab, C#, C++ and Java.
#
# If you start using COM, please see also our COM introduction document:
# C:\Program Files\PTV Vision\PTV Vissim 9\Doc\Eng\Vissim 9 - COM Intro.pdf
#
# For information about the attributes and methods of PTV Vissim objects, see
# the COM Help, which is located in the PTV Vissim menu: Help > COM Help.
#
# Hint: You can easily see all attributes of the PTV Vissim objects in the lists in
# Vissim. In case your PTV Vissim language is set to English, the name in the
# headline of the list correspond to the command to access via COM.
# Example: If you want to access the number of lanes of a link, go to PTV Vissim
# and see the headline of "Number of lanes" in the list, which is
# "NumLanes". To access this attribute via COM use:
# Vissim.Net.Links.ItemByKey(1).AttValue('NumLanes')
#
# For adding network objects with COM, please see the example Network Objects Adding


# COM-Server
import win32com.client as com
import os
import glob


## Connecting the COM Server => Open a new Vissim Window:
#Vissim = com.Dispatch("Vissim.Vissim")
# If you have installed multiple Vissim Versions, you can open a specific Vissim version adding the bit Version (32 or 64bit) and Version number
# Vissim = com.Dispatch("Vissim.Vissim-32.800") # Vissim 8 - 32 bit
# Vissim = com.Dispatch("Vissim.Vissim-64.800") # Vissim 8 - 64 bit
# Vissim = com.Dispatch("Vissim.Vissim-32.900") # Vissim 9 - 32 bit
Vissim = com.Dispatch("Vissim.Vissim-64.900") # Vissim 9 - 64 bit
ListFiles=glob.glob('D:/Dropbox/TTI_Projects/Road User Cost/VISSIM AM Peak V14/SB/SB 2045/*.inpx')
Lfs2=glob.glob('D:/Dropbox/TTI_Projects/Road User Cost/VISSIM AM Peak V14/SB/SB 2025/*.inpx')
ListFiles =ListFiles+Lfs2
## Load a Vissim Network:
Filename = ListFiles[1]

for file in ListFiles:
    Filename=file.replace("/","\\")
    layoutFile=Filename.replace(".inpx",".layx")
    
    flag_read_additionally  = False # you can read network(elements) additionally, in this case set "flag_read_additionally" to true
    Vissim.LoadNet(Filename, flag_read_additionally)
    Vissim.LoadLayout(layoutFile)
    ## ========================================================================
    # Simulation
    #==========================================================================
    # 5 runs 
    
    Vissim.Simulation.SetAttValue('UseMaxSimSpeed', True)
    Vissim.Graphics.CurrentNetworkWindow.SetAttValue('QuickMode', True)
    #Vissim.Simulation.SetAttValue('RandSeed', cnt_Sim + 1) # Note: RandSeed 0 is not allowed
    Vissim.Simulation.RunContinuous()

## ==========================
## ========================================================================
# End Vissim
#==========================================================================
Vissim = None