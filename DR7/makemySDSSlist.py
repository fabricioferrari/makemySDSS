#!/usr/bin/python

"""
Image URL (see http://www.sdss.org/dr7/algorithms/dataProcessing.html  [mas falta o camcol no diretorio])

FIELD:
http://das.sdss.org/imaging/%d/%d/corr/%d/fpC-%06d-%c%d-%04d.fit.gz        (run,rerun,camcol,run,filter,camcol,field)

PSF params:
http://das.sdss.org/imaging/%d/%d/objcs/%d/psField-%06d-%d-%04d.fit.gz 	(run,rerun,camcol,run,camcol,field)

EXAMPLE
wget -r -q -nd --directory-prefix=g http://das.sdss.org/imaging/1356/40/corr/2/fpC-001356-g2-0032.fit.gz

"""


import os
import pylab as pl
import numpy as np
from astLib  import astWCS
from sys import argv

if len(argv) < 3:
    print """

    makemySDSSlist LISTA FILTRO[s]   [check]

         where LISTA is
         objid,ra,dec,run,rerun,camcol,field
         """
    exit()

filtros = argv[2]
listfile = open(argv[1],'r')

if 'check' not in argv:
	print '#!/bin/bash'

for xx in listfile.readlines():
    objid,ra,dec,run,rerun,camcol,field,lixo,lixo,lixo =xx.split(',')

    try:
        objid = int(objid)
        ra    = float(ra)
        dec   = float(dec)
        run   = int(run)
        rerun = int(rerun)
        camcol = int(camcol)
        field  = int(field)
    except:
        continue


    psfurl = 'http://das.sdss.org/imaging/%d/%d/objcs/%d/psField-%06d-%d-%04d.fit' % \
             (run,rerun,camcol,run,camcol,field)

    psffile = 'psField-%06d-%d-%04d.fit' % (run,camcol,field)
    
    psfwgetcmd = 'wget -r -nd -q --directory-prefix=psField  ' 

    if 'check' in argv:
        if os.path.isfile('psField' + '/' + psffile):
            #print objid, 'PSF OK'
	    pass
        else:
            print objid, 'PSF NOT FOUND'
            

    if 'check' not in argv:
        print """
        if [ -e "psField/%s" ]; then
           echo "This file already exists!"
        else
           echo "Downloading %s"
        %s
        fi
        """ % (psffile, psfurl, psfwgetcmd + psfurl)



        
    for filter in filtros:
        imgurl = 'http://das.sdss.org/imaging/%d/%d/corr/%d/fpC-%06d-%c%d-%04d.fit.gz' % \
                  (run,rerun,camcol,run,filter,camcol,field)

        imgfile = 'fpC-%06d-%c%d-%04d.fit.gz' % (run,filter,camcol,field)
        imgdir = 'sdss_' + filter 
        imgwgetcmd = 'wget -r -q -nd --directory-prefix=%s  ' %  imgdir


        if 'check' in argv:
            if os.path.isfile(imgdir + '/' + imgfile):
                #print objid, 'OK'
                pass
            else:
                print objid, 'NOT FOUND'


        if 'check' not in argv:
            print """
            if [ -e "%s/%s" ]; then
               echo "This file already exists!"
            else
               echo "Downloading %s"
            %s
            fi
            """ % (imgdir, imgfile, imgurl, imgwgetcmd + imgurl)



if 'check' in argv:
   print 'if you SAW NOTHING then all files are there' 
