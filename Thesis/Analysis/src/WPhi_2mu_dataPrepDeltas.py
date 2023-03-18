import ROOT
from sys import argv
from os import chdir, getcwd
import numpy as np
from sklearn.model_selection import train_test_split
from WPhi_2mu_dataPrepXYZ import define_columns, LoadData
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

def Deltas(_df_):
    '''
    take input a data frame
    and return Pt1, Pt2, DeltaEta, DeltaPhi
    '''
    var = ('Pt', 'Eta', 'Phi', 'Energy')#original coordinates
    df = _df_
    df = df.Define('FVec1', 'ROOT::Math::PtEtaPhiEVector(Pt1, Eta1, Phi1, Energy1)')\
           .Define('FVec2', 'ROOT::Math::PtEtaPhiEVector(Pt2, Eta2, Phi2, Energy2)')\
           .Define('DeltaPhi', 'DeltaPhi( FVec1.Phi(), FVec2.Phi() )')\
           .Define('DeltaR', 'DeltaR( FVec1.Eta(), FVec1.Phi(), FVec2.Eta(), FVec2.Phi() )')\
           .Define('DeltaEta', 'FVec1.Eta() - FVec2.Eta()')
    #
    return df


def create_fnames(outpath, fileName):
    '''
    create the output file names
    '''
    purpose = ('Train', 'Test')
    label = ('Deltas_SIG_', 'Deltas_BKG_')
    #
    outfiles = [
        ('{}{}{}.root'.format(outpath, fileName + l, 'Train'),
         '{}{}{}.root'.format(outpath, fileName + l, 'Test'))
        for l in label
    ]
    return outfiles

def makeHist(_variables_, outfilename):
    '''
    takes as input a list of varibles
    and plots their histograms
    in the same axes
    '''
    import sys
    sys.path.insert(0, '/home/kpapad/UG_thesis/Thesis/share/lib')
    from plotslib import set_axes_title, PlotHist, create_legend, add_Header 
    ROOT.gROOT.SetBatch(True)
    
    ## Create the canvas 
    c = ROOT.TCanvas()
    c.cd()
    ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)

    ## Make the plot
    nbins = 50
    histRange = (5., 35)
    histOpts = (nbins, histRange)
    ax_labels = ('Mass[GeV]', 'Events')
    _Lcolor = (3,2)
    legend_entries = {}
    h_ = []
    for i, d in enumerate(_variables_):
        lca_ = [_Lcolor[i], 1]
        if i == 0:
            DrawLoc=''
            legend_mark = 'f'
            #
            pltData = (d[0], d[2])
            hist = PlotHist(
                d[1], pltData, histOpts, ax_labels,
                DrawLoc, lca=lca_ 
            )
        elif i == 1:
            DrawLoc = 'same'
            legend_mark = "f"
            #
            pltData = (d[0], d[2])
            hist = PlotHist(
                d[1], pltData, histOpts, ax_labels,
                DrawLoc, lca=lca_ 
            )
        #
        h_.append(hist) 
        legend_entries[d[1]] =(d[-1], legend_mark)
        #
        legend_loc = (0.3, 0.7, 0.4, 0.8)
        legend = create_legend(legend_loc, legend_entries)
        add_Header('Muon Pair Mass histogram')
        c.SetLogy(1)
        c.SaveAs(outfilename)
    return 


if __name__ == "__main__":
    ## Help message
    HelpMessage()
    
    ## Load data 
    sig_test, sig_train, bkg_test, bkg_train = LoadData(argv[1])
    sig_test = Deltas(sig_test).AsNumpy()
    sig_train = Deltas(sig_train).AsNumpy()
    bkg_test = Deltas(bkg_test).AsNumpy()
    bkg_train = Deltas(bkg_train).AsNumpy()
    
    ## Now split the filtered data for Training/Testing
    varNames = ["Pt1", "Pt2", "DeltaPhi", "DeltaR", "DeltaEta"]
        
    signal_test = np.vstack([sig_test[var] for var in varNames])
    signal_train = np.vstack([sig_train[var] for var in varNames])
    background_test = np.vstack([bkg_test[var] for var in varNames])
    background_train = np.vstack([bkg_train[var] for var in varNames])
    
    ## Configure output and write the splitted data to root files
    outpath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
    outName = argv[2]
    treeName = 'tree'
    label = ('SIG', 'BKG')
    purpose = ('Train', 'Test')
    outfiles = create_fnames(outpath, outName)
    Files = []
    for f in outfiles:
        Files.append(f[0])
        Files.append(f[1])
    #end for
    
    for i, events in enumerate((signal_train, signal_test,  background_train, background_test)):
        print('Writting {} in {}'.format(treeName, Files[i]))
        vars_dict = define_columns(5, varNames, events)
        df = ROOT.RDF.MakeNumpyDataFrame(vars_dict).Snapshot(treeName, Files[i])
    #
        
    
    
