import ROOT
import pickle
 
from CERN_MLtutorial_data_preparation import variables
from CERN_MLtutorial_Training import load_data
 
 
# Load data
x, y_true, w, _ = load_data("test_signal.root", "test_background.root")
 
# Load trained model
File = "tmva101.root"
if (ROOT.gSystem.AccessPathName(File)) :
    ROOT.Info("tmva102_Testing.py", File+"does not exist")
    exit()
 
bdt = ROOT.TMVA.Experimental.RBDT[""]("myBDT", File)
 
# Make prediction
print(type(x[0][0]))
exit()
y_pred = bdt.Compute(x)
print(y_pred)
print(y_true)
exit()
# Compute ROC using sklearn
from sklearn.metrics import roc_curve, auc
fpr, tpr, _ = roc_curve(y_true, y_pred, sample_weight=w)
score = auc(fpr, tpr) #reorder=True)
 
# Plot ROC
c = ROOT.TCanvas("roc", "", 600, 600)
g = ROOT.TGraph(len(fpr), fpr, tpr)
g.SetTitle("AUC = {:.2f}".format(score))
g.SetLineWidth(3)
g.SetLineColor(ROOT.kRed)
g.Draw("AC")
g.GetXaxis().SetRangeUser(0, 1)
g.GetYaxis().SetRangeUser(0, 1)
g.GetXaxis().SetTitle("False-positive rate")
g.GetYaxis().SetTitle("True-positive rate")
c.Draw()
