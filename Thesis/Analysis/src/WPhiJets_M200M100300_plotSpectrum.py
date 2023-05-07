import ROOT
import sys
import numpy as np
sys.path.insert(0, '/home/kpapad/UG_thesis/Thesis/share/lib')
from plotslib import create_legend, add_Header, set_axes_title
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
ROOT.gROOT.SetBatch(True)

## Functions
def aliases(df, original_vars, alias_vars):
    colNames = df.Display().AsString()
    for i, original in enumerate(original_vars):
        df = df.Alias(alias_vars[i], original) if original in colNames else df
    #
    return df
##
##
##


## Load Data 
p = 12 # smearing %
inPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"

sigNameSmeared = "WPhiJets_M60M5080Deltas_Application_Smeared"+str(p)+"_SIG_Test.root"
sigNameOriginal = "WPhiJets_M60M5080Deltas_Application_SIG_Test.root"
sigName = sigNameOriginal if p==0 else sigNameSmeared

bkgName = "WPhiJets_M60M5080Deltas_Application_BKG_Test.root"
sigFile,bkgFile = [inPath + inName for inName in (sigName, bkgName)]
#bkgFile = inPath + bkgName 

## Configure the output settings
#outName = "WPhiJets_M200M100300_Application_bkgFit.pdf"
outPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Plots/"
outNameSmeared = "WPhiJets_M60M5080_Application_Smeared"+str(p)+"_MassSpectrum.pdf"
outNameOriginal = "WPhiJets_M60M5080_Application_MassSpectrum.pdf"
outName = outNameOriginal if p==0 else outNameSmeared
outFile = outPath + outName

## Make the plot 
c = ROOT.TCanvas()
ROOT.gPad.SetLeftMargin(0.15)
ROOT.TGaxis.SetMaxDigits(2)
c.SetCanvasSize(800, 800)
c.cd()
c.SaveAs(outFile+'[')
df_data = ROOT.RDataFrame("tree", {sigFile, bkgFile} )
#df_data = ROOT.RDataFrame("tree", bkgFile)

c.SetLogy(0)
df_data = df_data.Histo1D(("df_data", " ; m_{XX} (GeV)", 50, 50, 75), "PairMass")
#
size = 0.045
set_axes_title(df_data, " m_{XX} (GeV)", "Counts / Bin")
df_data.GetXaxis().SetRangeUser(50, 75)
#df_data.GetXaxis().SetRangeUser(120, 300)
#df_data.GetYaxis().SetRangeUser(0.5, 1000)
df_data.GetYaxis().SetLabelSize(size)
df_data.GetYaxis().SetTitleSize(size)
df_data.GetXaxis().SetLabelSize(size)
df_data.GetXaxis().SetTitleSize(size)
df_data.GetYaxis().SetTitleOffset(1.5)
df_data.GetXaxis().SetNdivisions(205, ROOT.kFALSE);
df_data.SetMarkerColor(1)
df_data.SetLineColor(1)
df_data.SetMarkerStyle(8)
df_data.SetMarkerSize(1)
df_data.SetLineWidth(3)
df_data.Draw('EP')

'''
xmin = 120
xmax = 300
fb = ROOT.TF1( 'fb',
                '[0] + [1]/x^( 0.5 ) + [2]/x + [3]/x^1.5',  xmin, xmax)

b0 =  -4.46769e+03
b1 = 2.09374e+05
b2 = -3.27745e+06
b3 = 1.71866e+07
fb.SetParameter(0, b0)
fb.SetParameter(1, b1)
fb.SetParameter(2, b2)
fb.SetParameter(3, b3)
fb.SetLineColor(2)
fb.SetLineStyle(2)
fb.SetLineWidth(4)
fb.Draw('same')
'''

legend = ROOT.TLegend(0.60, 0.6, 0.7, 0.75)
legend.AddEntry(df_data.GetValue(), "Data")
#legend.AddEntry(fb, "Backgound", "l")
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetTextSize(size)
legend.Draw('same')

header = r'Y(60) \rightarrow XX'
legLabel = ROOT.TLatex()
legLabel.SetTextSize(size)
legLabel.DrawLatexNDC(0.60, 0.75, header)

c.SaveAs(outFile)
c.SaveAs(outFile + ']')
