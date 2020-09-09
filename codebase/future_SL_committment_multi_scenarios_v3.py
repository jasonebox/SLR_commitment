#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:10:13 2020

@author: Jason Box, GEUS, jeb@geus.dk

read in CMIP6 temperature projections for three scenarios and convert these to SLR commitment projections. Error envelopes are increased to twice the gradient by end of Century to offer a more conservative and realistic projection

preceded by /Users/jason/Dropbox/ELA/prog/SLR_committed.py

"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import locale
locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'
from numpy.polynomial.polynomial import polyfit

fs=30 # fontsize
th=1 # default line thickness
# plt.rcParams['font.sans-serif'] = ['Georgia']
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['axes.grid'] = False
plt.rcParams['grid.alpha'] = 1
plt.rcParams['grid.color'] = "grey"
plt.rcParams["font.size"] = fs
plt.rcParams['figure.figsize'] = 14, 13


gradient=230.25878907271235 # Each degree Celsius increase in summer air temperature drives a further 230±80 mm of SLR commitment
intercept=-17.040191866514792
fractional_fit_error=0.1971892983687014

fn='/Users/jason/Dropbox/CMIP6/ssp585.txt' # CMIP6 scenario years 1960 .. 2099 with columns as per below commented section
GCM=pd.read_csv(fn, delim_whitespace=True, skiprows=11)
# print(GCM.columns)
#      year count  TT_ANN  TT_ANN.1  TT_JJA  TT_JJA.1  PP_ANN  PP_ANN.1
# 0    1960    1:   252.7     2.321   266.2     1.981   430.1      65.8
# 1    1961    2:   252.6     2.032   266.2     2.200   434.3      53.3
# 2    1962    3:   252.4     2.287   266.3     1.917   422.5      77.5
# 3    1963    4:   252.2     2.369   266.2     2.096   419.6      65.9
# 4    1964    5:   252.1     2.328   266.0     1.998   416.6      70.2
# ..    ...   ...     ...       ...     ...       ...     ...       ...
# 135  2095  136:   259.7     2.425   272.6     1.566   591.6      92.7
# 136  2096  137:   259.7     2.357   272.7     1.491   582.5     102.2
# 137  2097  138:   259.9     2.564   272.5     1.957   592.8      85.5
# 138  2098  139:   260.0     2.366   272.6     1.585   584.7     103.7
# 139  2099  140:   260.1     2.554   272.9     1.660   606.1      89.4

x=GCM["year"]
v=((GCM.year>=1981)&(GCM.year<=2010))

SSP585=GCM["TT_JJA"]-273.15
SSP585std=GCM["TT_JJA.1"]
SSP585-=np.mean(SSP585[v])

fn='/Users/jason/Dropbox/CMIP6/ssp245.txt' # CMIP6 scenario years 1960 .. 2099
GCM=pd.read_csv(fn, delim_whitespace=True, skiprows=11)
SSP245=GCM["TT_JJA"]-273.15
SSP245std=GCM["TT_JJA.1"]
SSP245-=np.mean(SSP245[v])

fn='/Users/jason/Dropbox/CMIP6/ssp126.txt' # CMIP6 scenario years 1960 .. 2099
GCM=pd.read_csv(fn, delim_whitespace=True, skiprows=11)
SSP126=GCM["TT_JJA"]-273.15
SSP126std=GCM["TT_JJA.1"]
SSP126-=np.mean(SSP126[v])

SSP585-=np.mean(SSP585[v])      
SLC_SSP585=(SSP585*gradient)+intercept
SLC_SSP585std=gradient*SSP585std # CMIP6 uncertainty

SSP245-=np.mean(SSP245[v])      
SLC_SSP245=SSP245*gradient+intercept
SLC_SSP245std=gradient*SSP245std # CMIP6 uncertainty

SSP126-=np.mean(SSP126[v])      
SLC_SSP126=SSP126*gradient+intercept
SLC_SSP126std=gradient*SSP126std # CMIP6 uncertainty

# plt.close()

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
# ax2.scatter(x, SLC_SSP585,s=100,c='r',alpha=1,zorder=32)
# ax1.scatter(x, SSP585,s=100,c='b',alpha=1,zorder=62)
# ax2.scatter(x, SLC_SSP585+SLC_SSP585std,s=100,c='k',label='lab')
# ax2.scatter(x, SLC_SSP585-SLC_SSP585std,s=100,c='k',label='lab')

# ax2.axhline(y=0, xmin=2100,c='k')
# plt.scatter(x,y)
ax2.axhline(y=0., color='k', linestyle='--',linewidth=th*2,zorder=20)
#ax2.axhline(y=286., color='r', linestyle='--',linewidth=th*2)

ax1.set_xlabel('year')
ax1.set_ylabel('Greenland summer temperature anomaly\nvs 1981-2010, $^{o}$C', color='maroon')
ax2.set_ylabel('committed eustatic sea level rise\nfrom Greenland ice,  mm', color='k')

ax1.spines['left'].set_color('maroon')
ax1.yaxis.label.set_color('maroon')
ax1.tick_params(axis='y', colors='maroon')
ax1.set_ylim(-2,9.3)
#ax1.set_ylim(-4.1,8.9)
ax1.set_xlim(1961,2100)
ax2.spines['right'].set_color('k')
ax2.yaxis.label.set_color('k')
ax2.tick_params(axis='y', colors='k')
ax2.set_ylim(-500.,2150.)

# ax1.axvspan(2000,2019, alpha=0.2, color='gray')

fn='/Users/jason/Dropbox/ERA5/stats/ERA5_regional_Arctic_t2m_JJA.csv'
era=pd.read_csv(fn, delimiter=",")
# print(era.columns)
# print(era.year[21:])
v=((era.year>=2000)&(era.year<=2019))
era.Greenland-=np.mean(era.Greenland[v]) # make ERA5 anomaly relative to 2000-2019 period as that is the period for which SLR commitment is obtained
x_era=era.Greenland[21:].valuesx_era=era.year
y_era=era.Greenland

SLR_era=y_era*gradient+intercept # obtain SLR using ERA5 anomaly, for illustration purposes that the annual data have a noteworthy interannual variability!

v=((era.year>=1981)&(era.year<=2010))
SLR_era-=np.mean(SLR_era[v])# make SLR commitment relative to the 1981 to 2010 climate normal, according to WMO standards
ax2.scatter(x_era, SLR_era,s=100,c='k',alpha=1,zorder=17,label='ERA5-driven result')

b_era, m_era = polyfit(x_era, SLR_era, 1)
xx=np.linspace(np.min(x_era), np.max(x_era),2)
yx=np.linspace(np.min(SLR_era), np.max(SLR_era),2)
#ax2.plot(xx, xx*m_era+b_era, '--',color='k',linewidth=th*2,zorder=20,label='ERA5 trend') # not shown SLR_era linear trendline

coefs = np.polyfit(x, SLC_SSP585, 2)  # quadratic
fit_SSP585=coefs[0]*x**2+coefs[1]*x+coefs[2]
fit_SSP585=fit_SSP585.astype(float)
ax2.plot(x,fit_SSP585,'-',linewidth=th*3,c='r',label='CMIP6 SSP585',zorder=16) # quadratic fitline for illustration purposes

v=((x>=1979)&(x<=2019))
b_SSP585, m_SSP585 = polyfit(x[v], SLC_SSP585[v], 1)
xx=np.linspace(np.min(x[v]), np.max(x[v]),2)
yx=np.linspace(np.min(SLC_SSP585[v]), np.max(SLC_SSP585[v]),2)
#ax2.plot(xx, xx*m_SSP585+b_SSP585, '--',color='r',linewidth=th*2,zorder=20,label='SSP585 trend during ERA5') # not shown linear trendline

coefs = np.polyfit(x, SLC_SSP245, 2)  # quadratic
fit_SSP245=coefs[0]*x**2+coefs[1]*x+coefs[2]
fit_SSP245=fit_SSP245.astype(float)
ax2.plot(x,fit_SSP245,'-',linewidth=th*3,c='b',label='CMIP6 SSP245',zorder=16)# quadratic fitline for illustration purposes
coefs = np.polyfit(x, SLC_SSP126, 2)  # quadratic
fit_SSP126=coefs[0]*x**2+coefs[1]*x+coefs[2]
fit_SSP126=fit_SSP126.astype(float)
ax2.plot(x,fit_SSP126,'-',linewidth=th*3,c='g',label='CMIP6 SSP126',zorder=16)# quadratic fitline for illustration purposes

#print("end of century SSP126",str("%.0f"%fit_SSP126[-1:])+"±"+str("%.0f"%(fit_SSP126[-1:]*fractional_fit_error)))
#print("end of century SSP245",str("%.0f"%fit_SSP245[-1:])+"±"+str("%.0f"%(fit_SSP245[-1:]*fractional_fit_error)))
#print("end of century SSP585",str("%.0f"%fit_SSP585[-1:])+"±"+str("%.0f"%(fit_SSP585[-1:]*fractional_fit_error)))
# ax2.plot(x,x*m2+b,'.',linewidth=th*2,c='k',zorder=10)

print("end of century summer SSP126 T anom",str("%.1f"%SSP126[-1:])) # obtain end of Century values for discussion
print("end of century summer SSP245 T anom",str("%.1f"%SSP245[-1:])) # obtain end of Century values for discussion
print("end of century summer SSP585 T anom",str("%.1f"%SSP585[-1:])) # obtain end of Century values for discussion
# SSP585[-1:]*gradient

do_error_envelopes=1

# error envelopes are increased to twice the gradient by end of Century to offer a more conservative and realistic projection
if do_error_envelopes:
    alpha=0.4
    
    x1=2010 ; x2=2100
    y1=gradient ; y2=gradient*2
    m2=(y2-y1)/(x2-x1)
    b=y1-m2*x1
    err_SSP585=x*m2+b 
    # err_SSP585*=1.66
    #err_SSP585=fit_SSP585*fractional_fit_error
    #y=
    #y2=y-fit_SSP585-err_SSP585
    #y3=SLC_SSP585std[-1:]
    ax2.fill_between(x,fit_SSP585+err_SSP585,fit_SSP585-err_SSP585,color='red',zorder=12,alpha=0.3)#,label='std. dev.\n2007-2018')
    print("end of century SSP126",str("%.0f"%fit_SSP126[-1:])+"±"+str("%.0f"%SLC_SSP126std[-1:])) # obtain end of Century values for discussion
    
    err_SSP245=x*m2+b
    # err_SSP245*=1.66
    #err_SSP245=fit_SSP245*fractional_fit_error
    y=fit_SSP245+err_SSP245
    #y2=y-fit_SSP245-err_SSP245
    #y3=y2[-1:]-y[-1:]
    ax2.fill_between(x,y,fit_SSP245-err_SSP245,color='lightblue',zorder=15,alpha=0.7)#,label='std. dev.\n2007-2018')
    print("end of century SSP245",str("%.0f"%fit_SSP245[-1:])+"±"+str("%.0f"%SLC_SSP245std[-1:])) # obtain end of Century values for discussion
    
    err_SSP126=x*m2+b
    # err_SSP126*=1.66
    #err_SSP126=fit_SSP126*fractional_fit_error
    y=fit_SSP126+err_SSP126
    #y2=y-fit_SSP126-err_SSP126
    #y3=y2[-1:]-y[-1:]
    ax2.fill_between(x,y,fit_SSP126-err_SSP126,color='g',zorder=1,alpha=0.6)#,label='std. dev.\n2007-2018')
    print("end of century SSP585",str("%.0f"%fit_SSP585[-1:])+"±"+str("%.0f"%SLC_SSP585std[-1:])) # obtain end of Century values for discussion

#print("SSP585")
#print(fit_SSP585[139],fit_SSP585[139]+(x[139]*m2+b),fit_SSP585[139]-(x[139]*m2+b),(fit_SSP585[139]+(x[139]*m2+b))-(fit_SSP585[139]-(x[139]*m2+b)))

plt.legend(loc=2)
    
plt.show

ly='p'

if ly == 'x':plt.show()

if ly == 'p':
    figpath='/Users/jason/Dropbox/ELA/Figs/'
    figname=figpath+'future_SL_committment_Box_et_al_in_prep_v2.png'
    plt.savefig(figname, bbox_inches='tight', dpi=250)