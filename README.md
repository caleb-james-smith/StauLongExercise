# SUS PAG Long Exercise

## Introduction

The goal of this exercise is to search for stau pair production in 2022 data. The final state consists of 2 nonresonant taus and MET from the LSP. The analysis has not been done with Run-3 data yet, you are the first ones to do it! We will analyze the final state with a muon (coming from a leptonic tau decay) and a hadronic tau.

Question: What is the branching fraction for the mu+tauh final state?

Question: Why do we choose the mu+tauh final state to start with?

Question: What do you expect the backgrounds to be? What selection could reduce them?


## Prerequisites

For these exercises, you need to bring your laptop, have a working lpc account, and have a valid grid certificate.

The code snippets below describe the steps to follow to login and set up the necessary working area for this twiki. The requirements described in Prerequisites are necessary to proceed to this step.

Login on cmslpc:

```
kinit yourusername@FNAL.GOV
ssh -Y yourusername@cmslpc-el9.fnal.gov
```

Create a working directory in your nobackup area:

```
mkdir StauLongExercise
cd StauLongExercise
```

Connect to the grid:

```
voms-proxy-init -voms cms --valid 192:0
```

Check out the code:

```
cmsrel CMSSW_13_0_10
cd CMSSW_13_0_10/src
cmsenv

#setup nanoAOD-tools
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
scram b -j 8

#This package
git clone https://github.com/caleb-james-smith/StauLongExercise.git StauLongExercise
scram b -j 8

#Correctionlib
python3 -c 'import correctionlib._core; import correctionlib.schemav2'
```

All the places in the code you should modify have a comment starting with CHANGE.

## Wednesday: Part 1 - Make flat trees from NanoAOD

This part is based on the code in the "Analysis" folder.

The goal of this part is to make flat trees with a basic preselection (events with one muon and one hadronic tau passing the single muon trigger), saving the variables needed to perform the analysis.The flat trees will allow you to be very flexible with the analysis, reanalyzing data with different cuts or observables in only a few minutes.

You will learn how to run on NanoAOD files, submit the jobs to condor, and implement POG-provided scale factors with correctionlib.

### Part 1.1: Running the example

Run the basic existing code locally on a Drell-Yan file (instructions in this README) and inspect the output file.

### Part 1.2: Add lepton variables to the flat tree

Some of the variables already saved for the lepton (muon or tauh) objects are:

- LepCand\_taudm (tau decay mode)
- LepCand\_tauvsjet (tau DNN discrimination against jets 2017v2p1 training)
- LepCand\_tauvsmu (tau DNN discrimination against muons 2017v2p1 training)
- LepCand\_tauvse (tau DNN discrimination against electrons 2017v2p1 training)
- LepCand\_gen (genPartFlav - matching to gen particle)
- LepCand\_phi
- LepCand\_eta
- LepCand\_charge
- LepCand\_dxy
- LepCand\_dz


Add the branches that (in DiTau\_analysis.py) will be necessary for the rest of the analysis. We suggest this minimal list with the following naming convention:

- LepCand\_tauvsjet2018 (tau DNN discrimination against jets 2018v2p5 training) 
- LepCand\_tauvsmu2018 (tau DNN discrimination against jets 2018v2p5 training)
- LepCand\_tauvse2018 (tau DNN discrimination against jets 2018v2p5 training)

The documentation of the NanoAODv12 branches is available [here](https://cms-nanoaod-integration.web.cern.ch/autoDoc/NanoAODv12/2022/2023/doc_DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8_Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2.html#top).

You can add other branches too, which you think would be useful.

### Part 1.3: Save other NanoAOD collections/objects

Save some NanoAOD variables you want to use later and do not need any analysis-specific processing (edit keep\_in and keep\_out). The minimal set to save is:

```
PuppiMET pt and phi
Single muon HLT path (HLT_IsoMu24) 
```

Feel free to save other variables you want to study later.

### Part 1.4: Refine the object preselection:

To reduce the size of the output files and simplify the event processing later, apply a preselection on the muons and taus you keep for further analysis (edit objectSelector.py).

This preselection is already applied to muons:

- pT > 10 GeV
- abs(eta) < 2.4
- medium muon ID
- PF relative iso < 0.15 

This preselection is already applied to taus (loose preselection so we can play with the tau ID WPs later):

- pT > 20 GeV
- abs(eta) < 2.3
- (VVVLoose DNN2017 vs jet and VVVLoose DNN2017 vs e and VLoose DNN2017 vs mu) OR (VVVLoose DNN2018 vs jet and VVVLoose DNN2018 vs e and VLoose DNN2018 vs mu)
- abs(dz) < 0.2 

Edit the code to only save taus reconstructed in decay mode 0, 1, 10, or 11. You can also apply other preselections as long as they do not limit you in the analysis we will perform tomorrow.

### Part 1.5: Add scale factors using correctionlib

We will need to apply data/MC scale factors for the tau identification efficiency, the tau energy scale, the muon ID/iso efficiency, and the trigger efficiency. It is easier to add them at this stage in dedicated branches using correctionlib in python.

Muon ID, isolation, and trigger scale factors are already implemented. Add the scale factors for taus: 

Add the following branches:

- LepCand\_tauvsjet2018\_sf
- LepCand\_tauvsmu2018\_sf
- LepCand\_tauvse2018\_sf 

### Part 1.6: Submit the jobs to condor

First inspect the output obtained from running locally to make sure it is correctly filled and you have all the necessary information stored. Then follow the instructions in the README. Dont forget to edit runNtuplizer with the output location and the final state, and EraConfig based on whether you process data (json file selection) or MC (no json file selection).

## Thursday - Part 2: Analyze the flat trees and make datacards

### Part 2.1: Apply the selection in the mutau final state and make data distributions

Apply the final selection to the flat trees in FinalSelection\_mutau.cc:

- single muon trigger (HLT\_IsoMu24)
- muon pT > 26 GeV
- abs(muon eta) < 2.4
- tau pT > 30 GeV (can be lowered to 20 GeV but more backgrounds)
- abs(tau eta) < 2.3
- tau ID: Medium DNN vs jet, VVLoose DNN vs e, Tight DNN vs muons
- muon and tau have opposite sign (OS) charge
- DR(muon, tau) > 0.5
- muon ID and iso already applied when building the flat trees
- abs(muon dxy) < 0.1
- abs(muon dz) < 0.2 

Fill histograms to inspect the data (invariant mass of mutau, muon pt, tau pt, transverse mass between the muon and the MET, ...).

### Part 2.2: Do the same for MC

Use the same code to make MC histograms, but add the cross section reweighting. You can use the following cross sections:

- TTTo2L2Nu: 923.6 pb x 0.1061
- WW: 120 pb
- DY: 6345.99 pb 

The integrated luminosity for the 2022 postEE dataset is aboyt 20 fb-1 (exact value in the code).

Apply the data/MC scale factors saved as branches.

Make a plot to compare the data and MC predictions using this code. We are missing background events with jet to tauh fakes.

### Part 2.3: Estimate the jet->tau fake background

We will use a data-driven background estimation method to estimate processes with a jet faking a tauh because simulations are not available or too small, and we do not trust simulations to model correctly the jet to tauh fake rate.

Question: What processes with jet to tauh fakes contribute to the mutau final state? Which ones do you expect to dominate?

We are going to use a fake rate method. We need to measure the probability for jets that pass a very loose tau ID selection to also pass the nominal tau ID selection, so that we can reweigh events with anti-isolated taus to model the fake background in the signal region. The fake rates are measured in regions enriched in fake events (depleted in Z to tautau events, which have real tauh) and orthogonal to the signal region. We will use events with SS muon and tau. In this CR, do the following:

- Fill a histogram with the pt of the tau for events where the tau passes the VVVLoose DNN vs jets but fails the Medium DNN vs jets (or the WP chosen in the earlier step) = denominator
- Do the same for control region events with a tau passing the Medium DNN vs jets (or the WP chosen) = numerator
- Compute the ratio of the two histograms; this is the fake rate (take a flat number or fit the tau pt dependence)
- Select data events that pass the signal region selection except that the tau passes the VVVLoose DNN vs jets but fails the Medium DNN vs jets, and reweigh them with the fake rate of step 3.. This gives you the fake background prediction in the signal region
- This can be refined by subtracting the contribution of MC with real taus in the control regions, weighted with the same fake rates. 
- Since this estimates all events with a jet faking a tauh, veto those events in the MC simulation (gen = 0). 

### Part 2.4 (bonus): Separate Z->mumu from Z->tautau

In the DY simulation, we have Z to tautau events, but also Z to mumu events where a muon fakes a tau. The latter contribution has a distinctive signature in the dimuon mass distribution (narrow peak at 90 GeV). We want to measure the tau ID efficiency for real taus, and therefore we want to separate the two contributions in two different histograms. The two contributions can be separated based on the gen ID of the tau. Please make two separate histograms and plot them with different colors.

### Friday - Part 2.5: Optimize the analysis

Compare distributions of different variables between the signal and the dominant backgrounds, and choose which variables to cut on and which variable to use as observable to extract the results.

## Friday - Part 3: Use Combine to extract the expected limits

Install CombineHarvester and Combine in a separate area following these instructions.

To run Combine for this analysis you need a mutau datacard. In the datacard, you need a directory per signal region (e.g. OSiso), and inside the directory a histogram per process (data has to be called "data\_obs", the naming convention for other processes is free).

## Friday - Part 4: Use ReAna to make this analysis reinterpretable 

