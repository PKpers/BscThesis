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

## Confiugre input settings
Path = "/home/kpapad/UG_thesis/Thesis/Analysis/out/"
inName = "Data/WPhi_2mu_M50Mixed_Deltas_Smeared10.root"
inTree = "tree"
inFile = Path + inName

## Configure output settings
outHistName = "Plots/WPhi_2mu_M50Mixed_Deltas_Smeared10_Hist.pdf"
outHistFile = Path + outHistName

df_smeared = ROOT.RDataFrame(inTree, inFile)

c = ROOT.TCanvas()
c.cd()
c.SaveAs(outHistFile+"[")

hist = df_smeared.Histo1D(("hist", "; m_{\mu\mu} [GeV]", 50, 21, 119), "PairMass_smeared")
hist.SetMarkerColor(1)
hist.SetLineColor(1)
hist.SetMarkerStyle(8)
hist.SetMarkerSize(0.5)
hist.Draw("PE")
header = r'\phi \rightarrow \mu\mu'
add_Header(header)
c.SaveAs(outHistFile)

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
