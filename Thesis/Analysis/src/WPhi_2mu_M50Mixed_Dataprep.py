import ROOT
from sys import argv
from os import chdir, getcwd
import numpy as np
from sklearn.model_selection import train_test_split
from WPhi_2mu_dataPrepXYZ import define_columns, LoadData
from WPhi_2mu_Smear import Smear, Deltas, computeMass

## Load data 
inDir = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
bkg_files = [ inDir + "WPhi_2mu_M{}Data.root".format(str(i)) for i in [20, 30, 70, 80, 100, 125, 150] ]
sig_file = inDir + "WPhi_2mu_M50Data.root"
data_files = bkg_files + [sig_file]

## Compose a continous smeared background by the individual MCs 
background = []
Vars = ['Pt1_Smeared', 'Eta1', 'Phi1', 'Pt2_Smeared', 'Eta2', 'Phi2']
varNamesDelta = ["Pt1", "Pt2", "DeltaPhi", "DeltaR", "DeltaEta", "PairMass"]
Pt1, Pt2, DeltaPhi, DeltaR, DeltaEta, DimuonMass, Label = [[] for i in range(7)]

for i, f in enumerate(data_files):
    varNames = Vars
    smear = 0.9
    label = 0 # 0 for background 1 for signal
    
    if i == 0 or i ==  1:
        df = ROOT.RDataFrame("tree", f).Range(0, 3500)
        #
    elif i == len(data_files) -1 :
        df = ROOT.RDataFrame("tree", f).Range(800)
        smear = 0.17
        label = 1
    else:
        df = ROOT.RDataFrame("tree", f)
    #
    num_events = df.Count().GetValue()
    print(num_events)
    
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
outName = "WPhi_2mu_M50Mixed_Deltas2.root"

data = np.vstack([Pt1, Pt2, DeltaPhi, DeltaEta, DeltaR, DimuonMass, Label])
varNames = ["Pt1", "Pt2", "DeltaPhi", "DeltaR", "DeltaEta", "PairMass", "Label"]
vars_dict = define_columns(7, varNames, data)


df_data = ROOT.RDF.MakeNumpyDataFrame(vars_dict)\
    .Filter("PairMass > 20")\
    .Filter("PairMass < 119")\
    .Snapshot("tree", outPath + outName)
#
import sys
sys.path.insert(0, '/home/kpapad/UG_thesis/Thesis/share/lib')
from plotslib import create_legend, add_Header 
data_hist = df_data\
              .Histo1D(("data_hist", "; m_{\mu\mu} [GeV]", 50, 21, 119), "PairMass")
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
header = r'\phi \rightarrow \mu\mu'
add_Header(header)

c.SaveAs("/home/kpapad/UG_thesis/Thesis/Analysis/out/Plots/WPhi_2mu_M50Mixed_Deltas2_Mass.pdf")
