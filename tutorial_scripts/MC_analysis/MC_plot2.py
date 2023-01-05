import ROOT
ROOT.gInterpreter.ProcessLine('#include "test.h"')
## Import the tree--------------------------------------------------------------------------------------------------------
tree_path='~/UG_thesis/';
myFile_name=tree_path+"InvMassComp0.root";#read the root file
treeName="InvMasses";
inv_mass=ROOT.RDataFrame(treeName, myFile_name);
#plot the data ----------------------------------------------------------------------------------------------------------
def set_axes_title(hist, xtitle, ytitle):
    hist.GetXaxis().SetTitle(str(xtitle))
    hist.GetYaxis().SetTitle(str(ytitle))
    return 
#
c = ROOT.TCanvas("", "", 800, 700)
c.cd()
c.SetLogx(0); c.SetLogy(1)
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
#Plot my_invariant_mass
my_inv_mass=inv_mass.Histo1D( ("my_inv_mass", "", 50, -100, 500),
                              "Inv_Mass"
)
my_inv_mass.SetLineColor(1)
set_axes_title(my_inv_mass, 'Invariant mass [Gev]', 'counts')
my_inv_mass.Draw('hist')
#plot the ''correct'' invarian mass
c_inv_mass=inv_mass.Histo1D( ("c_inv_mass", "", 50, -100, 500),
                             "LeptonPairInvariantMass"
)
c_inv_mass.SetLineColorAlpha(3, 1)
c_inv_mass.SetLineStyle(2)
set_axes_title(c_inv_mass, 'Invariant mass [Gev]', 'counts')
c_inv_mass.Draw('same')
#create the legend 
legend=ROOT.TLegend(0.4, 0.7, 0.7, 0.8)
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetTextSize(0.03)
legend.AddEntry("my_inv_mass", "Invariant mass with TLornerntzVector", "l")
legend.AddEntry('info', "Lepton masses = 0", "")
legend.AddEntry("c_inv_mass", " 'correct' invariant mass", "l")
legend.Draw()
#add Header 
label = ROOT.TLatex()
label.SetTextSize(0.04)
label.DrawLatexNDC(0.16, 0.92, "#bf{Invariant mass comparison}")
#header = ROOT.TLatex()
#header.SetTextSize(0.03)
#header.DrawLatexNDC(0.63, 0.92, "#sqrt{s} = 8 TeV, L_{int} = 11.6 fb^{-1}")
c.SaveAs('inv_mass0_plt.pdf')
#c.SaveAs('inv_mass_plt.pdf]')

