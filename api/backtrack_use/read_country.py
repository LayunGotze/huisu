import xlrd
data=xlrd.open_workbook('国家名.xlsx')
table=data.sheets()[0]
name=table.col_values(1)
country=table.col_values(5)
print(len(country))
dict={}
for i in range(1,248):
    dict[name[i]]=country[i]
print(dict)