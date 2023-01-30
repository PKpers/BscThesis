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
    defince the variables of data frame
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
    label = ('_SIG_', '_BKG_')
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

def computeMass(_df_):
    '''
    take input a data frame
    and it compute the invariant
    mass of the lepton pair in each event
    '''
    var = ('Pt', 'Eta', 'Phi', 'Energy')
    df = _df_
    for v in var:
        df = df.Define('Pair{}'.format(v), 'Couple2({}1, {}2)'.format(v, v))
    #
        
    df=df.Define('Pair_Mass', 'ComputeInvariantMass(PairPt, PairEta, PairPhi, PairEnergy)')
    return df
 

if __name__ == "__main__":
    ## Help message
    if len(argv) != 4 :
        print('usage: {} {} {} {}'.format(argv[0], 'sigFIleName', 'bkgFileName', 'output' ))
        print('\nThe default output format will be of the form output_purpose_label.root')
        print('purpose: Testing/Training \nlabel: SIG(signal) BKG(background)')
        exit(-1)
    #end_if

    ## Load data 
    sig_filename, bkg_filename = [
        "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/" + argv[i] + '.root' if '.root' not in argv[i]
        else "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/" + argv[i] 
        for i in (1,2)
    ]
    data_sig = ROOT.RDataFrame("tree", sig_filename)
    data_bkg = ROOT.RDataFrame("tree", bkg_filename)

    ## Plot a histogram of the two masses on the same axes 
    MassThress = [24, 29] # we accept lepton pairs whose inv mass is larger that the threshold
    masses = [
        computeMass(df_).Filter('Pair_Mass > {}'.format(MassThress[i]))
        for i, df_ in enumerate((data_sig, data_bkg))
    ]

    print(
        '{} events passed for signal and {} events passed for background'\
        .format(masses[0].Count().GetValue(), masses[1].Count().GetValue())
    )
    
    variables = [
        (masses[0], 'masses_0', 'Pair_Mass', 'Signal(M = 25GeV)'),
        (masses[1], 'masses_1', 'Pair_Mass', 'Background(M = 30GeV)')
    ]
    outName = argv[3]
    outpath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Plots/"
    outHistName = outpath + outName +'Hist.pdf'
    makeHist(variables, outHistName)

    ## Now split the filtered data for Training/Testing
    data_sig = masses[0].AsNumpy()
    data_bkg = masses[1].AsNumpy()

    var = [
        ['Pt'+str(i), 'Eta'+str(i), 'Phi'+str(i), 'Energy'+str(i)]
        for i in (1,2)
    ]
    varNames = var[0] + var[1]
    signal = np.vstack([data_sig[var] for var in varNames]).T
    background = np.vstack([data_bkg[var] for var in varNames]).T[:signal.shape[0]]
    # background set was larger that signal
    
    # Signal and background have to be transposed so that each entry represents one event
    ## Split the data
    # data_sig_Train, data_sig_Test,
    # data_bkg_Train, data_bkg_Test
    SIG_BKG_TRAIN_TEST = train_test_split(
        signal, background,
        random_state=104, 
        test_size=0.50, #Half of the dataset will be for training 
        shuffle=True
    )

    ## Configure output and write the splitted data to root files
    outpath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
    treeName = 'tree'
    label = ('SIG', 'BKG')
    purpose = ('Train', 'Test')
    outfiles = create_fnames(outpath, outName)
    Files = []
    for f in outfiles:
        Files.append(f[0])
        Files.append(f[1])
    #end for
    for i, data in enumerate(SIG_BKG_TRAIN_TEST):
        data = data
        events = data.T
        print('Writting {} in {}'.format(treeName, Files[i]))

        vars_dict = define_columns(8, varNames, events)

        df = ROOT.RDF.MakeNumpyDataFrame(vars_dict).Snapshot(treeName, Files[i])
    #
        
        
    
    
