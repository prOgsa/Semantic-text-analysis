import csv
import math

res = {'m': [], 'f': [], 'c': []}
avg = {'m': [], 'f': [], 'c': []}
day = {'m': [], 'f': [], 'c': []}
for s in ['m', 'f', 'c']:
    for i in range(0, 24):
        res[s].append({'negative': [], 'positive': [], 'neutral': []})
        avg[s].append(
            {'negative': {'sum': 0, 'cnt': 0}, 'positive': {'sum': 0, 'cnt': 0}, 'neutral': {'sum': 0, 'cnt': 0}})
for s in ['m', 'f', 'c']:
    for i in range(0, 4):
        day[s].append(
            {'negative': {'sum': [], 'cnt': 0}, 'positive': {'sum': [], 'cnt': 0}, 'neutral': {'sum': [], 'cnt': 0}})

with open('eggs5.csv', 'r') as csvfile:
    rdr = csv.reader(csvfile, dialect='excel')
    for line in rdr:
        if len(line) == 0:
            continue
# добавление в массив параметров
        sex = line[6]
        hour = int(line[7])

        negative = float(line[3])
        positive = float(line[4])
        neutral = float(line[5])
        if negative >= 0.3:
            res[sex][hour]['negative'].append(negative)
        if positive >= 0.3:
            res[sex][hour]['positive'].append(positive)
        if neutral > 0:
            res[sex][hour]['neutral'].append(neutral)
# преобразование параметров
for sex in res:
    for hour, item in enumerate(res[sex]):
        for emo in item:
            if len(item[emo]) > 0:
                avg[sex][hour][emo]['sum'] = sum(item[emo]) / len(item[emo])
                avg[sex][hour][emo]['cnt'] = len(item[emo])
            h = int(hour / 6)
            if len(item[emo]) > 0:
                day[sex][h][emo]['sum'].append(sum(item[emo]))
                day[sex][h][emo]['cnt'] += len(item[emo])

for sex in day:
    for h, item in enumerate(day[sex]):
        for emo in item:
            if item[emo]['cnt'] > 0:
                day[sex][h][emo]['sum'] = sum(item[emo]['sum']) / item[emo]['cnt']


print(day)