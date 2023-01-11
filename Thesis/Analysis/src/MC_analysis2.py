import ROOT
import numpy as np 
## Functions ----------------------------------------------------------------------------------------------------
def is_dimuon(evnt_ids):
    '''
    Loops through the particle ids of a single event
    It returns
    True:  if the event has exactly two muons and one phi particle
    False: otherwise
    '''
    mu_p = 0 #number of anti muons in each event
    mu_n = 0 #number of muons in each evnt
    phi = 0# number of phi particles in each event
    for idx, id_ in enumerate(evnt_ids) :
        if id_ == 13:
            mu_p +=1 # count the anti muons 
            mu_p_idx = idx # update the index if an event is dimuon then this index will not be updated
        elif id_ == -13:
            mu_n += 1 # count the muons
            mu_n_idx = idx # update the index if an event is dimuon then this index will not be updated
        elif id_ == 54:
            phi += 1 # count the phi particles 
            phi_idx = idx # keep track of  their index
        else: continue 
    #
    if (mu_p, mu_n, phi) == (1, 1, 1) :
        return (True, mu_p_idx, mu_n_idx, phi_idx)
    else:
        return (False, None, None, None) 
#
## Import the tree--------------------------------------------------------------------------------------------------------
tree_path='~/UG_thesis/Thesis/Analysis/MC_Samples/WPhi_2mu_M-100_S_TuneCP5_madgraph-pythia8/'
FileName=tree_path+"analysisTree_hadd1of1.root";#read the root file
treeName="tree";
RFile = ROOT.TFile.Open(FileName)
DIR = RFile.GetDirectory("rootTupleTreeVeryLoose")
DIR.cd()
tree=DIR.Get(treeName)
##Main Event loop---------------------------------------------------------------------------------------------------------
k = 0
muon_mass_hist = ROOT.TH1D("muon_mass_hist", "muon_mass_hist", 50, 50, 110) #create a hist object
muons = []
for entry in tree:
    evnt_id = entry.GenPromptParticlePdgId # get the particle ids of each event
    #if k ==10: break
    dimuon, id_mup, id_mun, id_phi = is_dimuon(evnt_id)
    if dimuon: # we are interested only in dimuon evens comming from a phi particle 
        muon0 = ROOT.TLorentzVector()
        muon1 = ROOT.TLorentzVector()
        #print(evnt_id)
        Pt = entry.GenPromptParticlePt
        Eta = entry.GenPromptParticleEta
        Phi = entry.GenPromptParticlePhi
        Nrg = entry.GenPromptParticleEnergy
        #
        muon0.SetPtEtaPhiE(Pt[id_mup], Eta[id_mup], Phi[id_mup], Nrg[id_mup])
        muon1.SetPtEtaPhiE(Pt[id_mun], Eta[id_mun], Phi[id_mun], Nrg[id_mun] )
        #
        muons.append(
            [Pt[id_mup], Eta[id_mup], Phi[id_mup], Nrg[id_mup],
             Pt[id_mun], Eta[id_mun], Phi[id_mun], Nrg[id_mun]]
        )
        #
        dimuon_pair = muon0 + muon1
        dimuonMass = dimuon_pair.M()
        muon_mass_hist.Fill(dimuonMass)
        #print(dimuonMass)
    #
    k+=1
#
muon_mass_hist.SetDirectory(0)
RFile.Close()
## Write the outputs -------------------------------------------------------------------------------------
# Write the histogram
outFileName = 'test.root'
outFile = ROOT.TFile.Open(outFileName ,"RECREATE")
outFile.cd()
muon_mass_hist.Write()
#outHistFile.Close()
#
# Write the momenta and energy of the dilepton events to a root file
tree_name = 'myTree'
myTree = ROOT.TTree(treeName, treeName)
num_branches= 8
#
bn= [
    ['Pt'+str(i), 'Eta'+str(i), 'Phi'+str(i), 'Energy'+str(i)]
    for i in (1,2)
]
branchName= bn[0]+bn[1]
print(branchName)
branches_vecs = [
    ROOT.vector("float")(0) for n in range(num_branches)
]#the values of those will be stored to branches
#
branches = [
    myTree.Branch(branchName[i], "std::vector<float>", branches_vecs[i])
    for i in range(num_branches)
]
#
num_data = len(muons)
for i in range(num_data):
    for j, branch in enumerate(branches_vecs):
        branch.clear()
        d = muons[i][j]
        #print('appending {}'.format(d))
        branch.push_back(d)
    #
    myTree.Fill()
#
#outFileName.cd()
myTree.Write()
outFile.Close()
#print('{} has been created'.format(outfileName))


