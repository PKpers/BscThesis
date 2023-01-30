import ROOT
import sys
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

def define_columns(num_columns, var_names, var):
    '''
    defince the variables of data frame
    '''
    import numpy as np
    vars_ = {}
    for i in range(num_columns):
        vars_[var_names[i]] = np.array(var[i])
    #
    return vars_

## Import the tree--------------------------------------------------------------------------------------------------------
if __name__=='__main__':
    # Help message
    if len(sys.argv) != 3:
        print("Usage: {} {} {}".format(sys.argv[0], ' input_directory', 'output_name'))
        exit(-1)
    # 
    inDir = sys.argv[1]
    inFileName=inDir+"/analysisTree_hadd1of1.root";#read the root file
    treeName="tree";
    RFile = ROOT.TFile.Open(inFileName)
    DIR = RFile.GetDirectory("rootTupleTreeVeryLoose")
    DIR.cd()
    tree=DIR.Get(treeName)
    ##Main Event loop--------------------------------------------------------------------------------------------
    k = 0
    # Get the simulated mass from dir name. We need it to automatically set the limits of the hist
    Mass=int(inDir.split('-')[1].split('_')[0])
    muon_mass_hist = ROOT.TH1D("muon_mass_hist", "", 50, Mass-Mass/2, Mass+10 ) 
    muons = []
    for entry in tree:
        evnt_id = entry.GenPromptParticlePdgId # get the particle ids of each event
        dimuon, id_mup, id_mun, id_phi = is_dimuon(evnt_id)
        if dimuon: # we are interested only in dimuon evens comming from a phi particle 
            muon0 = ROOT.TLorentzVector()
            muon1 = ROOT.TLorentzVector()

            Pt = entry.GenPromptParticlePt
            Eta = entry.GenPromptParticleEta
            Phi = entry.GenPromptParticlePhi
            Nrg = entry.GenPromptParticleEnergy

            muon0.SetPtEtaPhiE(Pt[id_mup], Eta[id_mup], Phi[id_mup], Nrg[id_mup])
            muon1.SetPtEtaPhiE(Pt[id_mun], Eta[id_mun], Phi[id_mun], Nrg[id_mun] )

            muons.append(
                [Pt[id_mup], Eta[id_mup], Phi[id_mup], Nrg[id_mup],
                 Pt[id_mun], Eta[id_mun], Phi[id_mun], Nrg[id_mun]]
            )

            dimuon_pair = muon0 + muon1
            dimuonMass = dimuon_pair.M()
            muon_mass_hist.Fill(dimuonMass)
        else: continue
        k+=1
    #
    muon_mass_hist.SetDirectory(0)
    RFile.Close()
    ## Write the outputs -------------------------------------------------------------------------------------
    # Write the histogram
    outFileName = sys.argv[2]
    #
    outFilePath = '/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/' 
    outHistFile = ROOT.TFile.Open(outFilePath+outFileName+'Hist.root' ,"RECREATE")
    outHistFile.cd()
    print('Writting {} to {}'.format('dimuon mass hist', outFilePath+outFileName+'Hist.root'))
    muon_mass_hist.Write()
    outHistFile.Close()
    # Write the momenta and energy of the dilepton events to a root file
    tree_name = 'myTree'
    myTree = ROOT.TTree(treeName, treeName)
    num_branches= len(muons[0])
    #
    bn= [
        ['Pt'+str(i), 'Eta'+str(i), 'Phi'+str(i), 'Energy'+str(i)]
        for i in (1,2)
    ]
    branchName= bn[0]+bn[1]
    print('Writting {} to {} at {}'.format(branchName, tree_name, outFilePath+outFileName+'Data.root'))
    
    #branches_vecs = [
     #   ROOT.vector("float")(0) for n in range(num_branches)
    #]#the values of those will be stored to branches
    muons = np.array(muons, dtype=np.float32).T # from [[event 1], [event2], ...] to [[px], [py], ...]]
    branches = define_columns(num_branches, branchName, muons)
    
    df = ROOT.RDF.MakeNumpyDataFrame(branches)\
                 .Snapshot('tree', outFilePath+outFileName+'Data.root')




















    '''
    num_data = muons.shape[1]
    print('Im starting with the branches')
    branches_vecs = [
        np.zeros((num_data,), dtype=np.float32)
        for i in range(num_branches)
    ]

    branches = [
        myTree.Branch(branchName[i], branches_vecs[i], branchName[i]+'[{}]/F'.format(num_data))
        for i in range(num_branches)
    ]
    print('im done with the branches')
    for i in range(num_branches):
        for j in range(num_data):
            variable = muons[i]
            branches_vecs[i][j] = variable[j]
            myTree.Fill()
        #
    #
    print('Im starting with filling the tree')
    #for n in range(num_data):
    #
    #outFileName.cd()
    print('im starting to write')
    myTree.Write()
    #outFile.Write()
    outFile.Close()
    print('im done')
    exit(-1)
    #print('{} has been created'.format(outfileName))
        for i in range(num_data):
        for j, branch in enumerate(branches_vecs):
            branch.clear()
            d = muons[i][j]
            #print('appending {}'.format(d))
            branch.push_back(d)
        #
    '''

