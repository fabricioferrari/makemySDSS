#!/usr/bin/python
"""
   Then run theh query to select run,rerun,camcol,field and row,column for the filter

   FOR EXAMPLE
   Upload the table with OBJID of all field galaxies to CASJOBS casjobs.sdss.org
   in a table named Berlind_FIELD with the var name SDSS_ID

   
SELECT 
    G.objID, G.ra, G.dec, G.run, G.rerun, G.camcol, G.field,  G.colc_i, G.ro
FROM
    Galaxy as G, mydb.Berlind_FIELD as F
WHERE
    G.ObjID = F.SDSS_ID


#OBJID                   ra             dec             run    rerun   camcol  field   colc_i           rowc_i         petroRad_i
587722952230174996      236.24709547    -0.4752636      745     40      2       518     1513.816        311.6018        5.005875
587722952230175138      236.34218191    -0.46702283     745     40      2       518     1588.999        1176.786        7.268567
587722952230175145      236.35012242    -0.59823729     745     40      2       518     395.674         1248.519        5.768068
587722952230240617      236.39732174    -0.49345701     745     40      2       519     1348.735        317.2708        9.04242
...
"""


# how many Petrosian Radii to cut the stamp
SIZERP = 5


import pylab as pl
import numpy as np
import pyfits
import os
from sys import argv
from astLib import astWCS, astImages




PIXELSZ = 0.396 # arcsec/pix

if len(argv) < 3:
    print """

    makemySTAMPS LISTA FILTRO[s]

         where LISTA is
         objid,ra,dec,run,rerun,camcol,field, col, row, petroRAD

         NOTE: column, row and petroRAD refers to the specified filter
         
         """
    exit()



filtro = argv[2]
listfile = open(argv[1],'r')


stampdir = 'stamps_' + str(filtro)
if not os.path.isdir(stampdir):
    os.mkdir(stampdir)

for xx in listfile.readlines():
    objid,ra,dec,run,rerun,camcol,field,col,row,Rp =xx.split(',')

    try:
        objid  = int(objid)
        ra     = float(ra)
        dec    = float(dec)
        run    = int(run)
        rerun  = int(rerun)
        camcol = int(camcol)
        field  = int(field)
        x0     = int(round(float(col)))
        y0     = int(round(float(row)))
        Rp     = float(Rp)
    except:
        print 'err'
        continue

    print objid

    framefile = 'fpC-%06d-%c%d-%04d.fit.gz' % (run,filtro,camcol,field)
    framedir = 'sdss_' + filtro


    if not os.path.isfile(framedir + '/' + framefile):
        print 'FILE NOT FOUND:', framedir + '/' + framefile 
        continue

    
    print 'extracting:', objid, run,rerun,camcol, field, '  at  pixels ', x0,y0 
    frame,framehdr  = pyfits.getdata(framedir + '/' + framefile, header=1)

    wcs = astWCS.WCS(framedir + '/' + framefile)


    # stamp size in degrees
    Ddeg  = SIZERP * Rp / 3600.

    try:
        stamp = astImages.clipImageSectionWCS(frame,wcs, ra , dec, Ddeg)
        print stamp['clippedSection']

        print stampdir + '/' + str(objid) + '_' + str(filtro) + '.fits'
        astImages.saveFITS( stampdir + '/' + str(objid) + '_' + str(filtro) + '.fits', stamp['data'], stamp['wcs'])
    except:
        pass

    #stamp = image[y0-Dpix:y0+Dpix, x0-Dpix:x0+Dpix]
    #pyfits.writeto(stampdir + '/' + str(objid) + '_' + str(filtro) + '.fits', stamp, clobber=1)

    
