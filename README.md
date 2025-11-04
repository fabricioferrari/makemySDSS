# makemySDSS
Cut  SDSS images stamps for a given listas of ObjIDs

--------------------------------------------------------
	makemySDSS suite 

For downloading SDSS Fields and generating PSF for them.


Fabricio Ferrari, www.ferrari.pro.br, 2013-2025
--------------------------------------------------------

NEEDS

- read_PSF executable from the SDSS 
(http://www.sdss.org/dr7/products/images/read_psf.html)

- astLib python library to transform WCS to PIXEL
(http://astlib.sourceforge.net)




HOWTO.

[1] INPUT

is list of objects (header optional), say named mysample.csv

#objidDR10,ra,dec,run,rerun,camcol,field,petroRad
1237651190281666763,126.187140409114,46.9071889705194,1331,301,2,148,23.83807
1237651190283043469,129.265168367017,49.3086669209961,1331,301,2,169,2.702712
1237651190283174242,129.495305982605,49.4856515513676,1331,301,2,171,3.757454
1237651190283174527,129.548809479637,49.4585025873575,1331,301,2,171,2.382144
1237651190283174530,129.570170366669,49.4502017215905,1331,301,2,171,2.969478
...



[2] IDENTIFYING UNIQUE SETUPS (run,rerun,camcol,field)

run the 1.makemySDSSunique.py  on it 

$   python 1.makemySDSSunique.py  mysample.csv > uniqueframes.csv



[3] Downloading files

run the 2.makemyGET.py script. It generates either WGET or RSYNC scripts. Usually you download the files 
with WGET and them ckeck for corrupted files with RSYNC. (WGET is faster in SDSS)

$ 2.makemyGET.py uniqueframes.csv r wget  > wget_download_script.sh




[4]. GENERATE STAMPS AND PSF

All files must be downloaded beforehand (see [3]).
Run the 3.makemySTAMPS.py script.

$  3.makemySTAMPS.py mysample.csv  uniqueframes.csv  band

It will extract the individual objects for each field and the corresponding psf. 
It will store the file in stamps_`band` and psf_`band`.

NOTES: - you may process only part of the frames identified in mysample.csv 
         (so you can split the whole process)
       - band is any of 'ugriz' (SDSS filters)
       - The stamps sizes are measure in object Petrosian Radius. 
         Check the header of makemySTAMPS.py 





F.Ferrari
[www.ferrari.pro.br] 2014
