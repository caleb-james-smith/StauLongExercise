# Analysis

Code to make flat trees from NanoAOD with baseline analysis preselection.

## To run locally on a file

Set up CMSSW environment and grid certificate (if not already done). 
```
cmsenv
voms-proxy-init --valid 192:00 -voms cms
voms-proxy-info
```

Run locally on a file:
```
python3 PhysicsTools/NanoAODTools/scripts/nano_postproc.py output root://cms-xrd-global.cern.ch//store/mc/Run3Summer22EENanoAODv12/DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8/NANOAODSIM/forPOG_130X_mcRun3_2022_realistic_postEE_v6-v2/2520000/344faad6-749a-42c3-b635-8d3e04c58de6.root --bi $CMSSW_BASE/src/StauLongExercise/Analysis/scripts/keep_in.txt --bo $CMSSW_BASE/src/StauLongExercise/Analysis/scripts/keep_out.txt -c "(nMuon>0&&nTau>0&&HLT_IsoMu24)" -I StauLongExercise.Analysis.DiTau_analysis analysis_mutaumc -N 1000
```

## To submit jobs for full datasets over Condor

First edit python/EraConfig.py (data or MC, object preselection in NanoAOD) and scripts/runNtuplizer (which channel to run, where to store the output files)

For MC:

```
python3 $CMSSW_BASE/src/StauLongExercise/Analysis/scripts/runNtuplizer.py --in $CMSSW_BASE/src/StauLongExercise/Analysis/data/listSamplesMC.txt
```

For data: 

```
python3 $CMSSW_BASE/src/StauLongExercise/Analysis/scripts/runNtuplizer.py --in $CMSSW_BASE/src/StauLongExercise/Analysis/data/listSamplesMuonData.txt
```

And follow the instructions printed on the screen (dont forget to type the new voms-proxy-init command printed). 

## To combine the output files once all condor jobs have run

First edit my\_hadd.sh with the location of your output files. Then:
```
sh my_hadd.sh
```

