import json

DATA_HOUR={}
DATA_DAYS={}
DATA_ALL_HOURS={}
WEEKDAYS=["Понеделник","Вторник","Сряда","Четвъртък","Петък","Събота","Неделя"]
with open("data_hours.json","r",encoding="utf-8") as file:
    data=json.load(file)
    i=1
    for day in WEEKDAYS:
        DATA_HOUR[day]=[int(data[k][i]) for k in range(1,len(data)-1)]
        i+=3
        DATA_DAYS['ден']=WEEKDAYS
        DATA_DAYS["Брой ПТП"]=[int(data[-1][j]) for j in range(1,22,3)]
        DATA_DAYS["Ранени"]=[int(data[-1][j]) for j in range(3,22,3)]
        DATA_DAYS["Загинали"]=[int(data[-1][j]) for j in range(2,22,3)]

    DATA_ALL_HOURS["час"]=[data[k][0] for k in range(1,len(data)-1)]
    for i in range(3):
        DATA_ALL_HOURS[data[0][-3+i]]=[int(data[k][-3+i]) for k in range(1,len(data)-1)]
        


print(DATA_ALL_HOURS) 
#print(type(DATA_DAYS["Загинали"][2]))