import os
import csv

if not os.path.exists('./new_pattern_result'):
    os.mkdir('./new_pattern_result')
for i in range(1, 67):
    no_rebuffer_score = []
    rebuffer_score = []
    all_score = []

    re_no_rebuffer_score = []
    re_rebuffer_score = []
    re_all_score = []

    no_rebuffer_index = 1
    rebuffer_index = 1
    test_index = 1
    score = 0
    f = os.walk('./csv_result/subject' + str(i) + '/')
    if not os.path.exists('./new_pattern_result/subject' + str(i)):
        os.mkdir('./new_pattern_result/subject' + str(i))
    # 不卡顿的视频
    if not os.path.exists('./new_pattern_result/subject' + str(i) + '/WaterlooSQoE-I'):
        os.mkdir('./new_pattern_result/subject' + str(i) + '/WaterlooSQoE-I')
    # 卡顿的视频
    if not os.path.exists('./new_pattern_result/subject' + str(i) + '/WaterlooSQoE-II'):
        os.mkdir('./new_pattern_result/subject' + str(i) + '/WaterlooSQoE-II')
    # 总的视频
    if not os.path.exists('./new_pattern_result/subject' + str(i) + '/test1'):
        os.mkdir('./new_pattern_result/subject' + str(i) + '/test1')
    for file in f:
        for files in file[2]:
            index = 0
            datas_score = []
            vmaf = []
            rebuffer_duration = []
            is_no_rebuffer = True

            datas = open('./csv_result/subject' + str(i) + '/' + files, 'r')
            datas_reader = csv.reader(datas)
            rows = list(datas_reader)
            while (index + 2) < len(rows):
                datas_score.append(rows[2 + index])
                index += 2
            for row in datas_score:
                if (int(row[0]) != 0):
                    is_no_rebuffer = False
                rebuffer_duration.append(row[0])
                score = float(row[3])

                vmaf.append(row[1])

            if is_no_rebuffer:
                no_rebuffer_score.append(score)
            else:
                rebuffer_score.append(score)
            all_score.append(score)

            if is_no_rebuffer:
                if not os.path.exists('./new_pattern_result/subject' + str(i) + '/WaterlooSQoE-II/streaming_logs'):
                    os.mkdir('./new_pattern_result/subject' + str(i) + '/WaterlooSQoE-II/streaming_logs')
                tof = open('./new_pattern_result/subject' + str(i) + '/WaterlooSQoE-II/streaming_logs/' + '00' + str(
                    no_rebuffer_index) + '.csv',
                           'w')
                headers = ['vmaf']
                f_csv = csv.DictWriter(tof, headers)
                output_rows = []
                for row in vmaf:
                    output_rows.append({'vmaf': row})
                f_csv.writeheader()
                f_csv.writerows(output_rows)
                no_rebuffer_index += 1
                tof.close()
            else:
                if not os.path.exists('./new_pattern_result/subject' + str(i) + '/WaterlooSQoE-I/streaming_logs'):
                    os.mkdir('./new_pattern_result/subject' + str(i) + '/WaterlooSQoE-I/streaming_logs')
                tof = open('./new_pattern_result/subject' + str(i) + '/WaterlooSQoE-I/streaming_logs/' + '00' + str(
                    rebuffer_index) + '.csv',
                           'w')
                headers = ['vmaf', 'rebuffering duration']
                f_csv = csv.DictWriter(tof, headers)
                output_rows = []
                for j in range(len(vmaf)):
                    output_rows.append({'vmaf': vmaf[j], 'rebuffering duration': rebuffer_duration[j]})
                f_csv.writeheader()
                f_csv.writerows(output_rows)
                rebuffer_index += 1
                tof.close()

            if not os.path.exists('./new_pattern_result/subject' + str(i) + '/test1/streaming_logs'):
                os.mkdir('./new_pattern_result/subject' + str(i) + '/test1/streaming_logs')
            tof = open(
                './new_pattern_result/subject' + str(i) + '/test1/streaming_logs/' + '00' + str(test_index) + '.csv',
                'w')
            headers = ['vmaf', 'rebuffering duration']
            f_csv = csv.DictWriter(tof, headers)
            test_output_rows = []
            for j in range(len(vmaf)):
                test_output_rows.append({'vmaf': vmaf[j], 'rebuffering duration': rebuffer_duration[j]})
            f_csv.writeheader()
            f_csv.writerows(test_output_rows)
            test_index += 1
            tof.close()

    max_score = 0.0
    for row in rebuffer_score:
        if row > max_score:
            max_score = row
    for row in no_rebuffer_score:
        if row > max_score:
            max_score = row

    for j in no_rebuffer_score:
        j /= max_score
        j *= 50
        j += 50
        re_no_rebuffer_score.append(j)

    for j in rebuffer_score:
        j /= max_score
        j *= 50
        j += 50
        re_rebuffer_score.append(j)

    for j in all_score:
        j /= max_score
        j *= 50
        j += 50
        re_all_score.append(j)

    tof = open('./new_pattern_result/subject' + str(i) + '/WaterlooSQoE-II/' + 'data' + '.csv', 'w')
    headers = ['streaming_log', 'mos']
    f_csv = csv.DictWriter(tof, headers)
    output_rows = []
    no_rebuffer_index = 1
    for row in re_no_rebuffer_score:
        output_rows.append({'streaming_log': '00' + str(no_rebuffer_index) + '.csv', 'mos': row})
        no_rebuffer_index += 1
    f_csv.writeheader()
    f_csv.writerows(output_rows)
    tof.close()

    tof = open('./new_pattern_result/subject' + str(i) + '/WaterlooSQoE-I/' + 'data' + '.csv', 'w')
    headers = ['streaming_log', 'mos']
    f_csv = csv.DictWriter(tof, headers)
    output_rows = []
    rebuffer_index = 1
    for row in re_rebuffer_score:
        output_rows.append({'streaming_log': '00' + str(rebuffer_index) + '.csv', 'mos': row})
        rebuffer_index += 1
    f_csv.writeheader()
    f_csv.writerows(output_rows)
    tof.close()

    tof = open('./new_pattern_result/subject' + str(i) + '/test1/' + 'data' + '.csv', 'w')
    headers = ['streaming_log', 'mos']
    f_csv = csv.DictWriter(tof, headers)
    output_rows = []
    test_index = 1
    for row in re_all_score:
        output_rows.append({'streaming_log': '00' + str(test_index) + '.csv', 'mos': row})
        test_index += 1
    f_csv.writeheader()
    f_csv.writerows(output_rows)
    tof.close()
