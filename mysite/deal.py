f=open("table1.txt","r")
f2=open("table2.txt","w")
d=dict()
for line in f:
    row=line.strip().split('\t')
    key=(row[1].strip(),row[2].strip())
    value=row[0].strip()
    if value=='1':
        d[key]=value
    if value=='-1':
        if d.has_key(key) and d[key]=='1':
            None
        else:
            d[key]=value

for item in d.items():
    print >> f2, item[1],item[0][0],item[0][1]
