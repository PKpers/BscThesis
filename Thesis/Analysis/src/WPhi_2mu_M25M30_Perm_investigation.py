import ROOT 
import sys
from sys import argv
from os import chdir, getcwd
import numpy as np
from sklearn.model_selection import train_test_split
from WPhi_2mu_dataPrepXYZ import define_columns, create_fnames, Pxyz, LoadData
from WPhi_2mu_makepermute import configure_output, pair_permute
sys.path.insert(0, '/home/kpapad/UG_thesis/Thesis/share/lib')
from plotslib import set_axes_title, PlotHist, create_legend, add_Header, set_axes_range
# include custom c libraries
workingDIR = getcwd()
chdir('/home/kpapad/UG_thesis/Thesis/Analysis/lib/')
ROOT.gInterpreter.ProcessLine('#include "funcy.h"')
chdir(workingDIR)


## Import the data 
fileDir = "/home/kpapad/UG_thesis/Thesis/share/Predictions/"
fileName ="WPhi_2mu_M25M30_Smear30DeltasPredScoreData.root" 
inFile = fileDir + fileName

## Filter out irrelevant evetns | keep only those with bdt score <0.1
events = ROOT.RDataFrame("myTree", inFile)
num = events.Count()
signal = events.Filter("yRef_pred > 0.80")
signal_false =events.Filter("yRef_pred > 0.99") 
signal_pass = signal.Count().GetValue()
false_pass = signal_false.Count().GetValue()
print("{} signal events passed the filter".format(signal_pass))
print("{} false signal events passed the filter".format(false_pass))

## Plot the invariant mass of the passed events
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)

c = ROOT.TCanvas()
c.SetLogy(1)

signal_mass = signal.Define('sigMass', 'sqrt(2 * Pt1 * Pt2 * (cosh(DeltaEta) - cos(DeltaPhi)) )')\
                    .Histo1D(('signal_mass', "", 50, 1, 45), "sigMass")
#
signal_mass.SetLineColor(3)
Fsignal_mass = signal_false.Define('falseMass', 'sqrt(2 * Pt1 * Pt2 * (cosh(DeltaEta) - cos(DeltaPhi)) )')\
                     .Histo1D(('Fsignal_mass', "", 50, 1, 45), "falseMass")
#

Fsignal_mass.SetLineColor(2)
entriesLedg = {
     'signal_mass' : ('Signal ', 'l') ,
     'Fsignal_mass' : ('Flase signal', 'l') 
}

signal_mass.Draw()
Fsignal_mass.Draw('same')
set_axes_title(signal_mass, "GeV", "Counts")

legend = create_legend((0.6, 0.3, 0.7, 0.4), entriesLedg )
add_Header("Signal like BKG events ")
c.SaveAs('WPhi_2mu_M25M30_smeared30_inv.pdf')
exit()



events = events.Define("coupled",
        """
        coup(
        Px1Px1, Py1Py1, Pz1Pz1, 
        Px2Px2, Py2Py2, Pz2Pz2, 
        Px1Px2, Py1Py2, Pz1Pz2 
        )"""
)
        
events = events.Define("Cart1",
                    """
                   ROOT::Math::PxPyPzMVector(
                   TMath::Sqrt(Px1Px1),
                   TMath::Sqrt(Py1Py1),
                   TMath::Sqrt(Pz1Pz1),
                   0)
                   """
)
events = events.Define("Cart2",
                   """
                   ROOT::Math::PxPyPzMVector(
                   TMath::Sqrt(Px2Px2),
                   TMath::Sqrt(Py2Py2),
                   TMath::Sqrt(Pz2Pz2),
                   0)
                   """
)

events = events.Define('nrg', "(Cart1+Cart2).E()")
    
evetns = events.Define('Ptot', 'computeMomentumTot(coupled)')
events = events.Define("SumP", "Px1Px2 + Py1Py2 + Pz1Pz2")
events = events.Define('nlt', "computeProductsSQ(coupled)")
events = events.Define('enrg2', "TMath::Sqrt(SumP + 2*nlt)")
#
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)

c = ROOT.TCanvas()
c.SaveAs('WPhi_2mu_M25M30_Perm_inv.pdf[')

nltH = events.Histo1D(('nltH', "", 50, 0, 10000), "nlt")
set_axes_title(nltH, "GeV^{2}", "Counts")
nltH.SetLineStyle(2)

sumPH = events.Histo1D(('sumPH', "", 50, 0, 10000), "SumP")
sumPH.SetMarkerColor(3)
entriesLedg = {
     'nltH' : ('|#vec{P_{l1}}| |#vec{P_{l2}}| \n', 'l') ,
     'sumPH' : ('#vec{P_{l1}} #vec{P_{l2}}', 'l') 
}
nltH.Draw()
sumPH.Draw('same')
legend = create_legend((0.6, 0.3, 0.7, 0.4), entriesLedg )
add_Header("Comparison of the non linear and linear term")
c.SaveAs('WPhi_2mu_M25M30_Perm_inv.pdf')

nltH.GetXaxis().SetRangeUser(1, 3000)
#c.SetLogx(1)
c.SaveAs('WPhi_2mu_M25M30_Perm_inv.pdf')
c.SaveAs('WPhi_2mu_M25M30_Perm_inv.pdf]')
