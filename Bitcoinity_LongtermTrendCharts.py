#-----------------------------------------------------------------------------------------------------------
#Simon Ackermann
#Python script for analysing bitcoinity data [USD/BTC]
#-----------------------------------------------------------------------------------------------------------
import os,openpyxl,datetime
from datetime import date
from datetime import datetime, timezone
import calendar
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter
import scipy.optimize as optimization
import math
from scipy import interpolate
import matplotlib.ticker as mticker
from matplotlib.legend_handler import HandlerTuple
print(os.getcwd())          #Print path
print("UTC at script run start:", datetime.now(timezone.utc))
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
print('Plot: Bitcoinity_LongtermTrendChart_log10.png')
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
leg=plt.legend(handles=[line1,line2,line12,line5],fontsize=4,loc='lower right',bbox_to_anchor=(0.95,0.05),edgecolor='none',facecolor='white')
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
ax.text(date_abs_year[lnr-1]+0.02,price_fit_low[lnr-1]*0.9,price_fit_low_end+' (daily growth:'+price_grow_fit_low_end+'%)',color='xkcd:violet',fontname='DejaVu Sans',style='normal',weight='ultralight',size=1.5)
ax.text(date_abs_year[lnr-1]+0.02,price_fit_mid1[lnr-1]*0.9,price_fit_mid1_end,color='xkcd:blue',fontname='DejaVu Sans',style='normal',weight='ultralight',size=1.5)
ax.text(date_abs_year[lnr-1]+0.02,price_fit_mid2[lnr-1]*0.9,price_fit_mid2_end,color='xkcd:turquoise',fontname='DejaVu Sans',style='normal',weight='ultralight',size=1.5)
ax.text(date_abs_year[lnr-1]+0.02,price_fit_mid3[lnr-1]*0.9,price_fit_mid3_end,color='lime',fontname='DejaVu Sans',style='normal',weight='ultralight',size=1.5)
ax.text(date_abs_year[lnr-1]+0.02,price_fit_mid4[lnr-1]*0.9,price_fit_mid4_end,color='lime',fontname='DejaVu Sans',style='normal',weight='ultralight',size=1.5)
ax.text(date_abs_year[lnr-1]+0.02,price_fit_mid5[lnr-1]*0.9,price_fit_mid5_end,color='xkcd:lime',fontname='DejaVu Sans',style='normal',weight='ultralight',size=1.5)
ax.text(date_abs_year[lnr-1]+0.02,price_fit_mid6[lnr-1]*0.9,price_fit_mid6_end,color='gold',fontname='DejaVu Sans',style='normal',weight='ultralight',size=1.5)
ax.text(date_abs_year[lnr-1]+0.02,price_fit_mid7[lnr-1]*0.9,price_fit_mid7_end,color='xkcd:orange',fontname='DejaVu Sans',style='normal',weight='ultralight',size=1.5)
ax.text(date_abs_year[lnr-1]+0.02,price_fit_up[lnr-1]*0.9,price_fit_up_end+' (daily growth:'+price_grow_fit_up_end+'%)',color='red',fontname='DejaVu Sans',style='normal',weight='ultralight',size=1.5)
ax.text(date_abs_year[0]+0.02,ymax*0.6,'Last plot update: '+str(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")),color='black',fontname='DejaVu Sans',style='normal',weight='ultralight',size=3)
os.makedirs("site", exist_ok=True)
filename='site/Bitcoinity_LongtermTrendChart_log10.png'
plt.savefig(filename,dpi=1000)
#-----------------------------------------------------------------------------------------------------------
#Gains of halving cycles
date_halving1=datetime(2012,11,28,0,0,0)
date_halving2=datetime(2016,7,9,0,0,0)
date_halving3=datetime(2020,5,11,0,0,0)
date_halving4=datetime(2024,4,20,0,0,0)
for j in range(0,lnr):
    if date_halving1>=datetime(year[j],month[j],day[j],0,0,0):
        j1=j
    if date_halving2>=datetime(year[j],month[j],day[j],0,0,0):
        j2=j
    if date_halving3>=datetime(year[j],month[j],day[j],0,0,0):
        j3=j
    if date_halving4>=datetime(year[j],month[j],day[j],0,0,0):
        j4=j
    if datetime(2013,12,9,0,0,0)==datetime(year[j],month[j],day[j],0,0,0):
        jx1=j
    if datetime(2017,12,9,0,0,0)==datetime(year[j],month[j],day[j],0,0,0):
        jx2=j
    if datetime(2021,12,9,0,0,0)==datetime(year[j],month[j],day[j],0,0,0):
        jx3=j
    if datetime(2025,12,9,0,0,0)==datetime(year[j],month[j],day[j],0,0,0):
        jx4=j
ndays1=[0 for i in range(0,lnr)]
ndays2=[0 for i in range(0,lnr)]
ndays3=[0 for i in range(0,lnr)]
ndays4=[0 for i in range(0,lnr)]
nweeks1=[0 for i in range(0,lnr)]
nweeks2=[0 for i in range(0,lnr)]
nweeks3=[0 for i in range(0,lnr)]
nweeks4=[0 for i in range(0,lnr)]
price_norm_h1=[0 for i in range(0,lnr)]
price_norm_h2=[0 for i in range(0,lnr)]
price_norm_h3=[0 for i in range(0,lnr)]
price_norm_h4=[0 for i in range(0,lnr)]
for j in range(0,lnr):
    ndays1[j]=ndays[j]-ndays[j1]
    ndays2[j]=ndays[j]-ndays[j2]
    ndays3[j]=ndays[j]-ndays[j3]
    ndays4[j]=ndays[j]-ndays[j4]
    nweeks1[j]=ndays1[j]/7.0
    nweeks2[j]=ndays2[j]/7.0
    nweeks3[j]=ndays3[j]/7.0
    nweeks4[j]=ndays4[j]/7.0
    price_norm_h1[j]=price[j]/price[j1]
    price_norm_h2[j]=price[j]/price[j2]
    price_norm_h3[j]=price[j]/price[j3]
    price_norm_h4[j]=price[j]/price[j4]
nweeks_x1=(ndays[jx1]-ndays[j1])/7.0
price_norm_hx1=price[jx1]/price[j1]
nweeks_x2=(ndays[jx2]-ndays[j2])/7.0
price_norm_hx2=price[jx2]/price[j2]
nweeks_x3=(ndays[jx3]-ndays[j3])/7.0
price_norm_hx3=price[jx3]/price[j3]
nweeks_x4=(ndays[jx4]-ndays[j4])/7.0
price_norm_hx4=price[jx4]/price[j4]
#-----------------------------------------------------------------------------------------------------------
#Plot gains of halving cycles
print('Plot: Bitcoinity_halving_cycles.png')
fs=6
lw=0.5
xmin=0
xmax=52*4
xstep=13
ymax=100
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
ax.set_ylim([0.8,ymax])
major_xticks=np.arange(xmin,xmax+0.01,xstep)
ax.set_xticks(major_xticks)
ax.set_xticklabels(major_xticks,**myfont)
ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
#ax.set_yticklabels(ax.get_yticks(),**myfont)
label_format='{:,.0f}'
ticks_loc=ax.get_yticks().tolist()
ax.yaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
ax.set_yticklabels([label_format.format(x) for x in ticks_loc],**myfont)
plt.xlabel('Weeks since halving: ~4 years between halvings',**myfont)
plt.ylabel('Actual price / halving price [-]',**myfont)
line1,=plt.semilogy(nweeks1,price_norm_h1,'k-',linewidth=0.5,solid_capstyle='round')
line2,=plt.semilogy(nweeks2,price_norm_h2,'b-',linewidth=0.5,solid_capstyle='round')
line3,=plt.semilogy(nweeks3,price_norm_h3,'r-',linewidth=0.5,solid_capstyle='round')
line4,=plt.semilogy(nweeks4,price_norm_h4,'g-',linewidth=0.5,solid_capstyle='round')
line5,=plt.semilogy(nweeks_x1,price_norm_hx1,'ko',linewidth=0.5,markersize=4,markerfacecolor='none')
line6,=plt.semilogy(nweeks_x2,price_norm_hx2,'bo',linewidth=0.5,markersize=4,markerfacecolor='none')
line7,=plt.semilogy(nweeks_x3,price_norm_hx3,'ro',linewidth=0.5,markersize=4,markerfacecolor='none')
line8,=plt.semilogy(nweeks_x4,price_norm_hx4,'go',linewidth=0.5,markersize=4,markerfacecolor='none')
#leg=plt.legend(handles=[line1,line2,line3,line4,line7],fontsize=4,loc='lower right',bbox_to_anchor=(0.95,0.01),edgecolor='none',facecolor='white')
str1='{:.2f}'.format(price[j1])
str2='{:.2f}'.format(price[j2])
str3='{:.2f}'.format(price[j3])
str4='{:.2f}'.format(price[j4])
leg=plt.legend([line1,line2,line3,line4,line5],
               ['Starts at 1$^\mathrm{st}$ halving on 28.11.2012: 10$^0$ = \$'+str1,
                'Starts at 2$^\mathrm{nd}$ halving on 09.07.2016: 10$^0$ = \$'+str2,
                'Starts at 3$^\mathrm{rd}$ halving on 11.05.2020: 10$^0$ = \$'+str3,
                'Starts at 4$^\mathrm{th}$ halving on 20.04.2024: 10$^0$ = \$'+str4,
                '09.12. in 2013, 2017, 2021, 2025'],
               numpoints=1,handler_map={tuple: HandlerTuple(ndivide=None)},
               fontsize=3,loc='upper right',bbox_to_anchor=(0.85,0.999),edgecolor='none',facecolor='white')
leg.get_frame().set_linewidth(0.5)
leg.get_frame().set_alpha(1.0)
os.makedirs("site", exist_ok=True)
filename='site/Bitcoinity_halving_cycles.png'
plt.savefig(filename,dpi=1000)
#-----------------------------------------------------------------------------------------------------------
#Fibonacci analysis
start_time=2022
end_time=2028
ymax=130000
ystep=10000
fib_min=max(price)
fib_max=min(price)
for j in range(0,lnr):
    if date_abs_year[j]<start_time:
        j_start=j
    if date_abs_year[j]>start_time and date_abs_year[j]<end_time:
        if price[j]>fib_max:
            fib_max=price[j]
            j_max=j
        if price[j]<fib_min:
            fib_min=price[j]
            j_min=j
print(fib_min,fib_max)
#Levels
fib_range=fib_max-fib_min
fib_lv_1=fib_min+0.146*fib_range    #0.382*0.382
fib_lv_2=fib_min+0.236*fib_range
fib_lv_3=fib_min+0.382*fib_range
fib_lv_4=fib_min+0.5*fib_range
fib_lv_5=fib_min+0.618*fib_range
fib_lv_6=fib_min+0.786*fib_range
fib_lv_7=fib_min+0.886*fib_range
fib_lv_8=fib_min+1.382*fib_range
fib_lv_9=fib_min+1.5*fib_range
fib_lv_10=fib_min+1.618*fib_range
fib_lv_11=fib_min+2.0*fib_range
fib_lv_12=fib_min+2.618*fib_range
fib_lv_13=fib_min+3.618*fib_range
fib_lv_14=fib_min+4.236*fib_range
str_fib_min='{:.1f}'.format(fib_min)
str_fib_max='{:.1f}'.format(fib_max)
str_fib_lv_1='{:.1f}'.format(fib_lv_1)
str_fib_lv_2='{:.1f}'.format(fib_lv_2)
str_fib_lv_3='{:.1f}'.format(fib_lv_3)
str_fib_lv_4='{:.1f}'.format(fib_lv_4)
str_fib_lv_5='{:.1f}'.format(fib_lv_5)
str_fib_lv_6='{:.1f}'.format(fib_lv_6)
str_fib_lv_7='{:.1f}'.format(fib_lv_7)
str_fib_lv_8='{:.1f}'.format(fib_lv_8)
str_fib_lv_9='{:.1f}'.format(fib_lv_9)
str_fib_lv_10='{:.1f}'.format(fib_lv_10)
str_fib_lv_11='{:.1f}'.format(fib_lv_11)
str_fib_lv_12='{:.1f}'.format(fib_lv_12)
str_fib_lv_13='{:.1f}'.format(fib_lv_13)
str_fib_lv_14='{:.1f}'.format(fib_lv_14)
str_fib_min_f='{:.3f}'.format(0.0)
str_fib_max_f='{:.3f}'.format(1.0)
str_fib_lv_1_f='{:.3f}'.format(0.146)
str_fib_lv_2_f='{:.3f}'.format(0.236)
str_fib_lv_3_f='{:.3f}'.format(0.382)
str_fib_lv_4_f='{:.3f}'.format(0.5)
str_fib_lv_5_f='{:.3f}'.format(0.618)
str_fib_lv_6_f='{:.3f}'.format(0.764)
str_fib_lv_7_f='{:.3f}'.format(0.886)
str_fib_lv_8_f='{:.3f}'.format(1.382)
str_fib_lv_9_f='{:.3f}'.format(1.5)
str_fib_lv_10_f='{:.3f}'.format(1.618)
str_fib_lv_11_f='{:.3f}'.format(2.0)
str_fib_lv_12_f='{:.3f}'.format(2.618)
str_fib_lv_13_f='{:.3f}'.format(3.618)
str_fib_lv_14_f='{:.3f}'.format(4.236)
#-----------------------------------------------------------------------------------------------------------
#Plot Fibonacci
print('Plot: Bitcoinity_Fibonacci.png')
fs=5
lw=0.75
xmin=math.floor(start_time)
xmax=math.ceil(end_time)
#xmax=math.ceil(max(date_abs_year))
xstep=1.0
ymin=0
plt.rcParams['axes.linewidth']=lw
fig=plt.figure(figsize=(10/2.54,7/2.54),facecolor='white')
ax=plt.subplot()
ax.tick_params(width=lw)
plt.subplots_adjust(left=0.13,right=0.96,top=0.96,bottom=0.12)
myfont={'fontname':'DejaVu Sans','style':'normal','fontweight':'ultralight','size':fs}
ax.set_xlim([xmin,xmax])
ax.set_ylim([ymin,ymax])
major_xticks=np.arange(xmin,xmax+0.01,xstep)
ax.set_xticks(major_xticks)
ax.set_xticklabels(major_xticks,**myfont)
ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
major_yticks=np.arange(ymin,ymax+0.01,ystep)
ax.set_yticks(major_yticks)
ax.set_yticklabels(major_yticks,**myfont)
ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
#plt.xlabel('Year',**myfont)
plt.ylabel('Price [USD]',**myfont)
for i in range(j_start,lnr,1):
    if price[i]>=price[i-1]:
        line1,=plt.plot([date_abs_year[i-1],date_abs_year[i]],[price[i-1],price[i]],'g-',linewidth=0.5,label='Price',solid_capstyle='round')
    else:
        line1,=plt.plot([date_abs_year[i-1],date_abs_year[i]],[price[i-1],price[i]],'r-',linewidth=0.5,label='Price',solid_capstyle='round')
line2,=plt.plot([date_abs_year[j_min],end_time],[fib_min,fib_min],'-',color='k',linewidth=0.5,label='fib1')
line3,=plt.plot([date_abs_year[j_max],end_time],[fib_max,fib_max],'-',color='k',linewidth=0.5,label='fib_max')
line4,=plt.plot([date_abs_year[j_max],end_time],[fib_lv_1,fib_lv_1],'-',color='gray',linewidth=0.5,label='fib2')
line5,=plt.plot([date_abs_year[j_max],end_time],[fib_lv_2,fib_lv_2],'-',color='gray',linewidth=0.5,label='fib3')
line6,=plt.plot([date_abs_year[j_max],end_time],[fib_lv_3,fib_lv_3],'-',color='gray',linewidth=0.5,label='fib4')
line7,=plt.plot([date_abs_year[j_max],end_time],[fib_lv_4,fib_lv_4],'-',color='gray',linewidth=0.5,label='fib5')
line8,=plt.plot([date_abs_year[j_max],end_time],[fib_lv_5,fib_lv_5],'-',color='gray',linewidth=0.5,label='fib6')
line9,=plt.plot([date_abs_year[j_max],end_time],[fib_lv_6,fib_lv_6],'-',color='gray',linewidth=0.5,label='fib7')
line10,=plt.plot([date_abs_year[j_max],end_time],[fib_lv_7,fib_lv_7],'-',color='gray',linewidth=0.5,label='fib8')
line11,=plt.plot([date_abs_year[j_max],end_time],[fib_lv_8,fib_lv_8],'-',color='gray',linewidth=0.5,label='fib9')
line12,=plt.plot([date_abs_year[j_max],end_time],[fib_lv_9,fib_lv_9],'-',color='gray',linewidth=0.5,label='fib10')
line13,=plt.plot([date_abs_year[j_max],end_time],[fib_lv_10,fib_lv_10],'-',color='gray',linewidth=0.5,label='fib11')
line14,=plt.plot([date_abs_year[j_max],end_time],[fib_lv_11,fib_lv_11],'-',color='gray',linewidth=0.5,label='fib12')
line15,=plt.plot([date_abs_year[j_max],end_time],[fib_lv_12,fib_lv_12],'-',color='gray',linewidth=0.5,label='fib13')
line16,=plt.plot([date_abs_year[j_max],end_time],[fib_lv_13,fib_lv_13],'-',color='gray',linewidth=0.5,label='fib14')
line17,=plt.plot([date_abs_year[j_max],end_time],[fib_lv_14,fib_lv_14],'-',color='gray',linewidth=0.5,label='fib15')
#plt.title('Fibonacci resistance levels according to last bull market',**myfont)
fs=4
myfont={'fontname':'DejaVu Sans','style':'normal','fontweight':'ultralight','size':fs}
os_x=-1
os_y=800
ax.text(end_time+os_x,fib_min+os_y,str_fib_min+' ('+str_fib_min_f+')',color='k',**myfont)
ax.text(end_time+os_x,fib_max+os_y,str_fib_max+' ('+str_fib_max_f+')',color='k',**myfont)
ax.text(end_time+os_x,fib_lv_1+os_y,str_fib_lv_1+' ('+str_fib_lv_1_f+')',color='gray',**myfont)
ax.text(end_time+os_x,fib_lv_2+os_y,str_fib_lv_2+' ('+str_fib_lv_2_f+')',color='gray',**myfont)
ax.text(end_time+os_x,fib_lv_3+os_y,str_fib_lv_3+' ('+str_fib_lv_3_f+')',color='gray',**myfont)
ax.text(end_time+os_x,fib_lv_4+os_y,str_fib_lv_4+' ('+str_fib_lv_4_f+')',color='gray',**myfont)
ax.text(end_time+os_x,fib_lv_5+os_y,str_fib_lv_5+' ('+str_fib_lv_5_f+')',color='gray',**myfont)
ax.text(end_time+os_x,fib_lv_6+os_y,str_fib_lv_6+' ('+str_fib_lv_6_f+')',color='gray',**myfont)
ax.text(end_time+os_x,fib_lv_7+os_y,str_fib_lv_7+' ('+str_fib_lv_7_f+')',color='gray',**myfont)
ax.text(end_time+os_x,fib_lv_8+os_y,str_fib_lv_8+' ('+str_fib_lv_8_f+')',color='gray',**myfont)
ax.text(end_time+os_x,fib_lv_9+os_y,str_fib_lv_9+' ('+str_fib_lv_9_f+')',color='gray',**myfont)
ax.text(end_time+os_x,fib_lv_10+os_y,str_fib_lv_10+' ('+str_fib_lv_10_f+')',color='gray',**myfont)
ax.text(end_time+os_x,fib_lv_11+os_y,str_fib_lv_11+' ('+str_fib_lv_11_f+')',color='gray',**myfont)
ax.text(end_time+os_x,fib_lv_12+os_y,str_fib_lv_12+' ('+str_fib_lv_12_f+')',color='gray',**myfont)
ax.text(end_time+os_x,fib_lv_13+os_y,str_fib_lv_13+' ('+str_fib_lv_13_f+')',color='gray',**myfont)
ax.text(end_time+os_x,fib_lv_14+os_y,str_fib_lv_14+' ('+str_fib_lv_14_f+')',color='gray',**myfont)
os.makedirs("site", exist_ok=True)
filename='site/Bitcoinity_Fibonacci_Bear2026.png'
plt.savefig(filename,dpi=1000)
#-----------------------------------------------------------------------------------------------------------
