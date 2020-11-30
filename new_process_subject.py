import re
import scipy.io as scio
import numpy as np
import os
import csv

pattern = re.compile(r'content:\d+ ABR:\d+ trace:\d+')
pattern2 = re.compile(r'score of subject \d+')
pattern1 = re.compile(r'[-]?\d+[.]?\d*')
scio.loadmat
subject = [[]] * 66
ave_subject = [[]] * 66
content = ''
ABR = ''
trace = ''


def get_train_index():
    temp_train_index = []
    for i in range(0, 120):
        temp_train_index.append(i)
    return temp_train_index
def get_test_index():
    temp_test_index = []
    for i in range(120, 150):
        temp_test_index.append(i)
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


for i in range(1, 67):
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
    print(i - 1)
    subject[i - 1] = temp_num

for i in range(1, 67):
    temp_num = {}
    with open('aver_zscore.txt', 'r') as f:
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
    print(i - 1)
    ave_subject[i - 1] = temp_num

if not os.path.exists('./train_subject'):
    os.mkdir('./train_subject')
if not os.path.exists('./test_subject'):
    os.mkdir('./test_subject')
headers = ['vmaf', 'rebuffering_duration', 'switch', 'score']

train_average_data = []
for i in range(0,15):
    temp_content = []
    for j in range(0,4):
        temp_ABR = []
        for k in range(0, 7):
            temp_ABR.append([])
        temp_content.append(temp_ABR)
    train_average_data.append(temp_content)

train_index = get_train_index()

test_index = get_test_index()

for i in range(0,15):
    temp_content = []
    for j in range(0,4):
        temp_ABR = []
        for k in range(0, 7):
            temp_ABR.append([])
        temp_content.append(temp_ABR)
    train_average_data.append(temp_content)

for j in range(1, 66):
    if not os.path.exists('./train_subject'):
        os.mkdir('./train_subject')
    if not os.path.exists('./test_subject'):
        os.mkdir('./test_subject')

    train_tof = open('./train_subject/subject' + str(j) + '/' + name + '.csv', 'w')
    test_tof = open('./test_subject/subject' + str(j) + '.csv', 'w')
    test_f_csv = csv.DictWriter(test_tof, headers)

    for key, values in subject[j - 1].items():

        content = pattern1.findall(key)[0]
        ABR = pattern1.findall(key)[1]
        trace = pattern1.findall(key)[2]

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
        headers = ['rebuffering_duration', 'vmaf', 'ave_score', 'score']
        index = 0
        segement_index = 0
        last = 0
        rebuff_index = 0
        result_vmaf = []
        result_rebuffering_duration = []
        for i in scene_cuts:
            temp = i - last
            divid = temp
            last = i
            vmaf = 0
            temp_rebuff = 0

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
        train_rows = []
        test_rows = []
        for i in range(segement_index):
            if i in train_index:
                train_rows.append({'rebuffering_duration': result_rebuffering_duration[i], 'vmaf': result_vmaf[i],
                             'ave_score': ave_subject[j - 1][key], 'score': subject[j - 1][key]})
                train_average_data[content - 1][ABR - 1][trace - 1].append(subject[j - 1][key])
            elif i in test_index:
                test_rows.append({'rebuffering_duration': result_rebuffering_duration[i], 'vmaf': result_vmaf[i],
                             'ave_score': ave_subject[j - 1][key], 'score': subject[j - 1][key]})
        train_f_csv = csv.DictWriter(train_tof, headers)
        train_f_csv.writeheader()
        train_f_csv.writerows(train_rows)
        train_tof.close()

        test_f_csv.writeheader()
        test_f_csv.writerows(test_rows)
        test_tof.close()

