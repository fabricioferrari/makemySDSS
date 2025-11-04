#!/usr/bin/python
"""
Generate the download list of frames and psfields for wget or rsync

"""

__version__ = 3.2


##### DATARELEASE #####
DR=10

# how many Petrosian Radii to cut the stamp
SIZERP = 4.


import makemySDSSlibv3 as makemySDSS 
import pylab as pl
import numpy as np
#import pyfits
import os
import time
#from astLib import astWCS, astImages
from sys import argv,stderr


PIXELSZ   = 0.396 # arcsec/pix
FILTERNUM = {'u':1, 'g':2, 'r':3, 'i':4, 'z':5}


if len(argv) < 3:
    print ("""

    makemyGET  FRAMELIST  FILTER[s] wget/rsync 

         FRAMELIST is
         run,rerun,camcol,field

         and FILTER is any combinations of 'ugriz' 


         IF 'wget'  is on the command line generates the download script

         IF 'rsync' is on the command line, generates the file list to rsync


         >>>>>   IF 'test' is on the command line, put test of file existnace in output
         
         """)

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
    
    print ('\n# RUN,RERUN,CAMCOL,FIELD', RN, RR, CC, FF)

    frameurl      = makemySDSS.frameurl(RN, RR, CC, FF, band=band, DR=DR)
    framelocalbz2 = makemySDSS.frameurl(RN, RR, CC, FF, band=band, site=0, DR=DR)
    framelocal    = framelocalbz2.replace('.bz2', '')
    framedir      = 'frames_%s' % band  

    psFurl    = makemySDSS.psfurl(RN, RR, CC, FF, DR=DR)
    psFlocal  = makemySDSS.psfurl(RN, RR, CC, FF, site=0, DR=DR)
    psFdir    = 'psField'   

    if 'wget' not in argv and 'rsync' not in argv:
        print ('you MUST choose: wget or rsync!!!\n\n\n')


    # command to test if file already exist
    testcmdV1 = 'test ! -e  %s/'%(framedir)  + framelocalbz2 + ' && ' 
    testcmdF1 = ' || echo %s already downloaded' % framelocalbz2

    testcmdV2 = 'test ! -e  %s/'%(psFdir)  + psFlocal + ' && ' 
    testcmdF2 = ' || echo %s already downloaded' % psFlocal

    if 'wget' in argv:
        getcmd1 = 'wget -r -c -nd --directory-prefix=%s  '%(framedir)  + frameurl
        getcmd2 = 'wget -r -c -nd --directory-prefix=%s  '%(psFdir)    + psFurl


    elif 'rsync' in argv:
        frameurl = frameurl.replace('http', 'rsync')
        frameurl = frameurl.replace('sas/','')

        psFurl = psFurl.replace('http', 'rsync')
        psFurl = psFurl.replace('sas/','')

        getcmd1 = 'rsync --no-motd -vau ' + frameurl + ' ./' + framedir + '/'
        getcmd2 = 'rsync --no-motd -vau ' + psFurl + ' ./' + psFdir + '/'


    if 'test' in argv:
        print (testcmdV1, getcmd1, testcmdF1)
        print (testcmdV2, getcmd2, testcmdF2)
    else:
        print (getcmd1)
        print (getcmd2)



