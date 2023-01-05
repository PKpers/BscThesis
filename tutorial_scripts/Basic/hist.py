from __future__ import print_function
import ROOT
import math
from copy import copy 
import numpy as np

myFile=ROOT.TFile.Open("file1.root", "READ")
myTree=myFile.Get("mytree1")
n=myTree.GetEntries()


#exit()
#bins, counts = ([], [])
bins=[]
counts=[]
print(bins)
for i, e in enumerate(myTree):
    
    print(e.bins_)
    if i==5: break 
    bins.append(copy(e.bins_))
    #counts.append(e.counts_)
#
for b in bins:
    print(b)
exit()
#print(' ')
#print(bins)
#exit()
#print(len(counts))
#print(' ')
bins=np.array(bins)
counts=np.array(counts)
'''
bins=np.array(
    [b.bins_ for b in myTree]
)
counts=np.array(
    [c.counts_ for c in myTree]
)
'''

#print(
 #   [b for b in bins]
    #' ', 
#    [c for c in counts]
#)
exit()
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

exit()
