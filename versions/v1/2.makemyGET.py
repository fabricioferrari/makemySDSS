#!/usr/bin/python
"""
Generate the download list of frames and psfields for wget or rsync

"""

##### DATARELEASE #####
DR=10

# how many Petrosian Radii to cut the stamp
SIZERP = 4.


import makemySDSSlib as makemySDSS 
import pylab as pl
import numpy as np
import pyfits
import os
import time
from astLib import astWCS, astImages
from sys import argv,stderr


PIXELSZ   = 0.396 # arcsec/pix
FILTERNUM = {'u':1, 'g':2, 'r':3, 'i':4, 'z':5}


if len(argv) < 3:
    print """

    makemyGET  FRAMELIST  FILTER[s] wget/rsync 

         FRAMELIST is
         run,rerun,camcol,field

         and FILTER is any combinations of 'ugriz' 


         IF 'wget'  is on the command line generates the download script

         IF 'rsync' is on the command line, generates the file list to rsync

         
         """

    exit()



framefile = argv[1]
band      = argv[2]




objids  = []
ras     = []
decs    = []
runs    = []
reruns  = []
camcols = []
fields  = []
Rps     = []


stamprootdir = 'stamps_' + str(band)
if not os.path.isdir(stamprootdir):
    os.mkdir(stamprootdir)

psfrootdir = 'psf_' + str(band)
if not os.path.isdir(psfrootdir):
    os.mkdir(psfrootdir)


for xx in open(framefile, 'r'): 
    RN, RR, CC, FF  = xx.split(',')
    RN = int(RN)
    RR = int(RR)
    CC = int(CC)
    FF = int(FF)
    
    print '\n# RUN,RERUN,CAMCOL,FIELD', RN, RR, CC, FF

    frameurl      = makemySDSS.frameurl(RN, RR, CC, FF, band=band, DR=DR)
    framelocalbz2 = makemySDSS.frameurl(RN, RR, CC, FF, band=band, site=0, DR=DR)
    framelocal    = framelocalbz2.replace('.bz2', '')
    framedir      = 'frames_%s' % band  

    psFurl    = makemySDSS.psfurl(RN, RR, CC, FF, DR=DR)
    psFlocal  = makemySDSS.psfurl(RN, RR, CC, FF, site=0, DR=DR)
    psFdir    = 'psField'   

    if 'wget' not in argv and 'rsync' not in argv:
        print 'you MUST choose: wget or rsync!!!\n\n\n'


    if 'wget' in argv:
        wgetcmd1 = 'wget -r -c -nd --directory-prefix=%s  '%(framedir)  + frameurl
        wgetcmd2 = 'wget -r -c -nd --directory-prefix=%s  '%(psFdir)    + psFurl
        print wgetcmd1
        print wgetcmd2
    elif 'rsync' in argv:
        frameurl = frameurl.replace('http', 'rsync')
        frameurl = frameurl.replace('sas/','')
        rsynccmd1 = 'rsync --no-motd -vau ' + frameurl + ' ./' + framedir + '/'

        psFurl = psFurl.replace('http', 'rsync')
        psFurl = psFurl.replace('sas/','')
        rsynccmd2 = 'rsync --no-motd -vau ' + psFurl + ' ./' + psFdir + '/'

        print rsynccmd1
        print rsynccmd2



