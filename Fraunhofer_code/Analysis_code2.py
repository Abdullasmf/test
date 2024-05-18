# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 14:58:56 2021

@author: Abdulla
"""


import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter
#import time
N=508 #No. of .ALL Files +1
D=60 #No. of DuTs
Ft=np.zeros((D)) #fail time array (0 for did not fail yet)
Ftx=np.zeros((D)) #time step of failure
Ft1=np.zeros((D)) 
Ftx1=np.zeros((D))
Time=np.zeros((N,1))
Current=np.zeros((N,D))
Voltage=np.zeros((N,D))
grp1=range(60)
'''
grp2= grp1+1 #  1.26 mA
grp3= grp2+1 #  2.44 mA
grp4= grp3+1 #  3.86 mA
grp5= grp4+1 #  5.88 mA
'''
grps=[grp1]

for n in range(N): #loop over every .ALL Output File
    #start_time = time.time()
    RE=str(n).zfill(6)
    f = open("1E%s.ALL" %RE, "r")
    Content= f.read().split()
    Time[n]=Content[0]
    for d in range(D): #loop Over every DuT, reading values from 1 file
        Voltage[n,d]=Content[7*(d+1)]
        Current[n,d]=Content[(7*(d+2))-1]
    f.close()
    #print("--- %s seconds ---" % (time.time() - start_time))



Resistance=np.divide(Voltage,Current)
Time=np.divide(Time, 3600)

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


def get_change(current, previous):
    if current == previous:
        return 0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return float('inf')


for d in range(D):
    if (Ft1[d] != 0):
        continue
    for n in range(N-1):
        if (get_change(Resistance[n+1,d],Resistance[0,d])>=5):  #relative comparison
            Ft1[d]=Time[n]
            Ftx1[d]=n
            break

'''
for d in range(D):
    if (Ft1[d] != 0):
        continue
    for n in range(N-1):
        if (abs(Resistance[n+1,d]-Resistance[n,d])>=5):  #absolute value comparison
            Ft1[d]=Time[n]
            Ftx1[d]=n
            break
        '''
#print('Failures using relative method: %s' %np.count_nonzero(Ft))     
print('Failures: %s' %np.count_nonzero(Ft1))  

grp1ft=Ft[grp1]
'''
grp2ft=Ft[grp2]
grp3ft=Ft[grp3]
grp4ft=Ft[grp4]
grp5ft=Ft[grp5]
grp1ft1=Ft1[grp1]
grp2ft1=Ft1[grp2]
grp3ft1=Ft1[grp3]
grp4ft1=Ft1[grp4]
grp5ft1=Ft1[grp5]
'''



for DUT in grp1:
    plt.plot(Time, Current[:,DUT], label = "DUT %s" %int(DUT+1))
    if (Ft1[DUT] != 0):
        plt.plot(Ft1[DUT],Current[int(Ftx1[DUT]),DUT], 'rx' )
        plt.xlim((0, Ft1[DUT]+20))
    plt.legend()
    plt.xlabel('Time (h)')
    plt.ylabel('Current')
    plt.savefig('(current)DUT %s.png' %int(DUT+1),dpi=300)
    plt.show()

for DUT in grp1:
    plt.plot(Time, Resistance[:,DUT], label = "DUT %s" %int(DUT+1))
    if (Ft1[DUT] != 0):
        plt.plot(Ft1[DUT],Resistance[int(Ftx1[DUT]),DUT], 'rx' )
        plt.xlim((0, Ft1[DUT]+20))
    plt.legend()
    plt.xlabel('Time (h)')
    plt.ylabel('Resistance')
    plt.savefig('DUT %s.png' %int(DUT+1),dpi=300)
    plt.show()
    
for f in range(len(grps)):
    temp=np.empty((0))
    GN=np.array(grps[f])
    for g in range(len(GN)):
        plt.plot(Time, Resistance[:,GN[g]], label = "DUT %s" %int(g+1))
        if (Ft1[GN[g]] != 0):
            plt.plot(Ft1[GN[g]],Resistance[int(Ftx1[GN[g]]),GN[g]] , 'rx')
            temp=np.append(temp,Ft1[GN[g]])
    if (len(temp) != 0):
        plt.xlim((0, np.amax(temp)+20))
    lgd=plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title('Resistance Graph')
    plt.xlabel('Time (h)')
    plt.ylabel('Resistance (ΔΩ)')
    plt.savefig('Group %s.png' %int(f+1),dpi=600, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.show()
for f in range(len(grps)):
    temp=np.empty((0))
    GN=np.array(grps[f])
    for g in range(len(GN)):
        plt.plot(Time, Current[:,GN[g]], label = "DUT %s" %int(g+1))
        if (Ft1[GN[g]] != 0):
            plt.plot(Ft1[GN[g]],Current[int(Ftx1[GN[g]]),GN[g]] , 'rx')
            temp=np.append(temp,Ft1[GN[g]])
    if (len(temp) != 0):
        plt.xlim((0, np.amax(temp)+20))
    lgd=plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title('Current Graph')
    plt.xlabel('Time (h)')
    plt.ylabel('Current')
    plt.savefig('Current Group %s.png' %int(f+1),dpi=600, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.show()




