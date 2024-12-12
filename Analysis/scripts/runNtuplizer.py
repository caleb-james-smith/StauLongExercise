#!/usr/bin/env python
import os
import sys
import optparse
import shutil
import random
from glob import glob
from StauLongExercise.Analysis.EraConfig import *

cmssw=os.environ['CMSSW_BASE']

def makeSandbox(FarmDirectory,rand):
    sandbox_cmd = f"tar --exclude='CMSSW_13_0_10/src/*' --exclude-caches-all -cf {FarmDirectory}/CMSSW_13_0_10_{rand}.tar -C $CMSSW_BASE/../ CMSSW_13_0_10"
    os.system(sandbox_cmd)
    sandbox_cmd = f"tar -rf {FarmDirectory}/CMSSW_13_0_10_{rand}.tar -C $CMSSW_BASE/../ CMSSW_13_0_10/src/PhysicsTools/ CMSSW_13_0_10/src/StauLongExercise/Analysis/python/DiTau_analysis.py CMSSW_13_0_10/src/StauLongExercise/Analysis/python/objectSelector.py CMSSW_13_0_10/src/StauLongExercise/Analysis/muon_Z.json CMSSW_13_0_10/src/StauLongExercise/Analysis/tau_DeepTau2018v2p5_2022_postEE.json"
    os.system(sandbox_cmd)
    sandbox_cmd = f"gzip {FarmDirectory}/CMSSW_13_0_10_{rand}.tar"
    os.system(sandbox_cmd)

def buildCondorFile(opt,FarmDirectory):

    """ builds the condor file to submit the ntuplizer """

    rand='{:03d}'.format(random.randint(0,123456))
    print(f"making sandbox {FarmDirectory}/CMSSW_13_0_10_{rand}.tar.gz")
    makeSandbox(FarmDirectory,rand)
	
    datasets=open(opt.input).read().splitlines()
    #condor submission file
    condorFile='%s/condor_generator_%s.sub'%(FarmDirectory,rand)
    print('Writes: %s'%condorFile)
    with open (condorFile,'w') as condor:
        condor.write('executable = {0}/worker_{1}.sh\n'.format(FarmDirectory,rand))
        condor.write('output = {0}/output_{1}.out\n'.format(FarmDirectory,rand))
        condor.write('error = {0}/output_{1}.err\n'.format(FarmDirectory,rand))
        condor.write('log = {0}/output_{1}.log\n'.format(FarmDirectory,rand))
        condor.write('use_x509userproxy = true\n')
        OpSysAndVer = str(os.system('cat /etc/redhat-release'))
        OpSysAndVer = "AlmaLinux9"
        condor.write('requirements = (OpSysAndVer =?= "{0}")\n\n'.format(OpSysAndVer))
        condor.write('should_transfer_files = YES\n')
        condor.write('when_to_transfer_output = ON_EXIT\n')
        condor.write(f'transfer_input_files = {cmssw}/src/StauLongExercise/Analysis/scripts/keep_in.txt,{cmssw}/src/StauLongExercise/Analysis/scripts/keep_out.txt,{FarmDirectory}/CMSSW_13_0_10_{rand}.tar.gz\n')
        for dataset in datasets:
          if "#" in dataset or len(dataset)<2: continue
          print('INFO: Processing %s'%(dataset))
          sufix=''
          prefix=''
          year='2022'
          if '22Sep' in dataset or 'Run3' in dataset:
            dataset_name = '_'.join(dataset.split('/')[1:3])
            sufix='data'
            cmd='dasgoclient --query=\"file dataset={} status=*\"'.format(dataset)
            file_list=os.popen(cmd).read().split()
            prefix='root://cmsxrootd.fnal.gov/'
          elif 'eos' in dataset.split('/'):
            sufix='mc'
            dataset_name = dataset.split('/')[-1]
            file_list=glob(dataset+'/*root')
          else:
            print('ERROR: found invalid dataset = ',dataset,'stop the code')
            sys.exit(1)
          if "Muon" in dataset:
              sufix='data'
          else:
              sufix='mc'
	      # CHANGE: indicate which channel you want to run on
          channels=['mutau']
          #channels=['mumu']
            
          #prepare output
          output=opt.output+'/'+dataset_name
			
          for channel in channels:
            output_full=output+"_"+channel
            # apply filter to data: trigger and GRL
            filter=ANALYSISCUT[year][channel]
            os.system('mkdir -p {}'.format(output_full))
            for file in file_list:
              outfile='%s/%s'%(output_full,os.path.basename(file).replace('.root','_Skim.root'))
              if os.path.isfile(outfile) and not opt.force: continue
              condor.write('arguments = %s %s %s %s\n'%(prefix+file,'analysis_'+channel+sufix,output_full,filter))
              skim_output_name = file.split('/')[-1:][0].split('.')[0]+"_Skim.root"
              condor.write(f'transfer_output_files={skim_output_name}\n')
              condor.write(f'transfer_output_remaps="{skim_output_name}={output_full}/{skim_output_name}"\n')
              condor.write('queue 1\n')
              if opt.test:
                break
            if opt.test:
              break
          if opt.test:
            break

    workerFile='%s/worker_%s.sh'%(FarmDirectory,rand)
    with open(workerFile,'w') as worker:
        worker.write('#!/bin/bash\n')
        worker.write('startMsg="Job started on "`date`\n')
        worker.write('echo $startMsg\n')
        worker.write('WORKDIR=$(pwd)\n')
        worker.write('########### INPUT SETTINGS ###########\n')
        worker.write('input=${1}\n')
        worker.write('channel=${2}\n')
        worker.write('output=./\n')
        worker.write('filter=${@:4}\n')
        worker.write('filename=`echo ${1} | rev | cut -d"/" -f1 | rev | cut -d"." -f1`\n')
        worker.write('######################################\n')
        worker.write('echo "worker_%s.sh arguments:"\n'%(rand))
        worker.write('echo input="$input"\necho channel="$channel"\necho output="$output"\necho filter="$filter"\n')
        worker.write('######################################\n')
        worker.write('source /cvmfs/cms.cern.ch/cmsset_default.sh\n')
        worker.write(f'tar -xf CMSSW_13_0_10_{rand}.tar.gz\n')
        worker.write(f'rm CMSSW_13_0_10_{rand}.tar.gz\n')
        worker.write('cd CMSSW_13_0_10/src/\n')
        worker.write('scramv1 b ProjectRename\n')
        worker.write('eval `scramv1 runtime -sh`\n')
        worker.write('echo "INFO: Run ntuplizer"\n')
        worker.write('echo "python3 $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py \\\\"\n')
        worker.write('echo "$filename ${input}  \\\\"\n')
        worker.write('echo "--bi $WORKDIR/keep_in.txt   \\\\"\n')
        worker.write('echo "--bo $WORKDIR/keep_out.txt  \\\\"\n')
        worker.write('echo "${filter} -I StauLongExercise.Analysis.DiTau_analysis ${channel} "\n')
        worker.write('python3 $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py \\\n')
        worker.write('$filename ${input}  \\\n')
        worker.write('--bi $WORKDIR/keep_in.txt   \\\n')
        worker.write('--bo $WORKDIR/keep_out.txt  \\\n')
        worker.write('${filter} -I StauLongExercise.Analysis.DiTau_analysis ${channel} \n')
        worker.write('mv ${filename}/*.root $WORKDIR/\n')
        worker.write('echo made output file: ${filename}_Skim.root\n')
        worker.write('echo $startMsg\n')
        worker.write('echo job finished on `date`\n')
    os.system('chmod u+x %s'%(workerFile))

    return condorFile

def main():

    if not os.environ.get('CMSSW_BASE'):
      print('ERROR: CMSSW not set')
      sys.exit(0)
    
    cmssw=os.environ['CMSSW_BASE']
    user=os.environ['USER']

    #configuration
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('-i', '--in',     dest='input',  help='list of input datasets',    default='listSamples.txt', type='string')

    # CHANGE: indicate the area in eos where the output files should be stored (and create it with mkdir before submitting the jobs)
    parser.add_option('-o', '--out',      dest='output',   help='output directory',  default=cmssw+'/src/cmsdas2025/ntuples_mutau_2022', type='string')

    parser.add_option('-f', '--force',      dest='force',   help='force resubmission',  action='store_true')
    parser.add_option('-s', '--submit',   dest='submit',   help='submit jobs',       action='store_true')
    parser.add_option('-t', '--test',     dest='test',    help='only create single test job', action='store_true')
    (opt, args) = parser.parse_args()
     
    if not os.path.isfile(opt.input): 
      print('ERROR: bad input file (%s)'%opt.input)
      sys.exit(1)
	
    #prepare directory with scripts
    FarmDirectory=os.environ['PWD']+'/FarmLocalNtuple'
    if not os.path.exists(FarmDirectory):  os.system('mkdir -vp '+FarmDirectory)
    #os.environ['X509_USER_PROXY']='%s/myproxy509'%FarmDirectory

    #build condor submission script and launch jobs
    condor_script=buildCondorFile(opt,FarmDirectory)
    #print('\nINFO: IMPORTANT MESSAGE: RUN THE FOLLOWING SEQUENCE:')
    #print('voms-proxy-init --voms cms --valid 72:00 --out %s/myproxy509\n'%FarmDirectory)

    #submit to condor
    if opt.submit:
        os.system('condor_submit {}'.format(condor_script))
    else:
        print('condor_submit {}\n'.format(condor_script))
		

if __name__ == "__main__":
    sys.exit(main())
