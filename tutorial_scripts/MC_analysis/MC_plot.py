from __future__ import print_function
import ROOT
import math
from copy import copy 
import numpy as np

#Import the  tree-----------------------------------------------------------------------------------------
tree_path='~/UG_thesis/'
myFile=ROOT.TFile(tree_path+"hist.root")#read the root file 
with open('hist_names.txt', 'r') as f:
    names = f.readlines()
#
names = [n.split('\n')[0] for n in names]
histos=[]
for i, n in enumerate(names):
    hist=myFile.Get(n)#get the (only) tree in the file
    hist.SetDirectory(0)
    histos.append(hist)
#
myFile.Close()
#plot the histograms----------------------------------------------------------------------------------------------------
#c=ROOT.TCanvas("can1", "leptons histograms", 800, 600)
c=ROOT.TCanvas()
c.cd()
c.SetGrid()
c.SaveAs("plots.pdf[")
#create the histogram
def set_axes(xtitle, ytitle):
    c.Clear()
    h.GetXaxis().SetTitle(str(xtitle))
    h.GetYaxis().SetTitle(str(ytitle))
    return 
#
ytitle='counts'
for i, h in enumerate(histos):
    if 'Charge' in names[i]:
        #c.Clear()
        set_axes(names[i], ytitle)
    elif 'Eta' in names[i] or 'Phi' in names[i]:
        if "Phi" in names[i]: 
            c.Clear()
            set_axes(names[i], ytitle)
        elif "Eta" in names[i]:
            c.Clear()
            set_axes(names[i], ytitle)
        # 
    elif "Pt" in names[i]:
        c.Clear()
        set_axes(names[i], ytitle)
    else:
        c.Clear()
        set_axes(names[i], ytitle)
    #
    h.Draw()
    c.SaveAs("plots.pdf") 
#
c.SaveAs('plots.pdf')
c.SaveAs('plots.pdf]')
exit()

