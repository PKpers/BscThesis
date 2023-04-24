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
    inPath + "WPhiJets_M200M100300Deltas_Application_Smeared"+str(p)+"HistFit.root" 
    for p in [0, 5, 10, 15, 20]
]

c = ROOT.TCanvas()
c.cd()
c.SetLogx(0); c.SetLogy(1)
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
c.SaveAs("WPhiJets_M200M100300_FitALL.pdf[")

useless = list()
smear = [n for n in (0, 5, 10, 15, 20) ]
for i, infile in enumerate(inFiles):
    legend = ROOT.TLegend(0.65, 0.6, 0.75, 0.75)
    myFile = ROOT.TFile.Open(infile, "READ") 
    
    data =myFile.Get("data")
    data.GetXaxis().SetRangeUser(120, 300)
    data.GetYaxis().SetRangeUser(0.5, 1000)
    set_axes_title(data, " m_{XX} (GeV)", "Counts / Bin")
    
    data.SetMarkerColor(1)
    data.SetLineColor(1)
    data.SetMarkerStyle(8)
    data.SetMarkerSize(0.5)
    data.Draw('EP')

    useless.append(data)
    legend.AddEntry(data, "Data(Smearing: {}%)".format(smear[i]))
    
    fsb = myFile.Get("fsb")
    fsb.Draw('same')
    useless.append(fsb)

    legend.AddEntry(fsb, "Signal + Background", "l")

    fb = myFile.Get("fb")
    fb.SetLineColor(4)
    fb.SetLineStyle(2)
    fb.Draw('same')
    useless.append(fb)

    legend.AddEntry(fb, "Backgound", "l")
    
    fs = myFile.Get("fs")
    fs.SetLineColor( 3 )
    fs.SetLineStyle(2)
    fs.Draw('Same')
    useless.append(fs)

    legend.AddEntry(fs, "Signal", "l")
    
    #myFile.Close()
        
    ## Plot the legend
    legend.SetFillColor(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.03)
    legend.Draw('same')
    
    header = r'Y(200) \rightarrow XX'
    legLabel = ROOT.TLatex()
    legLabel.SetTextSize(0.035)
    legLabel.DrawLatexNDC(0.65, 0.77, header)


    c.Update()
    c.SaveAs("WPhiJets_M200M100300_FitALL.pdf")
    myFile.Close()
# 


inPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
bkgName = "WPhiJets_M200M100300Deltas_Application_BKG_Test.root"

p = 30 # smearing %
for p in (30, 40, 50):
    sigName = "WPhiJets_M200M100300Deltas_Application_Smeared"+str(p)+"_SIG_Test.root"
    sigFile,bkgFile = [inPath + inName for inName in (sigName, bkgName)]

    df_data = ROOT.RDataFrame("tree", {sigFile, bkgFile} )\
                  .Histo1D(("df_data", " ; m_{XX} (GeV)", 100, 100, 300), "PairMass")
    #
    set_axes_title(df_data, " m_{XX} (GeV)", "Counts / Bin")
    df_data.GetXaxis().SetRangeUser(120, 300)
    df_data.GetYaxis().SetRangeUser(0.5, 1000)
    df_data.SetMarkerColor(1)
    df_data.SetLineColor(1)
    df_data.SetMarkerStyle(8)
    df_data.SetMarkerSize(0.5)
    df_data.Draw('EP')

    legend = ROOT.TLegend(0.65, 0.7, 0.75, 0.75)
    legend.AddEntry(df_data.GetValue(), "Data(Smearing: {}%)".format(p), "lp")

    legend.SetFillColor(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.03)
    legend.Draw('same')

    header = r'Y(200) \rightarrow XX'
    legLabel = ROOT.TLatex()
    legLabel.SetTextSize(0.035)
    legLabel.DrawLatexNDC(0.65, 0.77, header)

    c.SaveAs("WPhiJets_M200M100300_FitALL.pdf")
#

c.SaveAs("WPhiJets_M200M100300_FitALL.pdf]")
#exit()
# Get the BDT cut 
