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

for j in range(1, 67):
    if not os.path.exists('./subject' + str(j)):
        os.mkdir('./subject' + str(j))
    for key, values in subject[j - 1].items():
        # tof.write(key + ' ave_score:' + str(ave_subject[i - 1][key]) + ' score:' + str(subject[i - 1][key]) + '\n')
        name = get_key_name(key)
        data = scio.loadmat('./data/' + name)
        tof = open('./subject' + str(j) + '/' + name + '.csv', 'w')
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
        # tof.write('rebuffering_duration    vmaf    ave_score    score' + '\n')
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
        rows = []
        for i in range(segement_index):
            rows.append({'rebuffering_duration': result_rebuffering_duration[i], 'vmaf': result_vmaf[i],
                         'ave_score': ave_subject[j - 1][key], 'score': subject[j - 1][key]})
            # tof.write(str(result_rebuffering_duration[i]) + '    ' + str(
            # result_vmaf[i]) + '    ' + str(ave_subject[j - 1][key]) + '    ' + str(subject[j - 1][key]) + '\n')
        f_csv = csv.DictWriter(tof, headers)
        f_csv.writeheader()
        f_csv.writerows(rows)
        tof.close()
