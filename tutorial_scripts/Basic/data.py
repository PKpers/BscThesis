import numpy as np
import random as rand
import matplotlib.pyplot as plt 
import ROOT
import math
ROOT.gROOT.SetBatch(True) # I will se what it does later 
## Frist lets create a data set 
# A function that simulates a random step in one dimention. 0: do not move, 1, move one step
def randStep():
    u=rand.random()
    step=0
    if u>=0.5:
        step=1
    #
    return step

#a function that simulates a random walk consisted of n steps
def randWalk(nsteps):
    distance=sum([randStep() for i in range(nsteps)])
    return distance

Nsteps=1000
Nwalkers=100000
walks=[randWalk(Nsteps) for i in range(Nwalkers)]


#Write the data set to a txt file 
print('distance in step units', file=open('data.txt', 'w'))
for w in walks:
    print(
        w,
        file=open('data.txt', 'a')
    )
#


## Create a Root Tree file and put the histogram inside.
counts, bins, etc=plt.hist(walks, 50)#Extract the count and the bins of the histogram

treefile1 = ROOT.TFile.Open('file1.root', 'RECREATE')
tree1=ROOT.TTree('mytree1','mytree1')
counts_=ROOT.vector("double")(0)
bins_=ROOT.vector("double")(0)

tree1.Branch("counts_", "std::vector<double>", counts_)
tree1.Branch("bins_", "std::vector<double>", bins_)
for i in range(len(counts)):
    counts_.clear()
    bins_.clear()

    counts_.push_back(counts[i])
    bins_.push_back(bins[i])

    tree1.Fill()
#
treefile1.cd()
tree1.Write()
treefile1.Close()

    
    
exit()

