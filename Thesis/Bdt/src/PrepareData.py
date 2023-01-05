#!/usr/bin/python
import ROOT
import sys
import numpy as np

def pair_permute(__list__):
    '''
    combine the items of a list
    in pairs of two.
    order doesn't matter
    repetition allowed
    '''
    permutations = []
    for i, xi in enumerate(__list__):
        if type(xi) is not str:
            p = np.array([xi*xj for xj in __list__[i:]])
        else :
            p = np.array([xi+xj for xj in __list__[i:]])
        #
        permutations = np.hstack((permutations, p))
    #
    return permutations

# Read data from ROOT files
if len(sys.argv) != 3:
    print('Usage: {} {} {}'.format(sys.argv[0], ' dataset', ' outname'))
    exit(-1)
#
## Load data
dataset = sys.argv[1]
inpath = '/home/kpapad/UG_thesis/Thesis/share/SimuData/'
sig_filename = inpath+ "{}_SIG_Train.root".format(dataset)
bkg_filename = inpath+ "{}_BKG_Train.root".format(dataset)
data_sig = ROOT.RDataFrame("myTree", sig_filename).AsNumpy()
data_bkg = ROOT.RDataFrame("myTree", bkg_filename).AsNumpy()
## create the variable names(instead of typing them one by one)
variables = []
names=()
if "Pxyz" in sig_filename and "Pxyz" in bkg_filename:
    names=("Px", "Py", "Pz") 
else:
    names=("Pt", "Eta", "Phi") 
#
for j in range(1, 3):
    for name in names:
        variables.append(name+str(j))
    #
#
print(variables)
# Convert inputs to format readable by machine learning tools
x_sig = np.vstack([data_sig[var] for var in variables]).T
x_bkg = np.vstack([data_bkg[var] for var in variables]).T

x_sig = np.array(
    [pair_permute(x) for x in x_sig]
)
print(x_sig[10])

exit()
#x = np.vstack([x_sig, x_bkg])

