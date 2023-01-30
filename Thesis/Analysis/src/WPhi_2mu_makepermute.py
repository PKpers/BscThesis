import ROOT 
from sys import argv
from os import chdir, getcwd
import numpy as np
from sklearn.model_selection import train_test_split
from WPhi_2mu_dataPrepXYZ import define_columns, create_fnames, Pxyz, LoadData
# include custom c libraries
workingDIR = getcwd()
chdir('/home/kpapad/UG_thesis/Thesis/Analysis/lib/')
ROOT.gInterpreter.ProcessLine('#include "funcy.h"')
chdir(workingDIR)
##

def pair_permute(__list__):
    '''
    combine the items of a list
    in pairs of two.
    order doesn't matter
    repetition allowed
    '''
    permutations = []
    for i, xi in enumerate(__list__):
        if type(xi) is str:
            p = [(xi,xj) for xj in __list__[i:]]
        #
        permutations += p
    #
    return permutations

def calculatePermutations(_df_, _vars_):
    _vars_ = pair_permute(_vars_)
    df = _df_
    print(_vars_)# temporary
    k = 0
    for v in _vars_:
        df = df.Define(str(v[0]+v[1]), 'computeProduct({}, {})'.format(v[0], v[1]))
    #
    return df

def configure_output(outName, treeName):
    outpath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
    label = ('SIG', 'BKG')
    purpose = ('Train', 'Test')
    outfiles = create_fnames(outpath, outName)
    Files = []
    for f in outfiles:
        Files.append(f[0])
        Files.append(f[1])
    #end for
    return Files

if __name__ == "__main__" :
    ## Help messge
    if len(argv) != 3:
        print('usage: {} {} {}'.format(argv[0], 'DataSetName', 'output' ))
        print('\nThe default output format will be of the form outputPxyz_purpose_label.root')
        print('purpose: Testing/Training \nlabel: SIG(signal) BKG(background)')
        exit(-1)
    #end_if
    
    ## Load data
    data_set = argv[1]
    sig_test, sig_train, bkg_test, bkg_train = LoadData(data_set)
    
    ## Configure output
    outName = argv[2]
    treeName = 'tree'
    Files = configure_output(outName, treeName)
    
    ## Make the variables 
    var = [
        ['Px'+str(i), 'Py'+str(i), 'Pz'+str(i)]
        for i in (1,2)
    ]
    varNames = var[0] + var[1]
    permuted_vars = pair_permute(varNames)
    permuted_vars = [ str(p[0]+p[1]) for p in permuted_vars]
    # Loop through events do the caclulations and save the outpu
    for i, events in enumerate((sig_train, sig_test,  bkg_train, bkg_test)):
        print('Writting {} in {}'.format(treeName, Files[i]))
        df = calculatePermutations(events, varNames)\
            .Snapshot(treeName,Files[i], permuted_vars)
    #end_for

