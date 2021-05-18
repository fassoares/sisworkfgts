import mysql.connector as msql
from mysql.connector import Error
import csv
try:
    conn = msql.connect(host='localhost', user='chico',password='chic@oSQL2020', database ='bd_acaofgts',
                              auth_plugin='mysql_native_password',charset='utf8')
    cursor = conn.cursor()
except Error as e:
    print("Error while connecting to MySQL", e)
file = "C:\\Users\\chico\OneDrive\\Documents\\temp\\FGTS Francisco\\indicesinpc.csv"
openFile = open(file,'r')
lin=0
with openFile as arq:
    linhas = csv.DictReader(arq,delimiter = ';',fieldnames=['Data','Mes','Ano','indiceJAM3', 'INPC_E','Juros3_E','NovoIndice_E'])
    linhas.__next__()
    for linha in linhas: 
        lin+=1
        a1=linha['Data'].strip()
        a2=linha['Mes'].strip()
        a3=linha["Ano"].strip()
        a4=float(linha['indiceJAM3'].replace(',', '.').strip())
        a5=float(linha['INPC_E'].replace(',', '.').strip())
        a6=float(linha['Juros3_E'].replace(',', '.').strip())
        a7=float(linha['NovoIndice_E'].replace(',', '.').strip())
        print(a1)
        print(a2)
        print(a3)
        print(a4)
        print(a5)
        print(a6)
        print(a7)
        cursor.execute("INSERT INTO indiceinpc (mes,ano,IndiceJAM3,indiceINPC,juros3,novoindice) \
                    VALUES ( %s, %s, %s, %s, %s, %s)",(a2,a3,a4,a5,a6,a7))
        conn.commit()


print(lin)
openFile.close()
conn.close()