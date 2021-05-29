from pandas import *
import json

xls1 = ExcelFile("North_Korean_Fossil (Trilobite)_old.xlsx")
xls2 = ExcelFile("North_Korean_Fossil (Brachiopod).xlsx")
df1 = xls1.parse(xls1.sheet_names[1])
df2 = xls2.parse(xls2.sheet_names[1])
occurrence_hash1 = df1.to_dict(orient='records')
occurrence_hash2 = df2.to_dict(orient='records')

occurrence_hash = occurrence_hash1
occurrence_hash.extend( occurrence_hash2 )

json_object = "var nk_fossil_occurrence_data = " + json.dumps(occurrence_hash, indent = 4) + ";"
#print( lat_min, lat_max, lon_min, lon_max )
#print(json_object)

with open("nk_fossil_occurrence_data.js", 'w', newline='', encoding='utf-8') as jsfile:
    jsfile.write(json_object)
jsfile.close()