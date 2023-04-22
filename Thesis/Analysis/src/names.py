import ROOT

inPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
bkgName = "WPhiJets_M200M100300Deltas_Application_BKG_Test.root"
bkgFile = inPath + bkgName 


outNames = [
    "WPhiJets_M200M100300Deltas_Application_Smeared{}_BKG_Test.root".format(n)
    for n in [30, 40]
]
outFiles = [inPath + filename for filename in outNames]

df = ROOT.RDataFrame("tree", bkgFile)
for out in outFiles:
    print("saving data set in {}".format(out))
    df.Snapshot("tree", out)
#


