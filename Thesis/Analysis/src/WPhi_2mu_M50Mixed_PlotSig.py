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
inPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Plots/"
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
legend = ROOT.TLegend(0.4, 0.6, 0.5, 0.8)
smear = [ "{}%".format(n) for n in (0, 10, 15, 25, 50) ]
sig_lab = r'\frac{sig}{\sqrt{bkg}}'
colors = [40, 41, 30, 31]
for i, infile in enumerate(inFiles):
    myFile = ROOT.TFile.Open(infile, "READ") 
    graph=myFile.Get("significance")
    myFile.Close()
    graph_ = graph.GetListOfGraphs().At(0)
    if i == 4 :
        x = np.array([0.25*i for i in range(1,13)])
        y = np.zeros(x.shape[0])
        graph_ = ROOT.TGraph(x.shape[0], x, y)
        graph_.SetLineColor(6) 
    # 
    graph_.SetTitle("")
    gname = graph_.GetName()
    graph_.SetLineColor(i+1)
    graph_.GetYaxis().SetRangeUser(0, 20 )
    legend.AddEntry(graph_, '{}'.format(smear[i]), 'l')
    draw(graph_, i)

    add_Header("Significance for various cases of smearing")
    set_axes_title(graph_, '\sigma', '')
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
evol.GetYaxis().SetRangeUser(-1, 14 )
evol.SetMarkerStyle(21)
evol.Draw("AP")

set_axes_title(evol, 'smearing in %', '')
add_Header(r"Evolution of significance for cut at 0.5\sigma ")
Ylabel = ROOT.TLatex()
Ylabel.SetTextSize(0.035)
Ylabel.DrawLatexNDC(0.01, 0.85, sig_lab)

c.SaveAs("test.pdf")
c.SaveAs("test.pdf]")
