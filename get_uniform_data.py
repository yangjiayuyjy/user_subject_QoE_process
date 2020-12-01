import re
import scipy.io as scio
import numpy as np
import os
import csv
import random
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

pattern = re.compile(r'content:\d+ ABR:\d+ trace:\d+')
pattern2 = re.compile(r'score of subject \d+')
pattern1 = re.compile(r'[-]?\d+[.]?\d*')

train_rate = 0.8

subject = [[]] * 66
ave_subject = [[]] * 66
subject_max_score = [0] * 66
ave_subject_max_score = [0] * 66
content = ''
ABR = ''
trace = ''
loss_image = []
srcc_image = []

shuffle_num = []
for i in range(0, 150):
    shuffle_num.append(i)

def predict(a, b, row):
    return float(b[0]) * float(row['vmaf']) + float(b[1]) * float(row['rebuffering_duration']) + float(b[2]) * float(row['switch']) + float(a)


def get_loss(train_rows, test_rows):

    temp_data = []
    temp_score = []

    for row in train_rows:
        temp_row = []
        temp_row.append(row['vmaf'])
        temp_row.append(row['rebuffering_duration'])
        temp_row.append(row['switch'])
        temp_data.append(temp_row)
        temp_score.append(row['score'])

    #get line
    model = LinearRegression()
    model.fit(temp_data, temp_score)
    #截距
    a = model.intercept_
    #系数
    b = model.coef_

    loss = 0
    scores = []
    real_scores = []
    for row in test_rows:
        predict_score = predict(a, b, row)
        scores.append(predict_score)
        loss += abs(predict_score - row['score'])
        real_scores.append(row['score'])

    processed_data = pd.DataFrame({'predict': scores,
                                    'real': real_scores})
    rr = processed_data.corr('spearman')
    predicts = list(rr.get('predict'))
    print('loss:' + str(loss))
    print('srcc:' + str(predicts))
    loss_image.append(loss)
    srcc_image.append(predicts[1] * 500)

    return 1000 - predicts[1] * 500



def get_train_index():
    random.shuffle(shuffle_num)
    temp_train_index = []
    for i in range(0, int(150 * train_rate)):
        temp_train_index.append(shuffle_num[i])
    return temp_train_index


def get_test_index():
    temp_test_index = []
    for i in range(int(150 * train_rate), 150):
        temp_test_index.append(shuffle_num[i])
    return temp_test_index


def get_key_name(key):
    name = ''
    content = pattern1.findall(key)[0]
    ABR = pattern1.findall(key)[1]
    trace = pattern1.findall(key)[2]
    if content == '1':
        name += 'AirShow'
    elif content == '2':
        name += 'AsianFusion'
    elif content == '3':
        name += 'Chimera1102347'
    elif content == '4':
        name += 'Chimera1102353'
    elif content == '5':
        name += 'CosmosLaundromat'
    elif content == '6':
        name += 'ElFuenteDance'
    elif content == '7':
        name += 'ElFuenteMask'
    elif content == '8':
        name += 'GTA'
    elif content == '9':
        name += 'MeridianConversation'
    elif content == '10':
        name += 'MeridianDriving'
    elif content == '11':
        name += 'Skateboarding'
    elif content == '12':
        name += 'Soccer'
    elif content == '13':
        name += 'Sparks'
    elif content == '14':
        name += 'TearsOfSteelRobot'
    elif content == '15':
        name += 'TearsOfSteelStatic'
    name += '_'
    if ABR == '1':
        name += 'HuangBufferBasedAdaptor'
    elif ABR == '2':
        name += 'OracleVMAFViterbiQualityBasedAdaptor'
    elif ABR == '3':
        name += 'SimpleThroughputBasedAdaptor'
    elif ABR == '4':
        name += 'VMAFViterbiQualityBasedAdaptor'
    name += '_Trace_'
    name += str(int(trace) - 1)
    return name


for i in range(1, 66):
    temp_num = {}
    with open('zsocre_result.txt', 'r') as f:
        for line in f:
            match = pattern.search(line)
            match1 = pattern2.search(line)
            if match is not None:
                temp = pattern1.findall(line)
                content = pattern1.findall(line)[0]
                ABR = pattern1.findall(line)[1]
                trace = pattern1.findall(line)[2]
            if match1 is not None:
                temp = pattern1.findall(line)
                subject_num = int(pattern1.findall(line)[0])
                if subject_num == i:
                    score = float(pattern1.findall(line)[1])
                    if ('content:' + content + ' ABR:' + ABR + ' trace:' + trace) not in temp_num:
                        temp_num['content:' + content + ' ABR:' + ABR + ' trace:' + trace] = score
                    if score > subject_max_score[i - 1]:
                        subject_max_score[i - 1] = score
    print(i - 1)
    subject[i - 1] = temp_num

if not os.path.exists('./train_subject'):
    os.mkdir('./train_subject')
if not os.path.exists('./test_subject'):
    os.mkdir('./test_subject')
headers = ['vmaf', 'rebuffering_duration', 'switch', 'score']

train_average_data = []
for i in range(0, 15):
    temp_content = []
    for j in range(0, 4):
        temp_ABR = []
        for k in range(0, 7):
            temp_ABR.append([])
        temp_content.append(temp_ABR)
    train_average_data.append(temp_content)


for i in range(0, 15):
    temp_content = []
    for j in range(0, 4):
        temp_ABR = []
        for k in range(0, 7):
            temp_ABR.append([])
        temp_content.append(temp_ABR)
    train_average_data.append(temp_content)

headers = ['vmaf', 'rebuffering_duration', 'switch', 'score']

for j in range(1, 66):

    train_index = []

    test_index = []

    loss = 100000

    # new logic begin
    for k in range(80):
        train_rows = []
        test_rows = []
        train_or_test_index = 0
        new_train_data_index = get_train_index()
        new_test_data_index = get_test_index()
        for key, values in subject[j - 1].items():
            # tof.write(key + ' ave_score:' + str(ave_subject[i - 1][key]) + ' score:' + str(subject[i - 1][key]) + '\n')
            switch_sum = 0
            ave_vmaf = 0
            rebuff_sum = 0
            name = get_key_name(key)
            data = scio.loadmat('./data/' + name)
            VMAF = data.get('VMAF')[0]
            playout_bitrate = data.get('playout_bitrate')[0]
            is_rebuffered_bool = data.get('is_rebuffered_bool')[0]
            scene_cuts = data.get('scene_cuts')[0]
            new_scene_cuts = []
            for i in scene_cuts:
                new_scene_cuts.append(i)
            new_scene_cuts.append(len(VMAF))
            scene_cuts = np.array(new_scene_cuts)
            # tof.write('rebuffering_duration    vmaf    ave_score    score' + '\n')
            index = 0
            segement_index = 0
            last = 0
            rebuff_index = 0
            result_vmaf = []
            result_rebuffering_duration = []
            last_vmaf = 0
            for i in scene_cuts:
                temp = i - last
                divid = temp
                last = i
                vmaf = 0
                temp_rebuff = 0
                if i > 0 and last_vmaf != VMAF[index - rebuff_index]:
                    switch_sum -= (
                                max(VMAF[index - rebuff_index], last_vmaf) - min(VMAF[index - rebuff_index], last_vmaf))
                last_vmaf = VMAF[index - rebuff_index]
                while temp > 0 and index < len(is_rebuffered_bool):
                    if is_rebuffered_bool[index] != 1:
                        temp -= 1
                        vmaf += VMAF[index - rebuff_index]
                        index += 1
                    else:
                        rebuff_index += 1
                        temp_rebuff += 1
                        index += 1
                result_vmaf.append((float)(vmaf / divid))
                result_rebuffering_duration.append(temp_rebuff)
                segement_index += 1
            for i in range(segement_index):
                ave_vmaf += result_vmaf[i]
                rebuff_sum -= result_rebuffering_duration[i]

            if train_or_test_index in new_train_data_index:
                train_rows.append({'vmaf': ave_vmaf, 'rebuffering_duration': rebuff_sum, 'switch': switch_sum,
                                   'score': (subject[j - 1][key] * (50 / subject_max_score[j - 1]) + 50)})
            elif train_or_test_index in new_test_data_index:
                test_rows.append({'vmaf': ave_vmaf, 'rebuffering_duration': rebuff_sum, 'switch': switch_sum,
                                  'score': (subject[j - 1][key] * (50 / subject_max_score[j - 1]) + 50)})
            train_or_test_index += 1

        temp_loss = get_loss(train_rows, test_rows)
        #print('subject' + str(j) + 'temp_loss:' + str(loss))
        if temp_loss < loss:
            loss = temp_loss
            train_index = new_train_data_index
            test_index = new_test_data_index

    #new logic end


    #plt.plot(srcc_image, color = 'red', linewidth = 2.0, linestyle = '--')
    #plt.plot(loss_image, color='blue', linewidth=3.0, linestyle='-.')
    #plt.show()

    print('subject' + str(j) + 'loss:' + str(loss))

    train_tof = open('./train_subject/subject' + str(j) + '.csv', 'w')
    test_tof = open('./test_subject/subject' + str(j) + '.csv', 'w')
    train_f_csv = csv.DictWriter(train_tof, headers)
    test_f_csv = csv.DictWriter(test_tof, headers)
    train_rows = []
    test_rows = []

    train_or_test_index = 0
    for key, values in subject[j - 1].items():
        # tof.write(key + ' ave_score:' + str(ave_subject[i - 1][key]) + ' score:' + str(subject[i - 1][key]) + '\n')
        switch_sum = 0
        ave_vmaf = 0
        rebuff_sum = 0
        name = get_key_name(key)
        data = scio.loadmat('./data/' + name)
        VMAF = data.get('VMAF')[0]
        playout_bitrate = data.get('playout_bitrate')[0]
        is_rebuffered_bool = data.get('is_rebuffered_bool')[0]
        scene_cuts = data.get('scene_cuts')[0]
        new_scene_cuts = []
        for i in scene_cuts:
            new_scene_cuts.append(i)
        new_scene_cuts.append(len(VMAF))
        scene_cuts = np.array(new_scene_cuts)
        # tof.write('rebuffering_duration    vmaf    ave_score    score' + '\n')
        index = 0
        segement_index = 0
        last = 0
        rebuff_index = 0
        result_vmaf = []
        result_rebuffering_duration = []
        last_vmaf = 0
        for i in scene_cuts:
            temp = i - last
            divid = temp
            last = i
            vmaf = 0
            temp_rebuff = 0
            if i > 0 and last_vmaf != VMAF[index - rebuff_index]:
                switch_sum -= (max(VMAF[index - rebuff_index], last_vmaf) - min(VMAF[index - rebuff_index], last_vmaf))
            last_vmaf = VMAF[index - rebuff_index]
            while temp > 0 and index < len(is_rebuffered_bool):
                if is_rebuffered_bool[index] != 1:
                    temp -= 1
                    vmaf += VMAF[index - rebuff_index]
                    index += 1
                else:
                    rebuff_index += 1
                    temp_rebuff += 1
                    index += 1
            result_vmaf.append((float)(vmaf / divid))
            result_rebuffering_duration.append(temp_rebuff)
            segement_index += 1
        for i in range(segement_index):
            ave_vmaf += result_vmaf[i]
            rebuff_sum -= result_rebuffering_duration[i]

        if train_or_test_index in train_index:
            train_rows.append({'vmaf': ave_vmaf, 'rebuffering_duration': rebuff_sum, 'switch': switch_sum,
                               'score': (subject[j - 1][key] * (50 / subject_max_score[j - 1]) + 50)})
            train_average_data[int(pattern1.findall(key)[0]) - 1][int(pattern1.findall(key)[1]) - 1][
                int(pattern1.findall(key)[2]) - 1].append(
                {'vmaf': ave_vmaf, 'rebuffering_duration': rebuff_sum, 'switch': switch_sum,
                 'score': (subject[j - 1][key] * (50 / subject_max_score[j - 1]) + 50)})
        elif train_or_test_index in test_index:
            test_rows.append({'vmaf': ave_vmaf, 'rebuffering_duration': rebuff_sum, 'switch': switch_sum,
                              'score': (subject[j - 1][key] * (50 / subject_max_score[j - 1]) + 50)})
        train_or_test_index += 1

    train_f_csv.writeheader()
    train_f_csv.writerows(train_rows)
    train_tof.close()

    test_f_csv.writeheader()
    test_f_csv.writerows(test_rows)
    test_tof.close()

train_tof = open('./train_subject/subject' + str(66) + '.csv', 'w')
train_f_csv = csv.DictWriter(train_tof, headers)
train_rows = []

for i in range(0, 15):
    for j in range(0, 4):
        for k in range(0, 7):
            if not len(train_average_data[i][j][k]) == 0:
                ave_vmaf = 0
                ave_rebuffer = 0
                ave_switch = 0
                ave_score = 0
                for m in train_average_data[i][j][k]:
                    ave_vmaf += m.get('vmaf')
                    ave_rebuffer += m.get('rebuffering_duration')
                    ave_switch += m.get('switch')
                    ave_score += m.get('score')
                train_rows.append(
                    {'vmaf': ave_vmaf / len(train_average_data[i][j][k]),
                     'rebuffering_duration': ave_rebuffer / len(train_average_data[i][j][k]),
                     'switch': ave_switch / len(train_average_data[i][j][k]),
                     'score': ave_score / len(train_average_data[i][j][k])})

train_f_csv.writeheader()
train_f_csv.writerows(train_rows)
train_tof.close()
print(1)
