import ROOT
import sys

sys.path.insert(0, '/home/kpapad/UG_thesis/Thesis/share/lib')
from plotslib import set_axes_title, create_legend, add_Header 
ROOT.gROOT.SetBatch(True)

## I/O configuration ----------------------------------------------------------------------------------------------------
inFilePath = '/home/kpapad/UG_thesis/Thesis/Analysis/out/Data/' 
outFilePath = '/home/kpapad/UG_thesis/Thesis/Analysis/out/Plots/' 
# Help message
if len(sys.argv) != 3:
    print("Usage: {} {} {}".format(sys.argv[0], ' input_file', 'output_file'))
    print('Default input dir: {} \ndefault output dir: {}'.format(inFilePath, outFilePath))
    exit(-1)

# input file conf
inFileName = sys.argv[1]
inFile = inFilePath + inFileName
# output file conf
outFileName = sys.argv[2]
outFile = outFilePath + outFileName
#mass = int(outFileName.split('M')[1].split('_')[0])
## Load the histogram ----------------------------------------------------------------------------------------------------
myFile=ROOT.TFile.Open(inFile, "READ")
hist=myFile.Get("muon_mass_hist")
hist.SetDirectory(0)
myFile.Close()
## Make the plot ----------------------------------------------------------------------------------------------------
size = 0.045
c = ROOT.TCanvas()
c.cd()
c.SetLogx(0); c.SetLogy(1)
c.SetCanvasSize(800, 800)
ROOT.gPad.SetLeftMargin(0.15)
c.cd()
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
hist.GetXaxis().SetRangeUser(50, 300)
hist.GetYaxis().SetLabelSize(size)
hist.GetYaxis().SetTitleSize(size)
hist.GetXaxis().SetLabelSize(size)
hist.GetXaxis().SetTitleSize(size)
hist.GetYaxis().SetTitleOffset(1.5)
hist.SetLineWidth(2)
hist.SetLineStyle(2)
hist.SetMarkerStyle(8)
hist.SetMarkerSize(1)
hist.Draw("L")
hist2 = hist.Clone()
hist2.SetLineStyle(1)
hist2.SetLineColor(1)
hist2.Draw("sameE")
text = r"\gamma * / Z \rightarrow ll"
legend = ROOT.TLegend(0.55, 0.72, 0.65, 0.85)

legend.AddEntry(hist, text)
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetTextSize(0.05)
legend.Draw('same')

#add_Header('M = {}GeV'.format(mass))
set_axes_title(hist, 'm_{ll} (GeV)', 'Count / Bin')
c.SaveAs(outFile)


