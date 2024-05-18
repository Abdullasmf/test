# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 14:58:56 2021

@author: Abdulla
"""


import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter
#import time
N=414 #No. of .ALL Files +1
D=60 #No. of DuTs
Ft=np.zeros((D)) #fail time array (0 for did not fail yet)
Ftx=np.zeros((8)) #time step of failure
Ft1=np.zeros((8)) 
Ftx1=np.zeros((8))
Time=np.zeros((N,1))
Current=np.zeros((N,D))
Voltage=np.zeros((N,D))
EXT=np.zeros((N,D))
grp1=np.array([0,1,6,7]) #  5.88 mA
grp2= np.array([2,3,4,5]) #  5.88 mA

grps=[grp1, grp2]

for n in range(N): #loop over every .ALL Output File
    #start_time = time.time()
    RE=str(n).zfill(6)
    f = open("1E%s.ALL" %RE, "r")
    Content= f.read().split()
    Time[n]=Content[0]
    for d in range(D): #loop Over every DuT, reading values from 1 file
        Voltage[n,d]=Content[7*(d+1)]
        Current[n,d]=Content[(7*(d+2))-1]
        EXT[n,d]=Content[(7*(d+1))+1]
    f.close()
    #print("--- %s seconds ---" % (time.time() - start_time))


AD=np.array([0,30,2,32,27,57,29,59])
Resistance=np.divide(Voltage,Current)
Resistance=np.array(Resistance[:,(0,30,2,32,27,57,29,59)])
Current=np.array(Current[:,(0,30,2,32,27,57,29,59)])
EXT=np.array(EXT[:,(0,30,2,32,27,57,29,59)])
Time=np.divide(Time, 3600)
'''
workbook = xlsxwriter.Workbook('Resistances.xlsx')
worksheet = workbook.add_worksheet()
row = 0
for col, data in enumerate(Resistance):
    worksheet.write_column(row, col, data)
workbook.close()
workbook = xlsxwriter.Workbook('Time.xlsx')
worksheet = workbook.add_worksheet()
row = 0
for col, data in enumerate(Time):
    worksheet.write_column(row, col, data)
workbook.close()
'''

def get_change(current, previous):
    if current == previous:
        return 0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return float('inf')


for d in range(8):
    if (Ft[d] != 0):
        continue
    for n in range(N-1):
        if (get_change(Resistance[n+1,d],Resistance[n,d])>=20):  #relative comparison
            Ft[d]=Time[n]
            Ftx[d]=n
            break


for d in range(8):
    if (Ft1[d] != 0):
        continue
    for n in range(N-1):
        if (abs(Resistance[n+1,d]-Resistance[n,d])>=5):  #absolute value comparison
            Ft1[d]=Time[n]
            Ftx1[d]=n
            break
#print('Failures using relative method: %s' %np.count_nonzero(Ft))     
print('Failures using absolute method: %s' %np.count_nonzero(Ft1))
                                                             
grp1ft=Ft[grp1]
grp2ft=Ft[grp2]

grp1ft1=Ft1[grp1]
grp2ft1=Ft1[grp2]

'''
DUT=4 #edit here for individual DuT 11 16 56 0?? 5
plt.plot(Time, Resistance[:,DUT], label = "DUT %s" %int(DUT+1))
if (Ft1[DUT] != 0):
    plt.plot(Ft1[DUT],Resistance[int(Ftx1[DUT]),DUT], 'rx' )
    plt.xlim((-1, Ft1[DUT]+20))
plt.legend()
plt.xlabel('Time (h)')
plt.ylabel('Resistance (ΔΩ)')
plt.savefig('DUT %s.png' %int(DUT+1),dpi=300)
plt.show()
'''
for DUT in range(8):
    plt.plot(Time, Current[:,DUT], label = "DUT %s" %int(AD[DUT]+1))
    if (Ft1[DUT] != 0):
        plt.plot(Ft1[DUT],Current[int(Ftx1[DUT]),DUT], 'rx' )
        #plt.xlim((0, Ft1[DUT]+20))
    plt.legend()
    plt.xlabel('Time (h)')
    plt.ylabel('Current (mA)')
    plt.savefig('(current)DUT %s.png' %int(AD[DUT]+1),dpi=300)
    plt.show()
tEXT=EXT*1000
for DUT in range(8):
    print(DUT)
    fig, ax1 = plt.subplots()
    color = 'tab:blue'
    ax1.plot(Time, Resistance[:,DUT],  color=color, label = "DUT %s" %int(AD[DUT]+1))
    ax1.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=2)
    ax1.set_xlabel('Time (h)')
    ax1.set_ylabel('Resistance Change (Ω)', color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    if (Ft1[DUT] != 0):
        ax1.plot(Ft1[DUT],Resistance[int(Ftx1[DUT]),DUT], 'rx' )
        #plt.xlim((0, Ft1[DUT]+20))
    #if (DUT == 2 or DUT == 32 or DUT == 27 or DUT == 57):
    if AD[DUT] in (2,32,27,57):
        ax2 = ax1.twinx()
        color = 'green'
        ax2.set_ylabel('Ext. Current (mA)', color=color)  # we already handled the x-label with ax1
        ax2.plot(Time, tEXT[:,DUT], color=color)
        ax2.tick_params(axis='y', labelcolor=color)
    if AD[DUT] in (2,32,27,57):
        plt.savefig('DUT %s wEXT.png' %int(AD[DUT]+1),dpi=300)
    else:
        plt.savefig('DUT %s.png' %int(AD[DUT]+1),dpi=300)
    plt.show()

for f in range(len(grps)):
    temp=np.empty((0))
    GN=np.array(grps[f])
    for g in range(len(GN)):
        plt.plot(Time, Resistance[:,GN[g]], label = "DUT %s" %int(AD[GN[g]]+1))
        if (Ft1[GN[g]] != 0):
            plt.plot(Ft1[GN[g]],Resistance[int(Ftx1[GN[g]]),GN[g]] , 'rx')
            temp=np.append(temp,Ft1[GN[g]])
    #if (len(temp) != 0):
        #plt.xlim((0, np.amax(temp)+20))
    lgd=plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title('Group %s DUTs' %int(f+1))
    plt.xlabel('Time (h)')
    plt.ylabel('Resistance (ΔΩ)')
    plt.savefig('Group %s.png' %int(f+1),dpi=600, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.show()
    
for f in range(len(grps)):
    temp=np.empty((0))
    GN=np.array(grps[f])
    for g in range(len(GN)):
        plt.plot(Time, EXT[:,GN[g]], label = "DUT %s" %int(AD[GN[g]]+1))
        if (Ft1[GN[g]] != 0):
            plt.plot(Ft1[GN[g]],EXT[int(Ftx1[GN[g]]),GN[g]] , 'rx')
            temp=np.append(temp,Ft1[GN[g]])
    #if (len(temp) != 0):
        #plt.xlim((0, np.amax(temp)+20))
    lgd=plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title('Group %s DUTs' %int(f+1))
    plt.xlabel('Time (h)')
    plt.ylabel('Ext. Current (A)')
    plt.savefig('(EXT)Group %s.png' %int(f+1),dpi=600, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.show()
'''
for f in range(len(grps)):
    temp=np.empty((0))
    GN=np.array(grps[f])
    for g in range(len(GN)):
        plt.plot(Time, Current[:,GN[g]], label = "DUT %s" %int(GN[g]+1))
        if (Ft1[GN[g]] != 0):
            plt.plot(Ft1[GN[g]],Current[int(Ftx1[GN[g]]),GN[g]] , 'rx')
            temp=np.append(temp,Ft1[GN[g]])
    if (len(temp) != 0):
        plt.xlim((0, np.amax(temp)+20))
    lgd=plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title('Group %s DUTs' %int(f+1))
    plt.xlabel('Time (h)')
    plt.ylabel('Current')
    plt.savefig('Current Group %s.png' %int(f+1),dpi=600, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.show()
'''



