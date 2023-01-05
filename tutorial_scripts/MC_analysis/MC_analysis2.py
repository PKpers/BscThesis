import ROOT
ROOT.gInterpreter.ProcessLine('#include "test.h"')
## Import the tree--------------------------------------------------------------------------------------------------------
tree_path='~/UG_thesis/'
myFile_name=tree_path+"MC_2016_Z_2L.root"#read the root file
treeName="skimTree"
df=ROOT.RDataFrame(treeName, myFile_name)
c_all = df.Count()
##Analysis----------------------------------------------------------------------------------------------------------------
df=df.Define('Pt_sum', 'pt_sum(LeptonPt0, LeptonPt1)')
df=df.Define('solid_angle', 'S_angle(LeptonPhi0, LeptonPhi1, LeptonEta0, LeptonEta1)')
df=df.Define('Delta_Phi', 'delta_ang(LeptonPhi0, LeptonPhi1)');
no_boost=df.Filter('abs(Delta_Phi - TMath::Pi()) < 0.1*TMath::Pi()/180') #keep the z's with pt=0 before decay
no_boost = no_boost.Define('pt_ratio', 'LeptonPt0/LeptonPt1')
c_nb=no_boost.Count()
print(
    '{:.2f}% of entries passed the filter'\
    .format(c_nb.GetValue()/c_all.GetValue() * 100)
)
##Make the Plots-------------------------------------------------------------------------------------------------------
c = ROOT.TCanvas("c", "", 800, 700)
c.SetLogx(0); c.SetLogy(1)
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
#Pt0 no boost  
P0_hist_f=no_boost.Histo1D(("P0_hist_f", "Pt histogram", 50, 0, 500), "LeptonPt0")
P0_hist_f.SetLineColor(1)
P0_hist_f.GetXaxis().SetTitle('Transverse Momentum [GeV]')
P0_hist_f.GetYaxis().SetTitle('Counts')
P0_hist_f.Draw('hist')
#Pt1 no boost
P1_hist_f=no_boost.Histo1D(("P1_hist_f", "Pt1 histogram", 50, 0, 500), "LeptonPt1")
P1_hist_f.SetLineColor(2)
P1_hist_f.Draw('same')
#Pt0 unfiltered
P0_hist_nf = df.Histo1D(("P0_hist_nf", "Pt_0", 50, 0, 500), "LeptonPt0")
#P0_hist_nf=P0_hist_nf.GetValue()
P0_hist_nf.SetLineColor(3)
P0_hist_nf.Draw('Same')
#Pt1 unfiltered
P1_hist_nf = df.Histo1D(("P1_hist_nf", "Pt_1", 50, 0, 500), "LeptonPt1")
P1_hist_nf.SetLineColor(6)
P1_hist_nf.Draw('Same')
#Make the legend
#c.BuildLegend()
legend=ROOT.TLegend(0.6, 0.7, 0.9, 0.9)
legend.AddEntry("P0_hist_f", "P0 filtered", "l")
legend.AddEntry("P0_hist_nf", "P0 not filtered", "l")
legend.AddEntry("P1_hist_f", "P1 filtered", "l")
legend.AddEntry("P1_hist_nf", "P1 not filtered", "l")
legend.Draw('same')
#save the plot
c.SaveAs("Pt_FNf.pdf")
#Create a histogam to a different canvas 
cnew = ROOT.TCanvas("cnew", "", 800, 700)
cnew.SetLogx(0); cnew.SetLogy(1)
ROOT.gStyle.SetOptStat(1); ROOT.gStyle.SetTextFont(40)
#
P1vP2 = no_boost.Histo1D( ('P1vP2', '#frac{Pt0}{Pt1}', 50, 0, 10), 'pt_ratio')
P1vP2.GetXaxis().SetTitle('Transverse Momentum [eV]')
P1vP2.GetYaxis().SetTitle('Counts')
P1vP2.Draw()
cnew.SaveAs('P0P1_ratio.pdf')
#The end ---------------------------------------------------------------------------------------------------------------



#create a list that containts the name of the wanted branches
'''
#declare the pt, eta, phi, and E vectors
vectors=[]
for i in range(4):
    dum=ROOT.vector('float')()#dummy vector that will host the PtEtaPhiE values for a while
    for j in range(2):
        #branch_name='Lepton'+type_[i]+str(j)
        dum.push_back(float(35+i))
    #
    vectors.append(dum)
#
pt,eta,phi, e=vectors
#E=ROOT.vector('float')
#E.push_back(float(3.4))
#E.push_back(float(4.5))
#a = ROOT.ComputeInvariantMass(pt, eta, phi, e)
#print(a)
'''
#histogram stuf----------------------------------------------------------------------------------------------------
#h0=df.Histo1D(("Pt0", "Pt0", 50, 0, 500), "LeptonPt0")
#h = df.Histo1D(("Pt_sum", "Pt_sum", 50, 0, 500), "Pt_sum")
#ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
#c = ROOT.TCanvas("c", "", 800, 700)
#c.SetLogx(0); c.SetLogy(1)
#h.SetTitle("")
#h.GetXaxis().SetTitle("m_{#mu#mu} (GeV)"); h.GetXaxis().SetTitleSize(0.04)
#h.GetYaxis().SetTitle("N_{Events}"); h.GetYaxis().SetTitleSize(0.04)
'''
ROOT.gInterpreter.Declare(
    """
    using Vec_t = const ROOT::VecOps::RVec<float>;
    float ComputeInvariantMass(Vec_t& pt, Vec_t& eta, Vec_t& phi, Vec_t& e) {
                                  ROOT::Math::PtEtaPhiEVector p1(pt[0], eta[0], phi[0], e[0]);
                                  ROOT::Math::PtEtaPhiEVector p2(pt[1], eta[1], phi[1], e[1]);
                                  return (p1 + p2).mass() / 1000.0;
    }
    """)
'''

#read abt W and Z bozons
# original momenum pt of the z bozon before it decayed
#next meeting 3Aug 11:00
