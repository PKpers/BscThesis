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

nPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
sigName = "WPhiJets_M200M100300Deltas_Application_SIG_Test.root"
bkgName = "WPhiJets_M200M100300Deltas_Application_BKG_Test.root"
sigFile,bkgFile = [inPath + inName for inName in (sigName, bkgName)]
#bkgFile = inPath + bkgName 

## Configure the output settings
outPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Plots/"
outName = "testtesttest.pdf"
outFile = outName



## Make the plot 
c = ROOT.TCanvas()
c.cd()
c.SetLogy(1)
c.SaveAs(outFile+'[')
#ROOT.gStyle.SetOptFit(11);
df_data = ROOT.RDataFrame("tree", {sigFile, bkgFile})
#df_data = ROOT.RDataFrame("tree", bkgFile)
smeared_vars = ("Pt1_Smeared", "Pt2_Smeared", "PairMass_smeared")
alias = ("Pt1", "Pt2", "PairMass")

# alias Pt_smeared and Mass_smeared with Pt and PairMass, if needed   
df_data = aliases(df_data, smeared_vars, alias)\
    .Define("weights", "1/(abs(300-100)/200)")\
    .Histo1D(("df_data", "; m_{\mu\mu} [GeV]", 200, 100, 300), "PairMass", "weights")
#

# normalize the hist such that integrating over the bins gives the total number of events
binWidth = df_data.GetXaxis().GetBinWidth(1)
print(binWidth)
#df_data.Scale(1 / binWidth)
df_data.SetMarkerColor(1)
df_data.SetLineColor(1)
df_data.SetMarkerStyle(8)
df_data.SetMarkerSize(0.5)
df_data.Draw("PE")



exit()







