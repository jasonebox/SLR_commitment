/usr/bin/env -i HOME=/Users/jeb PATH=/usr/bin:/bin:/usr/sbin:/etc:/usr/lib /Applications/GRASS-7.6.app/Contents/MacOS/Grass.sh -text -c EPSG:3413 ./G

grass -c EPSG:3413 ./G

DATADIR=/Users/jason/Dropbox/ELA/ancil/mouginot/

# 226,SW,ICE_CAPS_SW,TW
# 227,NO,ICE_CAPS_NO,TW
# 228,NW,ICE_CAPS_NW,TW
# 229,NE,ICE_CAPS_NE,TW
# 230,CW,ICE_CAPS_CW,TW
# 256,CE,ICE_CAPS_CE,TW
# 260,SE,ICE_CAPS_SE,TW

# import
v.in.ogr input=${DATADIR}/Mouginot_2019/Greenland_Basins_PS_v1.4.2.shp output=M --o
g.region vector=M res=100 -pa

# extract islands to raster
v.to.rast input=M output=M where='(NAME == "ICE_CAPS_NO") | (NAME == "ICE_CAPS_NW") | (NAME == "ICE_CAPS_NE") | (NAME == "ICE_CAPS_SE") | (NAME == "ICE_CAPS_SW") | (NAME == "ICE_CAPS_CW") | (NAME == "ICE_CAPS_CE")' use=val value=1 --o

# clump raster (unique values = islands)
r.clump input=M output=clumps --o

# islands to vector
r.to.vect input=clumps output=islands type=area --o

# export vector group to folder
outpath=/Users/jason/Dropbox/ELA/ancil/mouginot/ICECAPS/Mouginot_2019_Islands
mkdir -p outpath
v.out.ogr input=islands output=${outpath} format=ESRI_Shapefile --overwrite

fn=/Users/jason/Dropbox/ELA/ancil/mouginot/ICECAPS/Mouginot_2019_Islands/islands.dbf
fn=/Users/jason/Dropbox/ELA/ancil/mouginot/ICECAPS/Mouginot_2019_Islands/islands.shp
v.import input=${fn} output=sectors_all --o

v.info map=sectors_all --o

db.select table=sectors_all | cat > ${outpath}/sectors.txt

v.vect.stats points=sectors_all areas=name -p


zip -r ~/Dropbox/out/islands.zip ./Mouginot_2019_Islands
dropbox sharelink ~/Dropbox/out/islands.zip | pbcopy
pbpaste
# https://www.dropbox.com/s/v48j9th0ykedyhx/islands.zip?dl=0
