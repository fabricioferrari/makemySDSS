#!/usr/bin/python

import pylab as pl
import numpy as np
import os
from astLib  import astWCS

from sys import argv

if len(argv) < 3:
    print """

    makemyPSF LISTA FILTRO[s]

         where LISTA is
         objid,ra,dec,run,rerun,camcol,field
         """
    exit()

filtros = argv[2]
listfile = open(argv[1],'r')


filternum = {'u':1, 'g':2, 'r':3, 'i':4, 'z':5}

for xx in listfile.readlines():
    objid,ra,dec,run,rerun,camcol,field =xx.split(',')

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

    print objid

    psffile = 'photoField/photoField-%06d-%d.fits' % (field,camcol)
        

    for filter in filtros:
                
        imgdir = 'stamps_' + filter 
        imgfile = 'photoField-%06d-%d.fits' % (field,camcol)

        #DR10
        #'http://data.sdss3.org/sas/dr9/env/BOSS_PHOTOOBJ/301/4623/photoField-004623-1.fits'  rerun,field,field,camcol
        #
        #'http://data.sdss3.org/sas/dr9/env/BOSS_PHOTOOBJ/%d/%d/photoField-%06d-%d.fits'  % (rerun,field,field,camcol)

        


	try:
            wcs = astWCS.WCS(imgdir + '/' + imgfile)
            x,y = wcs.wcs2pix(ra,dec)
        except:
	   print 'wcs error'
	   x=100
	   y=100

        if not os.path.exists('psf_' + filter):
            os.mkdir('psf_' + filter)

        
        psfout = 'psf_' + filter + '/' +  str(objid) + '_' + str(filter) + '_' + 'psf.fits'


        if not os.path.isfile('read_PSF'):
            print '\n\n you NEED read_PSF executable from SDSS. Check\n\n \
            http://www.sdss.org/dr7/products/images/read_psf.html\n\n'
            exit()

            
        os.system ('./read_PSF %s  %i  %f %f  %s' % (psffile,   filternum[filter],  x ,y, psfout ) ) 
