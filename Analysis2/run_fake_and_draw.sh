hadd -f output_mutau_2022/Data.root output_mutau_2022/Muon2022E.root output_mutau_2022/Muon2022F.root output_mutau_2022/Muon2022G.root
python3 Create_fake.py

hadd -f datacard_mutau.root output_mutau_2022/DY_postEE.root output_mutau_2022/TTTo2L2Nu_postEE.root output_mutau_2022/WW_postEE.root output_mutau_2022/Data.root output_mutau_2022/Fake.root output_mutau_2022/stau_left_postEE.root output_mutau_2022/stau_right_postEE.root 
python3 Draw_Hists.py

