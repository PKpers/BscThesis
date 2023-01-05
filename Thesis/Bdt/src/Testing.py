#!/usr/bin/python
import ROOT
import pickle
import numpy as np
from Training import load_data
import sys
from asdict import read_as_dict
from sklearn.metrics import roc_curve, auc
# Input settings
input_dir = '/home/kpapad/UG_thesis/Thesis/share/SimuData/'
TreeName = "myTree"
fileName = sys.argv[1]
modelName = sys.argv[2]
print("Started testing using data from {} with using the following model: {}"
      .format(fileName, modelName))
#
# Output settings
output_dir = '/home/kpapad/UG_thesis/Thesis/Bdt/out/Predictions/'
out_filename = sys.argv[3]
out_filename = output_dir + out_filename
#
# Load data
infiles = [
    ('{}{}{}.root'.format(input_dir, fileName+str("_SIG_"), p),
     '{}{}{}.root'.format(input_dir, fileName+str("_BKG_"), p))
    for p in ('Test', 'Train')
]
#
xTest, yTest_true, wTest, _= load_data(infiles[0][0], infiles[0][1])
xRef, yRef_true, wRef, _= load_data(infiles[1][0], infiles[1][1])
#
# Load trained model
model =  '/home/kpapad/UG_thesis/Thesis/Bdt/out/Models/'+ '{}.root'.format(modelName)
# If the file doesn't exist, raise exception and exit
if (ROOT.gSystem.AccessPathName(model)) :
    ROOT.Info(sys.argv[0], model+" does not exist")
    exit(-1)
#
# otherwise load the model 
bdt = ROOT.TMVA.Experimental.RBDT[""]("myBDT", model)
#
# Make prediction
y_pred = [
    bdt.Compute(x)
    for x in (np.array(xTest, dtype='float32'), np.array(xRef, dtype='float32'))
]
# calculate the auc score
fpr, tpr, _ = roc_curve(yTest_true, y_pred[0], sample_weight=wTest)
score = auc(fpr, tpr)
#
# Export trained results
print("exporting predicted data to {} ...".format(out_filename))
df1 = ROOT.RDF.MakeNumpyDataFrame(
    {
        "yTest_pred" :      np.array(y_pred[0]),
        "yTest_true" :      np.array(yTest_true),
    }
).Snapshot(TreeName, out_filename+"test.root") 

df2 = ROOT.RDF.MakeNumpyDataFrame(
    {
        "yRef_pred" :        np.array(y_pred[1]),
        "yRef_true" :        np.array(yRef_true),
    }
).Snapshot(TreeName, out_filename+"train.root")
   
print('done')
print(modelName,' : ',score, )

