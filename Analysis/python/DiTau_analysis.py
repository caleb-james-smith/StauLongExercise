#!/usr/bin/env python
import os, sys, math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
import correctionlib as _core

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection

from StauLongExercise.Analysis.objectSelector import ElectronSelector, MuonSelector, TauSelector

CMSSW = os.environ['CMSSW_BASE']

class Analysis(Module):
    def __init__(self, channel, isMC):
        self.channel = channel
        self.isMC    = isMC

        # Read tau corrections
        #https://gitlab.cern.ch/cms-tau-pog/jsonpog-integration/-/blob/TauPOG_v2_deepTauV2p5/POG/TAU/README.md#usage?ref_type=heads
        self.cset = _core.CorrectionSet.from_file(CMSSW+"/src/StauLongExercise/Analysis/tau_DeepTau2018v2p5_2022_postEE.json")
        self.corr1 = self.cset["DeepTau2018v2p5VSjet"]
        self.corr2 = self.cset["DeepTau2018v2p5VSmu"]
        self.corr3 = self.cset["tau_energy_scale"]
        self.corr7 = self.cset["DeepTau2018v2p5VSe"]

        # Read muon corrections
        #https://gitlab.cern.ch/cms-nanoAOD/jsonpog-integration/-/tree/master/POG/MUO?ref_type=heads
        self.cset2 = _core.CorrectionSet.from_file(CMSSW+"/src/StauLongExercise/Analysis/muon_Z.json")
        self.corr4 = self.cset2["NUM_MediumID_DEN_TrackerMuons"]
        self.corr5 = self.cset2["NUM_TightPFIso_DEN_MediumID"]
        self.corr6 = self.cset2["NUM_IsoMu24_DEN_CutBasedIdMedium_and_PFIsoMedium"]
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    
        self.out = wrappedOutputTree
        self.out.branch("nLepCand",          "I");
        self.out.branch("LepCand_id",        "I",  lenVar = "nLepCand");
        self.out.branch("LepCand_pt",        "F",  lenVar = "nLepCand");
        self.out.branch("LepCand_eta",       "F",  lenVar = "nLepCand");
        self.out.branch("LepCand_phi",       "F",  lenVar = "nLepCand");
        self.out.branch("LepCand_charge",    "I",  lenVar = "nLepCand");
        self.out.branch("LepCand_dxy",       "F",  lenVar = "nLepCand");
        self.out.branch("LepCand_dz",        "F",  lenVar = "nLepCand");
        self.out.branch("LepCand_taudm",     "I",  lenVar = "nLepCand");
        self.out.branch("LepCand_gen",       "I",  lenVar = "nLepCand");
        self.out.branch("LepCand_tauvse",    "I",  lenVar = "nLepCand");
        self.out.branch("LepCand_tauvsmu",   "I",  lenVar = "nLepCand");
        self.out.branch("LepCand_tauvsjet",  "I",  lenVar = "nLepCand");
        # CHANGE Add tau DNN 2018 v2p5 against jets, electrons, and muons (LepCand_tauvse2018, LepCand_tauvsmu2018, LepCand_tauvsjet2018)
        self.out.branch("LepCand_tauvsjet2018",  "F",  lenVar = "nLepCand");
        self.out.branch("LepCand_tauvsmu2018",  "F",  lenVar = "nLepCand");
        self.out.branch("LepCand_tauvse2018",  "F",  lenVar = "nLepCand");
        self.out.branch("LepCand_tauvsjet2018_sf",  "F",  lenVar = "nLepCand");
        self.out.branch("LepCand_tauvsmu2018_sf",  "F",  lenVar = "nLepCand");
        self.out.branch("LepCand_tauvse2018_sf",  "F",  lenVar = "nLepCand");
        self.out.branch("LepCand_muonID_sf",  "F",  lenVar = "nLepCand");
        self.out.branch("LepCand_muonIso_sf",  "F",  lenVar = "nLepCand");
        self.out.branch("LepCand_trg_sf",  "F",  lenVar = "nLepCand");
        self.out.branch("nJets",             "I");
 
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def selectMuons(self, event, muSel):
        ## access a collection in nanoaod and create a new collection based on this

        event.selectedMuons = []
        muons = Collection(event, "Muon")
        for mu in muons:
            if not muSel.evalMuon(mu): continue
            setattr(mu, 'id', 13)
            event.selectedMuons.append(mu)

        event.selectedMuons.sort(key=lambda x: x.pt, reverse=True)

    def selectElectrons(self, event, elSel):
        event.selectedElectrons = []
        electrons = Collection(event, "Electron")
        for el in electrons:
            if not elSel.evalElectron(el): continue
            #check overlap with selected leptons 
            deltaR_to_leptons=[ el.p4().DeltaR(lep.p4()) for lep in event.selectedMuons ]
            hasLepOverlap=sum( [dR<0.4 for dR in deltaR_to_leptons] )
            if hasLepOverlap>0: continue

            setattr(el, 'id', 11)
            event.selectedElectrons.append(el)
        event.selectedElectrons.sort(key=lambda x: x.pt, reverse=True)


    def selectTaus(self, event, tauSel):
        event.selectedTaus = []
        taus = Collection(event, "Tau")
        for tau in taus:
            #check overlap with selected leptons 
            deltaR_to_leptons=[ tau.p4().DeltaR(lep.p4()) for lep in event.selectedMuons+event.selectedElectrons ]
            hasLepOverlap=sum( [dR<0.4 for dR in deltaR_to_leptons] )
            if hasLepOverlap>0: continue

            if not tauSel.evalTau(tau): continue
            setattr(tau, 'id', 15)
            event.selectedTaus.append(tau)
        event.selectedTaus.sort(key=lambda x: x.pt, reverse=True)



    def selectAK4Jets(self, event):
        ## Selected jets: pT>30, |eta|<4.7, pass tight ID
        
        event.selectedAK4Jets = []
        ak4jets = Collection(event, "Jet")
        for j in ak4jets:

            if j.pt<30 : 
                continue

            if abs(j.eta) > 4.7:
                continue
            
            #require tight (2^1) or tightLepVeto (2^2) [https://twiki.cern.ch/twiki/bin/view/CMS/JetID#nanoAOD_Flags]
            if j.jetId<2: 
                continue
                
            #check overlap with selected leptons 
            deltaR_to_leptons=[ j.p4().DeltaR(lep.p4()) for lep in event.selectedMuons+event.selectedElectrons ]
            hasLepOverlap=sum( [dR<0.4 for dR in deltaR_to_leptons] )
            if hasLepOverlap>0: continue

            event.selectedAK4Jets.append(j)
            
        event.selectedAK4Jets.sort(key=lambda x: x.pt, reverse=True)

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        elSel = ElectronSelector()
        muSel = MuonSelector()
        tauSel = TauSelector()
        
        # apply object selection
        self.selectMuons(event, muSel)
        self.selectElectrons(event, elSel)
        self.selectTaus(event, tauSel)
        self.selectAK4Jets(event)
        
        #apply event selection depending on the channel:
        if self.channel=="mutau":

            # CHANGE: Select events with exactly 1 muon with pT > 26 GeV, 0 electron, and 1 tauh
            if len(event.selectedTaus)==0: return False

            

        ######################################################
        ##### HIGH LEVEL VARIABLES FOR SELECTED EVENTS   #####
        ######################################################
        
        event.selectedLeptons=event.selectedElectrons+event.selectedMuons+event.selectedTaus
        event.selectedLeptons.sort(key=lambda x: x.pt, reverse=True)
        
        lep_id     = [lep.id for lep in event.selectedLeptons]
        lep_pt     = [lep.pt for lep in event.selectedLeptons]
        lep_eta    = [lep.eta for lep in event.selectedLeptons]
        lep_phi    = [lep.phi for lep in event.selectedLeptons]
        lep_charge = [lep.charge for lep in event.selectedLeptons]
        lep_dxy    = [lep.dxy for lep in event.selectedLeptons]
        lep_dz     = [lep.dz for lep in event.selectedLeptons]
        
        lep_tauvsjet=[]
        lep_tauvse=[]
        lep_tauvsmu=[]
        # CHANGE: save and fill the 2018 v2p5 DNN outputs for the taus
        lep_tauvsjet2018=[]
        lep_tauvsmu2018=[]
        lep_tauvse2018=[]
        lep_tauvsjet2018_sf=[]
        lep_tauvsmu2018_sf=[]
        lep_tauvse2018_sf=[]
        lep_muonID_sf=[]
        lep_muonIso_sf=[]
        lep_trg_sf=[]
        lep_taudm=[]
        lep_gen=[]
        for lep in event.selectedLeptons:
           # skip decayMode 5 and 6 for DeepTau from TAU POG REC: https://twiki.cern.ch/twiki/bin/view/CMS/TauIDRecommendationForRun2#Decay_Mode_Reconstruction
           if lep.id==15 and (lep.decayMode == 5 or lep.decayMode == 6): continue
           if self.isMC:
                lep_gen.append(lep.genPartFlav)
           else:
                lep_gen.append(-1)

        for lep in event.selectedLeptons:
           if lep.id==15:
              lep_tauvsjet.append(lep.idDeepTau2017v2p1VSjet)
              lep_tauvse.append(lep.idDeepTau2017v2p1VSe)
              lep_tauvsmu.append(lep.idDeepTau2017v2p1VSmu)
              lep_tauvsjet2018.append(lep.idDeepTau2018v2p5VSjet)
              lep_tauvse2018.append(lep.idDeepTau2018v2p5VSe)
              lep_tauvsmu2018.append(lep.idDeepTau2018v2p5VSmu)
              lep_taudm.append(lep.decayMode)
           else:
              lep_tauvsjet.append(-1)
              lep_tauvse.append(-1)
              lep_tauvsmu.append(-1)
              lep_tauvsjet2018.append(-1)
              lep_tauvse2018.append(-1)
              lep_tauvsmu2018.append(-1)
              lep_taudm.append(-1)

           #CHANGE fill the tau ID SFs
           if lep.id==15 and self.isMC:
              # 1: jet, 2: mu, 7: e
              val1 = self.corr1.evaluate(lep.pt,lep.decayMode,lep.genPartFlav,"Medium","VVLoose","nom","dm")
              val2 = self.corr2.evaluate(lep.eta,lep.genPartFlav,"Medium","nom")
              val7 = self.corr7.evaluate(lep.eta,lep.decayMode,lep.genPartFlav,"Medium","nom")
              lep_tauvsjet2018_sf.append(val1)
              lep_tauvsmu2018_sf.append(val2)
              lep_tauvse2018_sf.append(val7)
           else:
              lep_tauvsjet2018_sf.append(1.0)
              lep_tauvsmu2018_sf.append(1.0)
              lep_tauvse2018_sf.append(1.0)

           if lep.id==13 and self.isMC:
               if lep.pt < 26.:
                   lep_trg_sf.append(self.corr6.evaluate(abs(lep.eta),26.,"nominal"))
                   lep_muonID_sf.append(self.corr4.evaluate(abs(lep.eta),26.,"nominal"))
                   lep_muonIso_sf.append(self.corr5.evaluate(abs(lep.eta),26.,"nominal"))
               else:
                   lep_trg_sf.append(self.corr6.evaluate(abs(lep.eta),lep.pt,"nominal"))
                   lep_muonID_sf.append(self.corr4.evaluate(abs(lep.eta),lep.pt,"nominal"))
                   lep_muonIso_sf.append(self.corr5.evaluate(abs(lep.eta),lep.pt,"nominal"))
           else:
               lep_trg_sf.append(1.0)
               lep_muonID_sf.append(1.0)
               lep_muonIso_sf.append(1.0)



        ## store branches
        self.out.fillBranch("nLepCand",           len(event.selectedLeptons))
        self.out.fillBranch("LepCand_id" ,        lep_id)
        self.out.fillBranch("LepCand_pt" ,        lep_pt)
        self.out.fillBranch("LepCand_eta" ,       lep_eta)
        self.out.fillBranch("LepCand_phi" ,       lep_phi)
        self.out.fillBranch("LepCand_charge",     lep_charge)
        self.out.fillBranch("LepCand_dxy",        lep_dxy)
        self.out.fillBranch("LepCand_dz",         lep_dz)
        self.out.fillBranch("LepCand_tauvsjet",         lep_tauvsjet)
        self.out.fillBranch("LepCand_tauvsmu",         lep_tauvsmu)
        self.out.fillBranch("LepCand_tauvse",         lep_tauvse)
        # CHANGE Fill the branches with the 2018v2p5 DNNs
        self.out.fillBranch("LepCand_tauvsjet2018",         lep_tauvsjet2018)
        self.out.fillBranch("LepCand_tauvsmu2018",         lep_tauvsmu2018)
        self.out.fillBranch("LepCand_tauvse2018",         lep_tauvse2018)
        self.out.fillBranch("LepCand_tauvsjet2018_sf",         lep_tauvsjet2018_sf)
        self.out.fillBranch("LepCand_tauvsmu2018_sf",         lep_tauvsmu2018_sf)
        self.out.fillBranch("LepCand_tauvse2018_sf",         lep_tauvse2018_sf)
        self.out.fillBranch("LepCand_taudm",         lep_taudm)
        self.out.fillBranch("LepCand_gen",         lep_gen)
        self.out.fillBranch("LepCand_muonIso_sf",         lep_muonIso_sf)
        self.out.fillBranch("LepCand_muonID_sf",         lep_muonID_sf)
        self.out.fillBranch("LepCand_trg_sf",         lep_trg_sf)
        self.out.fillBranch("nJets" ,             len(event.selectedAK4Jets))

        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
analysis_mutaumc    = lambda : Analysis(channel="mutau", isMC=True)

analysis_mutaudata  = lambda : Analysis(channel="mutau", isMC=False)
