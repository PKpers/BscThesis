from __future__ import print_function
import ROOT
import math
from copy import copy 
import numpy as np

tree_path='~/UG_thesis/tutorial/'
myFile=ROOT.TFile.Open(tree_path+"file1.root", "READ")#read the root file 
myTree=myFile.Get("mytree1")#get the (only) tree in the file
n=myTree.GetEntries()# this returns the number of entries in the tree

#extract the values.
bins=[]
counts=[]
for e in range(n):
    myTree.GetEntry(e)
    bin_= getattr(myTree, "bins_")
    count_= getattr(myTree, "counts_")
    bins.append(copy(bin_))
    counts.append(copy(count_)) 
#
#exit()
bins=np.array(bins)
counts=np.array(counts)
c1=ROOT.TCanvas()
c1.SetGrid()
hist=ROOT.TGraph(n, bins, counts)
hist.SetMarkerColor(4)
hist.SetMarkerStyle(21)
hist.SetTitle('histogram')
hist.GetXaxis().SetTitle('bins')
hist.GetYaxis().SetTitle('counts')
hist.Draw('ACP')
c1.Update()


#exit()
