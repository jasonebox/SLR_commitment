RCM=RACMO
ver=2.3p2

RCM=MAR
ver=3.10

/bin/rm -R /tmp/G${RCM}
 
wc -l /Users/jason/Dropbox/${RCM}/ancil/lon.csv
wc -l /Volumes/2Tb/${RCM}${ver}/txt/1999/1999_001.txt

cd /Users/jason/Dropbox/${RCM}/prog

# /usr/bin/env -i HOME=/Users/jeb PATH=/usr/bin:/bin:/usr/sbin:/etc:/usr/lib /Applications/GRASS-7.6.app/Contents/MacOS/Grass.sh -text -c EPSG:3413 ./G

# grass -text -c EPSG:3413 /tmp/G${RCM}

RCM=RACMO
ver=2.3p2

RCM=MAR
ver=3.10

paste -d"|" /Users/jason/Dropbox/${RCM}/ancil/lon.csv /Users/jason/Dropbox/${RCM}/ancil/lat.csv | m.proj -i input=- | cut -d"|" -f1,2 > /Users/jason/Dropbox/${RCM}/ancil/xy.txt

wc -l /Users/jason/Dropbox/${RCM}/ancil/xy.txt

g.mapset PERMANENT

eval $(paste -d"|" /Users/jason/Dropbox/${RCM}/ancil/xy.txt /Users/jason/Dropbox/${RCM}/ancil/xy.txt | r.in.xyz -sg input=-) # set e,w,n,s variables in the shell
g.region e=$e w=$w s=$s n=$n                             # set bounds in GRASS
g.region res=1000 -pal                                    # set resolution and print
g.region -s                                              # save as default region

paste -d"|" /Users/jason/Dropbox/${RCM}/ancil/xy.txt /Volumes/2Tb/${RCM}${ver}/txt/1999/1999_001.txt | r.in.xyz --q input=- output=tmp --o
r.null map=tmp null=0
r.clump input=tmp output=clumps --o

# ocean_clump_ID=$(r.stats -c clumps sort=desc | head -n1 | cut -d" " -f1) 


cat << EOF > /Users/jason/Dropbox/${RCM}/ancil/filter.txt
TITLE     See r.mfilter manual
    MATRIX    3
    1 1 1
    1 1 1
    1 1 1
    DIVISOR   0
    TYPE      P
EOF

# workingpath=/media/jeb/ice/Jason/MAR/regrid_txt
# cd ${workingpath}
# cat << EOF > ${workingpath}/filter.txt
# TITLE     See r.mfilter manual
#     MATRIX    5
#     1 1 1 1 1
#     1 1 1 1 1
#     1 1 1 1 1
#     1 1 1 1 1
#     1 1 1 1 1
#     DIVISOR   25
#     TYPE      P
# EOF

g.region -d  # use default resolution
# r.mask -r

workingpath=/Volumes/2Tb/${RCM}${ver}/txt
# workingpath=/Users/jason/0_dat/MAR3.10/txt
cd ${workingpath}

for year in $(seq -w 1999 2004) 
do
echo $year
outpath=/Users/jason/0_dat/${RCM}${ver}/tif/${year}
outpath=/Volumes/2Tb/${RCM}${ver}/tif/${year}
mkdir -p ${outpath}

for d in $(ls ./${year}/*.txt) ; do
outname=$(basename ${d}).tif
# /bin/rm ${outpath}/${outname}
## 		echo $d #$(date)
## 		ls -lF ./${year}/${d}
## 		head ./${year}/${d}
infile=${d}
# ls -lF ${infile}
# wc -l ${infile}

# echo ${infile}
paste -d"|" /Users/jason/Dropbox/${RCM}/ancil/xy.txt  ${infile} | r.in.xyz --q input=- output=tmp type=DCELL --o
# r.null map=tmp setnull=0

r.mfilter -z input=tmp output=tmp_fill filter=/Users/jason/Dropbox/${RCM}/ancil/filter.txt --o
# r.mapcalc "tmp_fill_2 = if(clumps == ${ocean_clump_ID}, null(), tmp_fill)" --o

# r.resamp.interp input=tmp_fill output=tmp3 method=bilinear --o #method=nearest --o
r.resample input=tmp_fill output=tmp3 --o #method=nearest --o
outname=$(basename ${d} .txt).tif
# r.mapcalc "tmp3 = tmp3 / 10000." --o
r.out.gdal -cfm input=tmp3 output=${outpath}/${outname} type=Float32 createopt="COMPRESS=DEFLATE" --o
ls -lF ${outpath}/${outname}
done

done



