#include <TH2.h>
#include <TH2F.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TGraph.h>
#include <TGraphAsymmErrors.h>
#include "TMultiGraph.h"
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <utility>
#include <stdio.h>
#include <TF1.h>
#include <TDirectoryFile.h>
#include <TRandom3.h>
#include "TLorentzVector.h"
#include "TString.h"
#include "TLegend.h"
#include "TH1F.h"
#include "TKey.h"
#include "THashList.h"
#include "THStack.h"
#include "TPaveLabel.h"
#include "TFile.h"
#include "TTree.h"
#include "tr_Tree.h"

using namespace std;

int main(int argc, char** argv) {


    std::string year = *(argv + 1);
    std::string input = *(argv + 2);
    std::string output = *(argv + 3);
    std::string sample = *(argv + 4);
    std::string name = *(argv + 5);

    TFile *f_Double = new TFile(input.c_str());
    cout<<"XXXXXXXXXXXXX "<<input.c_str()<<" XXXXXXXXXXXX"<<endl;
    TTree *arbre = (TTree*) f_Double->Get("Events");

    TTree *arbre2 = (TTree*) f_Double->Get("Runs");
    float ngen=0;
    float ngenu=0;
    if (name!="data_obs") {
       Int_t nentries_wtn2 = (Int_t) arbre2->GetEntries();
       arbre2->SetBranchAddress("genEventCount", &genEventCount);
       for (Int_t i = 0; i < nentries_wtn2; i++) {
         arbre2->GetEntry(i);
         ngenu+=genEventCount;
       }
    }
    cout<<"N gen unweighted: "<<ngenu<<endl;

    float weight=1.0; float xs=1.0;
    // Info from https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun3Analysis
    float lumi2022C=5010.4;
    float lumi2022D=2970.0;
    float lumi2022E=5807.0;
    float lumi2022F=17781.9;
    float lumi2022G=3082.8;
    float lumi2022=34748.6;
    float lumi2022_postEE=lumi2022E+lumi2022F+lumi2022G;
    // CHANGE: compute the weight for each MC sample based on the integrated luminosity (lumi2022_postEE), the number of generated events (ngenu), and the sample cross section

    cout.setf(ios::fixed, ios::floatfield);
    cout.precision(10);

    arbre->SetBranchAddress("nLepCand", &nLepCand);
    arbre->SetBranchAddress("LepCand_id", &LepCand_id);
    arbre->SetBranchAddress("LepCand_pt", &LepCand_pt);
    arbre->SetBranchAddress("LepCand_eta", &LepCand_eta);
    arbre->SetBranchAddress("LepCand_phi", &LepCand_phi);
    arbre->SetBranchAddress("LepCand_tauvse2018", &LepCand_tauvse2018);
    arbre->SetBranchAddress("LepCand_tauvsmu2018", &LepCand_tauvsmu2018);
    arbre->SetBranchAddress("LepCand_tauvsjet2018", &LepCand_tauvsjet2018);
    arbre->SetBranchAddress("LepCand_charge", &LepCand_charge);
    arbre->SetBranchAddress("LepCand_taudm", &LepCand_taudm);
    arbre->SetBranchAddress("LepCand_gen", &LepCand_gen);
    arbre->SetBranchAddress("HLT_IsoMu24", &HLT_IsoMu24);
    arbre->SetBranchAddress("nJets", &nJets);
    arbre->SetBranchAddress("PuppiMET_phi", &PuppiMET_phi);
    arbre->SetBranchAddress("PuppiMET_pt", &PuppiMET_pt);

    arbre->SetBranchAddress("LepCand_tauvsjet2018_sf", &LepCand_tauvsjet2018_sf);
    arbre->SetBranchAddress("LepCand_tauvsmu2018_sf", &LepCand_tauvsmu2018_sf);
    arbre->SetBranchAddress("LepCand_muonIso_sf", &LepCand_muonIso_sf);
    arbre->SetBranchAddress("LepCand_muonID_sf", &LepCand_muonID_sf);
    arbre->SetBranchAddress("LepCand_trg_sf", &LepCand_trg_sf);

    TH1F* h_mvis = new TH1F("h_mvis","h_mvis",30,0,300); h_mvis->Sumw2();
    TH1F* h_mvis_anti = new TH1F("h_mvis_anti","h_mvis_anti",30,0,300); h_mvis_anti->Sumw2();

    // CHANGE: define here other histograms you want to fill and save

   Int_t nentries_wtn = (Int_t) arbre->GetEntries();
   for (Int_t i = 0; i < nentries_wtn; i++) {
	arbre->LoadTree(i);
        arbre->GetEntry(i);
        if (i % 10000 == 0) fprintf(stdout, "\r  Processed events: %8d of %8d ", i, nentries_wtn);
        fflush(stdout);
	
	int mu_index=-1;
	for (int j=0; j<nLepCand; ++j){
	   if (mu_index<0 and LepCand_id[j]==13) mu_index=j;
	}
        int tau_index=-1; float pt_tmp=0;
        for (int j=0; j<nLepCand; ++j){
           if (LepCand_id[j]==15 and LepCand_pt[j]>pt_tmp){
	      tau_index=j; 
	      pt_tmp=LepCand_pt[j];
	   }
        }

	// build and fill the four-vectors of the muon and the tau 
        TLorentzVector my_tau; 
        TLorentzVector my_mu; 
	my_tau.SetPtEtaPhiM(LepCand_pt[tau_index],LepCand_eta[tau_index],LepCand_phi[tau_index],0.1);
	my_mu.SetPtEtaPhiM(LepCand_pt[mu_index],LepCand_eta[mu_index],LepCand_phi[mu_index],0.1);


	// CHANGE: apply the selection on the muon and the tau (eta, pt, ID, ...)
	
	// CHANGE: apply the selection on the dilepton pair (DR > 0.5, OS, ...)
	
	// CHANGE: apply the trigger selection

	bool is_OS=(LepCand_charge[mu_index]*LepCand_charge[tau_index]<0);
	bool is_iso=(LepCand_tauvsjet2018[tau_index]>=5);

	float correction = 1.0;
	if (name!="data_obs"){
	   correction = correction; // CHANGE: add SFs for tau ID (against jets, electrons, or muons), muon ID, muon iso, and trigger
	}

	// fill the signal region histogram
	if (is_OS and is_iso) h_mvis->Fill((my_mu+my_tau).M(),weight*correction);

	// fill the anti-isolated histogram to estimate the fake background
	float fr=1.0; //CHANGE Calculate the tau fake rate and replace this value
	if (is_OS and !is_iso) h_mvis_anti->Fill((my_mu+my_tau).M(),weight*fr*correction);

	// CHANGE: fill the histograms needed to calculate the fake rate

    } // end of loop over events

    TFile *fout = TFile::Open(output.c_str(), "RECREATE");
    fout->cd();

    // You can store the histogram directly in the root file...
    h_mvis->Write();

    // or in a directory (necessary for the statistical analysis later)

    TDirectory *dir_OSiso =fout->mkdir("OSiso");
    dir_OSiso->cd();
    h_mvis->SetName(name.c_str());
    h_mvis->Write();

    TDirectory *dir_OSanti =fout->mkdir("OSanti");
    dir_OSanti->cd();
    h_mvis_anti->SetName(name.c_str());
    h_mvis_anti->Write();

    // CHANGE: save the other histograms you have filled

    fout->Close();
} 

