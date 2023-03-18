import ROOT 
import sys
from sys import argv
from os import chdir, getcwd
import numpy as np
from sklearn.model_selection import train_test_split
from WPhi_2mu_dataPrepXYZ import define_columns, create_fnames, Pxyz, LoadData
from WPhi_2mu_makepermute import configure_output, pair_permute
sys.path.insert(0, '/home/kpapad/UG_thesis/Thesis/share/lib')
# include custom c libraries
workingDIR = getcwd()
chdir('/home/kpapad/UG_thesis/Thesis/Analysis/lib/')
ROOT.gInterpreter.ProcessLine('#include "funcy.h"')
chdir(workingDIR)

#
ROOT.gROOT.SetBatch(True)
#

def helpMessage():
    '''
    checks the number of arguments
    and print this help massage if they are not correct
    '''
    if len(argv) != 3:
        print('usage: {} {} {}'.format(argv[0], 'DataSetName', 'output' ))
        print('\nThe default output format will be of the form outputPxyz_purpose_label.root')
        print('purpose: Testing/Training \nlabel: SIG(signal) BKG(background)')
        exit(-1)
    #end_if
    return

def computeMomentum(_df_):
    df = _df_
    k = 0
    df = df.Define("coupled",
                   """
                   coup(
                   Px1Px1, Py1Py1, Pz1Pz1, 
                   Px2Px2, Py2Py2, Pz2Pz2, 
                   Px1Px2, Py1Py2, Pz1Pz2 
                   )"""
    )
    
    df = df.Define("Cart1",
                   """
                   ROOT::Math::PxPyPzMVector(
                   TMath::Sqrt(Px1Px1),
                   TMath::Sqrt(Py1Py1),
                   TMath::Sqrt(Pz1Pz1),
                   0)
                   """
    )
    df = df.Define("Cart2",
                   """
                   ROOT::Math::PxPyPzMVector(
                   TMath::Sqrt(Px2Px2),
                   TMath::Sqrt(Py2Py2),
                   TMath::Sqrt(Pz2Pz2),
                   0)
                   """
    )

    df = df.Define('nrg', "(Cart1+Cart2).E()")
    df = df.Define('Ptot', '-computeMomentumTot(coupled) + (nrg * nrg)')
    df = df.Define("PtotSq", "TMath::Sqrt(Ptot)")
    return df

if __name__ == "__main__" :
    from plotslib import set_axes_title, PlotHist, create_legend, add_Header, PlotHist2, PlotScatter 

    ## Help messge
    helpMessage()

    ## Load data
    data_set = argv[1]
    sig_test, sig_train, bkg_test, bkg_train = LoadData(data_set)
    
    ## Configure output
    outName = argv[2]
    outpath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Plots/"
    outFile = outpath + outName +"_RetrievedMass.pdf"
    ## Loop through events do the caclulations and save the output  
    c = ROOT.TCanvas()
    c.Divide(2,2)
    ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
    
    hists =[]
    labels =[
        ("Signal", "training" ),
        ("Signal", "testing"),
        ("Background", "training"),
        ("Background", "testing") ]
    for i, events in enumerate((sig_train, sig_test,  bkg_train, bkg_test)):
        pad = i+1
        c.cd(pad)
        df = computeMomentum(events).Histo1D(('Hist'+str(i), "", 50, 23, 33), "PtotSq")
        set_axes_title(df, 'Mass[GeV]', 'Counts')
        df.Draw('hist')
        add_Header("Retrieved {} Mass \t {}".format(labels[i][0], labels[i][1]))
        hists.append(df)
    #end_for

    c.cd()
    c.SaveAs(outFile)

