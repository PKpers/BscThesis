#!/usr/bin/python
import sys
import ROOT
from plots import set_axes_title, PlotHist, create_legend, add_Header 
ROOT.gROOT.SetBatch(True)
#
# Load data
input_dir = "/home/kpapad/UG_thesis/tutorial_scripts/MachineLearning/RFiles/"
fileName = sys.argv[1] 
TreeName = "myTree"
infiles = [
    ('{}{}{}.root'.format(input_dir, fileName+str(1), p),
     '{}{}{}.root'.format(input_dir, fileName+str(2), p))
    for p in ('Test', 'Train')
]
# Configure output settings
output_dir = "/home/kpapad/UG_thesis/tutorial_scripts/MachineLearning/Plots/"
outName = sys.argv[2]
output_fnames = (outName+"sumsDist.pdf", outName+"numbersDist.pdf")
# Plot 
datasets = []
c_sums = ROOT.TCanvas("c_sums", "c_sums", 800, 600)
c_nums = ROOT.TCanvas("c_nums", "c_nums", 1000, 700)
c_nums .Divide(2,2,0,0)
c = (c_sums, c_nums)
c_sums.SetLogx(0); c_sums.SetLogy(1)
c_nums.SetLogx(0); c_nums.SetLogy(1)
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
#
# Read the data
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
# Plots configuration
h_sum = []
h_num = []
#
legend_entries = {} 
nbins = 50
histRange = (2, 10)
histOpts = (nbins, histRange)
ax_labels = ("sum of each set", 'events')
_Lcolor = [ (3,2),(4,1) ]
for j, df in enumerate(dataFrames):
    df_1 = df[0]
    df1_name = dfNames[j][0]
    #
    df_2 = df[1]
    df2_name = dfNames[j][1]
    #
    # Plot the invariant masses 
    sums = [
        (df_1,  df1_name, "sum", df1_name),
        (df_2,  df2_name, "sum", df2_name)
    ]
    c_sums.cd()
    for i in range(2):
        lca_ = [_Lcolor[j][i], 1]
        pltData = (sums[i][0], sums[i][2])
        c_sums.cd()
        if i == 0 and j == 0:
            DrawLoc='E1'
            legend_mark = 'lep'
            hist = PlotHist(
                sums[i][1], pltData, histOpts,
                ax_labels, DrawLoc, lca = lca_
            )
        elif i == 1 and j == 0:
            DrawLoc="E1" + 'same'
            legend_mark = 'lep'
            hist = PlotHist(
                sums[i][1], pltData, histOpts,
                ax_labels, DrawLoc, lca = lca_
            )
        else:
            DrawLoc='same'
            fs_ =  [1001, None, 3004]
            fca_ = [(_Lcolor[j][i], 0.15), None, (_Lcolor[j][i], 1)]
            legend_mark = 'f'
            hist = PlotHist(
                sums[i][1], pltData, histOpts,
                ax_labels, DrawLoc, lca = lca_,
                fca = fca_[i-1], fs=fs_[i-1]
            )
        #
        h_sum.append(hist)
        legend_entries[sums[i][1]] =(sums[i][-1], legend_mark)
    #
#
legend_loc = (0.5, 0.7, 0.7, 0.8)
legend = create_legend(legend_loc, legend_entries)
add_Header(' Sum of elements in each event ')
c_sums.SaveAs(output_dir+output_fnames[0])
#

branch_names = ['var_{}'.format(num) for num in range(4)]
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
    histRange = (-100, 100)
    histOpts = (nbins, histRange) 
    ax_laebels =("event components", 'counts')
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
#
legend_loc = (0.4, 0.7, 0.7, 0.8)
legend = create_legend(legend_loc, legend_entries)
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
    histRange = (-100, 100)
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
            nums_2[i][1], pltData, histOpts, ('', ''),
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
c_nums.SaveAs(output_dir+output_fnames[1])
    
    
    
    
    
