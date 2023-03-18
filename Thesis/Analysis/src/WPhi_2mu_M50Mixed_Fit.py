import ROOT
import sys
sys.path.insert(0, '/home/kpapad/UG_thesis/Thesis/share/lib')
from plotslib import create_legend, add_Header 
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
ROOT.gROOT.SetBatch(True)
## Load Data 
inPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/"
inName ="WPhi_2mu_M50Mixed_Deltas.root"
inFile = inPath + inName

## Configure the output settings
outPath = "/home/kpapad/UG_thesis/Thesis/Analysis/out/Plots/"
outName = "WPhi_2mu_M50Mixed_Fit.pdf"
outFile = outPath + outName

## Make the plot 
c = ROOT.TCanvas()
c.cd()
c.SaveAs(outFile+'[')

df_data = ROOT.RDataFrame("tree", inFile)\
              .Define("weights", "1/(abs(119-21)/50)")\
              .Histo1D(("df_bkg", "; m_{\mu\mu} [GeV]", 50, 21, 119), "PairMass", "weights")
#
# normalize the hist such that integrating over the bins gives the total number of events
binWidth = df_data.GetXaxis().GetBinWidth(1)
#df_data.Scale(1 / binWidth)
df_data.SetMarkerColor(1)
df_data.SetLineColor(1)
df_data.SetMarkerStyle(8)
df_data.SetMarkerSize(0.5)
df_data.Draw('PE')

#Make the fit
fsb = ROOT.TF1( 'fit', '[0]*exp(-0.5*((x-[1])/[2])**2)+[3]+[4]*x+[5]*x*x - [6]*x*x*x',  21,119 )
fsb.SetParameter(1,50)
fsb.SetParameter(2,10)
fsb.SetParameter(3,550)
fsb.SetLineColor(2)
fit = df_data.Fit( fsb, 'LRS' )
fit_ptr = ROOT.TFitResultPtr(fit)

fb = ROOT.TF1( 'fb', '[0]+[1]*x+[2]*x*x - [3]*x*x*x',  21, 119 )
fb.SetParameter(0,fsb.GetParameter(3))
fb.SetParameter(1,fsb.GetParameter(4))
fb.SetParameter(2,fsb.GetParameter(5))
fb.SetParameter(3,fsb.GetParameter(6))
fb.SetLineColor(4)
fb.SetLineStyle(2)
fb.Draw('same')

fs = ROOT.TF1( 'fs', '450 + [0]*exp(-0.5*((x-[1])/[2])**2)',  21, 119 )
fs.SetParameter(0,fsb.GetParameter(0))
fs.SetParameter(1,fsb.GetParameter(1))
fs.SetParameter(2,fsb.GetParameter(2))
fs.SetLineColor( 3 )
fs.SetLineStyle(2)
fs.Draw('Same')

header = r'\phi \rightarrow \mu\mu'
add_Header(header)
c.SaveAs(outFile)

## Draw the fit report 
frame =ROOT.TH1F() # I need wither a Graph class or a TH class to "clear" the canvas
frame.Draw("AI")
add_Header('Fit Report')
fit_report = ROOT.TPaveText(.05, .1, .95, .9);
fit_report.SetTextSize(0.04)

## To calculate the signal efficiency and bkg rejection I take a signal using 2sigma around median 
observation = df_data.Integral(38, 58)
background = fb.Integral(38, 58)/binWidth # normalize for the bin width

sb = fit_report.AddText('S + B: {:.2f}'.format(observation))
s = fit_report.AddText('S: {:.2f}'.format(abs(observation - background)))
b = fit_report.AddText('B: {:.2f}'.format(background))
ndf = fit_report.AddText('NDF: {:.2f}'.format(fsb.GetNDF()))
chi2 = fit_report.AddText((r'x^{{2}}: {:.2f}'.format(fsb.GetChisquare())))
chi2_ndf = fit_report.AddText(('chi2/NDF: {:.2f}'.format(fsb.GetChisquare()/fsb.GetNDF())))


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
