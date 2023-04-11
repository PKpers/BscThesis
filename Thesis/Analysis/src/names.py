import ROOT

inPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
bkgName = "WPhi_2mu_M50MixedDeltas_Application_BKG_Test.root"
bkgFile = inPath + bkgName 


outNames = [
    "WPhi_2mu_M50MixedDeltas_Application_Smeared{}_BKG_Test.root".format(n)
    for n in [10, 15, 25, 50]
]
outFiles = [inPath + filename for filename in outNames]

df = ROOT.RDataFrame("tree", bkgFile)
for out in outFiles:
    print("saving data set in {}".format(out))
    df.Snapshot("tree", out)
#


