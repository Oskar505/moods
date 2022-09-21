from dataclasses import replace
from datetime import date
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time
import colorama
from colorama import Fore, Back, Style
import mysql.connector
import datetime as dt
import os
import pyautogui





# COLOR

colorama.init()

# VARIABLES

weatherBad = False
weatherOk = False
weatherGood = False
weatherStatus = ''
weatherPoints = 0

dayGood = False
dayBad = False
dayStatus = ''
dayPoints = 0

assumedMood = 5
grade = ''
gradesList = []
gradesAv = 0


def normalVariables():
    global assumedMood
    global grade
    global gradesList
    global gradesAv
    global weekend
    global gradesBad
    global gradesOk
    global gradesGood
    global gradesNone
    global sleepBad
    global sleepOk
    global sleepGood
    global sportBad
    global sportWalk
    global sportRun
    global sportBike
    global sportWorkout
    global gradesStatus
    global sleepStatus
    global sportStatus
    global gradesPoints
    global sleepPoints
    global sportPoints


    assumedMood = 5
    grade = ''
    gradesList = []
    gradesAv = 0
    weekend = False

    gradesBad = False
    gradesOk = False
    gradesGood = False
    gradesNone = False


    sleepBad = False
    sleepOk = False
    sleepGood = False

    sportBad = False
    sportWalk = False
    sportRun = False
    sportBike = False
    sportWorkout = False


    gradesStatus = ''
    sleepStatus = ''
    sportStatus = ''


    gradesPoints = 0
    sleepPoints = 0
    sportPoints = 0


# FUNCTIONS

def average(list):
    listLen = len(list)
    listSum = sum(list)
    
    return listSum / listLen


# WEATHER

# scraping


url = 'https://pocasi.seznam.cz/misto/jihomoravsky-kraj-regi_14?lat=49.261&lon=17.018&z=6'

uClient = uReq(url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, 'html.parser')

temp = page_soup.findAll('span', {'class':'e_cp'})[0].text
temp = float(temp.replace('°C', ''))
temp = round(temp)
weather = page_soup.findAll('div', {'class':'e_cr'})[0].text
rain = page_soup.findAll('div', {'class':'e_cx'})[2].text
rain = float(rain.replace(' mm', ''))


print(temp, rain, weather)

# points

if rain < 0.5 and temp >= 0:
    if weather == 'Zataženo':
        weatherPoints = -0.5
        assumedMood = assumedMood + weatherPoints
        weatherBad = True
    
    elif weather == 'Oblačno':
        weatherPoints = -0.5
        assumedMood = assumedMood + weatherPoints
        weatherBad = True

    elif weather == 'Mlha':
        weatherPoints = -1
        assumedMood = assumedMood + weatherPoints
        weatherBad = True
    
    elif weather == 'Skoro zataženo':
        weatherPoints = 0
        assumedMood = assumedMood + weatherPoints
        weatherOk = True
    
    elif weather == 'Skoro jasno':
        weatherPoints = 1
        assumedMood = assumedMood + weatherPoints
        weatherGood = True

    elif weather == 'Jasno':
        weatherPoints = 1
        assumedMood = assumedMood + weatherPoints
        weatherGood = True
    
    else:
        print(Fore.RED + 'Weather error 1')
        print(Style.RESET_ALL)

elif rain < 0.5 and temp < 0 and weather != 'Zataženo sníh':
    if weather == 'Zataženo':
        weatherPoints = -1
        assumedMood = assumedMood + weatherPoints
        weatherBad = True
    
    elif weather == 'Oblačno':
        weatherPoints = -1
        assumedMood = assumedMood + weatherPoints
        weatherBad = True

    elif weather == 'Mlha':
        weatherPoints = -1
        assumedMood = assumedMood + weatherPoints
        weatherBad = True
    
    elif weather == 'Skoro zataženo':
        weatherPoints = - 0.5
        assumedMood = assumedMood + weatherPoints
        weatherBad = True
    
    elif weather == 'Skoro jasno':
        weatherPoints = 0.5
        assumedMood = assumedMood + weatherPoints
        weatherGood = True

    elif weather == 'Jasno':
        weatherPoints = 1
        assumedMood = assumedMood + weatherPoints
        weatherGood = True
    
    else:
        print(Fore.RED + 'Weather error 2')
        print(Style.RESET_ALL)

elif rain > 0.4 and temp >= 0 and weather != 'Zataženo':
    weatherPoints = -1.5
    assumedMood = assumedMood + weatherPoints
    weatherBad = True

elif weather == 'Zataženo vlhký sníh':
    weatherPoints = 1
    assumedMood = assumedMood + weatherPoints
    weatherGood = True

elif weather == 'Oblačno vlhký sníh':
    weatherPoints = 1
    assumedMood = assumedMood + weatherPoints
    weatherGood = True

elif weather == 'Zataženo déšť sníh':
    weatherPoints = -1.5
    assumedMood = assumedMood + weatherPoints
    weatherGood = True

elif 'sníh' in weather:
    weatherPoints = 2
    assumedMood = assumedMood + weatherPoints
    weatherGood = True

elif weather == 'Zataženo' and rain > 0.4 and temp >= 0:
    weatherPoints = -2
    assumedMood = assumedMood + weatherPoints
    weatherBad = True

else:
    print(Fore.RED + 'Weather error 3')
    print(Style.RESET_ALL)



# DATE

time_now = time.localtime()
currentDate = str(time_now.tm_mday)

# scraping


url = 'https://kalendar.beda.cz/'

uClient = uReq(url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, 'html.parser')

try:
    holiday = page_soup.findAll('td', {'class':'holiday current'})[0].text

except IndexError:
    dayPoints = 0
    dayBad = True
    holiday = ''


if currentDate in holiday:
    dayPoints = 1
    assumedMood = assumedMood + dayPoints
    dayGood = True



# GRADES

# Oskar

def gradesPointsCalc():

    global assumedMood
    global gradesGood
    global gradesOk
    global gradesBad
    global gradesNone
    global gradesPoints

    if gradesAv == 1:
        gradesPoints = 1
        assumedMood = assumedMood + gradesPoints
        gradesGood = True

    elif gradesAv == 2:
        gradesPoints = 0
        assumedMood = assumedMood + gradesPoints
        gradesOk = True

    elif gradesAv == 3:
        gradesPoints = -1
        assumedMood = assumedMood + gradesPoints
        gradesBad = True

    elif gradesAv == 4:
        gradesPoints = -2
        assumedMood = assumedMood + gradesPoints
        gradesBad = True

    elif gradesAv == 5:
        gradesPoints = -3
        assumedMood = assumedMood + gradesPoints
        gradesBad = True

    elif gradesAv == 0:
        gradesPoints = 0
        assumedMood = assumedMood + gradesPoints
        gradesNone = True

    else:
        print(Fore.RED + 'Grades error')
        print(Style.RESET_ALL)

# girls

def gradesPointsCalcGirls():

    global assumedMood
    global gradesGood
    global gradesBad
    global gradesNone
    global gradesPoints


    if gradesAv == 1:
        gradesPoints = 1
        assumedMood = assumedMood + gradesPoints
        gradesGood = True

    elif gradesAv == 2:
        gradesPoints = -1
        assumedMood = assumedMood + gradesPoints
        gradesBad = True

    elif gradesAv == 3:
        gradesPoints = -2
        assumedMood = assumedMood + gradesPoints
        gradesBad = True

    elif gradesAv == 4:
        gradesPoints = -3
        assumedMood = assumedMood + gradesPoints
        gradesBad = True

    elif gradesAv == 5:
        gradesPoints = -4
        assumedMood = assumedMood + gradesPoints
        gradesBad = True

    elif gradesAv == 0:
        gradesPoints = 0
        assumedMood = assumedMood + gradesPoints
        gradesNone = True

    else:
        print(Fore.RED + 'Grades error')
        print(Style.RESET_ALL)


# SLEEP

# Oskar

def sleepPointsCalcOsk():

    global assumedMood
    global sleepBad
    global sleepOk
    global sleepGood
    global sleepPoints
    global sleep

    if 'a' in sleep:
        sleep = sleep.replace('a', '')
        sleep = int(sleep)
        sleep = sleep -2

    else:
        sleep = int(sleep)


    if sleep < 6:
        sleepPoints = -4
        assumedMood = assumedMood + sleepPoints
        sleepBad = True

    elif sleep >= 6 and sleep < 7:
        sleepPoints = -2
        assumedMood = assumedMood + sleepPoints
        sleepBad = True

    elif sleep >= 7 and sleep < 8:
        sleepPoints = -0.5
        assumedMood = assumedMood + sleepPoints
        sleepOk = True

    elif sleep >= 8 and sleep < 9:
        sleepPoints = 0.5
        assumedMood = assumedMood + sleepPoints
        sleepGood = True

    elif sleep >= 9 and sleep < 10:
        sleepPoints = + 0.5
        assumedMood = assumedMood + sleepPoints
        sleepGood = True
        print(sleepGood)

    elif sleep >= 10 and sleep < 24:
        sleepPoints = 2
        assumedMood = assumedMood + sleepPoints
        sleepGood = True

    else:
        print(Fore.RED + 'Sleep error')
        print(Style.RESET_ALL)



# Adult

def sleepPointsCalcAdult():

    global assumedMood
    global sleepBad
    global sleepOk
    global sleepGood
    global sleepPoints

    if sleep < 6:
        sleepPoints = -3
        assumedMood = assumedMood + sleepPoints
        sleepBad = True

    elif sleep >= 6 and sleep < 7:
        sleepPoints = -1
        assumedMood = assumedMood + sleepPoints
        sleepBad = True

    elif sleep >= 7 and sleep < 8:
        sleepPoints = 0
        assumedMood = assumedMood + sleepPoints
        sleepOk = True

    elif sleep >= 8 and sleep < 9:
        sleepPoints = 1
        assumedMood = assumedMood + sleepPoints
        sleepGood = True

    elif sleep >= 9 and sleep < 10:
        sleepPoints = + 2
        assumedMood = assumedMood + sleepPoints
        sleepGood = True
        print(sleepGood)

    elif sleep >= 10 and sleep < 24:
        sleepPoints = 2
        assumedMood = assumedMood + sleepPoints
        sleepGood = True

    else:
        print(Fore.RED + 'Sleep error')
        print(Style.RESET_ALL)



# girls

def sleepPointsCalcGirls():

    global assumedMood
    global sleepBad
    global sleepOk
    global sleepGood
    global sleepPoints

    if sleep < 6:
        sleepPoints = -8
        assumedMood = assumedMood + sleepPoints
        sleepBad = True

    elif sleep >= 6 and sleep < 7:
        sleepPoints = -6
        assumedMood = assumedMood + sleepPoints
        sleepBad = True

    elif sleep >= 7 and sleep < 8:
        sleepPoints = -3
        assumedMood = assumedMood + sleepPoints
        sleepBad = True

    elif sleep >= 8 and sleep < 9:
        sleepPoints = -1
        assumedMood = assumedMood + sleepPoints
        sleepBad = True

    elif sleep >= 9 and sleep < 10:
        sleepPoints = 0.5
        assumedMood = assumedMood + sleepPoints
        sleepOk = True

    elif sleep >= 10 and sleep < 11:
        sleepPoints = 1
        assumedMood = assumedMood + sleepPoints
        sleepGood = True

    elif sleep >= 11 and sleep < 12:
        sleepPoints = 2
        assumedMood = assumedMood + sleepPoints
        sleepGood = True


    elif sleep >= 12 and sleep < 24:
        sleepPoints = 3
        assumedMood = assumedMood + sleepPoints
        sleepGood = True


    else:
        print(Fore.RED + 'Sleep error')
        print(Style.RESET_ALL)


# SPORT

def sportPointsCalc():

    global assumedMood
    global sportBike
    global sportRun
    global sportWalk
    global sportWorkout
    global sportBad
    global sportPoints

    if sport == 'kolo':
        sportPoints = 2
        assumedMood = assumedMood + sportPoints
        sportBike = True

    elif sport == 'běh':
        sportPoints = 1
        assumedMood = assumedMood + sportPoints
        sportRun = True

    elif sport == 'chůze':
        sportPoints = 1
        assumedMood = assumedMood + sportPoints
        sportWalk = True

    elif sport == 'workout':
        sportPoints = 1
        assumedMood = assumedMood + sportPoints
        sportWorkout = True

    else:
        sportBad = True


# PRINT DATA function

def printData():
    global weatherStatus
    global dayStatus
    global gradesStatus
    global sleepStatus
    global sportStatus
    global mood

    mood = input('Jakou máš dnes náladu? ')    # nálada

    print('Tvoje předpokládaná nálada je', assumedMood)
    print('Tvoje nálada je', mood)
    print('Body za počasí ', weatherPoints, ', Body za známky ', gradesPoints, ', body za den ', dayPoints, ', body za spánek ', sleepPoints, ', body za sport ', sportPoints)
    print(Style.RESET_ALL)

    # bad
    print(Fore.RED)

    if weatherBad == True:
        print('Počasí je špatné.')
        weatherStatus = 'Bad'

    if dayBad == True:
        print('Dnes není víkend.')
        dayStatus = 'Bad'

    if gradesBad == True:
        print('Dnes jsi dostal/a špatné známky.')
        gradesStatus = 'Bad'

    if sleepBad == True:
        print('Dnes jsi spal/a málo.')
        sleepStatus = 'Bad'

    if sportBad == True:
        print('Dnes jsi nesportoval/a.')
        sportStatus = 'Bad'

    print(Style.RESET_ALL)

    # ok

    if weatherOk == True:
        print(Fore.YELLOW + 'Počasí je ok.')
        weatherStatus = 'Ok'

    if gradesOk == True:
        print(Fore.YELLOW + 'Dnes jsi dostal/a ok známky.')
        gradesStatus = 'Ok'
        
    if sleepOk == True:
        print(Fore.YELLOW +'Dnes jsi spal/a vpohodě.')
        sleepStatus = 'Ok'

    print(Style.RESET_ALL)


    # good

    if weatherGood == True:
        print(Fore.LIGHTGREEN_EX + 'Počasí je dobré.')
        weatherStatus = 'Good'

    if dayGood == True:
        print(Fore.LIGHTGREEN_EX + 'Dnes je víkend.')
        dayStatus = 'Good'

    if gradesGood == True:
        print(Fore.LIGHTGREEN_EX + 'Dnes jsi dostal/a dobré známky.')
        gradesStatus = 'Good'

    if sleepGood == True:
        print(Fore.LIGHTGREEN_EX + 'Dnes jsi spal/a dobře.')
        sleepStatus = 'Good'

    if sportBike == True:
        print(Fore.LIGHTGREEN_EX + 'Dnes jsi jel/a na kole.')
        sportStatus = 'Good bike'

    if sportRun == True:
        print(Fore.LIGHTGREEN_EX + 'Dnes jsi byl/a běhat.')
        sportStatus = 'Good run'

    if sportWalk == True:
        print(Fore.LIGHTGREEN_EX + 'Dnes jsi se byl/a projít.')
        sportStatus = 'Good walk'

    if sportWalk == True:
        print(Fore.LIGHTGREEN_EX + 'Dnes jsi dělal/a workout.')
        sportStatus = 'Good workout'

    print(Style.RESET_ALL)

    # none

    if gradesNone == True:
        print(Fore.GREEN + 'Dnes jsi nedostal/a žádné známky.')
        gradesStatus = 'none'

    print(Style.RESET_ALL)


#start xampp

os.chdir('C:\\xampp\\')
os.startfile("xampp-control")           
time.sleep(1)
pyautogui.click(583,528)
pyautogui.click(586,562)
time.sleep(0.3)
pyautogui.hotkey('Alt', 'Tab')
time.sleep(0.3)



members = input('Zadej členy na které nechceš odpověděť (použij dvě první písmena ze jména, malým, krátce): ')


#______________________________________________________________#
#OSKAR

if 'os' not in members:
    normalVariables()

    # GET DATA

    print(Fore.BLUE + 'Oskar')
    print(Style.RESET_ALL)

    while grade != 'a':   # známky
        grade = input('Jaké jsi dnes dostal známky? ')
        
        if grade == '1' or grade == '2' or grade == '3' or grade == '4' or grade == '5':
            grade = int(grade)
            gradesList.append(grade)
            gradesAv = average(gradesList)
            gradesAv = round(gradesAv)
        
        elif grade == 'a':
            1+1
        else:
            print('Tuto známku neznám')

    sleep = input('Jak dlouho jsi dnes spal? ')
    sport = input('Sportoval jsi dnes? ')


    # CALCULATE

    gradesPointsCalc()
    
    sleepPointsCalcOsk()

    sportPointsCalc()

    # PRINT DATA

    printData()

    # DATA TO DB

    # connect
    db = mysql.connector.connect(host='localhost', user='root', passwd='', database='moods')
    cursor = db.cursor()

    # getting date
    dateNow = dt.date.today()

    # inserting data
    cursor.execute("INSERT INTO oskar (id, date, assumedMood, userMood, weather, day, grades, sleep, sport) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", ('', dateNow, assumedMood, mood, weatherStatus, dayStatus, gradesStatus, sleepStatus, sportStatus))
    db.commit()



#________________________________________________________#
# SARA

if 'sa' not in members:

    normalVariables()

    # GET DATA
    print(Fore.BLUE + 'Sára')
    print(Style.RESET_ALL)

    grade = ''
    assumedMood = 5

    while grade != 'a':   # známky
        grade = input('Jaké jsi dnes dostal/a známky? ')
        
        if grade == '1' or grade == '2' or grade == '3' or grade == '4' or grade == '5':
            grade = int(grade)
            gradesList.append(grade)
            gradesAv = average(gradesList)
            gradesAv = round(gradesAv)
        
        elif grade == 'a':
            1+1
        else:
            print('Tuto známku neznám')

    sleep = int(input('Jak dlouho jsi dnes spal/a? '))
    sport = input('Sportoval/a jsi dnes? ')


    # CALCULATE

    gradesPointsCalcGirls()
    sleepPointsCalcGirls()
    sportPointsCalc()


    # PRINT DATA

    printData()


    # DATA TO DB

    #connect
    db = mysql.connector.connect(host='localhost', user='root', passwd='', database='moods')
    cursor = db.cursor()

    # getting date
    dateNow = dt.date.today()

    # inserting data
    cursor.execute("INSERT INTO sara (id, date, assumedMood, userMood, weather, day, grades, sleep, sport) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", ('', dateNow, assumedMood, mood, weatherStatus, dayStatus, gradesStatus, sleepStatus, sportStatus))
    db.commit()

    # INSERT INTO DB TURN ON



#________________________________________________________#
# SOFCA

if 'so' not in members:

    normalVariables()

    # GET DATA
    print(Fore.BLUE + 'Sofča')
    print(Style.RESET_ALL)

    grade = ''
    assumedMood = 5

    while grade != 'a':   # známky
        grade = input('Jaké jsi dnes dostal/a známky? ')
        
        if grade == '1' or grade == '2' or grade == '3' or grade == '4' or grade == '5':
            grade = int(grade)
            gradesList.append(grade)
            gradesAv = average(gradesList)
            gradesAv = round(gradesAv)
        
        elif grade == 'a':
            1+1
        else:
            print('Tuto známku neznám')

    sleep = int(input('Jak dlouho jsi dnes spal/a? '))
    sport = input('Sportoval/a jsi dnes? ')


    # CALCULATE

    gradesPointsCalcGirls()
    sleepPointsCalcGirls()
    sportPointsCalc()


    # PRINT DATA

    printData()


    # DATA TO DB

    #connect
    db = mysql.connector.connect(host='localhost', user='root', passwd='', database='moods')
    cursor = db.cursor()

    # getting date
    dateNow = dt.date.today()

    # inserting data
    cursor.execute("INSERT INTO sofca (id, date, assumedMood, userMood, weather, day, grades, sleep, sport) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", ('', dateNow, assumedMood, mood, weatherStatus, dayStatus, gradesStatus, sleepStatus, sportStatus))
    db.commit()

    # INSERT INTO DB TURN ON



#________________________________________________________#
# KLARA


if 'kl' not in members:

    normalVariables()

    # GET DATA
    print(Fore.BLUE + 'Klára')
    print(Style.RESET_ALL)

    grade = ''
    assumedMood = 5

    while grade != 'a':   # známky
        grade = input('Jaké jsi dnes dostal/a známky? ')
        
        if grade == '1' or grade == '2' or grade == '3' or grade == '4' or grade == '5':
            grade = int(grade)
            gradesList.append(grade)
            gradesAv = average(gradesList)
            gradesAv = round(gradesAv)
        
        elif grade == 'a':
            1+1
        else:
            print('Tuto známku neznám')

    sleep = int(input('Jak dlouho jsi dnes spal/a? '))
    sport = input('Sportoval/a jsi dnes? ')


    # CALCULATE

    gradesPointsCalcGirls()
    sleepPointsCalcGirls()
    sportPointsCalc()


    # PRINT DATA

    printData()


    # DATA TO DB

    #connect
    db = mysql.connector.connect(host='localhost', user='root', passwd='', database='moods')
    cursor = db.cursor()

    # getting date
    dateNow = dt.date.today()

    # inserting data
    cursor.execute("INSERT INTO klara (id, date, assumedMood, userMood, weather, day, grades, sleep, sport) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", ('', dateNow, assumedMood, mood, weatherStatus, dayStatus, gradesStatus, sleepStatus, sportStatus))
    db.commit()

    # INSERT INTO DB TURN ON


#_________________________________________#
# Máma

if 'ma' not in members:

    normalVariables()


    # GET DATA
    print(Fore.BLUE + 'Máma')
    print(Style.RESET_ALL)

    grade = ''
    sleep = int(input('Jak dlouho jsi dnes spal/a? '))
    sport = input('Sportoval/a jsi dnes? ')


    # CALCULATE

    sleepPointsCalcAdult()
    sportPointsCalc()


    # PRINT DATA

    printData()


    # DATA TO DB

    #connect
    db = mysql.connector.connect(host='localhost', user='root', passwd='', database='moods')
    cursor = db.cursor()

    # getting date
    dateNow = dt.date.today()

    # inserting data
    cursor.execute("INSERT INTO mama (id, date, assumedMood, userMood, weather, day, grades, sleep, sport) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", ('', dateNow, assumedMood, mood, weatherStatus, dayStatus, gradesStatus, sleepStatus, sportStatus))
    db.commit()

    # INSERT INTO DB TURN ON


#_________________________________________#
# Tata

normalVariables()

if 'ta' not in members:

    # GET DATA
    print(Fore.BLUE + 'Táta')
    print(Style.RESET_ALL)

    grade = ''
    sleep = int(input('Jak dlouho jsi dnes spal/a? '))
    sport = input('Sportoval/a jsi dnes? ')


    # CALCULATE

    sleepPointsCalcAdult()
    sportPointsCalc()


    # PRINT DATA

    printData()


    # DATA TO DB

    #connect
    db = mysql.connector.connect(host='localhost', user='root', passwd='', database='moods')
    cursor = db.cursor()

    # getting date
    dateNow = dt.date.today()

    # inserting data
    cursor.execute("INSERT INTO tata (id, date, assumedMood, userMood, weather, day, grades, sleep, sport) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", ('', dateNow, assumedMood, mood, weatherStatus, dayStatus, gradesStatus, sleepStatus, sportStatus))
    db.commit()

    # INSERT INTO DB TURN ON