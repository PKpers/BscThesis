import ROOT as root
import numpy as np
import math
pi=math.pi
filename ="data.txt"
with open(filename, 'r') as f:
    lines = f.readlines()[1:]
#
data = [float(l) for l in lines]

#A helpull function fills a histogram
def fill_hist(list_inp, hist_inp):
    '''
    this function takes a list as input
    and fils the given histogram with its elements
    '''
    for l in list_inp:
        hist_inp.Fill(l)
    #
    return

c=root.TCanvas()
c.SetGrid()

#create the histogram
hist=root.TH1F("stat", "random walk hist", 50, 450, 550)
fill_hist(data, hist)
hist.GetXaxis().SetTitle("Distance")
hist.GetYaxis().SetTitle("counts")

#define the fit function
sqrt="1/([1]*sqrt(2*pi))"
exponent="pow( (x-[2])/(2*[1]), 2 )"
exponential="exp(- %s)"%(exponent)
norm="[0]"
gaus_ = "%s * %s * %s"%(norm, sqrt, exponential)
#define the function object
fit_func=root.TF1("fit_func", # see more on user functions 
                  gaus_,
                  450, 550
)

params=[5000, 15.67, 500]#amplitude, stdev, median
for i in range(3):
    fit_func.SetParameter(i, params[i])
#

hist.Fit(fit_func, "R")

#get the fit params
params=[]
for i in range(3):
    p=fit_func.GetParameter(i)
    #fit_func.SetParameter(i, p)#set the parameters to the finction obj
    params.append(p)
#
amp, stdev, median = params 

#calculate the ratio between theory(fit) and experiment(data)
Range=np.linspace(449, 551, 51)
theory=np.array(
    [fit_func(r) for r in Range]
)
experiment=np.array(
    [hist.GetBinContent(i) for i in range(51) ]
)
n=len(list(Range))
graph1=root.TGraph(n, Range, theory)
graph1.SetLineColor(4)
graph1.Draw("AC*")

graph2=root.TGraph(n, Range, experiment) 
graph2.SetLineColor(2)
graph2.SetMarkerStyle(21)
graph2.Draw("CP")

#add legend
legend=root.TLegend(0.2,0.75,0.4,0.85)
legend.AddEntry(graph1, "theory")
legend.AddEntry(graph2, "experiment")
legend.Draw()
ratio = abs( (experiment/theory) - 1)
#graph3=root.TGraph(n, Range, ratio) 
#graph3.Draw()

#hist.Draw() 
c.Update()

