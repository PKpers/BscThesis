import ROOT
from sys import argv
from os import chdir, getcwd
import numpy as np
from sklearn.model_selection import train_test_split
from WPhi_2mu_dataPrepXYZ import define_columns, LoadData
from WPhi_2mu_dataPrep import makeHist
# include my c libs
workingDIR = getcwd()
chdir('/home/kpapad/UG_thesis/Thesis/Analysis/lib/')
ROOT.gInterpreter.ProcessLine('#include "funcy.h"')
chdir(workingDIR)
#
def HelpMessage():
    if len(argv) != 3 :
        print('usage: {} {} {}'.format(argv[0], 'DataSetName', 'output' ))
        print('\nThe default output format will be of the form outputPxyz_purpose_label.root')
        print('purpose: Testing/Training \nlabel: SIG(signal) BKG(background)')
        exit(-1)
    #end_if
    return

def create_fnames(outpath, fileName):
    '''
    create the output file names
    '''
    purpose = ('Train', 'Test')
    label = ('_SIG_', '_BKG_')
    #
    outfiles = [
        ('{}{}{}.root'.format(outpath, fileName + l, 'Test'))
        for l in label
    ]
    return outfiles

def Smear(_df_, percentage):
    df = _df_
    df = df.Define('Pt1_Smeared', "Pt1 * gRandom->Gaus(1, {})".format(percentage))\
        .Define('Pt2_Smeared', "Pt2 * gRandom->Gaus(1, {})".format(percentage))
    #
    return df

def computeMass(_df_, var):
    '''
    take input a data frame
    and it compute the invariant
    mass of the lepton pair in each event
    '''
    df = _df_
    df = df.Define("Lep1","ROOT::Math::PtEtaPhiMVector({}, {}, {}, {})".format(var[0], var[1], var[2], float(0)))\
           .Define("Lep2","ROOT::Math::PtEtaPhiMVector({}, {}, {}, {})".format(var[3], var[4], var[5], float(0)))\
           .Define("PairMass", "(Lep1+Lep2).M()")
    return df

def Deltas(_df_, var):
    '''
    take input a data frame
    and return Pt1, Pt2, DeltaEta, DeltaPhi
    '''
    df = _df_
    df = df.Define('FVec1', 'ROOT::Math::PtEtaPhiMVector({}, {}, {}, {})'.format(var[0], var[1], var[2], float(0)))\
           .Define('FVec2', 'ROOT::Math::PtEtaPhiMVector({}, {}, {}, {})'.format(var[3], var[4], var[5], float(0)))\
           .Define('DeltaPhi', 'DeltaPhi( FVec1.Phi(), FVec2.Phi() )')\
           .Define('DeltaR', 'DeltaR( FVec1.Eta(), FVec1.Phi(), FVec2.Eta(), FVec2.Phi() )')\
           .Define('DeltaEta', 'FVec1.Eta() - FVec2.Eta()')
    #
    return df

if __name__ == "__main__":
    ## Help message
    HelpMessage()
    
    ## Load data 
    sig_test, _, bkg_test, _ = LoadData(argv[1])# We don't care about the training set in this case 
    bkg_test = Smear(bkg_test, 0.30) # smear the background
    sig_test = Smear(sig_test, 0.30) # smear the signal as well

    ## Calculate the smeared mass. Plot the masses 
    varNames_sig = ['Pt1', 'Eta1', 'Phi1', 'Pt2', 'Eta2', 'Phi2']
    varNames_bkg = ['Pt1_Smeared', 'Eta1', 'Phi1', 'Pt2_Smeared', 'Eta2', 'Phi2']
    var = [varNames_bkg, varNames_bkg ]
    
    masses = [
        computeMass(df, var[i])
        for i,df in enumerate( (sig_test, bkg_test))
    ]
    variables = [
        (masses[0], 'masses_0', 'PairMass', 'Signal(Smeared 30%)'),
        (masses[1], 'masses_1', 'PairMass', 'Background(Smeared 30%)')
    ]
    
    outName = argv[2]
    outpath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Plots/"
    outHistName = outpath + outName +'Hist.pdf'
    makeHist(variables, outHistName)

    
    ## Configure output and write the data to root files
    sig_test = Deltas(sig_test, varNames_sig ).AsNumpy()
    bkg_test = Deltas(bkg_test, varNames_bkg).AsNumpy()
    
    varNames_sig = ["Pt1", "Pt2", "DeltaPhi", "DeltaR", "DeltaEta"]
    varNames_bkg = ["Pt1_Smeared", "Pt2_Smeared", "DeltaPhi", "DeltaR", "DeltaEta"]
    signal_test = np.vstack([sig_test[var].astype(np.float32) for var in varNames_bkg])
    background_test = np.vstack([bkg_test[var].astype(np.float32) for var in varNames_bkg])
    
    outpath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
    treeName = 'tree'
    label = ('SIG', 'BKG')
    purpose = ('Test')
    Files = create_fnames(outpath, outName+'Deltas')
    
    varNames = [varNames_sig, varNames_sig]
    for i, events in enumerate((signal_test, background_test)):
        print('Writting {} in {}'.format(treeName, Files[i]))
        vars_dict = define_columns(5, varNames[i], events)
        df = ROOT.RDF.MakeNumpyDataFrame(vars_dict).Snapshot(treeName, Files[i])
    #
 
