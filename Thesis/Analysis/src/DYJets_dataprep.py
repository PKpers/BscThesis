import ROOT
from sys import argv
from os import chdir, getcwd
import numpy as np
from sklearn.model_selection import train_test_split
from WPhi_2mu_dataPrepXYZ import define_columns, LoadData
from WPhi_2mu_Smear import Smear, Deltas, computeMass

## Load data 
inDir = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
bkg_files =[ inDir + "WPhi_2mu_M{}Data.root".format(str(i)) for i in [150, 40, 30, 20, 10, 5] ]
bkg_files += [ inDir + "DYJets_M{}Data.root".format(str(i)) for i in [50] ]
sig_file = inDir + "WPhi_2mu_M60Data.root"
data_files =  [sig_file] + bkg_files 

## Compose a continous smeared background by the individual MCs 
background = []
Vars = ['Pt1_Smeared', 'Eta1', 'Phi1', 'Pt2_Smeared', 'Eta2', 'Phi2']
varNamesDelta = ["Pt1_Smeared", "Pt2_Smeared", "DeltaPhi", "DeltaR", "DeltaEta", "PairMass"]
Pt1, Pt2, DeltaPhi, DeltaR, DeltaEta, DimuonMass, Label = [[] for i in range(7)]

for i, f in enumerate(data_files):
    varNames = Vars
    smear = 2
    label = 0 # 0 for background 1 for signal
    if i == 0:
        smear = 0.1
        label = 1
        df = ROOT.RDataFrame("tree", f).Range(1250)
    else:
        df = ROOT.RDataFrame("tree", f)
    #
    df = Smear(df, smear)# smear the background by 30%
    df = computeMass(df, varNames) # Compute the smeared mass
    df = Deltas(df, varNames) # Transformed the smeared Pts etas and phis to Deltas 
    df = df.AsNumpy()

    pt1, pt2, dphi, deta, dr, m =[ df[var] for var in varNamesDelta]
    Pt1.append(pt1)
    Pt2.append(pt2)
    DeltaPhi.append(dphi)
    DeltaEta.append(deta)
    DeltaR.append(dr)
    DimuonMass.append(m)
    Label.append([label for i in pt1]) 
#
Pt1 = np.hstack(Pt1).astype(np.float32)
Pt2 = np.hstack(Pt2).astype(np.float32)
DeltaPhi = np.hstack(DeltaPhi).astype(np.float32)
DeltaEta = np.hstack(DeltaEta).astype(np.float32)
DeltaR = np.hstack(DeltaR).astype(np.float32)
DimuonMass = np.hstack(DimuonMass).astype(np.float32)
Label = np.hstack(Label).astype(np.float32)

## Save the data in a root file
outPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
outName = "WPhiJets_M60Mixed_Deltas.root"

data = np.vstack([Pt1, Pt2, DeltaPhi, DeltaEta, DeltaR, DimuonMass, Label])
varNames = ["Pt1", "Pt2", "DeltaPhi", "DeltaR", "DeltaEta", "PairMass", "Label"]
vars_dict = define_columns(7, varNames, data)


df_data = ROOT.RDF.MakeNumpyDataFrame(vars_dict)\
    .Filter("PairMass > 16")\
    .Filter("PairMass < 130")\
    .Snapshot("tree", outPath + outName)
#
bkg_counts = df_data.Filter("Label == 0").Count().GetValue()
sig_counts = df_data.Filter("Label == 1").Count().GetValue()
print("background events: ", bkg_counts)
print("Signal events: ", sig_counts)
import sys
sys.path.insert(0, '/home/kpapad/UG_thesis/Thesis/share/lib')
from plotslib import create_legend, add_Header 
data_hist = df_data\
              .Histo1D(("data_hist", "; m_{\mu\mu} [GeV]", 50, 16, 130), "PairMass")
#
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
ROOT.gROOT.SetBatch(True)
#
c = ROOT.TCanvas()
c.cd()
data_hist.SetMarkerColor(1)
data_hist.SetLineColor(1)
data_hist.SetMarkerStyle(8)
data_hist.SetMarkerSize(0.5)
data_hist.Draw('PE')
header = r'\mu\mu'
add_Header(header)

c.SaveAs("/home/kpapad/UG_thesis/Thesis/Analysis/out/Plots/DYJets_test.pdf")
