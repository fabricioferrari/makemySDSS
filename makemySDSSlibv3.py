"""
http://data.sdss.org/sas/dr10/boss/photoObj/frames/[rerun]/[run]/[camcol]/frame-[band]-[run6]-[camcol]-[field].fits.bz2


PSF

$PHOTO_REDUX/RERUN/RUN/objcs/CAMCOL

http://mirror.sdss3.org/sas/dr10/env/PHOTO_REDUX/RERUN/RUN/objcs/CAMCOL/psField-RRRRRR-C-FFFF.fit

RERUN is RERUN
RRRRRR is RUN
C CAMCOL
FFFF  FIELD
"""




def frameurl(run, rerun, camcol, field, band='r', file=True, site=True, DR=10):

    if DR==10:
        imgsite = 'http://data.sdss.org/sas/dr10/boss/photoObj/frames/%d/%d/%d/' % (rerun, run, camcol)
        imgfile = 'frame-%c-%06d-%d-%04d.fits.bz2' % (band, run, camcol, field)
    elif DR==7:
        imgsite = 'http://das.sdss.org/imaging/%d/%d/corr/%d/' % (run,rerun,camcol)
        imgfile = 'fpC-%06d-%c%d-%04d.fit.gz' % (run,band,camcol,field)

    if file and site:
        return imgsite+imgfile
    elif file and ~site:
        return imgfile
    elif site and ~file:
        return imgsite






def psfurl(run, rerun, camcol, field, file=True, site=True, DR=10):

    if DR==10:
        psfsite = 'http://data.sdss.org/sas/dr10/env/PHOTO_REDUX/%d/%d/objcs/%d/' % (rerun,run,camcol)
        psffile = 'psField-%06d-%d-%04d.fit' % (run,camcol,field)
    elif DR==7:
        #http://das.sdss.org/imaging/%d/%d/objcs/%d/psPlan-%06d-%d-%04d.fit 	run, rerun, camcol, run, camcol, field
        psfsite = 'http://das.sdss.org/imaging/%d/%d/objcs/%d/' % (run,rerun,camcol)
        psffile = 'psField-%06d-%d-%04d.fit' % (run,camcol,field)

    if file and site:
        return psfsite+psffile
    elif file and ~site:
        return psffile
    elif site and ~file:
        return psfsite

