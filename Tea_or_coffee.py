import csv

#Функция получения данных из базы и преобразования их в список
def processing_cvs(DataBaseName):
    with open(DataBaseName, newline='') as csvfile:
        dataBase = list(csv.DictReader(csvfile, delimiter=','))
    return dataBase


#Функция удаления данных из базы
def deleting_el(strList, dataBase):
    for row in dataBase:
        for key in strList:
            del row[key]
    return dataBase


#Функция преобразования строчных данных в числовые
def type_conversion_dataBase(strDict, row):
    for key in strDict:
        row[key] = strDict[key](row[key])
    return row


#Функция нормализации одномерных показателей
def linear_normalization(dataBase, params, person):
    for param in params:
        maxValue = max(dataBase, key=lambda x:x[param])[param]
        minValue = min(dataBase, key=lambda x:x[param])[param]
        person[param] = (person[param] - minValue)/(maxValue - minValue)
        for row in dataBase:
            row[param] = (row[param] - minValue)/(maxValue-minValue)
    return dataBase, person


#Функция вычисления связей между отдельными n-мерными показателями
def volume_normalization (dataBase, person, params):
    volumeDataBase = {}
    for param in params:
        volumeDataBase[param] = []
        for row in dataBase:
            a = 0
            for index, item in enumerate(row[param]):
                a = a + (item-person[param][index])**2
            volumeDataBase[param].append(a**(1/2))
    return volumeDataBase


#Функция преобразования текстового значения округов в числовые списки, где первый элемент - координата по x, второй элемент - координата по y
def district(row):
    if row['Округ']=='СВАО':
        row['Округ']=[2**(1/2)/4, 2**(1/2)/4, 0]
    elif row['Округ']=='ВАО':
        row['Округ']=[0.5, 0, 0]
    elif row['Округ']=='ЮВАО':
        row['Округ']=[2**(1/2)/4, -2**(1/2)/4, 0]
    elif row['Округ']=='ЮАО':
        row['Округ']=[0, -0.5, 0]
    elif row['Округ']=='ЮЗАО':
        row['Округ']=[-2**(1/2)/4, -2**(1/2)/4, 0]
    elif row['Округ']=='ЗАО':
        row['Округ']=[-0.5, 0, 0]
    elif row['Округ']=='СЗАО':
        row['Округ']=[-2**(1/2)/4, 2**(1/2)/4, 0]
    elif row['Округ']=='САО':
        row['Округ']=[0, 0.5, 0]
    elif row['Округ']=='ЦАО':
        row['Округ']=[0, 0, 0]
    else:
        row['Округ']=[0, 0, 1]
    return row


#Функция преобразования цветов в числовой ряд, основываясь на принципе разложения белового света на спектр (черный - последний цвет)
def color(row):
    if row['Любимый цвет']=='Черный':
        row['Любимый цвет']=0
    elif row['Любимый цвет']=='Красный':
        row['Любимый цвет']=1
    elif row['Любимый цвет']=='Оранжевый':
        row['Любимый цвет']=2
    elif row['Любимый цвет']=='Желтый':
        row['Любимый цвет']=3
    elif row['Любимый цвет']=='Зеленый':
        row['Любимый цвет']=4
    elif row['Любимый цвет']=='Голубой':
        row['Любимый цвет']=5
    elif row['Любимый цвет']=='Синий':
        row['Любимый цвет']=6
    elif row['Любимый цвет']=='Фиолетовый':
        row['Любимый цвет']=7
    else:
        row['Любимый цвет']=8
    return row


#Функция преобразования значения знаков зодиака в числовой список
def zodiac_sign(row):
    if row['Знак зодиака']=='Овен':
         row['Знак зодиака']=[0.5, 0]
    elif row['Знак зодиака']=='Телец':
        row['Знак зодиака']=[3**(1/2)/4, 1/4]
    elif row['Знак зодиака']=='Близнецы':
        row['Знак зодиака']=[1/4, 3**(1/2)/4]
    elif row['Знак зодиака']=='Рак':
        row['Знак зодиака']=[0, 0.5]
    elif row['Знак зодиака']=='Лев':
        row['Знак зодиака']=[-1/4, 3**(1/2)/4]
    elif row['Знак зодиака']=='Дева':
        row['Знак зодиака']=[-3**(1/2)/4, 1/4]
    elif row['Знак зодиака']=='Весы':
        row['Знак зодиака']=[-0.5, 0]
    elif row['Знак зодиака']=='Скорпион':
        row['Знак зодиака']=[-3**(1/2)/4, -1/4]
    elif row['Знак зодиака']=='Стрелец':
        row['Знак зодиака']=[-1/4, -3**(1/2)/4]
    elif row['Знак зодиака']=='Козерог':
        row['Знак зодиака']=[0, -0.5]
    elif row['Знак зодиака']=='Водолей':
        row['Знак зодиака']=[1/4, -3**(1/2)/4]
    else:
        row['Знак зодиака']=[3**(1/2)/4, -1/4]
    return row


#Функция получения данных от пользователя
def get_person(dataBase):
    keys = list(clearDataBase[0].keys())
    del keys[-1]
    personData = {}
    for item in keys:
        personData[item] = input("Введите "+item.lower()+": ")
    return personData


#Функция подсчета длины связей
def counting_links(dataBase, person, volumeDataBase, strList, volumeList):
    countingLinks = {}
    for item, row in enumerate(dataBase):
        linkLength = 0
        for el in strList:
            linkLength = linkLength + (dataBase[item][el] - person[el])**2
        for el in volumeList:
            linkLength = linkLength + volumeDataBase[el][item]**2
        countingLinks[item] = linkLength**(1/2)
    return countingLinks


#Функция подсчета результата
def choose_coffee_or_tea(array):
    coffee = array.count('К')
    tea = array.count('Ч')
    return 'coffee' if coffee > tea else 'tea'


dataBase = processing_cvs('Gruppy_22__1_-_01.csv')


clearDataBase = deleting_el(['28.сен', 'ФИО', '№'], dataBase)


for row in clearDataBase:
    row = type_conversion_dataBase({'Продолжительность сна': float, 'Время подъема': float, 'Есть работа': int}, row)
    row = district(row)
    row = color(row)
    row = zodiac_sign(row)


person = get_person(clearDataBase)
person = type_conversion_dataBase({'Продолжительность сна': float, 'Время подъема': float, 'Есть работа': int}, person)
person = district(person)
person = color(person)
person = zodiac_sign(person)


normalizeDataBase, person = linear_normalization(clearDataBase, ['Продолжительность сна', 'Время подъема', 'Любимый цвет'], person)


volumeDataBase = volume_normalization(normalizeDataBase, person, ['Знак зодиака', 'Округ'])


countingLinksBase = counting_links(normalizeDataBase, person, volumeDataBase, ['Продолжительность сна', 'Время подъема', 'Любимый цвет'], ['Знак зодиака', 'Округ'])


sortedCountingLinksBase = dict(sorted(countingLinksBase.items(), key = lambda item: item[1]))


nearestIDs = list(sortedCountingLinksBase.keys())[0:5]


preferences = []
for idd in nearestIDs:
    preferences.append(clearDataBase[idd]['К/Ч'])


print(choose_coffee_or_tea(preferences))
