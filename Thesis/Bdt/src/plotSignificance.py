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
inFile = inPath + "WPhiJets_M200M100300Deltas_Application_Smeared0.root" 
inFiles =[
    inPath + "WPhiJets_M200M100300Deltas_Application_Smeared{}Pred12.root".format(n)
    for n in [5, 10, 15, 20, 30, 40 ,50]
]

inFiles = [inFile] + inFiles
c = ROOT.TCanvas()
c.cd()
c.SetCanvasSize(800, 800)
c.SetLogx(0); c.SetLogy(0)
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
ROOT.gPad.SetLeftMargin(0.13)
ROOT.gPad.SetBottomMargin(0.11)
c.SaveAs("WPhiJets_M200M100300_Significance0bdt.pdf[")

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
smear = [ "{}%".format(n) for n in (0, 5, 7, 10, 12) ]
sig_lab = r'\frac{sig}{\sqrt{bkg}}'
size = 0.045
for i, infile in enumerate(inFiles):
    if i!=0: break
    myFile = ROOT.TFile.Open(infile, "READ") 
    graph=myFile.Get("significance")
    myFile.Close()

    graph_ = graph.GetListOfGraphs().At(0)
    graph_.SetTitle("")
    gname = graph_.GetName()
    graph_.SetLineColor(i+1)
    graph_.SetLineWidth(3)
    legend.AddEntry(graph_, '{}'.format(smear[i]), 'l')
    draw(graph_, i)
    graph_.GetYaxis().SetRangeUser(20, 125)
    if i==0:
        graph_.GetYaxis().SetLabelSize(size)
        graph_.GetYaxis().SetTitleSize(size)
        graph_.GetXaxis().SetLabelSize(size)
        graph_.GetXaxis().SetTitleSize(size)
        graph_.GetYaxis().SetTitleOffset(1.5)

        set_axes_title(graph_, 'BDT score', 'Significance')
    #
    graphs.append(graph)
    

    # Get the BDT cut 
    cut1 = 0.96
    y_val1 = graph_.Eval(cut1)
    sign_cut1.append(y_val1)

    cut2 = 0
    y_val2 = graph_.Eval(cut2)
    sign_cut2.append(y_val2)

#
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetTextSize(0.03)
legend.Draw('same')
c.Update()
c.SaveAs("WPhiJets_M200M100300_Significance0bdt.pdf")
c.SaveAs("WPhiJets_M200M100300_Significance0bdt.pdf]")
exit()


## Get the fit based results 
inSigPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Plots/"
inSig=ROOT.TFile.Open(inSigPath + "WPhiJets_M60M5080Deltas_SigEvol.root", "READ")   
graphSig=inSig.Get("FitSig")
inSig.Close()

inAdaPath = inSigPath
inAda = ROOT.TFile.Open(inSigPath + "WPhiJets_M60M5080Deltas_SigEvolAda.root", "READ")   
graphAda = inAda.Get("FitSig")
inAda.Close()

c.SetLogy(0)
sign_cut1 = np.array(sign_cut1).astype(np.float64)
sign_cut2 = np.array(sign_cut2).astype(np.float64)
x= np.array([0, 5, 7, 10, 12]).astype(np.float64)
#print(x.shape)
#print(sign_cut.shape)

evol1 = ROOT.TGraph(x.shape[0],x, sign_cut1)
evol1.SetTitle("")
evol1.GetYaxis().SetRangeUser(58, 70)
evol1.GetXaxis().SetRangeUser(-5, 13 )
evol1.GetYaxis().SetLabelSize(size)
evol1.GetYaxis().SetTitleSize(size)
evol1.GetXaxis().SetLabelSize(size)
evol1.GetXaxis().SetTitleSize(size)
evol1.GetYaxis().SetTitleOffset(1.5)
evol1.SetMarkerSize(1.5)
evol1.SetMarkerStyle(21)
evol1.Draw("APl")

'''
evol2 = ROOT.TGraph(x.shape[0],x, sign_cut2)
evol2.SetTitle("")
evol2.SetMarkerStyle(21)
evol2.SetMarkerSize(1.5)
evol2.SetMarkerColor(ROOT.kBlue)
evol2.Draw("Pl same")
'''

legend = ROOT.TLegend(0.45, 0.7, 0.55, 0.85)
legend.AddEntry(evol1, "BDT cut = {}".format(cut1), "p")
#legend.AddEntry(evol2, "BDT cut = {}".format(cut2), "p")
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetTextSize(0.04)
legend.Draw('same')

set_axes_title(evol1, 'smearing in %', 'significance')
c.SaveAs("WPhiJets_M60M5080_Significance0bdt.pdf")



#GraphSig = graphSig.GetListOfGraphs().At(0)
c.Clear()
graphSig.GetYaxis().SetRangeUser(10, 50)
graphSig.GetYaxis().SetLabelSize(size)
graphSig.GetYaxis().SetTitleSize(size)
graphSig.GetXaxis().SetLabelSize(size)
graphSig.GetXaxis().SetTitleSize(size)
graphSig.GetYaxis().SetTitleOffset(1.5)
graphSig.SetTitle("")
graphSig.SetMarkerStyle(21)
graphSig.SetMarkerSize(1.5)
graphSig.SetMarkerColor(ROOT.kGreen)
graphSig.Draw("APl")

graphAda.SetTitle("")
graphAda.SetMarkerStyle(21)
graphAda.SetMarkerSize(1.5)
graphAda.SetMarkerColor(ROOT.kRed)
graphAda.Draw("Pl same")


# Plot the legend
legend = ROOT.TLegend(0.4, 0.7, 0.5, 0.85)
#legend.AddEntry(evol1, "BDT cut = {}".format(cut1), "p")
#legend.AddEntry(evol2, "BDT cut = {}".format(cut2), "p")
legend.AddEntry(graphSig, "Fixed window: 6.38GeV ", "p") 
legend.AddEntry(graphAda, r"Adaptive window: 1.5\sigma ", "p") 
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetTextSize(size)
legend.Draw('same')


set_axes_title(graphSig, 'smearing in %', 'significance')
#add_Header("Evolution of significance ")
c.SaveAs("WPhiJets_M60M5080_Significance.pdf")

c.Clear()
evol1.Draw("APL")
evol1.GetYaxis().SetRangeUser(15, 70)
#evol2.Draw("PL same")
graphSig.Draw("PL same")
graphAda.Draw("PL same")

legend = ROOT.TLegend(0.45, 0.55, 0.55, 0.70)
legend.AddEntry(evol1, "BDT cut = {}".format(cut1), "p")
#legend.AddEntry(evol2, "BDT cut = {}".format(cut2), "p")
legend.AddEntry(graphSig, "Fixed window: 6.38 GeV", "p") 
legend.AddEntry(graphAda, r"Adaptive window: 1.5\sigma ", "p") 
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetTextSize(0.04)
legend.Draw('same')

c.SaveAs("WPhiJets_M60M5080_Significance.pdf")
c.SaveAs("WPhiJets_M60M5080_Significance.pdf]")
