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
inFile = inPath + "WPhiJets_M60M5080Deltas_Application_Smeared7HistFit.root" 

outName = "WPhiJets_M60M5080_MassWinodwShow2.pdf"
size = 0.045
c = ROOT.TCanvas()
c.SetCanvasSize(800, 800)
ROOT.gPad.SetLeftMargin(0.15)
c.cd()
c.SetLogx(0); c.SetLogy(0)
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
c.SaveAs(outName + "[")

useless = list()
smear = [n for n in (0, 5, 7, 10, 12) ]
legend = ROOT.TLegend(0.55, 0.72, 0.65, 0.85)
myFile = ROOT.TFile.Open(inFile, "READ") 
 
data =myFile.Get("data")
data.GetXaxis().SetRangeUser(50, 75)
data.GetYaxis().SetRangeUser(280, 1000)
data.GetYaxis().SetLabelSize(size)
data.GetYaxis().SetTitleSize(size)
data.GetXaxis().SetLabelSize(size)
data.GetXaxis().SetTitleSize(size)
data.GetYaxis().SetTitleOffset(1.5)
data.GetXaxis().SetNdivisions(205, ROOT.kFALSE);

set_axes_title(data, " m_{XX} (GeV)", "Counts / Bin")

data.SetMarkerColor(1)
data.SetLineColor(1)
data.SetMarkerStyle(8)
data.SetMarkerSize(1)
data.SetLineWidth(2)
data.Draw('PE')

useless.append(data)
legend.AddEntry(data, "Data")

fsb = myFile.Get("fsb")
fsb.SetLineWidth(3)
fsb.DrawClone('same')
useless.append(fsb)

"""
fb = myFile.Get("fb")
fb.SetLineColor(4)
fb.SetLineStyle(2)
fb.SetLineWidth(3)

fb.Draw('same')
useless.append(fb)

fs = myFile.Get("fs")
fs.SetLineColor( 3 )
fs.SetLineStyle(2)
fs.SetLineWidth(3)
fs.Draw('Same')
useless.append(fs)
"""
## Plot the legend
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetTextSize(0.03)
legend.Draw('same')

header = r'Y(60) \rightarrow XX'
legLabel = ROOT.TLatex()
legLabel.SetTextSize(0.035)
legLabel.DrawLatexNDC(0.55, 0.82, header)
c.SaveAs(outName)

x_min = data.GetXaxis().GetXmin()
x_max = data.GetXaxis().GetXmax()
y_min = data.GetMinimum()
y_max = data.GetMaximum()

## Plot the fb arrow
# Calculate the arrow coordinates relative to the axis range
arrow_x_start = x_min + 0.3 * (x_max - x_min)
arrow_x_end = x_min + 0.4 * (x_max - x_min)
arrow_y_start = y_min + 0.75 * (y_max - y_min)
arrow_y_end = y_min + 0.55 * (y_max - y_min)

FWline = ROOT.TLine(60-3.19, 640 ,60+3.19, 660)
FWline.SetLineWidth(2)
FWline.SetLineColor(4)
FWline.DrawClone()

# Plot the arrow
FWArrow = ROOT.TArrow(arrow_x_start, arrow_y_start, arrow_x_end, arrow_y_end, 0.02,"|>")
FWArrow.SetLineWidth(2)
FWArrow.SetFillColor(4)
FWArrow.DrawClone()

# plot the corresponding text
FWText = ROOT.TLatex()
FWText.SetTextSize(0.035)
FWText.DrawLatexNDC(0.3, 0.75, "#color[4]{ #splitline{Fixed}{Window} } " )
c.Update()
c.SaveAs(outName)
# 
## Plot the adaptive window lines
# Calculate the arrow coordinates relative to the axis range
arrow_x_start = x_min + 0.6 * (x_max - x_min)
arrow_x_end = x_min + 0.5 * (x_max - x_min)
arrow_y_start = y_min + 0.65 * (y_max - y_min)
arrow_y_end = y_min + 0.47 * (y_max - y_min)

AWline = ROOT.TLine(60-5.54, 565 ,60+5.54, 620)
AWline.SetLineWidth(2)
AWline.SetLineColor(3)
AWline.DrawClone()

# Plot the arrow
AWArrow = ROOT.TArrow(arrow_x_start, arrow_y_start, arrow_x_end, arrow_y_end, 0.02,"|>")
AWArrow.SetLineWidth(2)
AWArrow.SetFillColor(3)
AWArrow.DrawClone()

# plot the corresponding text
AWText = ROOT.TLatex()
AWText.SetTextSize(0.035)
AWText.DrawLatexNDC(0.55, 0.65, "#color[3]{ #splitline{Adaptive}{Window} } " )
c.Update()
c.SaveAs(outName)


myFile.Close()
c.SaveAs(outName+"]")
exit()

## Plot the fs arrow
# Calculate the arrow coordinates relative to the axis range
arrow_x_start = x_min + 0.6 * (x_max - x_min)
arrow_x_end = x_min + 0.5 * (x_max - x_min)
arrow_y_start = y_min + 0.6 * (y_max - y_min)
arrow_y_end = y_min + 0.42 * (y_max - y_min)

fsArrow = ROOT.TArrow(arrow_x_start, arrow_y_start, arrow_x_end, arrow_y_end, 0.02,"|>")
fsArrow.SetLineWidth(2)
fsArrow.SetFillColor(3)
fsArrow.DrawClone()

# plot the corresponding text
fsText = ROOT.TLatex()
fsText.SetTextSize(0.035)
fsText.DrawLatexNDC(0.55, 0.65, "#color[3]{ #splitline{Modeled}{Signal} } " )
c.Update()
c.SaveAs(outName)

## Plot the fsb arrow
# Calculate the arrow coordinates relative to the axis range
arrow_x_start = x_min + 0.15 * (x_max - x_min)
arrow_x_end = x_min + 0.3 * (x_max - x_min)
arrow_y_start = y_min + 0.8 * (y_max - y_min)
arrow_y_end = y_min + 0.6 * (y_max - y_min)

fsbArrow = ROOT.TArrow(arrow_x_start, arrow_y_start, arrow_x_end, arrow_y_end, 0.02,"|>")
fsbArrow.SetLineWidth(2)
fsbArrow.SetFillColor(2)
fsbArrow.DrawClone()
useless.append(fsbArrow)

# plot the corresponding text
fsbText = ROOT.TLatex()
fsbText.SetTextSize(0.035)
fsbText.DrawLatexNDC(0.2, 0.8, "#color[2]{#splitline{#splitline{Modeled}{Mass}}{Spectrum}}" )

c.Update()
c.SaveAs(outName)


c.SaveAs(outName)
myFile.Close()
# 
c.SaveAs(outName+"]")
exit()
