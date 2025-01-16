## CMSSW setup - ONLY ONCE

First, set up a new working area (separate from what you have been using up to this point)
to install Combine and CombineHarvester.

Note that we are using a different CMSSW version for Combine and CombineHarvester
compared to what we used previously for the analysis up to this point!

Do NOT "nest" CMSSW installations or install them in "series," please!
For example, your installation should NOT look like `CMSSW_1_2_3/src/CMSSW_4_5_6/src`.
Rather, you should install them in parallel.
For example, `CMSSW_1_2_3/src` and `CMSSW_4_5_6/src`
should be two separate directories that are not in the same path.

Add the following alias `use_sl7` to `~/.bash_profile`.
```
# Use SL7 container
alias use_sl7='cmssw-el7 -p --bind `readlink $HOME` --bind `readlink -f ${HOME}/nobackup/` --bind /uscms_data --bind /cvmfs --bind /uscmst1b_scratch -- /bin/bash -l'
```

You can also add the following to `~/.bash_profile` to modify your prompts (optional):
```
# used to show git branch in prompt
parse_git_branch ()
{
    git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}

# make sure function works for apptainer (e.g. SL7 container)
export -f parse_git_branch


# command prompt
export PS1='\[\e[32m\]${HOSTNAME}\[\e[0;36m\] \W \[\e[01;34m\]#\[\e[m\]$(parse_git_branch)\[\033[00m\] \[\e[1;00m\]'

# use a similar prompt for apptainer (e.g. SL7 container)
# - note that you need to escape $ with \$ (will not work otherwise)
# - replaced # with "*" (quotes are required to prevent expansion)
export APPTAINERENV_PS1='\[\e[32m\]\${HOSTNAME}\[\e[0;36m\] \W \[\e[01;34m\]"*"\[\e[m\]\$(parse_git_branch)\[\033[00m\] \[\e[1;00m\]'
```

Then do
```
source ~/.bash_profile
```

```
# Use SL7 container
use_sl7

# Set SCRAM_ARCH for SL7
export SCRAM_ARCH=slc7_amd64_gcc700

# Set up CMSSW
cmsrel CMSSW_11_3_4
cd CMSSW_11_3_4/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester

cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v9.2.1

# Make sure to run scramv1 from the CMSSW_11_3_4/src directory!!
cd $CMSSW_BASE/src
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

Extra task: Optimize the analysis selection, and reproduce the limit. How much does the limit improve? Why?
