import pandas
import numpy
import mysql.connector


def youthScore(year):
    if year == 'Fr.':
        return 20
    elif year =='So.':
        return 5
    elif year == 'Jr.':
        return 0
    else:
        return -5

def heightScore(height):
    if height in ('7-5','7-4','7-3', '7-2'):
        return 20
    elif height in ('7-1', '7-0', '6-11'):
        return 18
    elif height in ('6-10', '6-9'):
        return 16
    elif height in ('6-8'):
        return 14
    elif height in ('6-7'):
        return 12
    elif height in ('6-6'):
        return 10
    elif height in ('6-5'):
        return 8
    elif height in ('6-4'):
        return 5
    elif height in ('6-3'):
        return 3
    elif height in ('6-2'):
        return 2
    elif height in ('6-1'):
        return 1
    else:
        return 0
    
ppgIndex = 4
mpgIndex = 3
fgmIndex = 5
fgaIndex=6
fgpIndex=7
tpmIndex = 8
tpaIndex=9
tppIndex=10
ftpIndex=13
orbIndex=14
drbIndex=15
rpgIndex=16
apgIndex=17
spgIndex=18
bpgIndex=19
tovIndex=20


mydb = mysql.connector.connect(

    host = 'localhost',
    user = 'root',
    password = 'Apple300!',
    database = 'nbaplayerdb'
)
playerscores = []

mycursor = mydb.cursor(buffered=True)
agecursor = mydb.cursor(buffered=True)
mycursor.execute("SELECT * FROM players WHERE PNAME='paolo vanchero'")
for x in mycursor:
    hands = (x[spgIndex]-1.1) * 8 + 7.5
    if hands < 0:
        hands = 0
    if hands > 15:
        hands =15

    rimProtection = (x[bpgIndex]-.4)
    if rimProtection <= -.2:
        rimProtection = 0
    elif rimProtection <= 0:
        rimProtection = 1
    else:
        rimProtection = rimProtection * 10
    if rimProtection > 15:
        rimProtection = 15
    
    shooting = 1*((x[tppIndex] - .35)* 100)+ (x[tpaIndex] - 3) +   1*(x[ftpIndex] - .7) * 100
    
    if shooting > 17:
        shooting = 17
    if shooting < 0:
        shooting = 0

    rebounding = (x[orbIndex]*3 + x[drbIndex])
    if rebounding > 15:
        rebounding=15

    playmaking = (x[apgIndex] * x[apgIndex]/x[tovIndex])
    if playmaking > 20:
        playmaking =20
    if playmaking < 0:
        playmaking = 0 

    scoring = (x[ppgIndex]*.7)
    if scoring > 17:
        scoring =17
   
    
    print("hands score: ", (hands))
    print("rim protection: ", (rimProtection))
    print("shooting: ", (shooting))
    print(x[tppIndex], x[tpaIndex], x[ftpIndex])
    print("rebounding: ", (rebounding))
    print("playmaking: ", (playmaking))
    print("scoring: ", (scoring))
    name = x[0]
    agestmt = f"SELECT * FROM 2023ageheight WHERE PNAME='{name}'"
    agecursor.execute(agestmt)
    youth = 0
    tall = 0
    for ppl in agecursor:
        youth = youthScore(ppl[1])
        tall = heightScore(ppl[2])
    print(ppl[2], ppl[1])    
    print("height score: ", (tall))
    print("youth score: ", (youth))
    sum = hands + rimProtection + shooting + rebounding + playmaking + scoring + youth + tall
    if sum >0:
        playerscores.append(x[0] + ", " + str(int(sum)))
    

for i in playerscores:
    print(i)


mydb.close()