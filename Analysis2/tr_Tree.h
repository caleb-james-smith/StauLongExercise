   Long64_t       genEventCount;
   Double_t       genEventSumw;

   UInt_t          run;
   UInt_t          luminosityBlock;
   ULong64_t       event;
   Int_t           nLepCand;
   Int_t           nJets;
   Float_t         PuppiMET_phi;
   Float_t         PuppiMET_pt;
   Bool_t          HLT_IsoMu24;
   Int_t           LepCand_id[3];   //[nLepCand]
   Float_t         LepCand_pt[3];   //[nLepCand]
   Float_t         LepCand_eta[3];   //[nLepCand]
   Float_t         LepCand_phi[3];   //[nLepCand]
   Int_t           LepCand_charge[3];   //[nLepCand]
   Float_t         LepCand_dxy[3];   //[nLepCand]
   Float_t         LepCand_dz[3];   //[nLepCand]
   Int_t           LepCand_taudm[3];   //[nLepCand]
   Int_t           LepCand_gen[3];   //[nLepCand]
   Int_t           LepCand_tauvse2018[3];   //[nLepCand]
   Int_t           LepCand_tauvsmu2018[3];   //[nLepCand]
   Int_t           LepCand_tauvsjet2018[3];   //[nLepCand]
   Float_t         LepCand_tauvsjet2018_sf[3];
   Float_t         LepCand_tauvsmu2018_sf[3];
   Float_t         LepCand_muonIso_sf[3];
   Float_t         LepCand_muonID_sf[3];
   Float_t         LepCand_trg_sf[3];

   // CHANGE: add the variables stored in the flat trees and not defined above (use MakeClass to easily get the list from the Root file)
