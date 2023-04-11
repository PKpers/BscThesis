import ROOT
from sys import argv
from os import chdir, getcwd
import numpy as np
from sklearn.model_selection import train_test_split
from WPhi_2mu_dataPrepXYZ import define_columns, LoadData
from WPhi_2mu_dataPrep import create_fnames, makeHist
from WPhi_2mu_Smear import Deltas, computeMass
import sys
sys.path.insert(0, '/home/kpapad/UG_thesis/Thesis/share/lib')
from plotslib import create_legend, add_Header 
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
ROOT.gROOT.SetBatch(True)

np.random.seed(1)
def Smear(df, percentage):
    ROOT.gInterpreter.Declare('''
    float smear(float var, float percentage, int seed ){
            TRandom *rand = new TRandom();
            rand->SetSeed(seed);
            float smeared = var * rand->Gaus(1, percentage);
           return smeared;
    }
    ''')
    df = df.Define('Pt1_Smeared', "smear({}, {}, {})".format("Pt1", percentage, 0))\
           .Define('Pt2_Smeared', "smear({}, {}, {})".format("Pt2", percentage, 0))
    
    #
    return df

## Configure input settings 
inPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
inName = "WPhiJets_M60MixedDeltas_Application_SIG_Test.root"
treeName = 'tree'
inFile = inPath + inName

## Configure output settings 
outPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/"
outName = "Data/WPhiJets_M60MixedDeltas_Application_Smeared60_SIG_Test.root"
outFile = outPath + outName
#
outHistName = "Plots/WPhiJets_M60MixedDeltas_Application_SIG_Smeared60_Hist.pdf"
outHistFile = outPath + outHistName

## Smear the data and save the output
df = ROOT.RDataFrame(treeName, inFile)

varNames = [
    "Pt1", "Pt2", "DeltaPhi", "DeltaR", "DeltaEta", "PairMass", "Label"
]
df_smeared = Smear(df, 0.60)\
    .Redefine('PairMass', 'sqrt(2 * Pt1_Smeared * Pt2_Smeared* (cosh(DeltaEta) - cos(DeltaPhi)))')\
    .Redefine("Pt1", "Pt1_Smeared")\
    .Redefine("Pt2", "Pt2_Smeared")\
    .Snapshot("tree", outFile, {v for v in varNames if v != "Label"})
#

## Plot the Mass histogram
c = ROOT.TCanvas()
c.cd()
c.SaveAs(outHistFile+"[")

hist = df_smeared.Histo1D(("hist", "; m_{\mu\mu} [GeV]", 50, 20, 119), "PairMass")
hist.SetMarkerColor(1)
hist.SetLineColor(1)
hist.SetMarkerStyle(8)
hist.SetMarkerSize(0.5)
hist.Draw("PE")
header = r'\phi \rightarrow \mu\mu'
add_Header(header)
c.SaveAs(outHistFile)

c.SaveAs(outHistFile + "]")
exit()
df_sig = df_smeared.Filter("Label == 1")\
                .Histo1D(("df_hist", "; m_{\mu\mu} [GeV]", 50, 21, 119), "PairMass_smeared")
#
#df_sig.SetMarkerColor(1)
df_sig.SetLineColor(3)
df_sig.SetMarkerStyle(8)
df_sig.SetMarkerSize(0.5)
df_sig.Draw("PE")

c.SaveAs(outHistFile)
c.SaveAs(outHistFile + "]")
exit()










'''
signal = df.Filter("Label == 1")
#

smeared_signal = Smear(signal, 0.25, 0)\
    .Define('PairMass_smeared', 'sqrt(2 * Pt1_Smeared * Pt2_Smeared* (cosh(DeltaEta) - cos(DeltaPhi)))')\
    .AsNumpy()
#
background = df.Filter("Label == 0").AsNumpy()
smeared_background = Smear(background, 0.25, 0)\

varNames_bkg = ["Pt1", "Pt2", "DeltaPhi", "DeltaR", "DeltaEta", "PairMass", "Label"]
varNames_sig = [
    "Pt1_Smeared", "Pt2_Smeared", "DeltaPhi", "DeltaR", "DeltaEta", "PairMass_smeared", "Label"
]


pt1_s, pt2_s, dphi_s, deta_s, dr_s, ms, ls  = np.vstack(
    [smeared_signal[var].astype(np.float32) for var in varNames_sig]
)
pt1_b, pt2_b, dphi_b, deta_b, dr_b, mb, lb  = np.vstack(
    [background[var].astype(np.float32) for var in varNames_bkg]
)

Pt1 = np.hstack([pt1_s, pt1_b])
Pt2 = np.hstack([pt2_s, pt2_b])
DeltaPhi = np.hstack([dphi_s, dphi_b])
DeltaEta = np.hstack([deta_s, deta_b])
DeltaR = np.hstack([dr_s, dr_b])
DimuonMass = np.hstack([ms, mb])
Label = np.hstack([ls, lb])

data = np.vstack([Pt1, Pt2, DeltaPhi, DeltaEta, DeltaR, DimuonMass, Label])
varNames = ["Pt1", "Pt2", "DeltaPhi", "DeltaR", "DeltaEta", "PairMass", "Label"]
vars_dict = define_columns(7, varNames, data)

df_data = ROOT.RDF.MakeNumpyDataFrame(vars_dict).Snapshot("tree", outFile)
'''

## This part is only for the application set.
## Load data
sigName = inFile + "_SIG_Test.root"
bkgName = inFile + "_BKG_Test.root"

c = ROOT.TCanvas()
c.cd()

hist = ROOT.RDataFrame(treeName, {sigName, bkgName})\
         .Histo1D(("hist", "; m_{\mu\mu} [GeV]", 50, 21, 119), "PairMass")
#
hist.SetMarkerColor(1)
hist.SetLineColor(1)
hist.SetMarkerStyle(8)
hist.SetMarkerSize(0.5)
hist.Draw("PE")

header = r'\phi \rightarrow \mu\mu'
add_Header(header)
c.SaveAs(outHistFile)
exit()

