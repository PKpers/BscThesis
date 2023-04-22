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
    inPath + "WPhiJets_M200M100300Deltas_Application_Smeared{}.root".format(n)
    for n in [0, 5, 10, 15, 20]
]



c = ROOT.TCanvas()
c.cd()
c.SetLogx(0); c.SetLogy(0)
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
c.SaveAs("WPhiJets_M200M100300_Significances.pdf[")
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
legend = ROOT.TLegend(0.7, 0.2, 0.8, 0.4)
smear = [ "{}%".format(n) for n in (0, 5, 10, 15, 20) ]
sig_lab = r'\frac{sig}{\sqrt{bkg}}'
colors = [40, 41, 30, 31]
#c.SetLogy(1)
for i, infile in enumerate(inFiles):
    myFile = ROOT.TFile.Open(infile, "READ") 
    graph=myFile.Get("significance")
    myFile.Close()
    graph_ = graph.GetListOfGraphs().At(0)
    '''
    if i == 4 :
        x = np.array([0.25*i for i in range(1,13)])
        y = np.zeros(x.shape[0])
        graph_ = ROOT.TGraph(x.shape[0], x, y)
        graph_.SetLineColor(6) 
    # 
    '''
    graph_.SetTitle("")
    gname = graph_.GetName()
    graph_.SetLineColor(i+1)
    graph_.GetYaxis().SetRangeUser(10, 210 )
    legend.AddEntry(graph_, '{}'.format(smear[i]), 'l')
    draw(graph_, i)

    add_Header("Significance for various cases of smearing")
    set_axes_title(graph_, '\sigma', '')
    Ylabel = ROOT.TLatex()
    Ylabel.SetTextSize(0.035)
    Ylabel.DrawLatexNDC(0.01, 0.85, sig_lab)
    graphs.append(graph)
    

    # Get the BDT cut 
    cut = 1.5
    y_val = graph_.Eval(cut)
    sign_cut.append(y_val)
#

legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetTextSize(0.03)
legend.Draw('same')
c.Update()
c.SaveAs("WPhiJets_M200M100300_Significances.pdf")



sign_cut = np.array(sign_cut).astype(np.float64)
x= np.array([0, 5, 10, 15, 20]).astype(np.float64)
print(x.shape)
print(sign_cut.shape)

#c.SetLogy(1)
evol = ROOT.TGraph(x.shape[0],x, sign_cut)
evol.SetTitle("")
evol.GetXaxis().SetRangeUser(-1, 54 )
#evol.GetYaxis().SetRangeUser(0.001, 250 )
evol.SetMarkerStyle(21)
evol.Draw("AP")

set_axes_title(evol, 'smearing in %', '')
add_Header(r"Evolution of significance for cut at 1.5\sigma ")
Ylabel = ROOT.TLatex()
Ylabel.SetTextSize(0.035)
Ylabel.DrawLatexNDC(0.01, 0.85, sig_lab)

c.SaveAs("WPhiJets_M200M100300_Significances.pdf")
c.SaveAs("WPhiJets_M200M100300_Significances.pdf]")
