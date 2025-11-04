#!/usr/bin/python

"""
all DR 10 !!!!!!!!!!!

makes a list of unique   run,rerun,camcol,field and objids in it


INPUT
objid,ra,dec,run,rerun,camcol,field

OUTPUT
run,rerun,camcol,field  objid_1, objid_2, ..., objid_N

"""

import makemySDSSlib as makemySDSS 
import os
import pylab as pl
import numpy as np
from astLib  import astWCS
from sys import argv,stderr



if len(argv) < 2:
    print """

    makemySDSSunique LISTA
    
         where LISTA is
         objid,ra,dec,run,rerun,camcol,field

         generates a UNIQUE lista of run,rerun,camcol,field contained in LISTA file

         """

    exit()



dbfile = argv[1]





objids  = []
ras     = []
decs    = []
runs    = []
reruns  = []
camcols = []
fields  = []
Rps     = []

for linha in open(dbfile, 'r'): 
    Sobjid,Sra,Sdec,Srun,Srerun,Scamcol,Sfield,SRp = linha.split(',')
    
    try:
        objids.append(  int(Sobjid) )
        ras.append(     float(Sra)  )
        decs.append(    float(Sdec) )
        runs.append(    int(Srun)   )
        reruns.append(  int(Srerun) )
        camcols.append( int(Scamcol))
        fields.append(  int(Sfield) )
        Rps.append(     float(SRp)  )
    except:
        print >> stderr, 'missing line', linha
        continue



N = len(objids)

objids  = np.array(objids)
ras     = np.array(ras)
decs    = np.array(decs)
runs    = np.array(runs)
reruns  = np.array(reruns)
camcols = np.array(camcols)
fields  = np.array(fields)
Rps     = np.array(Rps)


# remove duplicate setups 
frameids = set( zip(runs,reruns,camcols,fields) )










for (RN,RR,CC,FF)  in frameids:

    print '%d,%d,%d,%d' % (RN,RR,CC,FF)

        
            

