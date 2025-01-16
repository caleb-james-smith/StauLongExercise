from __future__ import absolute_import
import CombineHarvester.CombineTools.ch as ch

import ROOT as R
import glob
import os

cb = ch.CombineHarvester()
cb.SetVerbosity(3)

auxiliaries  = os.environ['CMSSW_BASE'] + '/src/auxiliaries/'

chns = ['mt']

#CHANGE 1: Add the reducible background process to the list of backgrounds
bkg_procs = {'mt' : ['DY', 'TTTo2L2Nu', 'WW']}

#CHANGE 2: Add signal process following structure above; choose one of the available ones

cats = {
    'mt_13TeV' : [
    (0, 'OSiso'),
  ],
}

for chn in chns:
    cb.AddObservations(  ['*'],  [''], ['13TeV'], [chn],                 cats[chn+"_13TeV"]      )
    cb.AddProcesses(     ['*'],  [''], ['13TeV'], [chn], bkg_procs[chn], cats[chn+"_13TeV"], False  )
#CHANGE 3: Add line for the signal process

print('>> Adding systematic uncertainties...')
#CHANGE 4: Add the systematic uncertainties also for the chosen signal process
cb.cp().process({"DY", "TTTo2L2Nu", "WW"}).AddSyst(cb, 'lumi_13TeV', 'lnN', ch.SystMap()(1.03))
cb.cp().process({"DY", "TTTo2L2Nu", "WW"}).AddSyst(cb, "CMS_eff_m", "lnN", ch.SystMap()(1.02));
cb.cp().process({"DY", "TTTo2L2Nu", "WW"}).AddSyst(cb, "CMS_eff_t", "lnN", ch.SystMap()(1.08));

#CHANGE 5: Add a flat 50% log normal systematic uncertainty for the reducible background

print('>> Extracting histograms from input root files...')
for chn in chns:
    file = auxiliaries + chn + "/datacard_mutau.root" 
    cb.cp().channel([chn]).era(['13TeV']).backgrounds().ExtractShapes(
        file, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')
    #CHANGE 6: Extract the histograms of signal

bins = cb.bin_set()

output=R.TFile("mt.input.root", "RECREATE");

for b in bins:
  cb.cp().bin({b}).WriteDatacard("mt.txt", output);

