# Créé par erwan, le 17/12/2022 en Python 3.7
fichier=open('input.txt')

data=[]


separateur = " "
for ligne in fichier :
    ligne = ligne.rstrip()
    liste = ligne.split(separateur)
    a=liste[0]
    if  a!='':
        data.append(int(a))
    else:
        data.append(a)
fichier.close()

max1=0
max2=0
max3=0
current=0
elfe=0

for i in range (len(data)):
    if data[i]!='':
        current+=data[i]
    else:
        elfe+=1
        if current >=max1 :
            max3=max2
            max2=max1
            max1=current
        elif current >=max2 :
            max3=max2
            max2=current
        elif current >=max3 :
            max3=current
        current=0
print(max1+max2+max3)
