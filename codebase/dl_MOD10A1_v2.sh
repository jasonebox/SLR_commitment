#!/bin/sh

# https://earthdata.nasa.gov/earth-observation-data/near-real-time/download-nrt-data/modis-nrt#ed-modis-terra-c6
# l: jasonbox
# p: a.A.6_6_a


touch ~/.netrc
echo "machine urs.earthdata.nasa.gov login jasonbox password a.A.6_6_a" > ~/.netrc
chmod 0600 ~/.netrc
touch ~/.urs_cookies


dummy=gg

for collection in 6
#for year in 2016
do

dl_path=/Volumes/Ice/Jason/MOD10A1/HDF/6/
dl_path=/users/jason/0_dat/MOD10A1/HDF/${collection}/
#dl_path=/Volumes/Ice/Jason/HDF/${collection}/
#for year in 2000 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016

#for year in 2000 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2015 2016 2017
for year in 2020
# for year in 2000 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 2014 2015 2016 2017
# for year in $(seq -w 2000 2017)

do
mkdir -p ${dl_path}${year}
    cd ${dl_path}${year}


#     for month in 05 06 07 08 09
# for month in 01 02 11 12
    for month in 07
    do
#            for day in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31
#    for day in 27 28 29 30 31
    for day in 01 02 03 04 05 06 07 08 09 10 11

        do
            echo ${year}${month}${day}
echo https://n5eil01u.ecs.nsidc.org/MOST/MOD10A1.00${collection}/${year}.${month}.${day}/

rm -f /tmp/${dummy}1.txt > /dev/null
rm -f /tmp/${dummy}2.txt > /dev/null
	curl -b ~/.urs_cookies -c ~/.urs_cookies -L -n https://n5eil01u.ecs.nsidc.org/MOST/MOD10A1.00${collection}/${year}.${month}.${day}/ -o /tmp/${dummy}1.txt

  cat /tmp/${dummy}1.txt | grep -v 'xml$' | grep -v 'jpg$' | grep 'h15v01' >> /tmp/${dummy}2.txt
  cat /tmp/${dummy}1.txt | grep -v 'xml$' | grep -v 'jpg$' | grep 'h15v02' >> /tmp/${dummy}2.txt
  cat /tmp/${dummy}1.txt | grep -v 'xml$' | grep -v 'jpg$' | grep 'h16v00' >> /tmp/${dummy}2.txt
  cat /tmp/${dummy}1.txt | grep -v 'xml$' | grep -v 'jpg$' | grep 'h16v01' >> /tmp/${dummy}2.txt
  cat /tmp/${dummy}1.txt | grep -v 'xml$' | grep -v 'jpg$' | grep 'h16v02' >> /tmp/${dummy}2.txt
  cat /tmp/${dummy}1.txt | grep -v 'xml$' | grep -v 'jpg$' | grep 'h17v00' >> /tmp/${dummy}2.txt
  cat /tmp/${dummy}1.txt | grep -v 'xml$' | grep -v 'jpg$' | grep 'h17v01' >> /tmp/${dummy}2.txt
  cat /tmp/${dummy}1.txt | grep -v 'xml$' | grep -v 'jpg$' | grep 'h17v02' >> /tmp/${dummy}2.txt

    	    cat /tmp/${dummy}2.txt | grep h15 > /tmp/${dummy}3.txt
    	    cat /tmp/${dummy}2.txt | grep h16 >> /tmp/${dummy}3.txt
    	    cat /tmp/${dummy}2.txt | grep h17 >> /tmp/${dummy}3.txt
    	    cat /tmp/${dummy}3.txt | grep 'hdf"' > /tmp/${dummy}4.txt
			# cat /tmp/${dummy}3.txt
    	    # cat /tmp/${dummy}2.txt | grep '18"'> /tmp/${dummy}3.txt

#  	    cat /tmp/${dummy}3.txt | cut -c 54-98 >/tmp/${dummy}4.txt
# 	    cat /tmp/${dummy}3.txt | cut -c 55-99 >/tmp/${dummy}4.txt
    	cat /tmp/${dummy}4.txt |cut -d"<" -f4 | cut -d'"' -f2 >/tmp/${dummy}5.txt
    	    while read LINE
    	    
    	    do
    	    	echo
    	    	echo
    	    	echo ${LINE}


wget --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies --no-check-certificate --auth-no-challenge=on -r --reject "index.html*" -np -e robots=off https://n5eil01u.ecs.nsidc.org/MOST/MOD10A1.00${collection}/${year}.${month}.${day}/${LINE}
#https://n5eil01u.ecs.nsidc.org/MOST/MOD10A1.006/2017.09.04/

/bin/mv ${dl_path}${year}/n5eil01u.ecs.nsidc.org/MOST/MOD10A1.006/${year}.${month}.${day}/${LINE} ${dl_path}/${year}/

            done < /tmp/${dummy}5.txt
        done
    done
  done
done