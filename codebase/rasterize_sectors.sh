# /usr/bin/env -i HOME=/Users/jeb PATH=/usr/bin:/bin:/usr/sbin:/etc:/usr/lib /Applications/GRASS-7.6.app/Contents/MacOS/Grass.sh -text -c EPSG:3413 ./G

# grass -c EPSG:3413 ./G

# import
fn=/Users/jason/Dropbox/ELA/ancil/mouginot/Mouginot_2019/Greenland_Basins_PS_v1.4.2.shp
fn=/Users/jason/Dropbox/ELA/ancil/mouginot/ICECAPS/Mouginot_2019_Islands/islands.shp
v.in.ogr input=${fn} output=M --o
g.region vector=M res=100 -pa

v.info map=M
db.tables

# extract islands to raster
# v.to.rast input=M output=M where='(NAME == "ICE_CAPS_NO") | (NAME == "ICE_CAPS_NW") | (NAME == "ICE_CAPS_NE") | (NAME == "ICE_CAPS_SE") | (NAME == "ICE_CAPS_SW") | (NAME == "ICE_CAPS_CW") | (NAME == "ICE_CAPS_CE")' use=val value=1 --o

# v.to.rast input=M output=M where='(NAME != "ICE_CAPS_NO") | (NAME != "ICE_CAPS_NW") | (NAME != "ICE_CAPS_NE") | (NAME != "ICE_CAPS_SE") | (NAME != "ICE_CAPS_SW") | (NAME != "ICE_CAPS_CW") | (NAME != "ICE_CAPS_CE")' use=val value=1 --o


# v.to.rast input=M output=M2 where='(NAME=="UMIAMMAKKU_ISBRAE") | (NAME=="GEIKIE_UNNAMED_VESTFORD_S") | (NAME=="RINK_ISBRAE") | (NAME=="KANGERLUSSUUP_SERMERSUA") | (NAME=="CW_NONAME3") | (NAME=="SERMEQ_SILARLEQ") | (NAME=="CW_NONAME2") | (NAME=="LILLE_GLETSCHER") | (NAME=="STORE_GLETSCHER") | (NAME=="SERMEQ_AVANNARLEQ2") | (NAME=="USULLUUP_SERMIA") | (NAME=="INUPPAAT_QUUAT") | (NAME=="KANGILINNGUATA_SERMIA") | (NAME=="NARSAP_SERMIA") | (NAME=="AKULLERSUUP-QAMANAARSUUP") | (NAME=="KANGIATA_NUNAATA_SERMIA") | (NAME=="SW_NONAME1") | (NAME=="SERMEQ-KANGAASARSUUP") | (NAME=="AVANNARLEQ-NIGERLIKASIK") | (NAME=="SERMILIGAARSSUK_BRAE") | (NAME=="QAJUUTTAP_SERMIA") | (NAME=="KIATTUUT-QOOQQUP") | (NAME=="INNGIA_ISBRAE") | (NAME=="NW_NONAME1") | (NAME=="UPERNAVIK_ISSTROM_SS") | (NAME=="NUNATAKASSAAP_SERMIA") | (NAME=="KAKIVFAAT_SERMIAT") | (NAME=="QEQERTARSUUP_SERMIA") | (NAME=="USSING_BRAEER") | (NAME=="USSING_BRAEER_N") | (NAME=="CORNELL_GLETSCHER") | (NAME=="ILLULLIP_SERMIA") | (NAME=="ALISON_GLETSCHER") | (NAME=="HAYES_GLETSCHER_M_SS") | (NAME=="KJER_GLETSCHER") | (NAME=="SVERDRUP_GLETSCHER") | (NAME=="NANSEN_GLETSCHER") | (NAME=="STEENSTRUP-DIETRICHSON") | (NAME=="STORM") | (NAME=="SAQQAP-MAJORQAQ-SOUTHTERRUSSEL_SOUTHQUARUSSEL") | (NAME=="NORDENSKIOLD_GLESCHER_NW") | (NAME=="NONAME_NORTH_OSCAR") | (NAME=="ISSUUARSUIT_SERMIA") | (NAME=="RINK_GLETSCHER") | (NAME=="CARLOS") | (NAME=="LEIDY-MARIE-SERMIARSUPALUK") | (NAME=="HEILPRIN_GLETSCHER") | (NAME=="TRACY_GLETSCHER") | (NAME=="HARALD_MOLTKE_BRAE") | (NAME=="HUMBOLDT_GLETSCHER") | (NAME=="NO_NONAME1") | (NAME=="NEWMAN_BUGT") | (NAME=="RYDER_GLETSCHER") | (NAME=="NO_NONAME2") | (NAME=="MARIE_SOPHIE_GLETSCHER") | (NAME=="ACADEMY") | (NAME=="NO_NONAME3") | (NAME=="NIOGHALVFJERDSFJORDEN") | (NAME=="ZACHARIAE_ISSTROM") | (NAME=="DAUGAARD-JENSEN") | (NAME=="EIELSON_HARE_FJORD-ROLIGE") | (NAME=="UNNAMED_KANGER_W") | (NAME=="HELHEIMGLETSCHER") | (NAME=="IKERTIVAQ_NN") | (NAME=="MOGENS_HEINESEN_S") | (NAME=="NAPASORSUAQ_C_S") | (NAME=="KOGE_BUGT_SS") | (NAME=="KOGE_BUGT_N") | (NAME=="UKAASORSUAQ") | (NAME=="FREDERIKSHABS-NAKKAASORSUAQ") | (NAME=="ISUNNGUATA-RUSSELL") | (NAME=="EQIP_SERMIA") | (NAME=="SE_NONAME2") | (NAME=="KONG_CHRISTIAN") | (NAME=="SORGENFRI") | (NAME=="VESTFJORD") | (NAME=="JUNGERSEN_HENSON_NARAVANA") | (NAME=="DOCKER_SMITH_GLETSCHER") | (NAME=="SE_NONAME4") | (NAME=="TINGMIARMIUT_FJORD") | (NAME=="SERMEQ_KUJALLEQ") | (NAME=="KANGILERNGATA_SERMIA") | (NAME=="GRAULV") | (NAME=="OSTENFELD_GLETSCHER") | (NAME=="KANGERLUARSUUP_SERMIA") | (NAME=="UPERNAVIK_ISSTROM_N") | (NAME=="WORDIE-VIBEKE") | (NAME=="SE_NONAME1") | (NAME=="SE_NONAME5") | (NAME=="SE_NONAME6") | (NAME=="SE_NONAME7") | (NAME=="SE_NONAME8") | (NAME=="FENRISGLETSCHER") | (NAME=="MIDGARDGLETSCHER") | (NAME=="UNNAMED_DECEPTION_O_CN_CS") | (NAME=="KIV_STEENSTRUP_NODRE_BRAE") | (NAME=="UNNAMED_KANGER_E") | (NAME=="MAGGA_DAN_GLETSCHER") | (NAME=="GEIKIE1") | (NAME=="FREDERIKSBORG_GLETSCHER") | (NAME=="UNNAMED_SORGENFRI_W") | (NAME=="KANGERLUSSUAQ") | (NAME=="FARQUHAR_GLETSCHER") | (NAME=="MELVILLE_GLETSCHER") | (NAME=="SHARP") | (NAME=="KOGE_BUGT_C") | (NAME=="PUISORTOQ_N") | (NAME=="MOGENS_HEINESEN_SS_SSS") | (NAME=="HARDER_GLETSCHER") | (NAME=="UNNAMED_SOUTH_DANELL_FJORD") | (NAME=="SOUTHERN_TIP") | (NAME=="HERLUF_TROLLE-KANGERLULUK-DANELL") | (NAME=="UNNAMED_KANGERLULUK") | (NAME=="UNNAMED_HERLUF_TROLLE_S") | (NAME=="UNNAMED_HERLUF_TROLLE_N") | (NAME=="UNNAMED_ANORITUUP_KANGERLUA_SS") | (NAME=="ANORITUUP_KANGERLUA") | (NAME=="UNNAMED_ANORITUUP_KANGERLUA_S") | (NAME=="SE_NONAME9") | (NAME=="UNNAMED_DANELL_FJORD") | (NAME=="MAELKEVEJEN") | (NAME=="UNNAMED_LAUBE_S") | (NAME=="LAUBE_GLETSCHER") | (NAME=="UNNAMED_POLARIC_S") | (NAME=="HEIMDAL_GLETSCHER") | (NAME=="SKINFAXE") | (NAME=="KONG_OSCAR_GLETSCHER") | (NAME=="FIMBULGETLSCHER") | (NAME=="BLSEBR_GAMMEL_HELLERUP_GLETSJER") | (NAME=="QAJUUTTAP_SERMIA_N") | (NAME=="SIORALIK-ARSUK-QIPISAQQU") | (NAME=="SERMILIK") | (NAME=="ILORLIIT-SERMINNGUAQ") | (NAME=="EQALORUTSIT_KILLIIT_SERMIAT") | (NAME=="QALERALLIT_SERMIAT") | (NAME=="NAAJAT_SERMIAT") | (NAME=="AVANNARLEQ_N") | (NAME=="ADOLF_HOEL") | (NAME=="WALTERSHAUSEN") | (NAME=="GERARD_DE_GEER") | (NAME=="JAETTEGLETSCHER") | (NAME=="NORDENSKIOLD_NE") | (NAME=="PASSAGE_CHARPENTIER_GLETSCHER") | (NAME=="HISINGER_GLETSCHER") | (NAME=="WAHLENBERG_VIOLINGLETSJER") | (NAME=="STEENSBY_GLETSCHER") | (NAME=="GADE-MORELL") | (NAME=="DOCKER_SMITH_GLETSCHER_W") | (NAME=="GEIKIE4") | (NAME=="ROSENBORG") | (NAME=="KRONBORG") | (NAME=="BORGGRAVEN") | (NAME=="SYDBR") | (NAME=="BREDEGLETSJER") | (NAME=="GEIKIE2") | (NAME=="GEIKIE3") | (NAME=="GEIKIE6") | (NAME=="DENDRITGLETSCHER") | (NAME=="SHARP_W") | (NAME=="HART") | (NAME=="HART_W") | (NAME=="HUBBARD") | (NAME=="GABLE_MIRROR") | (NAME=="BOWDOIN") | (NAME=="SUN") | (NAME=="SUN_W") | (NAME=="VERHOEFF") | (NAME=="VERHOEFF_W") | (NAME=="MEEHAN") | (NAME=="MEEHAN_W") | (NAME=="SIORARSUAQ") | (NAME=="MORRIS_JESUP") | (NAME=="MORRIS_JESUP_W") | (NAME=="DIEBITSCH") | (NAME=="BAMSE") | (NAME=="DODGE") | (NAME=="SAVISSUAQ_UNNAMED1") | (NAME=="SAVISSUAQ_WWWWW") | (NAME=="SAVISSUAQ_UNNAMED2") | (NAME=="NW_NONAME2") | (NAME=="PITUGFIK") | (NAME=="SAVISSUAQ_UNNAMED3") | (NAME=="SAVISSUAQ_WWWW") | (NAME=="SAVISSUAQ_UNNAMED4") | (NAME=="SAVISSUAQ") | (NAME=="NONAME_IKERTIVAQ_N") | (NAME=="APUSEERAJIK") | (NAME=="NONAME_IKERTIVAQ_S") | (NAME=="KOGE_BUGT_S") | (NAME=="UMIIVIK_FJORD") | (NAME=="APUSEERSERPIA") | (NAME=="GYLDENLOVE") | (NAME=="RIMFAXE") | (NAME=="SAVISSUAQ-HELLAND-YNGVAR_NIELSEN-MOHN-CARLOS") | (NAME=="YNGVAR_NIELSEN_BRAE_W") | (NAME=="HELLAND") | (NAME=="YNGVAR_NIELSEN_BRAE") | (NAME=="MOHN_GLETSJER") | (NAME=="HEIM_GLETSCHER") | (NAME=="BRCKNER_GLETSCHER") | (NAME=="SE_NONAME10") | (NAME=="BUSSEMAND") | (NAME=="F_GRAAE") | (NAME=="CHARCOT") | (NAME=="GEIKIE5") | (NAME=="SORTEBRAE") | (NAME=="UPERNAVIK_ISSTROM_C") | (NAME=="UPERNAVIK_ISSTROM_S") | (NAME=="PUISORTOQ_S") | (NAME=="NAPASORSUAQ_N") | (NAME=="IKERTIVAQ_N") | (NAME=="IKERTIVAQ_M") | (NAME=="IKERTIVAQ_S") | (NAME=="HAYES_GLETSCHER_N_NN") | (NAME=="BRIKKERNE_GLETSCHER") | (NAME=="HAGEN_BRAE") | (NAME=="NE_NONAME1") | (NAME=="JAKOBSHAVN_ISBRAE") | (NAME=="SAQQARLIUP_ALANGORLIUP") | (NAME=="NORDENSKIOLD_GLETSCHER") | (NAME=="CW_NONAME1") | (NAME=="SERMEQ_AVANNARLEQ") | (NAME=="PETERMANN_GLETSCHER") | (NAME=="PETERMANN_GLETSCHER_N") | (NAME=="TUGTO") | (NAME=="MOGENS_HEINESEN_C") | (NAME=="GYLDENLOVE_SS") | (NAME=="AP_BERNSTOFF_GLETSCHER") | (NAME=="GEIKIE7") | (NAME=="UNNAMED_POLARIC_C") | (NAME=="KIV_STEENSTRUP_SONDRE_BRAE") | (NAME=="GYLDENLOVE_S") | (NAME=="NW_NONAME3") | (NAME=="SAVISSUAQ_W") | (NAME=="SAVISSUAQ_WW") | (NAME=="NW_NONAME4") | (NAME=="SAVISSUAQ_WWW") | (NAME=="MOGENS_HEINESEN_N") | (NAME=="AB_DRACHMANN_GLETSCHER_L_BISTRUP_BRAE") | (NAME=="SORANERBRAEEN-EINAR_MIKKELSEN-HEINKEL-TVEGEGLETSCHER-PASTERZE") | (NAME=="STORSTROMMEN") | (NAME=="ADMIRALTY_TREFORK_KRUSBR_BORGJKEL_PONY") | (NAME=="UNNAMED_UUNARTIT_ISLANDS") | (NAME=="POLARIC-DECEPTION_O_N") | (NAME=="NORDFJORD") | (NAME=="STYRTE") | (NAME=="COURTAULD") | (NAME=="KOLVEGLETSJER") | (NAME=="UNNAMED_DECEPTION_N") | (NAME=="KRUUSE_FJORD") | (NAME=="GLACIERDEFRANCE") | (NAME=="KNUD-RASMUSSEN") | (NAME=="NIGERTULUUP_KATTILERTARPIA")' use=val value=1 --o


quote=\"
# name=JAKOBSHAVN_ISBRAE

# for name in PETERMANN_GLETSCHER JAKOBSHAVN_ISBRAE
# for name in UMIAMMAKKU_ISBRAE GEIKIE_UNNAMED_VESTFORD_S RINK_ISBRAE KANGERLUSSUUP_SERMERSUA CW_NONAME3 SERMEQ_SILARLEQ CW_NONAME2 LILLE_GLETSCHER STORE_GLETSCHER SERMEQ_AVANNARLEQ2 USULLUUP_SERMIA INUPPAAT_QUUAT KANGILINNGUATA_SERMIA NARSAP_SERMIA AKULLERSUUP-QAMANAARSUUP KANGIATA_NUNAATA_SERMIA SW_NONAME1 SERMEQ-KANGAASARSUUP AVANNARLEQ-NIGERLIKASIK SERMILIGAARSSUK_BRAE QAJUUTTAP_SERMIA KIATTUUT-QOOQQUP INNGIA_ISBRAE NW_NONAME1 UPERNAVIK_ISSTROM_SS NUNATAKASSAAP_SERMIA KAKIVFAAT_SERMIAT QEQERTARSUUP_SERMIA USSING_BRAEER USSING_BRAEER_N CORNELL_GLETSCHER ILLULLIP_SERMIA ALISON_GLETSCHER HAYES_GLETSCHER_M_SS KJER_GLETSCHER SVERDRUP_GLETSCHER NANSEN_GLETSCHER STEENSTRUP-DIETRICHSON STORM SAQQAP-MAJORQAQ-SOUTHTERRUSSEL_SOUTHQUARUSSEL NORDENSKIOLD_GLESCHER_NW NONAME_NORTH_OSCAR ISSUUARSUIT_SERMIA RINK_GLETSCHER CARLOS LEIDY-MARIE-SERMIARSUPALUK HEILPRIN_GLETSCHER TRACY_GLETSCHER HARALD_MOLTKE_BRAE HUMBOLDT_GLETSCHER NO_NONAME1 NEWMAN_BUGT RYDER_GLETSCHER NO_NONAME2 MARIE_SOPHIE_GLETSCHER ACADEMY NO_NONAME3 NIOGHALVFJERDSFJORDEN ZACHARIAE_ISSTROM DAUGAARD-JENSEN EIELSON_HARE_FJORD-ROLIGE UNNAMED_KANGER_W HELHEIMGLETSCHER IKERTIVAQ_NN MOGENS_HEINESEN_S NAPASORSUAQ_C_S KOGE_BUGT_SS KOGE_BUGT_N UKAASORSUAQ FREDERIKSHABS-NAKKAASORSUAQ ISUNNGUATA-RUSSELL EQIP_SERMIA SE_NONAME2 KONG_CHRISTIAN SORGENFRI VESTFJORD JUNGERSEN_HENSON_NARAVANA DOCKER_SMITH_GLETSCHER SE_NONAME4 TINGMIARMIUT_FJORD SERMEQ_KUJALLEQ KANGILERNGATA_SERMIA GRAULV OSTENFELD_GLETSCHER KANGERLUARSUUP_SERMIA UPERNAVIK_ISSTROM_N WORDIE-VIBEKE SE_NONAME1 SE_NONAME5 SE_NONAME6 SE_NONAME7 SE_NONAME8 FENRISGLETSCHER MIDGARDGLETSCHER UNNAMED_DECEPTION_O_CN_CS KIV_STEENSTRUP_NODRE_BRAE UNNAMED_KANGER_E MAGGA_DAN_GLETSCHER GEIKIE1 FREDERIKSBORG_GLETSCHER UNNAMED_SORGENFRI_W KANGERLUSSUAQ FARQUHAR_GLETSCHER MELVILLE_GLETSCHER SHARP KOGE_BUGT_C PUISORTOQ_N MOGENS_HEINESEN_SS_SSS HARDER_GLETSCHER UNNAMED_SOUTH_DANELL_FJORD SOUTHERN_TIP HERLUF_TROLLE-KANGERLULUK-DANELL UNNAMED_KANGERLULUK UNNAMED_HERLUF_TROLLE_S UNNAMED_HERLUF_TROLLE_N UNNAMED_ANORITUUP_KANGERLUA_SS ANORITUUP_KANGERLUA UNNAMED_ANORITUUP_KANGERLUA_S SE_NONAME9 UNNAMED_DANELL_FJORD MAELKEVEJEN UNNAMED_LAUBE_S LAUBE_GLETSCHER UNNAMED_POLARIC_S HEIMDAL_GLETSCHER SKINFAXE KONG_OSCAR_GLETSCHER FIMBULGETLSCHER BLSEBR_GAMMEL_HELLERUP_GLETSJER QAJUUTTAP_SERMIA_N SIORALIK-ARSUK-QIPISAQQU SERMILIK ILORLIIT-SERMINNGUAQ EQALORUTSIT_KILLIIT_SERMIAT QALERALLIT_SERMIAT NAAJAT_SERMIAT AVANNARLEQ_N ADOLF_HOEL WALTERSHAUSEN GERARD_DE_GEER JAETTEGLETSCHER NORDENSKIOLD_NE PASSAGE_CHARPENTIER_GLETSCHER HISINGER_GLETSCHER WAHLENBERG_VIOLINGLETSJER STEENSBY_GLETSCHER GADE-MORELL DOCKER_SMITH_GLETSCHER_W GEIKIE4 ROSENBORG KRONBORG BORGGRAVEN SYDBR BREDEGLETSJER GEIKIE2 GEIKIE3 GEIKIE6 DENDRITGLETSCHER HART HUBBARD GABLE_MIRROR BOWDOIN SUN VERHOEFF MEEHAN SIORARSUAQ MORRIS_JESUP MORRIS_JESUP_W DIEBITSCH BAMSE DODGE SAVISSUAQ_UNNAMED1 SAVISSUAQ_WWWWW SAVISSUAQ_UNNAMED2 NW_NONAME2 PITUGFIK SAVISSUAQ_UNNAMED3 SAVISSUAQ_WWWW SAVISSUAQ_UNNAMED4 SAVISSUAQ NONAME_IKERTIVAQ_N APUSEERAJIK NONAME_IKERTIVAQ_S KOGE_BUGT_S UMIIVIK_FJORD APUSEERSERPIA GYLDENLOVE RIMFAXE YNGVAR_NIELSEN_BRAE_W HELLAND YNGVAR_NIELSEN_BRAE MOHN_GLETSJER HEIM_GLETSCHER BRCKNER_GLETSCHER SE_NONAME10 BUSSEMAND F_GRAAE CHARCOT GEIKIE5 SORTEBRAE UPERNAVIK_ISSTROM_C UPERNAVIK_ISSTROM_S PUISORTOQ_S NAPASORSUAQ_N IKERTIVAQ_N IKERTIVAQ_M IKERTIVAQ_S HAYES_GLETSCHER_N_NN BRIKKERNE_GLETSCHER HAGEN_BRAE NE_NONAME1 JAKOBSHAVN_ISBRAE SAQQARLIUP_ALANGORLIUP NORDENSKIOLD_GLETSCHER CW_NONAME1 SERMEQ_AVANNARLEQ PETERMANN_GLETSCHER PETERMANN_GLETSCHER_N TUGTO MOGENS_HEINESEN_C GYLDENLOVE_SS AP_BERNSTOFF_GLETSCHER GEIKIE7 UNNAMED_POLARIC_C KIV_STEENSTRUP_SONDRE_BRAE GYLDENLOVE_S NW_NONAME3 SAVISSUAQ_W SAVISSUAQ_WW SAVISSUAQ_WWW MOGENS_HEINESEN_N AB_DRACHMANN_GLETSCHER_L_BISTRUP_BRAE SORANERBRAEEN-EINAR_MIKKELSEN-HEINKEL-TVEGEGLETSCHER-PASTERZE STORSTROMMEN ADMIRALTY_TREFORK_KRUSBR_BORGJKEL_PONY UNNAMED_UUNARTIT_ISLANDS POLARIC-DECEPTION_O_N NORDFJORD STYRTE COURTAULD KOLVEGLETSJER UNNAMED_DECEPTION_N KRUUSE_FJORD GLACIERDEFRANCE KNUD-RASMUSSEN NIGERTULUUP_KATTILERTARPIA 
# 246 non ice cap catchments

# for name in SHARP_W HART_W SUN_W VERHOEFF_W MEEHAN_W SAVISSUAQ-HELLAND-YNGVAR_NIELSEN-MOHN-CARLOS NW_NONAME4
# 7 non ice cap catchments

for name in 1 6 55 50 91 75 93 119 109 134 126 145 140 139 153 146 155 164 200 209 210 224 213 208 238 237 250 236 267 263 292 255 303 329 317 287 300 332 293 306 357 343 350 334 362 376 373 338 368 366 371 361 382 387 397 392 394 409 405 393 348 434 417 433 443 454 467 442 464 487 527 516 535 538 551 558 557 589 588 599 604 607 608 613 638 643 641 669 676 674 678 692 684 697 709 721 722 730 739 749 752 755 759 764 769 771 775 778 780 789 803 808 819 816 818 827 831 846 857 870 871 875 883 884 893 908 909 928 929 939 944 950 949 956 962 981 990 1002 996 1001 1034 1038 1044 1088 1093 1095 1105 1110 1108 1106 1113 1119 1120 1141 1147 1160 1155 1168 1179 1202 1203 1218 1221 1263 1274 1304 1302 1303 1318 1323 1324 1332 1335 1341 1347 1365 1366 1387 1390 1394 1395 1406 1418 1417 1445 1444 1456 1468 1470 1480 1534 1546 1550 1554 1555 1572 1585 1588 1591 1599 1598 1611 1634 1637 1648 1653 1655 1659 1689 1686 1706 1712 1715 1717 1720 1722 1732 1742 1753 1760 1761 1772 1781 1798 1797 1808 1834 
# 227 ice cap catchments area >= 30sq km

# for name in 19 14 28 41 58 61 73 85 103 86 107 108 112 120 125 129 157 179 205 204 214 215 225 223 235 241 233 
# 27 ice caps 10 - 30 km2, but somehow all on N region

# for name in 1 6 55 50 91 75 93 119 109 134 126 145 140 139 153 146 155 164 200 209 210 224 213 208 238 237 250 
# 27 non ice cap catchments
	do

# 	v.to.rast input=M output=M2 where='(NAME=='${quote}${name}${quote}')' use=val value=1 --o
	v.to.rast input=M output=M2 where='(cat_=='${quote}${name}${quote}')' use=val value=1 --o

	# clump raster (unique values = islands)
	# r.clump input=M2 output=clumps --o

	outpath=/Users/jason/Dropbox/ELA/ancil/mouginot/output/
	outpath=/Users/jason/0_dat/catchments/
	mkdir -p ${outpath}

	# name=Greenland_Basins_PS_v1.4.2_rasterized_by_JEB_2020
	# name=Mouginot_sectors_no_icecaps
	r.out.gdal -cfm input=M2 output=${outpath}IC_${name}.tif type=Float32 createopt="COMPRESS=DEFLATE" --o

done


# export vector group to folder
# v.out.ogr input=Mouginot_sectors_simple output=${outpath}/ format=ESRI_Shapefile --overwrite
