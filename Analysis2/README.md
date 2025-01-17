# Analysis2

Code to analyze the flat trees and make plots and datacards.

To run on a flat tree:
```
mkdir -p output_mutau_2022
./Make.sh FinalSelection_mutau.cc
./FinalSelection_mutau.exe 2022 $CMSSW_BASE/src/cmsdas2025/ntuples_mutau_2022/Muon2022F.root output_mutau_2022/Muon2022F.root data_obs data_obs
```

To make a data/MC plot from a datacard:
```
python3 Draw_mutau.py
```

To run the full sequence (run on each flat tree, create the fake histogram, make the datacard, draw the distributions):
```
sh do_all.sh
```

To only run the fake histogram and draw steps, use:
```
sh run_fake_and_draw.sh
```

