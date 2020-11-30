import os
import pandas as pd
import csv

times = 20
def predict(subject, row):
    return float(subject[0]) * float(row[0]) + float(subject[1]) * float(row[1]) + float(subject[2]) * float(row[2]) + float(subject[3])

if not os.path.exists('./predict'):
      os.mkdir('./predict')

subject_para = []
ave_subject_para = []
subject_data = []

datas_score = []

good_line = []

diff_num = []

person_score = 0
ave_score = 0

good_loss_count = 0

losses = []
ave_losses = []

loss_count = 0
ave_loss_count = 0

person_count = 0
ave_count = 0

diff = []

new_adv_data = open('./line/' + 'subject' + str(66) + '.csv', 'r')
reader = csv.reader(new_adv_data)
row = list(reader)
ave_subject_para = row[2]

for i in range(1,66):
    loss = 0
    ave_loss = 0
    predict_result = []
    real_result = []
    ave_predict_result = []
    datas_score = []
    new_adv_data = open('./line/' + 'subject' + str(i) + '.csv', 'r')
    reader = csv.reader(new_adv_data)
    row = list(reader)
    subject_para = row[2]

    #tof = open('./predict/' + 'subject' + str(i) + '.csv', 'w')

    datas = open('./test_subject/subject' + str(i) + '.csv', 'r')
    datas_reader = csv.reader(datas)
    rows = list(datas_reader)
    index = 0
    while (index + 2) < len(rows):
        datas_score.append(rows[2 + index])
        index += 2

    for row in datas_score:
        predict_result.append(predict(subject_para, row))
        ave_predict_result.append(predict(ave_subject_para, row))
        real_result.append(float(row[3]))
        loss += abs(predict(subject_para, row) - float(row[3]))
        ave_loss += abs(predict(ave_subject_para, row) - float(row[3]))
    losses.append(loss)
    loss_count += loss
    ave_losses.append(ave_loss)
    ave_loss_count += ave_loss
    if loss < ave_loss:
        good_loss_count += 1

    processed_data = pd.DataFrame({'predict':predict_result,
                                'ave_predict':ave_predict_result,
                                'real':real_result})
    rr = processed_data.corr('spearman')
    predicts = list(rr.get('predict'))
    ave_predict = list(rr.get('ave_predict'))
    diff.append(predicts[2] - ave_predict[2])
    #if predicts[2] > ave_predict[2]:
    if predicts[2] > ave_predict[2]:
        person_count += predicts[2]
        ave_count += ave_predict[2]

    diff_num.append(predicts[2] - ave_predict[2])
    if predicts[2] < ave_predict[2]:
        person_score += 1
        good_line.append(i)
    else:
        ave_score += 1
    print(rr)
print(person_score)
print(ave_score)
print(good_loss_count)

print(person_count / 40)
print(ave_count / 40)

print(diff)

print(loss_count/65)

print(ave_loss_count/65)

print('very good :' + '\n')
sum = 0
count = 0
for i in diff_num:
    if i > 0.05:
        sum += i
        print(str(i) + '\n')
        count += 1
print(sum / count)
print(count)
print('very good end :' + '\n')
sum = 0
count = 0
min = 0
index = 0
for i in diff_num:
    if i == 0:
        sum += i
        print(index)
        count += 1
    index += 1

print('bad' + '\n')

index = 0
for i in diff_num:
    if i < -0.05:
        sum += i
        print(index)
        count += 1
    index += 1

print(sum / count)

index = 0
we_good = 0
they_good = 0
count = 0
sum = 0
we_sum = 0
for i in diff_num:
    if abs(i) > 0.02:
        sum += i
        count += 1
        if i > 0:
            we_good += 1
            we_sum += i
        else:
            they_good += 1
            print(i)
    index += 1

print(we_good)
print(they_good)
print(we_sum / we_good)
print(sum / count)

result_rows = []
index = 1
for i in diff_num:
    result_rows.append({'subject' : index, str(times) : i})
    index += 1
headers = ['subject', str(times)]
train_tof = open('./result' + str(times) + '.csv', 'w')
train_f_csv = csv.DictWriter(train_tof, headers)
train_f_csv.writeheader()
train_f_csv.writerows(result_rows)
train_tof.close()


