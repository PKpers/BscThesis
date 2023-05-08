#!/usr/bin/python
import sys
import ROOT

sys.path.insert(0, '/home/kpapad/UG_thesis/Thesis/share/lib')
from plotslib import set_axes_title, PlotHist, create_legend, add_Header, PlotHist2, PlotScatter 
ROOT.gROOT.SetBatch(True)

## Help message in case of wrong usage ## 
if len(sys.argv) != 3:
    print("Usage: {} {} {}".format(sys.argv[0], ' input_dataset', 'output_name'))
    exit(-1)

## Load data 
input_dir = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
fileName = sys.argv[1] 

## Figure out the coordinate system from the dataset name ##
if "Pxyz" in fileName:
    branch_names = ['Px', 'Py', 'Pz']
elif "Deltas" in fileName:
    branch_names = ["Pt1", "Pt2", "DeltaPhi", "DeltaR", "DeltaEta"]
else:
    branch_names = ['Pt', 'Eta', 'Phi']
#

TreeName = "tree"
label = ("_SIG_", "_BKG_")
infiles = [
    ('{}{}{}.root'.format(input_dir, fileName+l, 'Train'))
    for l in label
]

## Configure output settings ##
output_dir = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Plots/"
outName = sys.argv[2]
output_fnames = outName+".pdf"

## Read the data ##
'''
purpose = ('Train',)
Type = ('Signal', 'background')
dataFrames = []
dfNames = []
## Open the root files in dataframes and gather them in a list
for j, File in enumerate(infiles):
    df_1 = ROOT.RDataFrame(TreeName, File[0]) 
    df1_name = purpose[0]+Type[j]
    
    dataFrames.append( df_1)
    dfNames.append( df1_name )
#
'''
## Plot ##
## Create the canvas
df_sig = ROOT.RDataFrame("tree", infiles[0])
df_bkg = ROOT.RDataFrame("tree", infiles[1])

datasets = []
c_nums = ROOT.TCanvas("c_nums", "c_nums", 1000, 700)
#c_nums.SetBottomMargin(0.2)
c_nums.SetLeftMargin(0.2)
c_nums.SetLogx(0); c_nums.SetLogy(1)
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
c_nums.SaveAs( output_dir+output_fnames+str("[") )

## Plot the Pt1 and Pt2 in the same page in different pads of canvas
## Plot pt1 first
c_nums .Divide(2,1)
c_nums.cd(1)
ROOT.gPad.SetLeftMargin(0.15)
ROOT.gPad.SetBottomMargin(0.15)
ROOT.gStyle.SetLabelSize(0.05)
ROOT.gStyle.SetTitleSize(0.05)

Pt1_sig = df_sig.Histo1D( ("Pt1_sig", "; Pt (GeV) ; Counts / Bin", 50, -5, 700), "Pt1")
Pt1_sig.GetYaxis().SetRangeUser(0, 1300)
Pt1_sig.GetYaxis().SetLabelSize(0.05)
Pt1_sig.GetYaxis().SetTitleSize(0.05)
Pt1_sig.GetYaxis().SetMaxDigits(2)
Pt1_sig.GetXaxis().SetLabelSize(0.05)
Pt1_sig.GetXaxis().SetTitleSize(0.05)
Pt1_sig.SetLineColor(ROOT.kBlue)
Pt1_sig.SetFillStyle(1001)
Pt1_sig.SetFillColorAlpha(ROOT.kBlue, 0.2)
Pt1_sig.Draw()

Pt1_bkg = df_bkg.Histo1D(("Pt1_bkg", " ; Pt (GeV)", 100, -5, 700), "Pt1")
Pt1_bkg.SetLineColor(ROOT.kBlack)
Pt1_bkg.SetFillStyle(1001)
Pt1_bkg.SetFillColorAlpha(ROOT.kGray, 0.2)
Pt1_bkg.Draw('same')

# Plot the legend
pt1_legend = ROOT.TLegend(0.4, 0.6, 0.55, 0.75)
pt1_legend.AddEntry(Pt1_sig.GetValue(), "Pt1 Signal", 'lf')
pt1_legend.AddEntry(Pt1_bkg.GetValue(), "Pt1 Background", 'lf')
pt1_legend.SetFillColor(0)
pt1_legend.SetBorderSize(0)
pt1_legend.SetTextSize(0.055)
pt1_legend.Draw('same')

## Plot Pt2
c_nums.cd(2)
ROOT.gPad.SetLeftMargin(0.15)
ROOT.gPad.SetBottomMargin(0.15)

Pt2_sig = df_sig.Histo1D( ("Pt2_sig", "; Pt (GeV) ; Counts / Bins", 50, -5, 700), "Pt2")
Pt2_sig.GetYaxis().SetRangeUser(0, 1300)
Pt2_sig.GetYaxis().SetLabelSize(0.05)
Pt2_sig.GetYaxis().SetTitleSize(0.05)
Pt2_sig.GetYaxis().SetMaxDigits(2)
Pt2_sig.GetXaxis().SetLabelSize(0.05)
Pt2_sig.GetXaxis().SetTitleSize(0.05)
Pt2_sig.SetLineColor(ROOT.kBlue)
Pt2_sig.SetFillStyle(1001)
Pt2_sig.SetFillColorAlpha(ROOT.kBlue, 0.2)
Pt2_sig.Draw()

Pt2_bkg = df_bkg.Histo1D(("Pt2_bkg", " ; Pt (GeV)", 100, -5, 700), "Pt2")
Pt2_bkg.SetLineColor(ROOT.kBlack)
Pt2_bkg.SetFillStyle(1001)
Pt2_bkg.SetFillColorAlpha(ROOT.kGray, 0.2 )
Pt2_bkg.Draw('same')

# Plot the legend
pt2_legend = ROOT.TLegend(0.4, 0.6, 0.55, 0.75)
pt2_legend.AddEntry(Pt2_sig.GetValue(), "Pt2 Signal", 'lf')
pt2_legend.AddEntry(Pt2_bkg.GetValue(), "Pt2 Background", 'lf')
pt2_legend.SetFillColor(0)
pt2_legend.SetBorderSize(0)
pt2_legend.SetTextSize(0.055)
pt2_legend.Draw('same')

c_nums.SaveAs(output_dir+output_fnames)
## Plot Delta eta, Delta phi and Delta R preferabli inthe same canvas 
## Plot Dleta Eta
ROOT.gStyle.SetTextFont(42)
ROOT.gStyle.SetLabelSize(0.05)
ROOT.gStyle.SetTitleSize(0.05)

c_nums.cd(0)
c_nums.Clear()
c_nums .Divide(3,1)
c_nums.cd(1)

ROOT.gPad.SetLeftMargin(0.25)
ROOT.gPad.SetBottomMargin(0.15)
ROOT.gPad.SetTopMargin(0.15)

DEta_sig = df_sig.Histo1D( ("Deta_sig", ";\Delta\eta ; Counts / Bin", 50, -5, 5), "DeltaEta")
DEta_sig.GetYaxis().SetRangeUser(0, 400)
DEta_sig.GetYaxis().SetLabelSize(0.07)
DEta_sig.GetYaxis().SetTitleSize(0.07)
DEta_sig.GetXaxis().SetLabelSize(0.07)
DEta_sig.GetXaxis().SetTitleSize(0.07)
DEta_sig.SetLineColor(ROOT.kBlue)
DEta_sig.SetFillStyle(1001)
DEta_sig.SetFillColorAlpha(ROOT.kBlue, 0.2)
DEta_sig.Draw('hist')

DEta_bkg = df_bkg.Histo1D(("DEta_bkg", ";\Delta\eta ; Counts / Bin", 100, -5, 5), "DeltaEta")
DEta_bkg.SetLineColor(ROOT.kBlack)
DEta_bkg.SetFillStyle(1001)
DEta_bkg.SetFillColorAlpha(ROOT.kGray, 0.2 )
DEta_bkg.Draw('same')

# Plot the legend
DEta_legend = ROOT.TLegend(0.3, 0.70, 0.75, 0.8)
DEta_legend.AddEntry(DEta_sig.GetValue(), r"\Delta\eta Signal", 'lf')
DEta_legend.AddEntry(DEta_bkg.GetValue(), r"\Delta\eta Background", 'lf')
DEta_legend.SetFillColor(0)
DEta_legend.SetBorderSize(0)
DEta_legend.SetTextSize(0.075)
DEta_legend.Draw('same')

## Plot Delta phi
c_nums.cd(2)
ROOT.gPad.SetLeftMargin(0.25)
ROOT.gPad.SetBottomMargin(0.15)
ROOT.gPad.SetTopMargin(0.15)

DPhi_sig = df_sig.Histo1D( ("DPhi_sig", ";\Delta\phi ; Counts / Bin", 50, -5, 5), "DeltaPhi")
DPhi_sig.GetYaxis().SetRangeUser(0, 800)
DPhi_sig.GetYaxis().SetLabelSize(0.07)
DPhi_sig.GetYaxis().SetTitleSize(0.07)
DPhi_sig.GetXaxis().SetLabelSize(0.07)
DPhi_sig.GetXaxis().SetTitleSize(0.07)
DPhi_sig.SetLineColor(ROOT.kBlue)
DPhi_sig.SetFillStyle(1001)
DPhi_sig.SetFillColorAlpha(ROOT.kBlue, 0.2)
DPhi_sig.Draw('hist')

DPhi_bkg = df_bkg.Histo1D(("DPhi_bkg", " ; \Delta\phi ; Counts / Bin", 100, -5, 5), "DeltaPhi")
DPhi_bkg.SetLineColor(ROOT.kBlack)
DPhi_bkg.SetFillStyle(1001)
DPhi_bkg.SetFillColorAlpha(ROOT.kGray, 0.2 )
DPhi_bkg.Draw('same')

# Plot the legend
DPhi_legend = ROOT.TLegend(0.3, 0.7, 0.75, 0.82)
DPhi_legend.AddEntry(DPhi_sig.GetValue(), r"\Delta\phi Signal", 'lf')
DPhi_legend.AddEntry(DPhi_bkg.GetValue(), r"\Delta\phi Background", 'lf')
DPhi_legend.SetFillColor(0)
DPhi_legend.SetBorderSize(0)
DPhi_legend.SetTextSize(0.075)
DPhi_legend.Draw('same')

## Plot Delta R
c_nums.cd(3)
ROOT.gPad.SetLeftMargin(0.25)
ROOT.gPad.SetBottomMargin(0.15)
ROOT.gPad.SetTopMargin(0.15)

DR_sig = df_sig.Histo1D( ("DR_sig", ";\DeltaR ; Counts / Bin", 50, -1, 10), "DeltaR")
DR_sig.GetYaxis().SetRangeUser(0, 400)
DR_sig.GetYaxis().SetLabelSize(0.07)
DR_sig.GetYaxis().SetTitleSize(0.07)
DR_sig.GetXaxis().SetLabelSize(0.07)
DR_sig.GetXaxis().SetTitleSize(0.07)
DR_sig.SetLineColor(ROOT.kBlue)
DR_sig.SetFillStyle(1001)
DR_sig.SetFillColorAlpha(ROOT.kBlue, 0.2)
DR_sig.Draw('hist')

DR_bkg = df_bkg.Histo1D(("DR_bkg", r" ; \DeltaR ; Counts / Bin", 100, -1, 10), "DeltaR")
DR_bkg.SetLineColor(ROOT.kBlack)
DR_bkg.SetFillStyle(1001)
DR_bkg.SetFillColorAlpha(ROOT.kGray, 0.2 )
DR_bkg.Draw('same')

# Plot the legend
DR_legend = ROOT.TLegend(0.35, 0.73, 0.5, 0.83)
DR_legend.AddEntry(DR_sig.GetValue(), r"\DeltaR Signal", 'lf')
DR_legend.AddEntry(DR_bkg.GetValue(), r"\DeltaR Background", 'lf')
DR_legend.SetFillColor(0)
DR_legend.SetBorderSize(0)
DR_legend.SetTextSize(0.075)
DR_legend.Draw('same')

c_nums.SaveAs(output_dir+output_fnames)
c_nums.SaveAs(output_dir+output_fnames+"]")
exit()
