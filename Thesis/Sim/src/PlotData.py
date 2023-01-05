#!/usr/bin/python
import sys
import ROOT

sys.path.insert(0, '/home/kpapad/UG_thesis/Thesis/share/lib')
from plotslib import set_axes_title, PlotHist, create_legend, add_Header, PlotHist2, PlotScatter 
ROOT.gROOT.SetBatch(True)
#
## Help message in case of wrong usage ## 
#
if len(sys.argv) != 3:
    print("Usage: {} {} {}".format(sys.argv[0], ' input_dataset', 'output_name'))
    exit(-1)
#
## Load data #3
#
input_dir = "~/UG_thesis/Thesis/Sim/out/Data/"
fileName = sys.argv[1] 
#
## Figure out the coordinate system from the dataset code ##
#
if "Pxyz" in fileName:
    branch_names = ['Px1', 'Py1', 'Pz1']
else:
    branch_names = ['Pt1', 'Eta1', 'Phi1']
#
TreeName = "myTree"
infiles = [
    ('{}{}{}.root'.format(input_dir, fileName+str('_SIG_'), p),
     '{}{}{}.root'.format(input_dir, fileName+str("_BKG_"), p))
    for p in ('Test', 'Train')
]
#
## Configure output settings ##
#
output_dir = "~/UG_thesis/Thesis/Sim/out/PLots/"
outName = sys.argv[2]
output_fnames = outName+"DataPLot.pdf"
#
## Read the data ##
#
purpose = ('Test', 'Train')
Type = ('Signal', 'background')
dataFrames = []
dfNames = []
for j, File in enumerate(infiles):
    df_1 = ROOT.RDataFrame(TreeName, File[0])
    df1_name = purpose[j]+Type[0]
    #
    df_2 = ROOT.RDataFrame(TreeName, File[1])
    df2_name = purpose[j]+Type[1]
    dataFrames.append( (df_1, df_2) )
    dfNames.append( (df1_name, df2_name) )
#
#
## Plot ##
#
datasets = []
c_nums = ROOT.TCanvas("c_nums", "c_nums", 1000, 700)
c_nums .Divide(2,2,0,0)
c_nums.SetBottomMargin(0.2)
c_nums.SetLogx(0); c_nums.SetLogy(1)
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
c_nums.SaveAs(output_dir+output_fnames+str("["))
# Plots configuration
h_num = []
legend_entries = {} 
nbins = 50
histRange = (-50, 50)
histOpts = (nbins, histRange)
_Lcolor = [ (3,2),(4,1) ]

legend_entries = {}
for j, df in enumerate(dataFrames):
    df_1 = df[0]
    df1_name = dfNames[j][0]
    #
    nums_1 = [
        (df_1, 'df1'+v, v, v)
        for v in branch_names
    ]
    # Plot the signal dist of numbers in each event for the testing and training set
    if j == 0:
        cpads = 1
    else:
        cpads = 2 
    #
    c_nums.cd(cpads)
    nbins = 50
    histRange = (-10, 10)
    histOpts = (nbins, histRange) 
    ax_labels =("event components", 'counts')
    _Lcolor = [ 4,2,3,1]
    for i in range(len(nums_1)):
        lca_ = (_Lcolor[i], 1)
        pltData = ( nums_1[i][0], nums_1[i][2])
        if i == 0 and j==0:
            DrawLoc = 'hist'
        else:
            DrawLoc = 'same'
        #
        hist = PlotHist(
            nums_1[i][1], pltData, histOpts, ax_labels,
            DrawLoc, lca = lca_
        )
        h_num.append(hist)
        legend_entries[nums_1[i][1]] = (nums_1[i][-1], 'l')
        add_Header(purpose[j]+' Signal')
    #
    legend_loc = (0.6, 0.2, 0.9, 0.3)
    legend = create_legend(legend_loc, legend_entries)
#
#legend_loc = (0.6, 0.2, 0.9, 0.3)
#legend = create_legend(legend_loc, legend_entries)
#
legend_entries = {}
for j, df in enumerate(dataFrames):
    df_2 = df[1]
    df2_name = dfNames[j][1]
    #
    nums_2 = [
        (df_2, 'df2'+v, v, v)
        for v in branch_names
    ]
    # Plot the signal dist of numbers in each event for the testing and training set
    if j==0:
        cpads = 3 
    else:
        cpads = 4
    #
    c_nums.cd(cpads)
    nbins = 50
    histRange = (-10, 10)
    histOpts = (nbins, histRange) 
    ax_laebels =("event components", 'counts')
    _Lcolor = [ 4,2,3,1]
    for i in range(len(nums_2)):
        pltData = (nums_2[i][0], nums_2[i][2])
        lca_ = (_Lcolor[i], 1)
        if i == 0:
            DrawLoc = 'hist'
        else:
            DrawLoc = 'same'
        #
        hist = PlotHist(
            nums_2[i][1], pltData, histOpts, ('P[Gev]', ''),
            DrawLoc, lca=lca_
        )
        h_num.append(hist)
        legend_entries[nums_2[i][1]] = (nums_2[i][-1], 'l')
        add_Header(purpose[j]+' backgroundl')
    #
#
legend_loc = (0.6, 0.2, 0.9, 0.3)
legend = create_legend(legend_loc, legend_entries)
#c_sums.SaveAs(output_dir+output_fnames[0])
c_nums.cd()
c_nums.SaveAs(output_dir+output_fnames)
c_nums.SaveAs(output_dir+output_fnames+"]")
#dataframes
c_nums = ROOT.TCanvas()
c_nums.SetCanvasSize(800,400);
c_nums.cd().Divide(3,1, 0.00001)
#c_nums.SetRightMargin(0.1)
#c_nums.SetTopMargin(0.1)
#c_nums.SetBottomMargin(0.1)
#c_nums.SetLeftMargin(0.1)
c_nums.SaveAs(output_dir+output_fnames+'[')
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
c_nums.SetLogx(0); c_nums.SetLogy(0)
scatters = []
_type_ = ['sig', 'bkg']
k = 1
## Testing plots 
for i in (1,2):
    k=1
    for x in ['x', 'y']:
        for y in ['y', 'z']:
            if y != x:
                c_nums.cd(k)
                plt_data = (dataFrames[0][i-1], 'P{}1'.format(x), 'P{}1'.format(y))
                Yrange = (-5.5, 5.5)
                Xrange = (-5.5, 5.5)
                if i ==2:
                    Yrange = (-7, 7)
                    Xrange = (-7, 7)
                #
                ranges = (Xrange, Yrange)
                labels=(x, y)
                xyScatter = PlotScatter('XvsYT', plt_data, ranges, labels, 'ap')
                scatters.append(xyScatter)
                title = add_Header('{} vs {} Testing sampled numbers {}'.format(y, x, _type_[i-1]))
                k += 1
            #
        #
    #
    c_nums.SaveAs(output_dir+output_fnames)
#
## Treaining Plots
for i in (1,2):
    k=1
    for x in ['x', 'y']:
        for y in ['y', 'z']:
            if y != x:
                c_nums.cd(k)
                plt_data = (dataFrames[1][i-1], 'P{}1'.format(x), 'P{}1'.format(y))
                Yrange = (-5.5, 5.5)
                Xrange = (-5.5, 5.5)
                if i ==2:
                    Yrange = (-7, 7)
                    Xrange = (-7, 7)
                #
                ranges = (Xrange, Yrange)
                labels=(x, y)
                xyScatter = PlotScatter('XvsYT', plt_data, ranges, labels, 'ap')
                scatters.append(xyScatter)
                title = add_Header('{} vs {} Training sampled numbers {}'.format(y, x, _type_[i-1]))
                k += 1
            #
        #
    #
    c_nums.SaveAs(output_dir+output_fnames)
#
c_nums.cd()

c_nums.SaveAs(output_dir+output_fnames+"]")
exit()
## The following lines draw a plot that has to do with the Pt Eta Phi coordinate system
## Ignore it If not using this system
# Plot the pt vs eta correlation hist
# prepare the data 
c_nums.SetLeftMargin(0.1)
c_nums.SetRightMargin(0.2)
c_nums.SetTopMargin(0.1)
c_nums.SetBottomMargin(0.1)
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
c_nums.SetLogx(0); c_nums.SetLogy(0)
sig_data = (dataFrames[0][0], "Eta1", "Pt1") 
bkg_data = (dataFrames[0][1], "Eta1", "Pt1") 
plt_range = [ [50, (-4.5,4.5)], [50, (0, 8)] ]
ax_labels = ("Eta", "Pt[GeV]")
plt_data = (sig_data, bkg_data)
# Plot the data 
sig_hist = PlotHist2("sig_hist", sig_data, plt_range, ax_labels, 'colz')
bkg_hist = PlotHist2("blg_hist", bkg_data, plt_range, ax_labels, 'colzsame')

# add legend,, title etc
legend_entries2 = {
    "sig_hist" : ('signal', 'l')
}
legend_entries3 = {
    "bkg_hist" : ('background', 'l')
}
legend2_loc = (0.55, 0.75, 0.65, 0.75)
legend3_loc = (0.55, 0.55, 0.65, 0.65)
legend2 = create_legend(legend2_loc, legend_entries2)
legend3 = create_legend(legend3_loc, legend_entries3)
title = add_Header('Eta vs Pt correlation')
c_nums.SaveAs(output_dir+output_fnames)
## Plot the X vs Y sampled points 
