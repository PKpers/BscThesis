import ROOT
from sys import argv
from os import chdir, getcwd
import numpy as np
from sklearn.model_selection import train_test_split
from WPhi_2mu_dataPrepXYZ import define_columns, LoadData
from WPhi_2mu_dataPrep import create_fnames, makeHist
from WPhi_2mu_Smear import Smear, Deltas, computeMass
import sys
sys.path.insert(0, '/home/kpapad/UG_thesis/Thesis/share/lib')
from plotslib import create_legend, add_Header 
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
ROOT.gROOT.SetBatch(True)

np.random.seed(1)

## Configure input settings 
inPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
inName = "WPhi_2mu_M50MixedDeltas_Application"
treeName = 'tree'
inFile = inPath + inName

## Configure output settings 
outPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Plots/"
outName = "WPhi_2mu_M50MixedDeltas_Application_Hist.pdf"
outHistFile = outPath + outName

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

