import json

DATA_HOUR={}
DATA_DAYS={}
DATA_ALL_HOURS={}
WEEKDAYS=["Понеделник","Вторник","Сряда","Четвъртък","Петък","Събота","Неделя"]

def hour_cleaner(hour):
    hour=hour.replace("От ","")
    hour=hour.replace(" До ",":00-")
    return hour
with open("resources/data_hours.json", "r", encoding="utf-8") as file:
    data=json.load(file)
    i=1
    for day in WEEKDAYS:
        DATA_HOUR[day]=[int(data[k][i]) for k in range(1,len(data)-1)]
        i+=3
        DATA_DAYS['ден']=WEEKDAYS
        DATA_DAYS["Брой ПТП"]=[int(data[-1][j]) for j in range(1,22,3)]
        DATA_DAYS["Ранени"]=[int(data[-1][j]) for j in range(3,22,3)]
        DATA_DAYS["Загинали"]=[int(data[-1][j]) for j in range(2,22,3)]

    DATA_ALL_HOURS["час"]=[hour_cleaner(data[k][0]) for k in range(1,len(data)-1)]
    for i in range(3):
        DATA_ALL_HOURS[data[0][-3+i]]=[int(data[k][-3+i]) for k in range(1,len(data)-1)]
        

def load_json(file_path: str) -> dict:
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)

def get_provinces_GeoJSON() -> dict:
    return load_json("resources/provinces.geojson")
    
def get_nuts3() -> dict:
    return load_json("resources/ek_obl.json")
    
def get_ptp_regions_data() -> dict:
    ptp = load_json("resources/ptp01.01-30.06.2025.json")

    for i in range(1, len(ptp[0])):
        if "разлика" in ptp[0][i].lower():
            ptp[0][i] = ptp[0][i].replace("разлика", "разлика (спрямо миналата година)")
            ptp[0][i] = ptp[0][i].replace("Разлика", "Разлика (спрямо миналата година)")

    return ptp

def get_ptp_regions_data_months() -> dict:
    return load_json("resources/ptp01.01-30.06.2025_months.json")

print(DATA_ALL_HOURS) 
#print(type(DATA_DAYS["Загинали"][2]))