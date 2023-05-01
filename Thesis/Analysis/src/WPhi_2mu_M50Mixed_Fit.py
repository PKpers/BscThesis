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
p = 20 # smearing %
inPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
sigName = "WPhiJets_M200M100300Deltas_Application_Smeared"+str(p)+"_SIG_Test.root"
#sigName = "WPhiJets_M200M100300Deltas_Application_SIG_Test.root"
bkgName = "WPhiJets_M200M100300Deltas_Application_BKG_Test.root"
sigFile,bkgFile = [inPath + inName for inName in (sigName, bkgName)]
#bkgFile = inPath + bkgName 

## Configure the output settings
outPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Plots/"
outName = "WPhiJets_M200M100300_Application_Smeared"+str(p)+"_AdaFit.pdf"
#outName = "WPhiJets_M200M100300_Application_bkgonly_Fit.pdf"
outFile = outPath + outName



## Make the plot 
c = ROOT.TCanvas()
c.cd()
c.SaveAs(outFile+'[')
df_data = ROOT.RDataFrame("tree", {sigFile, bkgFile} )
#print(df_data.Count().GetValue())
#df_data = ROOT.RDataFrame("tree", bkgFile)
smeared_vars = ("Pt1_Smeared", "Pt2_Smeared", "PairMass_smeared")
alias = ("Pt1", "Pt2", "PairMass")

# alias Pt_smeared and Mass_smeared with Pt and PairMass, if needed   
c.SetLogy(1)
# Save the plots to a root file for further editting 
#outHistROOTName="WPhiJets_M200M100300Deltas_Application_Smeared"+str(p)+"HistFit.root"
#ROOTHist=ROOT.TFile(outPath + outHistROOTName , "recreate")   

df_data = aliases(df_data, smeared_vars, alias)\
    .Define("weights", "1")\
    .Histo1D(("df_data", " ; m_{XX} (GeV)", 100, 100, 300), "PairMass", "weights")
#
df_data.GetXaxis().SetRangeUser(120, 300)
df_data.GetYaxis().SetRangeUser(0.5, 1000)
set_axes_title(df_data, " m_{XX} (GeV)", "Counts / Bin")

binWidth = df_data.GetXaxis().GetBinWidth(1)
print(binWidth)

df_data.SetMarkerColor(1)
df_data.SetLineColor(1)
df_data.SetMarkerStyle(8)
df_data.SetMarkerSize(0.5)
df_data.Write("data")
df_data.Draw('EP')

#Make the fit
xmin = 120
xmax = 300
# fix the background
b0 =  -4.46769e+03
b1 = 2.09374e+05
b2 = -3.27745e+06
b3 = 1.71866e+07

c.SetLogy(1)
fsb = ROOT.TF1( 'fsb',
                ' [0]*exp( -0.5*( (x-200)/[1] )**2 ) + [2] + [3]/x^( 0.5 ) + [4]/x + [5]/x^1.5', xmin, xmax)
#
fsb.SetParameter(0, 78)
fsb.SetParameter(1, 28)
fsb.FixParameter(2, b0)
fsb.FixParameter(3, b1)
fsb.FixParameter(4, b2)
fsb.FixParameter(5, b3)

fsb.SetLineColor(2)
fit=df_data.Fit(fsb, 'R' )
fit_ptr = ROOT.TFitResultPtr(fit)
#fsb.Write("fsb")

fb = ROOT.TF1( 'fb',
                '[0] + [1]/x^( 0.5 ) + [2]/x + [3]/x^1.5',  xmin, xmax)

fb.SetParameter(0, fsb.GetParameter(2))
fb.SetParameter(1,fsb.GetParameter(3))
fb.SetParameter(2,fsb.GetParameter(4))
fb.SetParameter(3,fsb.GetParameter(5))

fb.SetLineColor(4)
fb.SetLineStyle(2)
#fb.Write("fb")
fb.Draw('same')


fs = ROOT.TF1( 'fs', '[0]*exp(-0.5*((x-200)/[1])**2)', xmin, xmax)
fs.SetParameter(0,fsb.GetParameter(0))
fs.SetParameter(1,fsb.GetParameter(1))
#fs.SetParameter(2,fsb.GetParameter(2))
fs.SetLineColor( 3 )
fs.SetLineStyle(2)
#fs.Write("fs")
#ROOTHist.Close()
fs.Draw('Same')


#header = r'\phi \rightarrow \mu\mu'
#add_Header(header)

## Plot the legend
legend = ROOT.TLegend(0.65, 0.6, 0.75, 0.75)
legend.AddEntry(df_data.GetValue(), "Data(Smearing: {}%)".format(p))
legend.AddEntry(fb, "Backgound", "l")
legend.AddEntry(fs, "Signal", "l")
legend.AddEntry(fsb, "Signal + Background", "l")
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetTextSize(0.03)
legend.Draw('same')

header = r'Y(200) \rightarrow XX'
legLabel = ROOT.TLatex()
legLabel.SetTextSize(0.035)
legLabel.DrawLatexNDC(0.65, 0.77, header)


c.SaveAs(outFile)
#c.SaveAs(outFile + ']')
#exit()

c.SetLogy(0)
## Calculate the signal efficiency and bkg rejection 
mu = 200# mu is fixed
sigma = fsb.GetParameter(1)
errSigma = fsb.GetParError(1)

#df_data_axis = df_data.GetXaxis()
#s = [3.8420590627655393, 7.684118125531079, 11.526177188296618, 15.368236251062157, 19.210295313827697, 23.052354376593236] # the bounds are fixed by the 0% fit

s = [ i*0.5 * sigma  for i in range(1, 7)]
#print(s)
observation = np.array(
    [ fsb.Integral( (mu - si), (mu + si) )/binWidth for si in s]
)
background = np.array(
    [ fb.Integral( (mu - si), (mu + si) )/binWidth for si in s]
)
signal = abs(observation - background)
significance = signal/np.sqrt(background)
'''
print("\nSmearing: ", p,
    "\nsigma: ", s[2],
    "\nSignal: ", signal[2],
    "\nBackground: ", background[2],
    file=open("/home/kpapad/UG_thesis/Thesis/Analysis/out/tables.txt", "a")
)
'''
#significance = np.zeros(signal.shape[0]) 
sigma_range = np.array( [ i*0.5 for i in range(1, 7)] ) 
#print(observation)
#print(background)
#print(significance)

outSig=ROOT.TFile(outPath + "WPhiJets_M200M100300Deltas_Application_Smeared"+str(p)+"Ada.root", "recreate")   
#outSig=ROOT.TFile(outPath + "WPhiJets_M200M100300Deltas_Application_Smeared"+str(p)+".root", "recreate")   
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
Mu = fit_report.AddText(r'\mu: {:.2f}\pm{:.2f}'.format(mu, float(0)))
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
