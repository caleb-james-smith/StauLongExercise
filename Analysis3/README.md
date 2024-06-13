## CMSSW setup - ONLY ONCE
```
cmssw-el7 #singularity needed

cmsrel CMSSW_11_3_4
cd CMSSW_11_3_4/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester

cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v9.2.1

scramv1 b clean; scramv1 b # always make a clean build
```

Move script to CombineHarvester
```
cp produceDataCard_mt.py CombineHarvester/CombineTools/scripts/produceDataCard_mt.py
```

Make sure that auxiliaries exist:
```
ls -l auxiliaries/mt/
```

If the directory doesn't exist, create it and copy the output file from Analysis2 must be placed under auxiliaries/mt/:

```
mkdir auxiliaries/
mkdir auxiliaries/mt/
cp <file> auxiliaries/mt/	

```

The following steps are to be done each time the analysis selection is changed; remember to copy the output file of Analysis2 under auxiliaries/mt!

Make the data card (remember to use singularity!)

```
cd $CMSSW_BASE/src/
cmsenv
python CombineHarvester/CombineTools/scripts/produceDataCard_mt.py

```

Ensure that data card and root file were made:

```
ls -l mt*
```

Inspect the data card, and then proceed as follows:
1. Apply changes 1 and 5 related to the reducible background: inspect how the data card looks
2. Apply changes 2-4, and 6 related to the chosen signal scenario: 

Once you are happy with the data card script, reproduce the data card and run limits

```
combine -M AsymptoticLimits mt.txt
```

Question: What is the output of this command? What do the values mean?

Question: How does the obtained limit compare to the previously published results [1]? Can these results be directly compared to each other? What is the main difference?  ([1] https://cms-results.web.cern.ch/cms-results/public-results/publications/SUS-21-001/, figs. 4d, 5d, and 6d). 

Extra task: Optimise the analysis selection, and reproduce the limit. How much does the limit improve? Why?
