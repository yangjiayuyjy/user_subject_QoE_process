# coding: utf-8
import re
import pickle

import scipy.io as scio
#tof = open('', 'w')
pattern = re.compile(r'quiche: path: 0, cwnd: \d+, rtt: \d+, bandwidth: \d+[.]?\d+ MB/s')
pattern1=re.compile(r'\d+[.]?\d*')

#data = scio.loadmat('AirShow_HuangBufferBasedAdaptor_Trace_0.mat')
#print(data.get('MSSIM'))

train_average_data = []
for i in range(0,15):
    temp_content = []
    for j in range(0,4):
        temp_ABR = []
        for k in range(0, 7):
            temp_ABR.append([])
        temp_content.append(temp_ABR)
    train_average_data.append(temp_content)

print(len(train_average_data[12][2][1]))
train_average_data[12][2][1].append(11)
print(len(train_average_data[12][2][1]))
print(train_average_data[12][2][1][0])
