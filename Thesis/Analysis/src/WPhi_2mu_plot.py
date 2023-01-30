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
mass = int(outFileName.split('M')[1].split('_')[0])
## Load the histogram ----------------------------------------------------------------------------------------------------
myFile=ROOT.TFile.Open(inFile, "READ")
hist=myFile.Get("muon_mass_hist")
hist.SetDirectory(0)
myFile.Close()
## Make the plot ----------------------------------------------------------------------------------------------------
c = ROOT.TCanvas()
c.cd()
c.SetLogx(0); c.SetLogy(1)
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
hist.Draw()
add_Header('W Phi 2 mu, M = {}GeV'.format(mass))
set_axes_title(hist, 'Mass[GeV]', 'Events')
c.SaveAs(outFile)


