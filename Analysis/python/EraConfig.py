import os
""" Year dependent configurations / files """

ANALYSISTRIGGER = {
    '2022': {'mutau':'(HLT_IsoMu24)','mumu':'(HLT_IsoMu24)'}
}

ANALYSISCHANNELCUT = {
    'mutau':'(nMuon>0&&nTau>0)',
    'mumu':'(nMuon>1)'
}

ANALYSISGRL = {
    '2022': 'Cert_Collisions2022_355100_362760_Golden.json'
}

ANALYSISCUT={'': {'mutau' : '-c "%s"'%ANALYSISCHANNELCUT['mutau'],'mumu' : '-c "%s"'%ANALYSISCHANNELCUT['mumu']}}

# CHANGE uncomment if running on data and comment next section

## for data, json selection
#for y in ANALYSISTRIGGER:
#  ANALYSISCUT[y]={}
#  for c in ANALYSISTRIGGER[y]:
#    ANALYSISCUT[y][c]='--cut %s&&%s --json %s'%(ANALYSISTRIGGER[y][c],ANALYSISCHANNELCUT[c],'./StauLongExercise/Analysis/data/'+ANALYSISGRL[y])

## for MC, no json
for y in ANALYSISTRIGGER:
  ANALYSISCUT[y]={}
  for c in ANALYSISTRIGGER[y]:
    ANALYSISCUT[y][c]='--cut %s&&%s '%(ANALYSISTRIGGER[y][c],ANALYSISCHANNELCUT[c])
