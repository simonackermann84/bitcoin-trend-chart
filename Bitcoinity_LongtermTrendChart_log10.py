#-----------------------------------------------------------------------------------------------------------
#Simon Ackermann
#Python script for analysing bitcoinity data [USD/BTC]
#-----------------------------------------------------------------------------------------------------------
import os,openpyxl,datetime
from datetime import date
from datetime import datetime
import calendar
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter
import scipy.optimize as optimization
import math
from scipy import interpolate
import matplotlib.ticker as mticker
print(os.getcwd())          #Print path
#Import data
myfile=open('bitcoinity_data.txt','r')
data=myfile.readlines()
#-----------------------------------------------------------------------------------------------------------
#Read lines and sort data into vectors
print('Read data')
with open('bitcoinity_data.txt') as fp:
    line=fp.readline()
    cnt=1
    while line:
        line=fp.readline()
        cnt+=1
lnr=cnt-1
snr=0
year=[0 for i in range(0,lnr)]
month=[0 for i in range(0,lnr)]
day=[0 for i in range(0,lnr)]
price=[0 for i in range(0,lnr)]
ndays=[0 for i in range(0,lnr)]
ndays_y=[0 for i in range(0,lnr)]
date_abs=[0 for i in range(0,lnr)]
date_abs_year=[0 for i in range(0,lnr)]
date_abs_year2=[0 for i in range(0,lnr)]
#print('Date, ndays, price')
for j in range(0,lnr):
    str1=data[j+snr].split('.')
    day[j]=int(str1[0])
    month[j]=int(str1[1])
    str2=str1[2].split('\t')
    year[j]=int(str2[0])
    price1=str2[1]
    str3=str1[3].split('\n')
    newstr='.'.join((price1,str3[0]))
    price[j]=float(newstr)
    #print(year[j],month[j],day[j],price[j])
    if j==0:
        year_s=year[j]
        month_s=month[j]
        day_s=day[j]
    a=datetime(year_s,month_s,day_s,0,0,0)
    b=datetime(year[j],month[j],day[j],0,0,0)
    date_abs[j]=b
    dt=b-a
    ndays[j]=dt.total_seconds()/86400
    ndays_y[j]=1+ndays[j]/365
    dt1=datetime(year[j],month[j],day[j],0,0,0)-datetime(year[j],1,1,0,0,0)
    year1=year[j]+1
    dt2=datetime(year1,1,1,0,0,0)-datetime(year[j],1,1,0,0,0)
    year_fraction=dt1/dt2
    date_abs_year[j]=year[j]+year_fraction
    date_abs_year2[j]=year[j]+year_fraction-2011
#-----------------------------------------------------------------------------------------------------------
#Least-squares fit of a non-linear logarithmic regression model onto the price data
def func1(x,L,A,k):
    y=L-A*np.exp(-k*x)
    #y=np.where(y<0.0000000001,0.0000000001,y)
    return y
g=np.array([5.37,4.68,0.193])   #Initial guess
p=optimization.curve_fit(func1,date_abs_year2,np.log10(price),g)
print(p[0])
price_fit=[0 for i in range(0,lnr)]
price_logdev=[0 for i in range(0,lnr)]
band_low_days=[]
band_low_price=[]
band_up_days=[]
band_up_price=[]
for i in range(0,lnr):
    price_fit[i]=10**(func1(date_abs_year2[i],*p[0]))
    #print(price[i],price_fit[i])
    price_logdev[i]=np.log(price[i]/price_fit[i])
    #Low band
    if date_abs_year[i]<2010.8:
        band_low_days.append(date_abs_year2[i])
        band_low_price.append(price[i])
    if date_abs_year[i]>2012 and date_abs_year[i]<2012.8:
        band_low_days.append(date_abs_year2[i])
        band_low_price.append(price[i])
    if date_abs_year[i]>2015.5 and date_abs_year[i]<2016.7:
        band_low_days.append(date_abs_year2[i])
        band_low_price.append(price[i])
    if date_abs_year[i]>2018.8 and date_abs_year[i]<2019.4:
        band_low_days.append(date_abs_year2[i])
        band_low_price.append(price[i])
    if date_abs_year[i]>2020.3 and date_abs_year[i]<2020.4:
        band_low_days.append(date_abs_year2[i])
        band_low_price.append(price[i])
    if date_abs_year[i]>2022.7 and date_abs_year[i]<2024.3:
        band_low_days.append(date_abs_year2[i])
        band_low_price.append(price[i])
    #High band
    #if date_abs_year[i]<2010.6:
    #    band_up_days.append(ndays_y[i])
    #    band_up_price.append(price[i])
    #if date_abs_year[i]>2011.4 and date_abs_year[i]<2011.6:
    #    band_up_days.append(ndays_y[i])
    #    band_up_price.append(price[i])
    if date_abs_year[i]>2013.7 and date_abs_year[i]<2014.1:
        band_up_days.append(date_abs_year2[i])
        band_up_price.append(price[i])
    if date_abs_year[i]>2017.9 and date_abs_year[i]<2018.1:
        band_up_days.append(date_abs_year2[i])
        band_up_price.append(price[i])
    if date_abs_year[i]>2021 and date_abs_year[i]<2022:
        band_up_days.append(date_abs_year2[i])
        band_up_price.append(price[i])
    if date_abs_year[i]>2025 and date_abs_year[i]<2026.2:
        band_up_days.append(date_abs_year2[i])
        band_up_price.append(price[i])
g_low=np.array([5,4,0.2])   #Initial guess
p_low=optimization.curve_fit(func1,band_low_days,np.log10(band_low_price),g_low)
print(p_low[0])
g_up=np.array([5,4,0.2])   #Initial guess
p_up=optimization.curve_fit(func1,band_up_days,np.log10(band_up_price),g_up)
print(p_up[0])
price_fit_low=[0 for i in range(0,lnr)]
price_fit_up=[0 for i in range(0,lnr)]
price_fit_mid1=[0 for i in range(0,lnr)]
price_fit_mid2=[0 for i in range(0,lnr)]
price_fit_mid3=[0 for i in range(0,lnr)]
price_fit_mid4=[0 for i in range(0,lnr)]
price_fit_mid5=[0 for i in range(0,lnr)]
price_fit_mid6=[0 for i in range(0,lnr)]
price_fit_mid7=[0 for i in range(0,lnr)]
for i in range(0,lnr):
    price_fit_low[i]=0.65*10**(func1(date_abs_year2[i],*p_low[0]))
    price_fit_up[i]=5.5*10**(0.88*func1(date_abs_year2[i],*p_up[0]))
    price_fit_mid1[i]=10**((np.log10(price_fit_low[i])+0.125*(np.log10(price_fit_up[i])-np.log10(price_fit_low[i]))))
    price_fit_mid2[i]=10**((np.log10(price_fit_low[i])+0.25*(np.log10(price_fit_up[i])-np.log10(price_fit_low[i]))))
    price_fit_mid3[i]=10**((np.log10(price_fit_low[i])+0.375*(np.log10(price_fit_up[i])-np.log10(price_fit_low[i]))))
    price_fit_mid4[i]=10**((np.log10(price_fit_low[i])+0.5*(np.log10(price_fit_up[i])-np.log10(price_fit_low[i]))))
    price_fit_mid5[i]=10**((np.log10(price_fit_low[i])+0.625*(np.log10(price_fit_up[i])-np.log10(price_fit_low[i]))))
    price_fit_mid6[i]=10**((np.log10(price_fit_low[i])+0.75*(np.log10(price_fit_up[i])-np.log10(price_fit_low[i]))))
    price_fit_mid7[i]=10**((np.log10(price_fit_low[i])+0.875*(np.log10(price_fit_up[i])-np.log10(price_fit_low[i]))))
#-----------------------------------------------------------------------------------------------------------
#Plot price
print('Plot: Bitcoinity_LongtermTrendChart_log10_1.png')
fs=6
lw=0.5
xmin=math.floor(min(date_abs_year))
#xmax=math.ceil(max(date_abs_year))+8
xmax=2032
xstep=2.0
ymax=1000000
plt.rcParams['axes.linewidth']=lw
fig=plt.figure(figsize=(10/2.54,7/2.54),facecolor='white')
ax=plt.subplot()
ax.tick_params(width=lw)
plt.grid(True,which='minor',color=[0.7,0.7,0.7],linestyle='-',linewidth=0.25)
plt.grid(True,which='major',color=[0.5,0.5,0.5],linestyle='-',linewidth=0.5)
#ax.grid(color=[0.5,0.5,0.5],linestyle='-',linewidth=0.5)
ax.set_axisbelow(True)      #Draw grid lines behind data
plt.subplots_adjust(left=0.12,right=0.96,top=0.96,bottom=0.12)
myfont={'fontname':'DejaVu Sans','style':'normal','fontweight':'ultralight','size':fs}
ax.set_xlim([xmin,xmax])
ax.set_ylim([0.01,ymax])
major_xticks=np.arange(xmin,xmax+0.01,xstep)
ax.set_xticks(major_xticks)
ax.set_xticklabels(major_xticks,**myfont)
ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
#ax.set_yticklabels(ax.get_yticks(),**myfont)
label_format='{:,.0f}'
ticks_loc=ax.get_yticks().tolist()
ax.yaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
ax.set_yticklabels([label_format.format(x) for x in ticks_loc],**myfont)
plt.xlabel('Year',**myfont)
plt.ylabel('USD/BTC',**myfont)
line1,=plt.semilogy(date_abs_year,price,'k-',linewidth=0.3,label='Volume averaged daily price',solid_capstyle='round')
line2,=plt.semilogy(date_abs_year,price_fit,'k--',linewidth=0.3,label='Model least-squares fit',solid_capstyle='round')
line5,=plt.fill(np.concatenate((date_abs_year,date_abs_year[::-1])),np.concatenate((price_fit_low,price_fit_mid1[::-1])),color='xkcd:violet',linewidth=0.0,label='Model capitulation zone',alpha=0.5)
line6,=plt.fill(np.concatenate((date_abs_year,date_abs_year[::-1])),np.concatenate((price_fit_mid1,price_fit_mid2[::-1])),color='xkcd:blue',linewidth=0.0,label='Spread',alpha=0.5)
line7,=plt.fill(np.concatenate((date_abs_year,date_abs_year[::-1])),np.concatenate((price_fit_mid2,price_fit_mid3[::-1])),color='xkcd:turquoise',linewidth=0.0,label='Spread',alpha=0.5)
line8,=plt.fill(np.concatenate((date_abs_year,date_abs_year[::-1])),np.concatenate((price_fit_mid3,price_fit_mid4[::-1])),color='lime',linewidth=0.0,label='Spread',alpha=0.5)
line9,=plt.fill(np.concatenate((date_abs_year,date_abs_year[::-1])),np.concatenate((price_fit_mid4,price_fit_mid5[::-1])),color='xkcd:lime',linewidth=0.0,label='Spread',alpha=0.5)
line10,=plt.fill(np.concatenate((date_abs_year,date_abs_year[::-1])),np.concatenate((price_fit_mid5,price_fit_mid6[::-1])),color='gold',linewidth=0.0,label='Spread',alpha=0.5)
line11,=plt.fill(np.concatenate((date_abs_year,date_abs_year[::-1])),np.concatenate((price_fit_mid6,price_fit_mid7[::-1])),color='xkcd:orange',linewidth=0.0,label='Spread',alpha=0.5)
line12,=plt.fill(np.concatenate((date_abs_year,date_abs_year[::-1])),np.concatenate((price_fit_mid7,price_fit_up[::-1])),color='red',linewidth=0.0,label='Model blow-off zone',alpha=0.5)
leg=plt.legend(handles=[line1,line2,line12,line5],fontsize=5,loc='lower right',bbox_to_anchor=(0.95,0.05),edgecolor='none',facecolor='white')
leg.get_frame().set_linewidth(0.5)
leg.get_frame().set_alpha(1.0)
price_fit_low_end='{:.1f}'.format(price_fit_low[lnr-1])
price_fit_mid1_end='{:.1f}'.format(price_fit_mid1[lnr-1])
price_fit_mid2_end='{:.1f}'.format(price_fit_mid2[lnr-1])
price_fit_mid3_end='{:.1f}'.format(price_fit_mid3[lnr-1])
price_fit_mid4_end='{:.1f}'.format(price_fit_mid4[lnr-1])
price_fit_mid5_end='{:.1f}'.format(price_fit_mid5[lnr-1])
price_fit_mid6_end='{:.1f}'.format(price_fit_mid6[lnr-1])
price_fit_mid7_end='{:.1f}'.format(price_fit_mid7[lnr-1])
price_fit_up_end='{:.1f}'.format(price_fit_up[lnr-1])
price_grow_fit_low_end='{:.3f}'.format(100*(price_fit_low[lnr-1]-price_fit_low[lnr-2])/price_fit_low[lnr-1])
price_grow_fit_up_end='{:.3f}'.format(100*(price_fit_up[lnr-1]-price_fit_up[lnr-2])/price_fit_up[lnr-1])
ax.text(date_abs_year[lnr-1]+0.02,price_fit_low[lnr-1]*0.9,price_fit_low_end+' (daily growth:'+price_grow_fit_low_end+'%)',color='xkcd:violet',fontname='DejaVu Sans',style='normal',weight='ultralight',size=2.5)
ax.text(date_abs_year[lnr-1]+0.02,price_fit_mid1[lnr-1]*0.9,price_fit_mid1_end,color='xkcd:blue',fontname='DejaVu Sans',style='normal',weight='ultralight',size=2.5)
ax.text(date_abs_year[lnr-1]+0.02,price_fit_mid2[lnr-1]*0.9,price_fit_mid2_end,color='xkcd:turquoise',fontname='DejaVu Sans',style='normal',weight='ultralight',size=2.5)
ax.text(date_abs_year[lnr-1]+0.02,price_fit_mid3[lnr-1]*0.9,price_fit_mid3_end,color='lime',fontname='DejaVu Sans',style='normal',weight='ultralight',size=2.5)
ax.text(date_abs_year[lnr-1]+0.02,price_fit_mid4[lnr-1]*0.9,price_fit_mid4_end,color='lime',fontname='DejaVu Sans',style='normal',weight='ultralight',size=2.5)
ax.text(date_abs_year[lnr-1]+0.02,price_fit_mid5[lnr-1]*0.9,price_fit_mid5_end,color='xkcd:lime',fontname='DejaVu Sans',style='normal',weight='ultralight',size=2.5)
ax.text(date_abs_year[lnr-1]+0.02,price_fit_mid6[lnr-1]*0.9,price_fit_mid6_end,color='gold',fontname='DejaVu Sans',style='normal',weight='ultralight',size=2.5)
ax.text(date_abs_year[lnr-1]+0.02,price_fit_mid7[lnr-1]*0.9,price_fit_mid7_end,color='xkcd:orange',fontname='DejaVu Sans',style='normal',weight='ultralight',size=2.5)
ax.text(date_abs_year[lnr-1]+0.02,price_fit_up[lnr-1]*0.9,price_fit_up_end+' (daily growth:'+price_grow_fit_up_end+'%)',color='red',fontname='DejaVu Sans',style='normal',weight='ultralight',size=2.5)
os.makedirs("site", exist_ok=True)
filename='site/Bitcoinity_LongtermTrendChart_log10_1.png'
plt.savefig(filename,dpi=1000)
#-----------------------------------------------------------------------------------------------------------
