import ROOT


fVV=ROOT.TFile("output_mutau_2022/WW_postEE.root","r")
fTT=ROOT.TFile("output_mutau_2022/TTTo2L2Nu_postEE.root","r")
fDY=ROOT.TFile("output_mutau_2022/DY_postEE.root","r")
fData=ROOT.TFile("output_mutau_2022/Data.root","r")
fout=ROOT.TFile("output_mutau_2022/Fake.root","recreate")

dir0=fout.mkdir("OSiso")

h0=fData.Get("OSanti/data_obs")
#CHANGE subtract MC prediction from other prompt backgrounds (Drell-Yan, diboson, ttbar, ...)

fout.cd()
dir0.cd()
h0.SetName("Fake")
h0.Write()

