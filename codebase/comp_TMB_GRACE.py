#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 14:10:15 2020

@author: Jason Box, GEUS, jeb@geus.dk

Illustrate total mass balance from this study relative to GRACE after Wouters et al and relative to IMBIE 2019...producing Fig S4. comparison of total mass balance from this study with independent satellite gravimetry

"""

ly='x'
do_gif=0

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from scipy import stats

fs=22
plt.rcParams['font.sans-serif'] = ['Georgia']
plt.rcParams["font.size"] = fs
plt.rcParams['axes.facecolor'] = 'w'
plt.rcParams['axes.edgecolor'] = 'k'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 1
plt.rcParams['grid.color'] = "#cccccc"
plt.rcParams["legend.facecolor"] ='w'
plt.rcParams["mathtext.default"]='regular'
x0=10
plt.rcParams["figure.figsize"] = [x0, x0/1.4]

type_choice_name=['TW_only','LT_only','TW_and_LT']
SMB_or_TMB='TMB'
versionx='20200320'
alb_devname=["lo","mid","hi"]
SID_devname=["0.9","1.0","1.1"]

cc=0
fns=['']*18
# ------------------------------------------------ loop over RCMs
RCM=['MAR','RACMO']
for mm in range(0,2):
# for mm in range(0,1):
# for mm in range(1,2):
    # ------------------------------------------------ loop over albedo uncertainty
    for alb_dev_index in range(0,3):
    # for alb_dev_index in range(1,2):
        # ------------------------------------------------ loop over SID uncertainty
        for SID_dev_index in range(0,3):
        # for SID_dev_index in range(1,2):
            # ------------------------------------------------ loop over volume treatments
            volume_name=['unscaled','scaled']
            # for volume_index in range(0,2):
            # for volume_index in range(1,2):
            for volume_index in range(0,1):

                fn='/Users/jason/Dropbox/ELA/stats/imbalance/TMB_annual_ALB'+alb_devname[alb_dev_index]+'_'+RCM[mm]+'_'+\
                volume_name[volume_index]+'_SID'+SID_devname[SID_dev_index]+\
                '_v'+versionx+'.csv'
                print(cc,fn)
                os.system('ls -lF '+fn)
                member = pd.read_csv(fn, delimiter=",")
                fns[cc]=fn
                cc+=1

    # break
print(cc)

cc=0
# os.system('ls -lF '+fns)
df1 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
df2 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
df3 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
df4 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
df5 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
df6 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1

df7 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
df8 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
df9 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
df10 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
df11 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
df12 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1

df13 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
df14 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
df15 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
df16 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
df17 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
df18 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1

# df19 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
# df20 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
# df21 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
# df22 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
# df23 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
# df24 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1

# df25 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
# df26 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
# df27 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
# df28 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
# df29 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
# df30 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1

# df31 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
# df32 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
# df33 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
# df34 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
# df35 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1
# df36 = pd.read_csv(fns[cc], delimiter=",") ; cc+=1

df_concat = pd.concat((df1,df2,df3,df4,df5,df6,\
                       df7,df8,df9,df10,df11,df12,\
                        df13,df14,df15,df16,df17,df18,\
                        # df19,df20,df21,df22,df23,df24,\
                        # df25,df26,df27,df28,df29,df30,\
                        # df31,df32,df33,df34,df35,df36,\
                           ))
    
by_row_index = df_concat.groupby(df_concat.index)
df_ensemble_count = by_row_index.count()
df_ensemble_count.to_csv('/Users/jason/Dropbox/ELA/stats/imbalance/TMB_annual_ensemble_count.csv', sep=',')

df_ensemble_min = by_row_index.min()
df_ensemble_min.to_csv('/Users/jason/Dropbox/ELA/stats/imbalance/TMB_annual_ensemble_min.csv', sep=',')
df_ensemble_max = by_row_index.max()
df_ensemble_max.to_csv('/Users/jason/Dropbox/ELA/stats/imbalance/TMB_annual_ensemble_max.csv', sep=',')
df_ensemble_std = by_row_index.std()
df_ensemble_std.to_csv('/Users/jason/Dropbox/ELA/stats/imbalance/TMB_annual_ensemble_std.csv', sep=',')
df_ensemble_mean = by_row_index.mean()
df_ensemble_mean.to_csv('/Users/jason/Dropbox/ELA/stats/imbalance/TMB_annual_ensemble_mean.csv', sep=',')

x=df_ensemble_mean.year
y=df_ensemble_mean.TMB

# ----------------------------------------------------------------------------------- IMBIE
fn='/Users/jason/Dropbox/imbie/imbie_dataset_greenland_dynamics-2020_02_28.xlsx'
imbie=pd.read_excel(fn)
print(imbie.columns)
imbie_GT=imbie["Rate of ice sheet mass change (Gt/yr)"]
imbie_year=imbie["Year"]

for i in range(2000,2020):
    print(i)
    

df = pd.DataFrame(columns=['year','TMB','TMB error'])
df["year"]=df_ensemble_mean.year
df["TMB"]=df_ensemble_mean.TMB
df["TMB error"]=df_ensemble_std.TMB
df.to_csv('/Users/jason/Dropbox/ELA/stats/imbalance/TMB_annual_ensemble_mean.csv', sep=',')
print(df)

fn='/Users/jason/Dropbox/AMAP/Arctic-multi-indicators/data_multi_indicators/glaciers/GrMB_2000-2019.txt'
GRACE=pd.read_csv(fn, delim_whitespace=True)
print(GRACE.columns)

co='gray'
co='k'
# co='g'


nstd=1.
plt.scatter(x,y, s=100, facecolor=co,linewidth=1,zorder=20,label='this study')
plt.errorbar(x,y,yerr=df_ensemble_std.TMB*nstd,color=co,zorder=5,fmt='none',linewidth=2)


(_, caps, _) = plt.errorbar(x,y,yerr=df_ensemble_std.TMB*nstd, capsize=8,color=co)
for cap in caps:
    cap.set_color(co)
    cap.set_markeredgewidth(1)
    
v=((GRACE.year>=2003)&(GRACE.year<=2019))
plt.fill_between(GRACE.year[v],GRACE.TMB[v]-GRACE.errx[v]*nstd,GRACE.TMB[v]+GRACE.errx[v]*nstd,label='GRACE after Wouters',color='C0')

print('mean GRACE',np.mean(GRACE.TMB[v]),np.mean(GRACE.errx[v])*nstd)
print('mean this study',np.mean(y[v]),np.mean(df_ensemble_std.TMB[v]))

v=((GRACE.year>=2003)&(GRACE.year<=2019))

statsx=stats.pearsonr(y[v], GRACE.TMB[v])
R=statsx
print("stats",statsx)
                
v=np.where((GRACE.year>=2018)&(GRACE.year<=2019))
# plt.plot(GRACE.year[v],GRACE.TMB[v],c='b',label='GRACE-FO',zorder=10)


plt.axhline(y=0., color='k', linestyle='--')

plt.scatter(imbie_year,imbie_GT,marker='|',s=200,c='m',label='IMBIE 2019',zorder=32)


plt.ylabel('Gt $y^{-1}$')
plt.legend()
# plt.xlabel(xtit)
# plt.ylim(-3100,3100)
# plt.ylim(-0.1,2)
# if by_area==0:plt.xlim(60,83.8)
#v=np.where(z=='SERMILIK')
#plt.plot(x[v],y[v],'ro')
# plt.title('specific '+varname2+', '+type_name)
# if by_area:plt.xscale('log')


# ax = plt.subplot(111)
#ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# props = dict(boxstyle='round', facecolor='w',edgecolor='grey',alpha=0.7)

# plt.text(0.55, 0.965,
#          # type_name+'\n'+
#          selection+'\n'+
#         period+'\nmean='+str("%8.0f"%meanx).lstrip()+'±'+str("%8.0f"%meanerr).lstrip()+' '+units+'\nN = '+\
#             str(N),
#         transform=ax.transAxes,color='k',
#         verticalalignment='top',
#         bbox=props,fontsize=fs*0.9)
# print(str("%8.0f"%meanx).lstrip()+'±'+str("%8.0f"%meanerr).lstrip())
# yx = [0,0] ; xx = [np.min(x),np.max(x)]
# plt.plot(xx, yx, color='grey',linewidth=2)

# plt.axhline(0, color="gray")
# xx = [np.min(x),np.max(x)] ; yx = [meanx,meanx]
# plt.plot(xx, yx,'--', color='r',linewidth=2,zorder=13)

 

fig_path='/Users/jason/Dropbox/ELA/Figs/'
os.system('mkdir -p '+fig_path)
if ly=='p':
    figname=fig_path+'=SMB_vs_TMB_'+\
            SMB_or_TMB+'_ALB'+alb_devname[alb_dev_index]+'_'+RCM[mm]+'_'+\
                volume_name[volume_index]+'_SID'+SID_devname[SID_dev_index]+'.png'
    plt.savefig(figname, bbox_inches='tight',dpi=250)#figsize=(200, 6))
    # os.system('open '+figname)
if ly == 'x': plt.show()
                  
if do_gif == 1:
    print("making .gif")
    os.system('/usr/local/bin/convert -delay 100 -loop 0 '+fig_path+'*.png '+fig_path+'anim_.gif')
