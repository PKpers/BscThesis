from __future__ import print_function
import ROOT
import math
from copy import copy 
import numpy as np

##Import the  tree-----------------------------------------------------------------------------------------
tree_path='~/UG_thesis/'
myFile=ROOT.TFile.Open(tree_path+"MC_2016_Z_2L.root", "READ")#read the root file 
skimTree=myFile.Get("skimTree")#get the (only) tree in the file
num_ent=skimTree.GetEntries()# this returns the number of entries in the tree
##extract the values.----------------------------------------------------------------------------------------------------
#create a list that containts the name of the wanted branches
type_=['Pt', 'Eta', 'Phi', 'Charge']
names=[]
for i in range(2):#create a list with the names of the wanted branches
    name=['Lepton'+t+str(i) for t in type_]
    for j, n in enumerate(name):
        names.append(n)
        if i==0 and j==0: #make sure every time this program is run, the file is overwritten
            print( n, file=open('hist_names.txt', 'w') )
        else: 
            print( n, file=open('hist_names.txt', 'a') )
    #
#
print("invariant mass", file=open("hist_names.txt", 'a'))
#get the events of each branch
events=[]
inv_mass=[]
for entry in range(num_ent):
    skimTree.GetEntry(entry)
    event= [getattr(skimTree, n) for n in names]
    IM=getattr(skimTree,  "LeptonPairInvariantMass")
    inv_mass.append(copy(IM))
    events.append(copy(event))
#
lepton_events=[]
for j in range(len(events[0])):
    #each element in the resulting list. will be a list that containts all the events of a specific branch
    le=[events[i][j] for i in range(len(events))]
    lepton_events.append(np.array(le))
#

##create the histograms-------------------------------------------------------------------------------------------------
def fill_hist(list_inp, hist_inp):
    '''
    this function takes a list as input
    and fils the given histogram with its elements
    '''
    for l in list_inp:
        hist_inp.Fill(l)
    #
    return
#create the histogram
out_hist=ROOT.TFile.Open("hist.root", "RECREATE")
out_hist.cd()
for i, lep in enumerate(lepton_events):
    if 'Charge' in names[i]: 
        hist=ROOT.TH1F(str(names[i]), "leptons", 50, -2, 2)
    elif 'Eta' in names[i] or 'Phi' in names[i]:
        hist=ROOT.TH1F(str(names[i]), "leptons", 50, -10, 10)
    elif "Pt" in names[i]:
        hist=ROOT.TH1F(str(names[i]), "leptons", 50, 0, 500)
    #
    fill_hist(lep, hist)
    hist.Write()
    hist.SetDirectory(0)
#
hist2=ROOT.TH1F("invariant mass", "invariant mass", 50, 0, 500)
fill_hist(inv_mass, hist2)
hist2.Write()
out_hist.Close()
exit()

