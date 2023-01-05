#!/usr/bin/python
import ROOT
ROOT.gROOT.SetBatch(True)
def set_axes_title(pltObj, xtitle, ytitle):
    pltObj.GetXaxis().SetTitle(str(xtitle))
    pltObj.GetYaxis().SetTitle(str(ytitle))
    return 
#

def set_axes_range(pltObj, Xrange, Yrange):
    pltObj.GetXaxis().SetRangeUser(Xrange[0], Xrange[1]);
    pltObj.GetYaxis().SetRangeUser(Yrange[0], Yrange[1]);
    return

def set_markerstyle(pltObj, styling_opts):
    if not styling_opts or not any(styling_opts.values()) :
        return
    else:
        options = styling_opts.keys()
        if "mca" or "marker color attributes" in options:
            mca = styling_opts.get("mca")
            if not mca:
                mca = styling_opts.get("markercolor attribute")
            #
            pltObj.SetMarkerColorAlpha(mca[0], mca[1])
        #

        if "msz" in options or "markersize" in options:
            msz = styling_opts.get("msz")
            if not msz:
                msz = styling_opts.get("markersize")
            #
            pltObj.SetMarkerSize(msz)
        #

        if "ms" in options or "markerstyle" in options:
            ms = styling_opts.get("ms")
            if not ms:
                ms = styling_opts.get("markerstyle")
            #
            pltObj.SetMarkerStyle(ms)
        #
    
        if "fs" in options or "fillstyle" in options:
            fs = styling_opts.get("fs")
            if not fs:
                fs = styling_opts.get("fillstyle")
            #
            pltObj.SetFillStyle(fs)
        #

        if "fca" in options or "fill color attribute" in options:
            fca = styling_opts.get("fca")
            if not fca:
                fca = styling_opts.get("fill color attribute")
            #
            pltObj.SetFillColorAlpha(fca[0], fca[1])
        #
        return
#
  
def set_linestyle(pltObj, styling_opts):
    if not styling_opts or not any(styling_opts.values()) :
        return
    else:
        options = styling_opts.keys()
        if "lca" or "line color attributes" in options:
            lca = styling_opts.get("lca")
            if not lca:
                lca = styling_opts.get("line color attribute")
            #
            pltObj.SetLineColorAlpha(lca[0], lca[1])
        #
    
        if "ls" in options or "linestyle" in options:
            ls = styling_opts.get("ls")
            if not ls:
                ls = styling_opts.get("linestyle")
            #
            pltObj.SetLineStyle(ls)
        #
    
        if "fs" in options or "fillstyle" in options:
            fs = styling_opts.get("fs")
            if not fs:
                fs = styling_opts.get("fillstyle")
            #
            pltObj.SetFillStyle(fs)
        #

        if "fca" in options or "fill color attribute" in options:
            fca = styling_opts.get("fca")
            if not fca:
                fca = styling_opts.get("fill color attribute")
            #
            pltObj.SetFillColorAlpha(fca[0], fca[1])
        #
        return
#
def PlotHist(HistName, pltData, histOpts, axLabels, DrawOpts, **kwargs):
    df, data = pltData
    Nbins, Range = histOpts
    Xlabel, Ylabel = axLabels
    #
    myHist = df.Histo1D(
        (HistName, "", Nbins, Range[0], Range[1]),
        data
    )
    set_linestyle(myHist, kwargs)
    #myHist.SetLineColor(_Lcolor)
    set_axes_title(myHist, Xlabel, Ylabel)
    myHist.Draw(DrawOpts)
    return myHist
#
def PlotHist2(HistName, pltData, histOpts, axLabels, DrawOpts, **kwargs):
    df, xdata, ydata = pltData
    xNbins, xRange = histOpts[0]
    yNbins, yRange = histOpts[1]
    Xlabel, Ylabel = axLabels
    #
    myHist = df.Histo2D(
        (HistName, "", xNbins, xRange[0], xRange[1], yNbins, yRange[0], yRange[1]),
        xdata, ydata
    )
    set_linestyle(myHist, kwargs)
    #myHist.SetLineColor(_Lcolor)
    set_axes_title(myHist, Xlabel, Ylabel)
    myHist.Draw(DrawOpts)
    return myHist
#
def PlotScatter(ScatterName, pltData, options, axLabels, DrawOpts, **kwargs):
    df, X, Y = pltData
    Xrange, Yrange = options
    Xlabel, Ylabel = axLabels
    #
    myGraph = df.Graph(X, Y)
    myGraph.SetName(ScatterName)
    myGraph.SetTitle("")
    set_linestyle(myGraph, kwargs)
    set_axes_title(myGraph, Xlabel, Ylabel)
    set_axes_range(myGraph, Xrange, Yrange)
    myGraph.Draw(DrawOpts)
    return myGraph
    

def create_legend(position, entries):
    xmin, ymin, xmax, ymax = position
    legend = ROOT.TLegend(xmin, ymin, xmax, ymax)
    legend.SetFillColor(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.03)
    for entry, attribs in entries.items():
        _name = entry
        _title, _linestyle = attribs
        legend.AddEntry(_name, _title, _linestyle)
    #
    legend.Draw('same')
    return legend
#
def add_Header(title):
    import ROOT
    label = ROOT.TLatex()
    label.SetTextSize(0.04)
    label.DrawLatexNDC(0.16, 0.92, "#bf{"+str(title)+"}")
    return 

if __name__ == "__main__":
    import sys
    dataset = sys.argv[1]
    #
    inpath = '/home/kpapad/UG_thesis/tutorial_scripts/MachineLearning/RFiles/PlotFiles/'
    outpath = '/home/kpapad/UG_thesis/tutorial_scripts/MachineLearning/Plots/'
    signal_filename = inpath+ "sum{}1Train.root".format(dataset)
    bkg_filename = inpath+ "sum{}2Train.root".format(dataset)
    treeName = "myTreesum"
    #
    data_sig = ROOT.RDataFrame(treeName, signal_filename)
    data_bkg = ROOT.RDataFrame(treeName, bkg_filename)
    # 
    nbins = 50
    data = (data_sig, data_bkg)
    histRange = (0, 10)
    xlabel = 'sum of sets'
    ylabel = 'counts'
    _Lcolor = (3, 1)
    histnames=tuple(
        ['hist{}'.format(i) for i in ('sig', 'bkg')]
    )
    #
    c = ROOT.TCanvas("", "", 800, 700)
    c.cd()
    c.SetLogx(0); c.SetLogy(1)
    #
    hd = {} #hist dict
    hists = []
    where=('hist', 'same')
    for j, d in enumerate(data):
        ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
        if j == 0:
            DrawLoc='hist'
            Type = 'signal'
        else:
            DrawLoc='same'
            Type = 'background'
        #
        hist = PlotHist(
            histnames[j], d, 'sum'+str(j), nbins, histRange,
            xlabel, ylabel, _Lcolor[j], DrawLoc
        )
        hists.append(hist)
        hd[histnames[j]]=(Type,  'l')
    #
    legend_loc = (0.6, 0.7, 0.9, 0.8)
    legend = create_legend(legend_loc, hd)
    add_Header('summing training data')

    #
    outFileName = outpath+'{}.pdf'.format(dataset)
   # print('Saving plot to {}...'.format(outFileName))
   # print('done')
    c.SaveAs(outFileName)
#
#header = ROOT.TLatex()
#header.SetTextSize(0.03)
#header.DrawLatexNDC(0.63, 0.92, "#sqrt{s} = 8 TeV, L_{int} = 11.6 fb^{-1}")
