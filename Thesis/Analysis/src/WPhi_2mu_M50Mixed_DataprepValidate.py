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

## Configure output settings 
outPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
outName = "WPhi_2mu_M50MixedDeltas_Application"
treeName = 'tree'

## Load data
df = ROOT.RDataFrame("tree", inFile)
background = df.Filter("Label == 0").Snapshot('tree', outPath+outName+"_BKG_Test.root") 
signal = df.Filter("Label == 1").Snapshot('tree', outPath+outName+"_SIG_Test.root")


