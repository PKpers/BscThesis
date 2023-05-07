import ROOT
from sys import argv
from os import chdir, getcwd
import numpy as np
from sklearn.model_selection import train_test_split
from WPhi_2mu_dataPrepXYZ import define_columns, LoadData
from WPhi_2mu_dataPrep import create_fnames, makeHist
from WPhi_2mu_Smear import Smear, Deltas, computeMass

np.random.seed(1)
## Configure input settings 
inPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
inName ="WPhiJets_M60M5080_Deltas.root"
inFile = inPath + inName

## Load data
df_sample = ROOT.RDataFrame("tree", inFile)

varNames = ["Pt1", "Pt2", "DeltaPhi", "DeltaR", "DeltaEta", "PairMass"]

## Split the signal in 3 parts. Testing Training Application
signal = df_sample.Filter("Label == 1")
signal = signal.AsNumpy()
signal = np.vstack([signal[var] for var in varNames]).T
np.random.shuffle(signal) #shuffle signal events

sig_len = signal.shape[0]
size = int(sig_len/3) # the size of each sig part
sig_app = signal[ : size ] # signal component of the application set 
sig_tt = signal[ size : ] # signal components of the train and testing set 
tt_size = sig_tt.shape[0] # the size of the train test set

## Split the background in 3 parts. Training Testing Application
background = df_sample.Filter("Label == 0")

background = background.AsNumpy()
background = np.vstack([background[var] for var in varNames]).T
np.random.shuffle(background) # shufle the background events

# Split the backgrounds
bkg_len = background.shape[0]
bkg_size = int(bkg_len / 3) # the size of each bkg part
bkg_app = background[ tt_size : ] # background component fo the application set
bkg_app = np.array( [ bkg_app[i] for i in range(0, bkg_app.shape[0], 3) ] )
bkg_tt = background[ : tt_size ]   # background components of train test sets. Same size as sig_tt

## group the train test data together 
SIG_BKG_TRAIN_TEST= ( 
    np.array( [sig_tt[i] for i in range(tt_size) if (i % 2) == 0 ] ), #sig_train
    np.array( [sig_tt[i] for i in range(tt_size) if (i % 2) != 0 ] ), #sig_test
    np.array( [bkg_tt[i] for i in range(tt_size) if (i % 2) == 0 ] ), #bkg_train
    np.array( [bkg_tt[i] for i in range(tt_size) if (i % 2) != 0 ] ), #bkg_test
)
print("Training signal events: ", SIG_BKG_TRAIN_TEST[0].shape[0])   
print("Training bkg events: ", SIG_BKG_TRAIN_TEST[2].shape[0])   
print("Testing signal events: ", SIG_BKG_TRAIN_TEST[1].shape[0])   
print("Testing bkg events: ", SIG_BKG_TRAIN_TEST[3].shape[0])   

## Configure output and write the splitted data to root files
outPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
outName = "WPhiJets_M60M5080Deltas"
treeName = 'tree'
label = ('SIG', 'BKG')
purpose = ('Train', 'Test')
outfiles = create_fnames(outPath, outName)
Files = []
for f in outfiles:
    Files.append(f[0])
    Files.append(f[1])
#end for

import sys
sys.path.insert(0, '/home/kpapad/UG_thesis/Thesis/share/lib')
from plotslib import create_legend, add_Header 
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
ROOT.gROOT.SetBatch(True)

outHistName = outName+"_Hist.pdf"
outHistFile = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Plots/" + outHistName
c = ROOT.TCanvas()
c.cd()
c.SaveAs(outHistFile+'[')

label=("Test  Signal", "Train Signal", "Test Background", "Train Background")
for i, data in enumerate(SIG_BKG_TRAIN_TEST):
    data = data.astype(np.float32)
    events = data.T
    print('Writting {} in {}'.format(treeName, Files[i]))
    
    vars_dict = define_columns(6, varNames, events)
    
    df = ROOT.RDF.MakeNumpyDataFrame(vars_dict)
    df.Snapshot(treeName, Files[i])
    
    #plot the mass histogram 
    hist=df.Histo1D(("hist", "; m_{\mu\mu} [GeV]", 50, 50, 75), "PairMass")
    hist.SetMarkerColor(1)
    hist.SetLineColor(1)
    hist.SetMarkerStyle(8)
    hist.SetMarkerSize(0.5)
    hist.Draw("PE")
    
    header = r'\phi \rightarrow \mu\mu'+str(" ")+str(label[i])
    add_Header(header)
    c.SaveAs(outHistFile)


#
c.SaveAs(outHistFile+"]")

## Write the application set to root files
outPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
outName = "WPhiJets_M60M5080Deltas_Application"
treeName = 'tree'

# Write the app bkg using testing bkg as well
bkg_app = np.vstack([bkg_app, SIG_BKG_TRAIN_TEST[-1]]).astype(np.float32)
vars_dict = define_columns(6, varNames, bkg_app.T)  
df = ROOT.RDF.MakeNumpyDataFrame(vars_dict)
df.Snapshot(treeName, outPath+outName+"_BKG_Test.root")
print("application bkg evens: ", df.Count().GetValue())

# Write the app sig using testing sig as well
#sig_app = np.vstack([sig_app, SIG_BKG_TRAIN_TEST[1]]).astype(np.float32)
vars_dict = define_columns(6, varNames, sig_app.T)  
df = ROOT.RDF.MakeNumpyDataFrame(vars_dict)
df.Snapshot(treeName, outPath+outName+"_SIG_Test.root")
print("application sig evens: ", df.Count().GetValue())
