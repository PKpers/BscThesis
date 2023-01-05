import ROOT
ROOT.gROOT.SetBatch(True)

treefile  = ROOT.TFile.Open('test.root','RECREATE')
tree      = ROOT.TTree('mytree','mytree')
myvalue1_ = ROOT.vector('float')(0)
myvalue2_ = ROOT.vector('int')(0)
#
tree.Branch("MyValue1", "std::vector<float>", myvalue1_)
tree.Branch("MyValue2", "std::vector<int>",   myvalue2_)
#
for i in range(1,11):
    myvalue1_.clear()
    myvalue2_.clear()
    #
    print(i)
    #
    if    i==5   : n=4
    elif  i==2   : n=0
    else         : n=1
    #
    for j in range(n):
        r=ROOT.TRandom3(0)
        x=r.Uniform(0,1)
        myvalue1_.push_back(x)
        myvalue2_.push_back(int(i))
    #
    tree.Fill()
#
treefile.cd()
tree.Write()
treefile.Close()
exit()
