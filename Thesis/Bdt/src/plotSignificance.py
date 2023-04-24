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
    inPath + "WPhiJets_M200M100300Deltas_Application_Smeared{}.root".format(n)
    for n in [0, 5, 10, 15, 20, 30, 40, 50]
]

c = ROOT.TCanvas()
c.cd()
c.SetLogx(0); c.SetLogy(0)
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
c.SaveAs("WPhiJets_M200M100300_Significance.pdf[")

def draw(_graph_, i):
    if i == 0 :
        _graph_.Draw("Al")
    else :
        _graph_.Draw("l")
    return _graph_
#
graphs=list()
bdt_cut = list()
sign_cut1 = list()
sign_cut2 = list()
legend = ROOT.TLegend(0.2, 0.6, 0.35, 0.85)
smear = [ "{}%".format(n) for n in (0, 5, 10, 15, 20, 30, 40, 50) ]
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
    graph_.GetYaxis().SetRangeUser(20, 125)
    if i==0:
        add_Header("Significance for various cases of smearing")
        set_axes_title(graph_, 'BDT score', '')
        Ylabel = ROOT.TLatex()
        Ylabel.SetTextSize(0.035)
        Ylabel.DrawLatexNDC(0.01, 0.85, sig_lab)
    #
    graphs.append(graph)
    

    # Get the BDT cut 
    cut1 = 0.85
    y_val1 = graph_.Eval(cut1)
    sign_cut1.append(y_val1)

    cut2 = 0.95
    y_val2 = graph_.Eval(cut2)
    sign_cut2.append(y_val2)

#
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetTextSize(0.03)
legend.Draw('same')
c.Update()
c.SaveAs("WPhiJets_M200M100300_Significance.pdf")

## Get the fit based results 
inSigPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Plots/"
inSig=ROOT.TFile.Open(inSigPath + "WPhiJets_M200M100300Deltas_SigEvol.root", "READ")   
graphSig=inSig.Get("FitSig")
inSig.Close()

inAdaPath = inSigPath
inAda = ROOT.TFile.Open(inSigPath + "WPhiJets_M200M100300Deltas_SigEvolAda.root", "READ")   
graphAda = inAda.Get("FitSig")
inAda.Close()

c.SetLogy(0)
sign_cut1 = np.array(sign_cut1).astype(np.float64)
sign_cut2 = np.array(sign_cut2).astype(np.float64)
x= np.array([0, 5, 10, 15, 20, 30, 40, 50]).astype(np.float64)
#print(x.shape)
#print(sign_cut.shape)

evol1 = ROOT.TGraph(x.shape[0],x, sign_cut1)
evol1.SetTitle("")
evol1.GetXaxis().SetRangeUser(-5, 65 )
evol1.GetYaxis().SetRangeUser(50, 220)
evol1.SetMarkerStyle(21)
evol1.Draw("APl")

evol2 = ROOT.TGraph(x.shape[0],x, sign_cut2)
evol2.SetTitle("")
evol2.SetMarkerStyle(21)
evol2.SetMarkerColor(ROOT.kBlue)
evol2.Draw("Pl same")

#GraphSig = graphSig.GetListOfGraphs().At(0)
graphSig.SetTitle("")
graphSig.SetMarkerStyle(21)
graphSig.SetMarkerColor(ROOT.kGreen)
graphSig.Draw("Pl same")

graphAda.SetTitle("")
graphAda.SetMarkerStyle(21)
graphAda.SetMarkerColor(ROOT.kRed)
graphAda.Draw("Pl same")


# Plot the legend
legend = ROOT.TLegend(0.65, 0.6, 0.75, 0.75)
legend.AddEntry(evol1, "cut at bdt score = {}".format(cut1), "p")
legend.AddEntry(evol2, "cut at bdt score = {}".format(cut2), "p")
legend.AddEntry(graphSig, "Fixed 23GeV window", "p") 
legend.AddEntry(graphAda, r"Adaptive 1.5\sigma window", "p") 
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetTextSize(0.03)
legend.Draw('same')


set_axes_title(evol1, 'smearing in %', 'significance')
add_Header("Evolution of significance ")
c.SaveAs("WPhiJets_M200M100300_Significance.pdf")
c.SaveAs("WPhiJets_M200M100300_Significance.pdf]")
