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
inPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
sigName = "WPhiJets_M60MixedDeltas_Application_Smeared60_SIG_Test.root"
bkgName = "WPhiJets_M60MixedDeltas_Application_BKG_Test.root"
sigFile,bkgFile = [inPath + inName for inName in (sigName, bkgName)]
#bkgFile = inPath + bkgName 

## Configure the output settings
outPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Plots/"
outName = "WPhiJets_M60Mixed_Application_Smeared60_Fit.pdf"
outFile = outPath + outName



## Make the plot 
c = ROOT.TCanvas()
c.cd()
c.SaveAs(outFile+'[')
#ROOT.gStyle.SetOptFit(11);
df_data = ROOT.RDataFrame("tree", {sigFile, bkgFile})
#df_data = ROOT.RDataFrame("tree", bkgFile)
smeared_vars = ("Pt1_Smeared", "Pt2_Smeared", "PairMass_smeared")
alias = ("Pt1", "Pt2", "PairMass")

# alias Pt_smeared and Mass_smeared with Pt and PairMass, if needed   
df_data = aliases(df_data, smeared_vars, alias)\
    .Define("weights", "1/(abs(119-21)/50)")\
    .Histo1D(("df_bkg", "; m_{\mu\mu} [GeV]", 50, 20, 120), "PairMass", "weights")
#

# normalize the hist such that integrating over the bins gives the total number of events
binWidth = df_data.GetXaxis().GetBinWidth(1)
print(binWidth)
#df_data.Scale(1 / binWidth)
df_data.SetMarkerColor(1)
df_data.SetLineColor(1)
df_data.SetMarkerStyle(8)
df_data.SetMarkerSize(0.5)
df_data.Draw('PE')

#Make the fit
fsb = ROOT.TF1( 'fit',
                '[0]*exp(-0.5*((x-[1])/[2])**2)+[3]+ [4]*x + [5]*x*x + [6]*x*x*x + [7]*x*x*x*x*x',  20, 120 )
fsb.SetParameter(0, 3500)
fsb.SetParameter(1, 61)
fsb.SetParameter(2, 5)
fsb.SetParameter(3,1700)
fsb.SetLineColor(2)
fit = df_data.Fit( fsb, 'LRS' )
fit_ptr = ROOT.TFitResultPtr(fit)

fb = ROOT.TF1( 'fb', '[0]+[1]*x + [2]*x*x + [3]*x*x*x + [4]*x*x*x*x*x',  21, 119 )
fb.SetParameter(0,fsb.GetParameter(3))
fb.SetParameter(1,fsb.GetParameter(4))
fb.SetParameter(2,fsb.GetParameter(5))
fb.SetParameter(3,fsb.GetParameter(6))
fb.SetParameter(4,fsb.GetParameter(7))
fb.SetParameter(5,fsb.GetParameter(8))
fb.SetLineColor(4)
fb.SetLineStyle(2)
fb.Draw('same')

fs = ROOT.TF1( 'fs', '1650 + [0]*exp(-0.5*((x-[1])/[2])**2)',  21, 119 )
fs.SetParameter(0,fsb.GetParameter(0))
fs.SetParameter(1,fsb.GetParameter(1))
fs.SetParameter(2,fsb.GetParameter(2))
fs.SetLineColor( 3 )
fs.SetLineStyle(2)
fs.Draw('Same')

#lower_bound = ROOT.TLine(40, 500, 40, 680)
#upper_bound = ROOT.TLine(55, 500, 55, 680)
#lower_bound.SetLineColor(1)
#lower_bound.SetLineStyle(2)
#upper_bound.SetLineColor(1)
#upper_bound.SetLineStyle(2)
#lower_bound.Draw('Same')
#upper_bound.Draw('Same')

header = r'\phi \rightarrow \mu\mu'
add_Header(header)
c.SaveAs(outFile)

## Calculate the signal efficiency and bkg rejection 
mu = fsb.GetParameter(1)
errMu = fsb.GetParError(1)
sigma = fsb.GetParameter(2)
errSigma = fsb.GetParError(2)

df_data_axis = df_data.GetXaxis()
mu_bin = df_data_axis.FindBin(mu)
sigma_bin = int(sigma/binWidth) if int(sigma/binWidth)!=0 else int(sigma/binWidth) + 1 
#l_bounds_df = [df_data_axis.FindBin( mu - 0.5*i*sigma ) for i in range(1, 7)]
#l_bounds_df = [int( mu_bin - i*0.5*sigma_bin)  for i in range(1, 7)]
#u_bounds_df = [int( mu_bin + i*0.5*sigma_bin)  for i in range(1, 7)]
#u_bounds_df = [df_data_axis.FindBin( mu + 0.5*i*sigma ) for i in range(1, 7)]

# The bounds are fixed from the 0 smearing fit 
l_bounds_df = [19, 19, 18, 18, 17, 17]
u_bounds_df = [20, 21, 21, 22, 22, 23]

#fb_axis = fb.GetXaxis()
#l_bounds_fb = [fb_axis.FindBin( mu - 0.5*i*sigma ) for i in range(1, 7)]
#u_bounds_fb = [fb_axis.FindBin( mu + 0.5*i*sigma ) for i in range(1, 7)]

#print(l_bounds_fb)
#print(u_bounds_fb)

observation = np.array(
    [ df_data.Integral(l_bounds_df[i], u_bounds_df[i]) for i in range(len(l_bounds_df)) ]
)
background = np.array(
    [ fb.Integral(l_bounds_df[i], u_bounds_df[i]) for i in range(len(l_bounds_df)) ]
)#normalize for the bin width
#print(background[9]/background[-1])
signal = abs(observation - background)
significance = signal/np.sqrt(background)
sigma_range = np.array( [ i*0.5 for i in range(1,7)] ) 
print(l_bounds_df)
print(u_bounds_df)
print(observation)
print(background)
## Plot the significance

outSig=ROOT.TFile(outPath + "WPhiJets_M60MixedDeltas_Application_Smeared60.root", "recreate")   
sign = ROOT.TMultiGraph("sign", "Significance")

significance_plot = ROOT.TGraph( sigma_range.shape[0], sigma_range, significance )
significance_plot.SetName("significance_plot")
significance_plot.SetDrawOption("P")
significance_plot.SetMarkerColor(4)
significance_plot.SetMarkerStyle(20)

sign.Add(significance_plot)
set_axes_title(sign, r"\sigma", "")
sig_lab = r'\frac{sig}{\sqrt{bkg}}'
sign.Write("significance")
outSig.Close()
sign.Draw('AP')

Ylabel = ROOT.TLatex()
Ylabel.SetTextSize(0.035)
Ylabel.DrawLatexNDC(0.01, 0.85, sig_lab)
c.SaveAs(outFile)
c.Update()
#c.SaveAs(outFile+"]")
#exit()
## Draw the fit report
frame =ROOT.TH1F() # I need wither a Graph class or a TH class to "clear" the canvas
frame.Draw("AI")
add_Header('Fit Report')
fit_report = ROOT.TPaveText(.05, .1, .95, .9);
fit_report.SetTextSize(0.04)

#sb = fit_report.AddText('S + B: {:.2f}'.format(observation))
#s = fit_report.AddText('S: {:.2f}'.format(signal))
#b = fit_report.AddText('B: {:.2f}'.format(background))
#sign = fit_report.AddText(r'\frac{{S}}{{\sqrt{{B}}}}: {:.2f}'.format(significance))
Mu = fit_report.AddText(r'\mu: {:.2f}\pm{:.2f}'.format(mu, errMu))
Sigma = fit_report.AddText(r'\sigma: {:.2f}\pm{:.2f}'.format(sigma, errSigma))
ndf = fit_report.AddText('NDF: {:.2f}'.format(fsb.GetNDF()))
chi2 = fit_report.AddText((r'x^{{2}}: {:.2f}'.format(fsb.GetChisquare())))
chi2_ndf = fit_report.AddText((r'x^{{2}}/NDF: {:.2f}'.format(fsb.GetChisquare()/fsb.GetNDF())))


fit_report.Draw('same')
c.Update()
c.SaveAs(outFile)

c.SaveAs(outFile+']')
exit()
print('S ',fs.Integral(38, 58))
print('B ',fb.Integral(38, 58))
print('NDF ',fsb.GetNDF())
print('Chi2 ',fsb.GetChisquare())
print('Chi2/NDF ',fsb.GetChisquare()/fsb.GetNDF(),'\n')

exit()
