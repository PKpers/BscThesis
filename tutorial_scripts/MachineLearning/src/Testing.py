#!/usr/bin/python
import ROOT
import pickle
import numpy as np
from Training import load_data
import sys
from asdict import read_as_dict
# Input settings
input_dir = "/home/kpapad/UG_thesis/tutorial_scripts/MachineLearning/RFiles/"
TreeName = "myTree"
fileName = sys.argv[1]
modelName = sys.argv[2]
print("Started testing using data from {} with using the following model: {}"
      .format(fileName, modelName))
#
# Output settings
output_dir = input_dir + "Predictions/"
out_filename = sys.argv[3]
out_filename = output_dir + out_filename
#
# Load data
infiles = [
    ('{}{}{}.root'.format(input_dir, fileName+str(1), p),
     '{}{}{}.root'.format(input_dir, fileName+str(2), p))
    for p in ('Test', 'Train')
]
#
xTest, yTest_true, wTest, _= load_data(infiles[0][0], infiles[0][1])
xRef, yRef_true, wRef, _= load_data(infiles[1][0], infiles[1][1])
#
# Load trained model
model = input_dir + 'Models/' + '{}.root'.format(modelName)
if (ROOT.gSystem.AccessPathName(model)) :
    ROOT.Info(sys.argv[0], model+" does not exist")
    exit(-1)
#
bdt = ROOT.TMVA.Experimental.RBDT[""]("myBDT", model)
# Make prediction
y_pred = [
    bdt.Compute(x)
    for x in (xTest, xRef)
]
print(xTest)
print(yTest_true)
exit()
x = [
    [sum(xi) for xi in x]
    for x in (xTest, xRef)
]
from sklearn.metrics import roc_curve, auc
fpr, tpr, _ = roc_curve(yTest_true, y_pred[0], sample_weight=wTest)
score = auc(fpr, tpr)
#
# Export trained results
print("exporting predicted data to {} ...".format(out_filename))
df1 = ROOT.RDF.MakeNumpyDataFrame(
    {
        "xTest" :              np.array(x[0]),
        "yTest_pred" :      np.array(y_pred[0]),
        "yTest_true" :      np.array(yTest_true),
    }
).Snapshot(TreeName, out_filename+"test.root") 

df2 = ROOT.RDF.MakeNumpyDataFrame(
    {
        "xRef" :                np.array(x[1]),
        "yRef_pred" :        np.array(y_pred[1]),
        "yRef_true" :        np.array(yRef_true),
    }
).Snapshot(TreeName, out_filename+"train.root")
   
print('done')
print(modelName,' : ',score, )
 
