#!/usr/bin/env python2.7

from DIRAC.Core.Base import Script
Script.parseCommandLine()
from DIRAC.Interfaces.API.Dirac import Dirac
from DIRAC.Interfaces.API.Job import Job

raw = 'lfn:/grid/t2k.org/nd280/raw/ND280/ND280/00014000_00014999/nd280_00014000_0000.daq.mid.gz'
exe = '/home/mhogan/software/ND280Computing/processing_scripts/P0DCalibProcess.py'
args = '-v v12r15 -i %s' % raw
stdout = 'std.out'
stderr = 'std.err'
logfile = 'ND280Custom.log'
# make sure to export VO_T2K_ORG_SW_DIR
environmentDict =\
    {
        'VO_T2K_ORG_SW_DIR': '/cvmfs/t2k.egi.eu'
    }
# these files are larger than 10 MB
inputData =\
    [
        raw
    ]
outputData =\
    [
        'LFN:*root'
    ]
# this file is needed remotely for the job
inputSandbox =\
    [
        exe,
        "../custom_parameters/P0DMOD.PARAMETERS.DAT",
        "RunCustom.py",
        "P0DCalibProcess.py",
        "../tools/ND280Computing.py",
        "../tools/ND280Configs.py",
        "../tools/ND280GRID.py",
        "../tools/ND280Job.py",
        "../tools/ND280Software.py",
        "../tools/pexpect.py",
        "../tools/StorageElement.py"
    ]
# these files are created by the job
outputSandbox =\
    [
        stdout,
        stderr,
        logfile
    ]

# the executible here '' is later set, so don't confuse users later on
diracJob = Job('', stdout, stderr)

# give a descriptive name
diracJob.setName('ND280Custom')

# set the program/executable, arguments, logFile, ...
diracJob.setExecutable(exe, arguments=args, logFile=logfile)

# set the job length
diracJob.setCPUTime(3600)

diracJob.setInputSandbox(inputSandbox)
diracJob.setExecutionEnv(environmentDict)
diracJob.setInputData(inputData)
diracJob.setOutputSandbox(outputSandbox)

"""
Output data is written to / <VO> / user / <initial> / <username>
so the full path of output data in this example is
/<VO>/user/<initial>/<username>/tests
"""
diracJob.setOutputData(outputData, outputSE='CA-TRIUMF-T2K1-disk', outputPath='tests')

print 'job being submitted...'
dirac = Dirac()
result = dirac.submit(diracJob)
print 'Submission Result: ', result
