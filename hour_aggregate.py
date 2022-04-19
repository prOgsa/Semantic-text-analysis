'''Дополнительная программа, в которой преобразуются часы: то есть преообразование 24 часов во временные промежутки (утро, день, вечер, ночь).'''

import csv

res = []
avg = []
day = []

for i in range(0, 24):
    res.append({'negative': [], 'positive': [], 'neutral': []})
    avg.append(
        {'negative': {'sum': 0, 'cnt': 0}, 'positive': {'sum': 0, 'cnt': 0}, 'neutral': {'sum': 0, 'cnt': 0}})
for i in range(0, 4):
    day.append(
        {'negative': {'sum': [], 'cnt': 0}, 'positive': {'sum': [], 'cnt': 0}, 'neutral': {'sum': [], 'cnt': 0}})

with open('eggs2s.csv', 'r') as csvfile:
    rdr = csv.reader(csvfile, dialect='excel')
    for line in rdr:
        if len(line) == 0:
            continue

# добавление в массив параметров
        hour = int(line[7])

        negative = float(line[3])
        positive = float(line[4])
        neutral = float(line[5])
        if negative >= 0.3:
            res[hour]['negative'].append(negative)
        if positive >= 0.3:
            res[hour]['positive'].append(positive)
        if neutral > 0:
            res[hour]['neutral'].append(neutral)
# преобразование параметров
for hour, item in enumerate(res):
    for emo in item:
        if len(item[emo]) > 0:
            avg[hour][emo]['sum'] = sum(item[emo]) / len(item[emo])
            avg[hour][emo]['cnt'] = len(item[emo])
        h = int(hour / 6)
        if len(item[emo]) > 0:
            day[h][emo]['sum'].append(sum(item[emo]))
            day[h][emo]['cnt'] += len(item[emo])


for h, item in enumerate(day):
    for emo in item:
        if item[emo]['cnt'] > 0:
            day[h][emo]['sum'] = sum(item[emo]['sum']) / item[emo]['cnt']


print(avg)
print(day)