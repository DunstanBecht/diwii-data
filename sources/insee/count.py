fd = open('StockEtablissement.csv', 'r', encoding='utf8')
n = 0
line = fd.readline()
while line :
    line = fd.readline()
    n += 1

print(n)
input('')
