import os
import pandas as pd
import csv

datas_score = []

vmaf_ave = 0
rebuffer_ave = 0
switch_ave = 0
score_ave = 0

if not os.path.exists('./new_seven_input'):
    os.mkdir('./new_seven_input')

for i in range(1, 67):
    datas = open('./subject/subject' + str(i) + '.csv', 'r')
    datas_reader = csv.reader(datas)
    rows = list(datas_reader)
    index = 0
    while (index + 2) < len(rows):
        datas_score.append(rows[2 + index])
        index += 2

    max_vmaf = 0
    min_rebuff = 0
    min_switch = 0
    max_score = 0
    for row in datas_score:
        if float(row[0]) > max_vmaf:
            max_vmaf = float(row[0])
        if float(row[1]) < min_rebuff:
            min_rebuff = float(row[1])
        if float(row[2]) < min_switch:
            min_switch = float(row[2])
        if float(row[3]) > max_score:
            max_score = float(row[3])

    for row in datas_score:
        row[0] = str(float(row[0]) / max_vmaf)
        row[1] = str(float(row[1]) / min_rebuff)
        row[2] = str(float(row[2]) / min_switch)
        row[3] = str(float(row[3]) / max_score)

    for row in datas_score:
        vmaf_ave += float(row[0])
        rebuffer_ave += float(row[1])
        switch_ave += float(row[2])
        score_ave += float(row[3])
    vmaf_ave /= len(datas_score)
    rebuffer_ave /= len(datas_score)
    switch_ave /= len(datas_score)
    score_ave /= len(datas_score)
    tof = open('./new_seven_input/subject' + str(i) + '.csv', 'w')
    headers = ['vmaf', 'rebuffering_duration', 'switch', 'vmaf_ave', 'rebuffering_duration_ave', 'switch_ave',
               'score_ave', 'score', ]
    f_csv = csv.DictWriter(tof, headers)
    output_rows = []
    for row in datas_score:
        output_rows.append(
            {'vmaf': row[0], 'rebuffering_duration': row[1], 'switch': row[2], 'vmaf_ave': vmaf_ave,
             'rebuffering_duration_ave': rebuffer_ave, 'switch_ave': switch_ave, 'score_ave': score_ave,
             'score': row[3], })
    f_csv.writeheader()
    f_csv.writerows(output_rows)
    tof.close()
