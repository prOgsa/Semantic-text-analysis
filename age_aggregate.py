import csv

res = {'в': [], 'д': [], '…': []}
avg = {'в': [], 'д': [], '…': []}
day = {'в': [], 'д': [], '…': []}
for s in ['в', 'д', '…']:
    for i in range(0, 24):
        res[s].append({'negative': [], 'positive': [], 'neutral': []})
        avg[s].append({'negative': {'sum': 0, 'cnt': 0}, 'positive': {'sum': 0, 'cnt': 0}, 'neutral': {'sum': 0, 'cnt': 0}})
for s in ['в', 'д', '…']:
    for i in range(0, 4):
        day[s].append(
            {'negative': {'sum': [], 'cnt': 0}, 'positive': {'sum': [], 'cnt': 0}, 'neutral': {'sum': [], 'cnt': 0}})
# добавление в массив параметров
with open('eggs5.csv', 'r') as csvfile:
    rdr = csv.reader(csvfile, dialect='excel')
    for line in rdr:
        if len(line) == 0:
            continue

        age = line[8]
        hour = int(line[7])

        negative = float(line[3])
        positive = float(line[4])
        neutral = float(line[5])
        if negative >= 0.3:
            res[age][hour]['negative'].append(negative)
        if positive >= 0.3:
            res[age][hour]['positive'].append(positive)
        if neutral > 0:
            res[age][hour]['neutral'].append(neutral)

# преобразование параметров
for age in res:
    for hour, item in enumerate(res[age]):
        for emo in item:
            if len(item[emo]) > 0:
                avg[age][hour][emo]['sum'] = sum(item[emo]) / len(item[emo])
                avg[age][hour][emo]['cnt'] = len(item[emo])
            h = int(hour / 6)
            if len(item[emo]) > 0:
                day[age][h][emo]['sum'].append(sum(item[emo]))
                day[age][h][emo]['cnt'] += len(item[emo])
for age in day:
    for h, item in enumerate(day[age]):
        for emo in item:
            if item[emo]['cnt'] > 0:
                day[age][h][emo]['sum'] = sum(item[emo]['sum']) / item[emo]['cnt']
print(day)
