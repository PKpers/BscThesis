def create_tree(treeName, outfileName, num_branches, branchName, data):
    '''
    creates a tree named, treeName, and stores it to outfileName.root.
    number of branches: num_branches, float
    name of the branches: branchName, list
    data to store: data, list of dimention num_branches
    '''
    import ROOT 
    if '.root' not in outfileName: #ensure that the we are creating a root file
        outfileName+='.root'
        #
    outfile = ROOT.TFile.Open(outfileName, 'RECREATE')
    tree1 = ROOT.TTree(treeName, treeName)
    branches_vecs = [ROOT.vector("float")(0) for n in range(num_branches)]#the values of those will be stored to branches
    #
    branches = [
        tree1.Branch(branchName[i], "std::vector<float>", branches_vecs[i])
        for i in range(num_branches)
    ]
    #
    num_data = len(data[0])
    #print(num_data)
    for i in range(num_data):
        for j, branch in enumerate(branches_vecs):
            branch.clear()
            d = data[j][i]
            print('appending {}'.format(d))
            branch.push_back(d)
        #
        tree1.Fill()
    #
    outfile.cd()
    tree1.Write()
    outfile.Close()
    print('{} has been created'.format(outfileName))
    return  
