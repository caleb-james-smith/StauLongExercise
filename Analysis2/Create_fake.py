import ROOT

fVV=ROOT.TFile("output_mutau_2022/WW_postEE.root","r")
fTT=ROOT.TFile("output_mutau_2022/TTTo2L2Nu_postEE.root","r")
fDY=ROOT.TFile("output_mutau_2022/DY_postEE.root","r")
fData=ROOT.TFile("output_mutau_2022/Data.root","r")
fout=ROOT.TFile("output_mutau_2022/Fake.root","recreate")

def make_fakes(dir_name, anti_dir_name):

    dir0=fout.mkdir(dir_name)

    h0=fData.Get(anti_dir_name + "/data_obs")
    #CHANGE subtract MC prediction from other prompt backgrounds (Drell-Yan, diboson, ttbar, ...)
    h1=fVV.Get(anti_dir_name + "/WW")
    h2=fTT.Get(anti_dir_name + "/TTTo2L2Nu")
    h3=fDY.Get(anti_dir_name + "/DY")

    hsum = h1.Clone()
    hsum.Add(h2)
    hsum.Add(h3)
    
    hfake = h0.Clone()
    hfake.Add(hsum, -1)
    hfake.Scale(.08)

    fout.cd()
    dir0.cd()
    hfake.SetName("Fake")
    hfake.Write()
    return

make_fakes("OSiso", "OSanti")
make_fakes("dz_mu", "dz_mu_anti")
make_fakes("dnn_tauvsjet", "dnn_tauvsjet_anti")
make_fakes("dnn_tauvsmu", "dnn_tauvsmu_anti")
make_fakes("dnn_tauvse", "dnn_tauvse_anti")
