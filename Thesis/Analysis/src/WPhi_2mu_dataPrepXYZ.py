import ROOT
from sys import argv
from os import chdir, getcwd
import numpy as np
from sklearn.model_selection import train_test_split
# include my c libs
workingDIR = getcwd()
chdir('/home/kpapad/UG_thesis/Thesis/Analysis/lib/')
ROOT.gInterpreter.ProcessLine('#include "funcy.h"')
chdir(workingDIR)

def define_columns(num_columns, var_names, var):
    '''
    define the variables of data frame
    '''
    import numpy as np
    vars_ = {}
    for i in range(num_columns):
        vars_[var_names[i]] = np.array(var[i])
    #
    return vars_

def create_fnames(outpath, fileName):
    '''
    create the output file names
    '''
    purpose = ('Train', 'Test')
    label = ('Pxyz_SIG_', 'Pxyz_BKG_')
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

def Pxyz(_df_):
    '''
    take input a data frame
    and convert pt eta phi to px py pz
    '''
    var = ('Pt', 'Eta', 'Phi', 'Energy')#original coordinates
    cart_var = ('Px', 'Py', 'Pz') #cartessian coordinates
    df = _df_
    
    for i, c in enumerate(cart_var) :
        df = df.Define(c+str(1), 'toCartesian( Pt1, Eta1, Phi1, Energy1, {} )'.format(int(i)))
        df = df.Define(c+str(2), 'toCartesian( Pt2, Eta2, Phi2, Energy2, {} )'.format(int(i)))
    #end for
    
    return df

def LoadData(data_set):
    data_path = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
    #
    purpose = ["Test", "Train"]
    sig_test, sig_train= [ 
        data_path + argv[1] + '_SIG_{}.root'.format(p) 
        for p in purpose
    ]
    bkg_test, bkg_train= [ 
        data_path + argv[1] + '_BKG_{}.root'.format(p) 
        for p in purpose
    ]
    data_files = [
        ROOT.RDataFrame("tree", datafile)
        for datafile in (sig_test, sig_train, bkg_test, bkg_train)
    ]
    return data_files

if __name__ == "__main__":
    ## Help message
    if len(argv) != 3 :
        print('usage: {} {} {}'.format(argv[0], 'DataSetName', 'output' ))
        print('\nThe default output format will be of the form outputPxyz_purpose_label.root')
        print('purpose: Testing/Training \nlabel: SIG(signal) BKG(background)')
        exit(-1)
    #end_if

    ## Load data 
    sig_test, sig_train, bkg_test, bkg_train = LoadData(argv[1])
    sig_test = Pxyz(sig_test).AsNumpy()
    sig_train = Pxyz(sig_train).AsNumpy()
    bkg_test = Pxyz(bkg_test).AsNumpy()
    bkg_train = Pxyz(bkg_train).AsNumpy()
    
    ## Now split the filtered data for Training/Testing
    var = [
        ['Px'+str(i), 'Py'+str(i), 'Pz'+str(i)]
        for i in (1,2)
    ]
    varNames = var[0] + var[1]
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
        vars_dict = define_columns(6, varNames, events)
        df = ROOT.RDF.MakeNumpyDataFrame(vars_dict).Snapshot(treeName, Files[i])
    #
        
    
    
