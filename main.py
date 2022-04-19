'''Основная программа, в которой преобразуются сырые данные. При помощи регулярных выражений вырезается нужная информация,
а именно дата/время, имя и текст сообщения, при помощи библиотеки Dostoevsky определяется эмоциональная окраска текста, которая
впоследствии распределяется по часам.'''

import csv
from datetime import datetime
from os import listdir
from os.path import isfile, join, isdir
from pathlib import Path
import re
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
import dateparser


mypath = r'/Users/nastya/PycharmProjects/олимпиада/Archive/messages/teachers'
path = Path(mypath)


res = []
for i in range(0, 24):
    res.append({'negative': [], 'positive': [], 'neutral': []})
with open('eggs6.csv', 'w', newline="\r\n") as csvfile:
    spamwriter = csv.writer(csvfile, dialect='excel')

    for f in listdir(mypath):
        if isdir(join(mypath, f)):
            cp = path.joinpath(f)

            for c in listdir(cp.absolute()):
                fname = cp.joinpath(c)
                if not isfile(fname):
                    continue

                rec = []
                with open(fname.absolute(), encoding='windows-1251') as reader:
                    a = reader.read()
                    #использую регулярные выражения
                    for i in re.findall(
                            r"<div class=\"message__header\">(.+?), (.+?)</div>\s*<div>(.+?)<div class=\"kludges\">", a):
                        i = list(i)
                        if i[1].find('span') == -1:
                            date: datetime = dateparser.parse(i[1])
                            hour = date.hour
                        else:
                            e = i[1]
                            date: datetime = dateparser.parse(e[:e.find('span')])
                            hour = date.hour
                        i[1] = str(date)

                        tokenizer = RegexTokenizer()
                        model = FastTextSocialNetworkModel(tokenizer=tokenizer)

                        messages = [i[2]]

                        results = model.predict(messages, k=2)
                        negative, positive, neutral = 0, 0, 0
                        for sentiment in zip(results):

                            negative = sentiment[0].get("negative", 0)
                            positive = sentiment[0].get("positive", 0)
                            neutral = sentiment[0].get("neutral", 0)
                        res[hour]['negative'].append(negative)
                        res[hour]['positive'].append(positive)
                        res[hour]['neutral'].append(neutral)
                        i.append(negative)
                        i.append(positive)
                        i.append(neutral)
                        spamwriter.writerow(i)

result = list(range(0, 24))
for l in range(0, 24):
    count = 0
    mid = 0
    for k in res[l]['negative']:
        if k >= 0.3:
            mid += k
            count += 1
    if count > 0:
        result[l] = {'negative': {'mid': mid / count, 'cnt': count}}
    else:
        result[l] = {'negative': {'mid': mid, 'cnt': count}}
    count = 0
    mid = 0
    for k in res[l]['positive']:
        if k >= 0.3:
            mid += k
            count += 1
    if count > 0:
        result[l]['positive'] = {'mid': mid / count, 'cnt': count}
    else:
        result[l]['positive'] = {'mid': mid, 'cnt': count}
    count = 0
    mid = 0
    for k in res[l]['neutral']:
        if k > 0:
            mid += k
            count += 1
    if count > 0:
        result[l]['neutral'] = {'mid': mid / count, 'cnt': count}
    else:
        result[l]['neutral'] = {'mid': mid, 'cnt': count}

print(result)
