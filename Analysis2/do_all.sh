# CHANGE replace with the location of your ntuples
#DATA_DIR=/uscms/home/caleb/nobackup/CMSDAS_2025/StauLongExercise/ntuples_mutau_2022_v0
#DATA_DIR=/uscms/home/caleb/nobackup/CMSDAS_2025/StauLongExercise/ntuples_mutau_2022_v1
DATA_DIR=/uscms/home/peter802/nobackup/CMSDAS_2025/StauLongExercise/CMSSW_13_0_10/src/cmsdas2025/ntuples_mutau_2022

mkdir -p output_mutau_2022

./Make.sh FinalSelection_mutau.cc
./FinalSelection_mutau.exe 2022postEE $DATA_DIR/DY_postEE.root output_mutau_2022/DY_postEE.root DY DY
./FinalSelection_mutau.exe 2022postEE $DATA_DIR/TTTo2L2Nu_postEE.root output_mutau_2022/TTTo2L2Nu_postEE.root TTTo2L2Nu TTTo2L2Nu
./FinalSelection_mutau.exe 2022postEE $DATA_DIR/WW_postEE.root output_mutau_2022/WW_postEE.root WW WW
./FinalSelection_mutau.exe 2022postEE $DATA_DIR/stau_left.root output_mutau_2022/stau_left_postEE.root stau_left stau_left
./FinalSelection_mutau.exe 2022postEE $DATA_DIR/stau_right.root output_mutau_2022/stau_right_postEE.root stau_right stau_right
./FinalSelection_mutau.exe 2022postEE $DATA_DIR/Muon2022E.root output_mutau_2022/Muon2022E.root data_obs data_obs
./FinalSelection_mutau.exe 2022postEE $DATA_DIR/Muon2022F.root output_mutau_2022/Muon2022F.root data_obs data_obs
./FinalSelection_mutau.exe 2022postEE $DATA_DIR/Muon2022G.root output_mutau_2022/Muon2022G.root data_obs data_obs

hadd -f output_mutau_2022/Data.root output_mutau_2022/Muon2022E.root output_mutau_2022/Muon2022F.root output_mutau_2022/Muon2022G.root
python3 Create_fake.py

hadd -f datacard_mutau.root output_mutau_2022/DY_postEE.root output_mutau_2022/TTTo2L2Nu_postEE.root output_mutau_2022/WW_postEE.root output_mutau_2022/Data.root output_mutau_2022/Fake.root output_mutau_2022/stau_left_postEE.root output_mutau_2022/stau_right_postEE.root 
python3 Draw_Hists.py

