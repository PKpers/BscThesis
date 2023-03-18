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
inName ="WPhi_2mu_M50Mixed_Deltas.root"
inFile = inPath + inName

## Load data
df_sample = ROOT.RDataFrame("tree", inFile)

## Split the background in 3 parts. Training Testing Application
varNames = ["Pt1", "Pt2", "DeltaPhi", "DeltaR", "DeltaEta", "PairMass"]
background = df_sample.Filter("Label == 0")
print("Background samples: {}".format(background.Count().GetValue()))
# shufle the background events
background = background.AsNumpy()
background = np.vstack([background[var] for var in varNames]).T
np.random.shuffle(background)

# Split the backgrounds
bkg_len = background.shape[0]
size = int(bkg_len / 3) # the size of each bkg part

bkg_app = background[ : size]
print("Application bkg samples {}".format(bkg_app.shape[0]))
bkg_tt = background[ size : ]
print("Train and Test bkg samples {}".format(bkg_tt.shape[0]))

## Split the signal in 3 parts. Testing Trining Application
# Application. We get the application from the MC sample
signal_app = df_sample.Filter("Label == 1")
counts_app = signal_app.Count()
print("Application signal events: {}".format(counts_app.GetValue()))

# Training and Testing. We get the train test sampe from the rest of the signal MC  
# The first 800 events were used for the application set.
df_sig = ROOT.RDataFrame("tree", inPath+"WPhi_2mu_M50Data.root").Range(801, 0)

Vars = ['Pt1_Smeared', 'Eta1', 'Phi1', 'Pt2_Smeared', 'Eta2', 'Phi2']
signal = Smear(df_sig, 0.17)
signal = computeMass(signal, Vars)
signal = Deltas(signal, Vars)

num_signal = signal.Count().GetValue()
print("Signal samples left for train test: {}".format(num_signal))
signal = signal.AsNumpy()

## Split the data 
signal = np.vstack([signal[var] for var in varNames]).T
np.random.shuffle(signal)
np.random.shuffle(bkg_tt)

#group the train test data together 
SIG_BKG_TRAIN_TEST= ( 
    np.array( [signal[i] for i in range(signal.shape[0]) if (i % 2) == 0 ] ), #sig_train
    np.array( [signal[i] for i in range(signal.shape[0]) if (i % 2) != 0 ] ), #sig_test
    np.array( [bkg_tt[i] for i in range(bkg_tt.shape[0]) if (i % 2) == 0 ] ), #sig_train
    np.array( [bkg_tt[i] for i in range(bkg_tt.shape[0]) if (i % 2) != 0 ] ), #sig_train
)

    
## Configure output and write the splitted data to root files
outPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
outName = "WPhi_2mu_M50MixedDeltas"
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
    hist=df.Histo1D(("hist", "; m_{\mu\mu} [GeV]", 50, 21, 119), "PairMass")
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
outName = "WPhi_2mu_M50MixedDeltas_Application"
treeName = 'tree'

#Write the app bkg
vars_dict = define_columns(6, varNames, bkg_app)  
df = ROOT.RDF.MakeNumpyDataFrame(vars_dict)
df.Snapshot(treeName, outPath+outName+"_BKG_Test.root")

#Write the app signal
signal_app.Snapshot(treeName, outPath+outName+"_SIG_Test.root")



