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

def Smear(df, percentage, seed):
    #rand = ROOT.TRandom()
    #rand.SetSeed(seed)
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
inName = "WPhi_2mu_M50MixedDeltas_Application_SIG_Test.root"
treeName = 'tree'
inFile = inPath + inName

## Configure output settings 
outPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/"
#
outHistName = "Plots/test_small_stat.pdf"
outHistFile = outPath + outHistName

## Load data
Vars = ['Pt1_Smeared', 'Eta1', 'Phi1', 'Pt2_Smeared', 'Eta2', 'Phi2']
varNamesDelta = ["Pt1", "Pt2", "DeltaPhi", "DeltaR", "DeltaEta", "PairMass"]
df = ROOT.RDataFrame(treeName, inFile)

test_var = df.Display().AsString()
print(test_var)
bool_ = "Pt1" in test_var
print(bool_)
vars_original = ("Pt1", "Pt2")
vars_alias = ("Pt1_Smeared", "Pt2_Smeared")

for i, var in enumerate(vars_original):
    df = df.Alias(vars_alias[i], var) if var in test_var else df
#
df_f = df.Filter("Pt1_Smeared > 3").Display().Print()
exit()







df = df.Define('testM1', 'sqrt(2 * Pt1 * Pt2* (cosh(DeltaEta) - cos(DeltaPhi)))')

c = ROOT.TCanvas()
c.cd()
c.SaveAs(outHistFile + "[")

hist = df.Histo1D(("hist", "; m_{\mu\mu} [GeV]", 50, 0, 119), "testM1")
hist.SetMarkerColor(1)
hist.SetLineColor(1)
hist.SetMarkerStyle(8)
hist.SetMarkerSize(0.5)
hist.Draw("PE")

## Fit 1
gaus1 = ROOT.TF1( 'fs', '[0]*exp(-0.5*((x-[1])/[2])**2)',  0, 119 )
gaus1.SetParameter(1,42)
gaus1.SetParameter(2,10)
gaus1.SetLineColor(2)
fit1 = hist.Fit( gaus1, 'LRS' )

header = r'\phi \rightarrow \mu\mu'
add_Header(header)
c.SaveAs(outHistFile)

## Fit2
df2 = Smear(df, 0.5, 1)
df2 = df2.Define('testM2', 'sqrt(2 * Pt1_Smeared * Pt2_Smeared* (cosh(DeltaEta) - cos(DeltaPhi)))')

hist2 = df2.Histo1D(("hist2", "; m_{\mu\mu} [GeV]", 50, 0, 119), "testM2")
hist2.SetMarkerColor(1)
hist2.SetLineColor(1)
hist2.SetMarkerStyle(8)
hist2.SetMarkerSize(0.5)
hist2.Draw("PE")

gaus2 = ROOT.TF1( 'fs', '[0]*exp(-0.5*((x-[1])/[2])**2)',  0, 119 )
gaus2.SetParameter(1,45)
gaus2.SetParameter(2,10)
gaus2.SetLineColor(2)
fit2 = hist2.Fit( gaus2, 'LRS' )

header = r'\phi \rightarrow \mu\mu'
add_Header(header)
c.SaveAs(outHistFile)

#

c.SaveAs(outHistFile + "]")

exit()
