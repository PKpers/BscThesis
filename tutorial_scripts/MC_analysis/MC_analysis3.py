import ROOT
import numpy as np
ROOT.gInterpreter.ProcessLine('#include "test.h"')
## Import the tree--------------------------------------------------------------------------------------------------------
tree_path='~/UG_thesis/';
myFile_name=tree_path+"MC_2016_Z_2L.root";#read the root file
treeName="skimTree";
df=ROOT.RDataFrame(treeName, myFile_name);
c_all = df.Count().GetValue();
##Compute the invariant mass of the two leptons and compare to the existing one in the tree----------
for i in range(2): #asnig the mass of each lepton given their type
    inp_b_name = 'LeptonFlavor{}'.format(str(i))#branch name, will be the input to the function bellow
    #function = 'asign_mass({})'.format(inp_b_name)
    function = '0'
    new_b_name = 'LeptonMass{}'.format(i)
    df=df.Define(new_b_name, function)
#

type_=['Pt', 'Eta', 'Phi', 'Mass']
names=[]
c_names=[]
for t in type_ : #create a list with the names of the wanted branches
    c1, c2 =['Lepton'+t+str(i) for i in range(2)]
    function = "Couple2({}, {})".format(c1, c2)
    couple_name = 'Coupled_{}'.format(t)
    df = df.Define(couple_name, function) 
    c_names.append(couple_name)
#
function = 'ComputeInvariantMass({}, {}, {}, {})'\
    .format(c_names[0], c_names[1], c_names[2], c_names[3])
#
df = df.Define('Inv_Mass', function)
outFile='InvMassComp0.root'
outTree='InvMasses'
df.Snapshot(outTree, outFile, ['Inv_Mass', 'LeptonPairInvariantMass'] )
print('Data stored in {}'.format(outFile))
