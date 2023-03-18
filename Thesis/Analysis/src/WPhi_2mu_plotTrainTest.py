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
input_dir = "~/UG_thesis/Thesis/Analysis/out/Data/"
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
    ('{}{}{}.root'.format(input_dir, fileName+l, 'Test'),
     '{}{}{}.root'.format(input_dir, fileName+l, 'Train'))
    for l in label
]

## Configure output settings ##
output_dir = "~/UG_thesis/Thesis/Analysis/out/Plots/"
outName = sys.argv[2]
output_fnames = outName+".pdf"

## Read the data ##
purpose = ('Test', 'Train')
Type = ('Signal', 'background')
dataFrames = []
dfNames = []
## Open the root files in dataframes and gather them in a list
for j, File in enumerate(infiles):
    df_1 = ROOT.RDataFrame(TreeName, File[0]) 
    df1_name = purpose[0]+Type[j]
    
    df_2 = ROOT.RDataFrame(TreeName, File[1])
    df2_name = purpose[1]+Type[j]
    dataFrames.append( df_1)
    dataFrames.append( df_2)
    dfNames.append( df1_name )
    dfNames.append( df2_name )

## Plot ##
## Create the canvas
datasets = []
c_nums = ROOT.TCanvas("c_nums", "c_nums", 1000, 700)
c_nums .Divide(2,2)
c_nums.SetBottomMargin(0.2)
c_nums.SetLogx(0); c_nums.SetLogy(1)
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
c_nums.SaveAs(output_dir+output_fnames+str("["))

## Plots configuration
hist_range = {
    0: (0, 300),
    1: (0, 300),
    2: (-5, 5),
    3: (0,10),
    4: (-4,4)
}
draw_loc = {
    0: 'hist',
    1: 'same'
}
h_num = []
headers = ['Test Signal', 'Train signal', 'Test Background', 'Train Background' ]

## Itterate over the files and plot the histograms
nbins = 50
line_color = [1,4]
for i, b in enumerate(branch_names):
    for j, df in enumerate(dataFrames):
        nums_1 =(df, 'df'+b, b, b) 
        '''
        nums_1 = [
            (df, 'df'+b+str(k), b+str(k), b+str(k))
            for k in (1,2)
        ]
        '''
        #
        # change to the wanted pad 
        cpads = j+1
        c_nums.cd(cpads)

        # histogram configuration
        histRange = hist_range[i]
        histOpts = (nbins, histRange) 
        ax_labels =(b, "counts")
        legend_entries = {}
        ## Make the plots 
        DrawLoc=draw_loc[0]
        lca_ = (line_color[0], 1)
        pltData = ( nums_1[0], nums_1[2])
        hist = PlotHist(
            nums_1[1], pltData, histOpts, ax_labels,
            DrawLoc, lca = lca_#lca: line color attrubute
        )
        h_num.append(hist)
        legend_entries[nums_1[1]] = (nums_1[-1], 'l')
        
        add_Header(headers[j])

        '''
        for k in range(len(nums_1)):
            DrawLoc=draw_loc[k]
            lca_ = (line_color[k], 1)
            pltData = ( nums_1[k][0], nums_1[k][2])
            hist = PlotHist(
            nums_1[k][1], pltData, histOpts, ax_labels,
            DrawLoc, lca = lca_#lca: line color attrubute
            )
            h_num.append(hist)
            legend_entries[nums_1[k][1]] = (nums_1[k][-1], 'l')
            
        add_Header(headers[j])
        '''
    #
    legend_loc = (0.6, 0.5, 0.9, 0.6)
    legend = create_legend(legend_loc, legend_entries)
    c_nums.cd()
    c_nums.SaveAs(output_dir+output_fnames)
#
c_nums.SaveAs(output_dir+output_fnames+"]")
##
