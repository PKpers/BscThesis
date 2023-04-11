import sys
sys.path.insert(0, '/home/kpapad/UG_thesis/Thesis/share/lib/')
#
import ROOT
from plotslib import set_axes_title, PlotHist, create_legend, add_Header, PlotHist2, set_markerstyle
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
ROOT.gROOT.SetBatch(True)
#outFile10,outFile15,outFile25,outFile50
inPath = "/home/kpapad/UG_thesis/Thesis/Bdt/out/Plots/"
inFiles =[
    inPath + "WPhi_2mu_M50MixedDeltas_Application_Smeared{}.root".format(n)
    for n in [0, 10, 15, 25, 50]
]

c = ROOT.TCanvas()
c.cd()
c.SetLogx(0); c.SetLogy(0)
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
c.SaveAs("test.pdf[")
def draw(_graph_, i):
    if i == 0 :
        _graph_.Draw("Al")
    else :
        _graph_.Draw("l")
    return _graph_
#
graphs=list()
bdt_cut = list()
sign_cut = list()
legend = ROOT.TLegend(0.4, 0.4, 0.45, 0.6)
smear = [ "{}%".format(n) for n in (0, 10, 15, 25, 50) ]
sig_lab = r'\frac{sig}{\sqrt{bkg}}'
colors = [40, 41, 30, 31]
for i, infile in enumerate(inFiles):
    myFile = ROOT.TFile.Open(infile, "READ") 
    graph=myFile.Get("significance")
    myFile.Close()

    graph_ = graph.GetListOfGraphs().At(0)
    graph_.SetTitle("")
    gname = graph_.GetName()
    graph_.SetLineColor(i+1)
    if i == 4 : graph_.SetLineColor(6) 
    legend.AddEntry(graph_, '{}'.format(smear[i]), 'l')
    draw(graph_, i)

    add_Header("Significance for various cases of smearing")
    set_axes_title(graph_, 'BDT score', '')
    Ylabel = ROOT.TLatex()
    Ylabel.SetTextSize(0.035)
    Ylabel.DrawLatexNDC(0.02, 0.85, sig_lab)
    graphs.append(graph)
    

    # Get the BDT cut 
    cut = 0.5
    y_val = graph_.Eval(cut)
    sign_cut.append(y_val)
#

legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetTextSize(0.03)
legend.Draw('same')
c.Update()
c.SaveAs("test.pdf")


sign_cut = np.array(sign_cut).astype(np.float64)
x= np.array([0, 10, 15, 25, 50]).astype(np.float64)
print(x.shape)
print(sign_cut.shape)

evol = ROOT.TGraph(x.shape[0],x, sign_cut)
evol.SetTitle("")
evol.GetXaxis().SetRangeUser(-1, 54 )
evol.SetMarkerStyle(21)
evol.Draw("AP")

set_axes_title(evol, 'smearing in %', '')
add_Header("Evolution of significance for cut at BDT score = 0.5 ")
Ylabel = ROOT.TLatex()
Ylabel.SetTextSize(0.035)
Ylabel.DrawLatexNDC(0.01, 0.85, sig_lab)

c.SaveAs("test.pdf")
c.SaveAs("test.pdf]")


exit()





























if len(sys.argv) != 3:
    print("usage: {} {} {}".format(sys.argv[0], "inp_file.root", "outfile.pdf"))
    exit(-1)
# Configure input settings
input_dir = "/home/kpapad/UG_thesis/Thesis/Bdt/out/Predictions/"
treeName = "myTree"
infile = sys.argv[1]
#
# Configure output settings 
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
sig_events = sigT.Count().GetValue()
bkgT = df1.Filter("yTest_true == 0")
bkg_events = bkgT.Count().GetValue()
print(sig_events, bkg_events)
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
    (bkgT, "bkgT", "yTest_pred", "background testing"), 
]
nbins = 50
histRange = (0., 1)
histOpts = (nbins, histRange)
ax_labels = ("bdt score", "events")
_Lcolor = (4,1)
legend_entries = {}
h_ = []
for i, d in enumerate(data):
    lca_ = [_Lcolor[i], 1]
    if i ==0:
        DrawLoc='hist' 
        fs_ =  [3004, None, 1001]
        fca_ = [(_Lcolor[i], 1), None, (_Lcolor[i], 0.15)]
        legend_mark = 'f'
        #
        pltData = (d[0], d[2])
        hist = PlotHist(
            d[1], pltData, histOpts, ax_labels,
            DrawLoc, lca=lca_, fca=fca_[i-1], fs=fs_[i-1],  
        )

    elif i == 1:
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
efficiency = []
rejection = []
for h in h_ :
    h = h.GetValue()
    axis = h.GetXaxis()
    bmax = axis.FindBin(float(1))
    thress = axis.FindBin(0.7)
    Int = [
        h.Integral(T, bmax)
        for T in range(h.GetNbinsX())
    ]
    TpFn = Int[0] # True positive Plus False negative of the class
    Tp = Int[thress] # True positive only of the class 
    eff = Tp / TpFn
    rej = (TpFn - Tp) / TpFn
    rejection.append(rej)
    efficiency.append(eff)
    integrals.append(Int)
    #
#

# Calculate significance sig/sqrt(bkg)
integrals = np.array(integrals)
significance = integrals[0][:-3]/np.sqrt(integrals[1][:-3])#0: signal, 1: background
bdt_score = np.arange(0, 1, 0.02)

#normalize the roc curve 
TestingTPR,  TestingFPR = [
    np.array(integrals[0])/sig_events,
    np.array(integrals[1])/bkg_events
]

TestingTNR = 1 -TestingFPR
c.SetLogy(0)
c.SetLogx(0)
roc = ROOT.TMultiGraph('roc', 'ROC')
roc_alt = ROOT.TMultiGraph('roc_alt', 'ROC')
Sign = ROOT.TMultiGraph('Sign', 'Significance')
# Testing
TestROC = ROOT.TGraph(len(TestingTPR), TestingFPR, TestingTPR)#(n,x,y)
TestROC.SetName('TestROC')
TestROC.SetTitle( 'Testing' )
TestROC.SetMarkerColor(3)
TestROC.SetMarkerStyle(21)
TestROC.SetDrawOption( 'ACP' )
#
Significance = ROOT.TGraph(bdt_score.shape[0], bdt_score, significance)#(n,x,y)
Significance.SetName('Significance')
Significance.SetTitle( 'Testing' )
Significance.SetMarkerColor(3)
Significance.SetMarkerStyle(21)
Significance.SetDrawOption( 'ACP' )

#
TestROC_alt = ROOT.TGraph(len(TestingTPR), TestingTNR, TestingTPR)
TestROC_alt.SetName('TestROC_alt')
TestROC_alt.SetTitle( 'Testing' )
TestROC_alt.SetMarkerColor(3)
TestROC_alt.SetMarkerStyle(21)
TestROC_alt.SetDrawOption( 'ACP' )

# Plot the curves
roc.Add(TestROC)
set_axes_title(roc, "FPR", "TPR")
roc.Draw('ALP')

# legend
legend_sig = 'Signal efficiency: {:.1f}%'.format(efficiency[0]*100)
legend_bkg = 'Background rejection: {:.1f}%'.format(rejection[1]*100)

legend = ROOT.TLegend(0.4, 0.4, 0.6, 0.6)
legend.AddEntry('', legend_sig, '')
legend.AddEntry('', legend_bkg, '')
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetTextSize(0.03)
legend.Draw('same')
c.SaveAs(output)

# Plot the significance curve 
Sign.Add(Significance)
sig_lab = r'\frac{sig}{\sqrt{bkg}}'
set_axes_title(Sign, "BDT score", "")
Sign.Draw('ALP')
# Draw the y axis title with the correct orientation
Ylabel = ROOT.TLatex()
Ylabel.SetTextSize(0.035)
Ylabel.DrawLatexNDC(0.02, 0.85, sig_lab)

# legend
c.SaveAs(output)
#
#Plot the roc curve with TNR indtead of FPR
roc_alt.Add(TestROC_alt)
#
set_axes_title(roc_alt, "TNR", "TPR")
roc_alt.Draw('ALP')
#
legend = ROOT.TLegend(0.4, 0.4, 0.6, 0.6)
legend.AddEntry(TestROC, 'Testing', 'lp')
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetTextSize(0.03)
legend.Draw('same')
c.SaveAs(output)
c.SaveAs(output+"]")
