import sys
sys.path.insert(0, '/home/kpapad/UG_thesis/Thesis/share/lib/')
#
import ROOT
from plotslib import set_axes_title, PlotHist, create_legend, add_Header, PlotHist2, set_markerstyle
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
ROOT.gROOT.SetBatch(True)

if len(sys.argv) != 3:
    print("usage: {} {} {}".format(sys.argv[0], "inp_file.root", "outfile.pdf"))
    exit(-1)
# Configure input settings
input_dir = "/home/kpapad/UG_thesis/Thesis/Bdt/out/Predictions/"
treeName = "myTree"
infile = sys.argv[1]
#
# Configure output settings 
output_dir = "/home/kpapad/UG_thesis/Thesis/Bdt/out/Plots/"
outfile = sys.argv[2]
if not outfile.endswith(".pdf"):
    outfile += ".pdf"
#
output = output_dir+outfile
#bdt_hist = output_dir+outfile+'hist.pdf'
#bdt_scatter = output_dir+outfile+'scatter.pdf'
#
# Load data
df1 = ROOT.RDataFrame(treeName, input_dir+'{}test.root'.format(infile))
df2= ROOT.RDataFrame(treeName, input_dir+'{}train.root'.format(infile))
sigT = df1.Filter("yTest_true == 1")
sigT_events = sigT.Count().GetValue()
bkgT = df1.Filter("yTest_true == 0")
bkgT_events = bkgT.Count().GetValue()
sigR = df2.Filter("yRef_true == 1")
sigR_events = sigR.Count().GetValue()
bkgR = df2.Filter("yRef_true == 0")
bkgR_events = bkgR.Count().GetValue()
#
# Make the plots
c = ROOT.TCanvas()
c.cd()
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
c.SaveAs(output+"[")
#

## Plot the histograms --------------------------------------------------------------------------------------------------
data = [
    (sigT, "sigT", "yTest_pred", "signal testing"),
    (sigR, "sigR", "yRef_pred", "signal training"),
    (bkgT, "bkgT", "yTest_pred", "background testing"), 
    (bkgR, "bkgR", "yRef_pred", "background training"), 
]
nbins = 50
histRange = (0., 1)
histOpts = (nbins, histRange)
ax_labels = ("bdt score", "events")
_Lcolor = (3,4,2,1)
legend_entries = {}
h_ = []
for i, d in enumerate(data):
    lca_ = [_Lcolor[i], 1]
    if i == 0:
        DrawLoc='E1'
        legend_mark = 'lep'
        #
        pltData = (d[0], d[2])
        hist = PlotHist(
            d[1], pltData, histOpts, ax_labels,
            DrawLoc, lca=lca_ 
        )
    elif i == 2:
        DrawLoc = "E1"+'same'
        legend_mark = "lep"
        #
        pltData = (d[0], d[2])
        hist = PlotHist(
            d[1], pltData, histOpts, ax_labels,
            DrawLoc, lca=lca_ 
        )

    elif i == 1 or i == 3:
        DrawLoc='same' 
        fs_ =  [3004, None, 1001]
        fca_ = [(_Lcolor[i], 1), None, (_Lcolor[i], 0.15)]
        legend_mark = 'f'
        #
        pltData = (d[0], d[2])
        hist = PlotHist(
            d[1], pltData, histOpts, ax_labels,
            DrawLoc, lca=lca_, fca=fca_[i-1], fs=fs_[i-1],  
        )
    #
    h_.append(hist) 
    hist.GetYaxis().SetRangeUser(1, 6000)
    legend_entries[d[1]] =(d[-1], legend_mark)
#
legend_loc = (0.4, 0.7, 0.5, 0.8)
legend = create_legend(legend_loc, legend_entries)
add_Header('BDT histogram')
c.SetLogy(0)
c.SaveAs(output)
c.SetLogy(1)
c.SaveAs(output)

# Calculate TPR and FPR and plot the roc curve -----------------------------------------------------------------
integrals = []
for h in h_ :
    h = h.GetValue()
    axis = h.GetXaxis()
    bmax = axis.FindBin(float(1))
    Int = [
        h.Integral(T, bmax)
        for T in range(h.GetNbinsX())
    ]
    integrals.append(Int)
    #
#
TestingTPR,  TestingFPR = [
    np.array(integrals[0])/sigT_events,
    np.array(integrals[2])/bkgT_events
]
TrainingTPR,  TrainingFPR = [
    np.array(integrals[1])/sigR_events,
    np.array(integrals[3])/bkgR_events 
]

TestingTNR = 1 -TestingFPR
TrainingTNR = 1 -TrainingFPR
c.SetLogy(0)
c.SetLogx(0)
roc = ROOT.TMultiGraph('roc', 'ROC')
roc_alt = ROOT.TMultiGraph('roc_alt', 'ROC')
# Testing
TestROC = ROOT.TGraph(len(TestingTPR), TestingFPR, TestingTPR)#(n,x,y)
TestROC.SetName('TestROC')
TestROC.SetTitle( 'Testing' )
TestROC.SetMarkerColor(3)
TestROC.SetMarkerStyle(21)
TestROC.SetDrawOption( 'ACP' )
#
TestROC_alt = ROOT.TGraph(len(TestingTPR), TestingTNR, TestingTPR)
TestROC_alt.SetName('TestROC_alt')
TestROC_alt.SetTitle( 'Testing' )
TestROC_alt.SetMarkerColor(3)
TestROC_alt.SetMarkerStyle(21)
TestROC_alt.SetDrawOption( 'ACP' )

# Training
TrainROC = ROOT.TGraph(len(TrainingTPR), TrainingFPR, TrainingTPR)
TrainROC.SetName('TrainROC')
TrainROC.SetTitle( 'Training' )
TrainROC.SetMarkerColor(4)
TrainROC.SetMarkerStyle(21)
TrainROC.SetDrawOption( 'ACP' )
#
TrainROC_alt = ROOT.TGraph(len(TrainingTPR), TrainingTNR, TrainingTPR)
TrainROC_alt.SetName('TrainROC_alt')
TrainROC_alt.SetTitle( 'Training' )
TrainROC_alt.SetMarkerColor(4)
TrainROC_alt.SetMarkerStyle(21)
TrainROC_alt.SetDrawOption( 'ACP' )

# Plot the curves
roc.Add(TestROC)
roc.Add(TrainROC)
#

set_axes_title(roc, "FPR", "TPR")
roc.Draw('ALP')
# legend
legend = ROOT.TLegend(0.4, 0.4, 0.6, 0.6)
legend.AddEntry(TestROC, 'Testing', 'lp')
legend.AddEntry(TrainROC, 'Training', 'lp')
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetTextSize(0.03)
legend.Draw('same')
#c.BuildLegend()
c.SaveAs(output)
#
#Plot the roc curve with TNR indtead of FPR
roc_alt.Add(TestROC_alt)
roc_alt.Add(TrainROC_alt)
#
set_axes_title(roc_alt, "TNR", "TPR")
roc_alt.Draw('ALP')
#
legend = ROOT.TLegend(0.4, 0.4, 0.6, 0.6)
legend.AddEntry(TestROC, 'Testing', 'lp')
legend.AddEntry(TrainROC, 'Training', 'lp')
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetTextSize(0.03)
legend.Draw('same')
c.SaveAs(output)
## Plot the ratios ------------------------------------------------------------------------------------------------------
c.SetLogx(0)
c.SetLogy(0)
legend_entries = {}
line_attribs = {
    "msz" : 0.5,
    "ms"  : 20
}
Range = (1, 3)
for i in Range:
    if i == 1:
        color = (3, 1)
        Type = "signal"
        DrawLoc = "p"
    else:
        color = (2, 1)
        Type = "background"
        DrawLoc = "psame"
    #
    training = h_[i].GetValue() 
    testing = h_[i - 1].GetValue() 
    training.Divide(testing)
    training.GetYaxis().SetRangeUser(0, 2)
    line_attribs["mca"] = color
    set_markerstyle(training, line_attribs)
    training.GetYaxis().SetTitle('Ratio')
    training.Draw(DrawLoc)
    legend_entries[training] = (Type, "p")
#
ratio_lloc = (0.7, 0.2, 0.8, 0.3)
add_Header('Training/Testing ratios')
legend = create_legend(ratio_lloc, legend_entries)
c.SaveAs(output)
c.SaveAs(output+"]")
exit()
#
## Plot the Heatmaps --------------------------------------------------------------------------------------------------
scatters = []
sig_data = (sigT, "xTest", "yTest_pred")
bkg_data = (bkgT, "xTest", "yTest_pred")
plt_range = [ [50, (2,10)], [50, (0, 1)] ]
ax_labels = ("sums", "bdt score")
plt_data = (sig_data, bkg_data)
k = 0
sig_hist = PlotHist2("sig_hist", sig_data, plt_range, ax_labels, 'colz')
bkg_hist = PlotHist2("blg_hist", bkg_data, plt_range, ax_labels, 'colzsame')
legend_entries2 = {
    "sig_hist" : ('signal', 'l')
}
legend_entries3 = {
    "bkg_hist" : ('background', 'l')
}
legend2_loc = (0.4, 0.7, 0.5, 0.8)
legend3_loc = (0.6, 0.7, 0.7, 0.8)
legend2 = create_legend(legend2_loc, legend_entries2)
legend3 = create_legend(legend3_loc, legend_entries3)
title = add_Header('BDT Testing 2d hist')
c.SetLogy(0)
c.SaveAs(output)
c.SaveAs(output+"]")
#
