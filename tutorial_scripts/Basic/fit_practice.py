from __future__ import print_function
import ROOT
import random as rand
import numpy as np
import math 

## Let's create some data first
x = np.linspace(1, 100, 1000)
data=x**2
data=np.array(
    [d+(rand.random()*d/10) for d in data]
)
#plot the data 
c1 = ROOT.TCanvas( 'c1', 'A Simple Graph Example', 200, 10, 700, 500 )

c1.SetGrid()
n=len(list(x)) 
gr = ROOT.TGraph( n, x, data )
gr.SetMarkerColor( 4 )
gr.SetMarkerStyle( 21 )
gr.SetTitle( 'Fit Practice' )
gr.GetXaxis().SetTitle( 'X' )
gr.GetYaxis().SetTitle( 'data' )
gr.Draw('ACP' )

# TCanvas.Update() draws the frame, after which one can change it
#c1.Update()
#c1.GetFrame().SetBorderSize( 12 )
#c1.Modified()
c1.Update()

## create the function to be fitted 
f1=ROOT.TF1("f1", "[0]*x*x", 0, 100)
gr.Fit(f1)
c1.Update()
c1.SaveAs("fit1.png")



    

    

    

