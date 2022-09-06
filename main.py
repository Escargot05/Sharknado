import xlrd
import mysql.connector
from dateutil import parser

import sharkDim
import victimDim

# Opening Excell file
book = xlrd.open_workbook("GSAF5.xls")
source = book.sheet_by_index(0)

# SQL connector
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "sharkdb"
)

mycursor = mydb.cursor()

# Count records in database
def countRecords():
    mycursor.execute("SELECT COUNT(*) FROM fact_attacks")
    recordsNumnber = mycursor.fetchone()

    return int(recordsNumnber[0])

# Count valid records in Excel file
def countAttacks():
    validRecords = 0

    for i in range(1, source.nrows):
        if(source.cell_value(rowx = i, colx = 3) == 'Unprovoked' or 
        source.cell_value(rowx = i, colx = 3) == 'Provoked' or
        source.cell_value(rowx = i, colx = 3) == 'Watercraft'):
            validRecords += 1

    return validRecords


def insertSharkDimension(recordNumber, sharkList):
    speciesAndSize = source.cell_value(rowx = recordNumber, colx = 14)

    species = sharkDim.determineSpecies(speciesAndSize, sharkList)
    size = sharkDim.determineSize(sharkDim.convertLengthToNumber(speciesAndSize))

    # Check if shark already exists in database
    sql = "SELECT shark_id FROM shark_dimension WHERE size LIKE %s AND species LIKE %s"
    val = size, species
    mycursor.execute(sql, val)
    sharkId = mycursor.fetchone()

    if not sharkId:
        mycursor.execute("SELECT COUNT(*) FROM shark_dimension")
        id = mycursor.fetchone()
        sharkId = int(id[0])
        sharkId += 1

        sql = "INSERT INTO shark_dimension (shark_id, species, size) VALUES (%s, %s, %s)"
        val = sharkId, species, size
        mycursor.execute(sql, val)
        mydb.commit()

        return sharkId
    
    else:
        return int(sharkId[0])


def insertVictimDimension(recordNumber):
    sexRecord = source.cell_value(rowx = recordNumber, colx = 9)
    ageRecord = source.cell_value(rowx = recordNumber, colx = 10)

    sex = victimDim.determineSex(sexRecord)
    age = victimDim.determineAge(ageRecord)

    # Check if victim already exists in database
    sql = "SELECT victim_id FROM victim_dimension WHERE sex LIKE %s AND age LIKE %s"
    val = sex, age
    mycursor.execute(sql, val)
    victimId = mycursor.fetchone()

    if not victimId:
        mycursor.execute("SELECT COUNT(*) FROM victim_dimension")
        id = mycursor.fetchone()
        victimId = int(id[0])
        victimId += 1

        sql = "INSERT INTO victim_dimension (victim_id, sex, age) VALUES (%s, %s, %s)"
        val = victimId, sex, age
        mycursor.execute(sql, val)
        mydb.commit()

        return victimId
    
    else:
        return int(victimId[0])

def insertCircumstancesDimension(recordNumber):
    country = source.cell_value(rowx = recordNumber, colx = 4)
    area = source.cell_value(rowx = recordNumber, colx = 5)
    location = source.cell_value(rowx = recordNumber, colx = 6)
    activity = source.cell_value(rowx = recordNumber, colx = 7)

    if country == "":
        country = "unknown"
    if area == "":
        area = "unknown"
    if location == "":
        location = "unknown"
    if activity == "":
        activity = "unknown"

    # Check if circumstances already exist in database
    sql = "SELECT circumstances_id FROM circumstance_dimension WHERE (activity LIKE %s AND country LIKE %s AND area LIKE %s AND location LIKE %s)"
    val = activity, country, area, location
    mycursor.execute(sql, val)
    circumstanceId = mycursor.fetchone()

    if not circumstanceId:
        mycursor.execute("SELECT COUNT(*) FROM circumstance_dimension")
        id = mycursor.fetchone()
        circumstanceId = int(id[0])
        circumstanceId += 1

        sql = "INSERT INTO circumstance_dimension (circumstances_id, activity, country, area, location) VALUES (%s, %s, %s, %s, %s)"
        val = circumstanceId, activity, country, area, location
        mycursor.execute(sql, val)
        mydb.commit()

        return circumstanceId
    
    else:
        return int(circumstanceId[0])

def insertTimeDimension(records):
    # pass
    for i in range(1, records + 1):
    # wybór komórki
        date = source.cell_value(rowx = i, colx = 1)
        if type(date) == str:
            date = date.replace(" ", "").replace("Reported", "").replace("Before","")
        
            try:
                dayOfWeek = parser.parse(date).strftime("%A")
            except ValueError:
                dayOfWeek = ""
            try:
                day = parser.parse(date).strftime("%d")
            except ValueError:
                day = -1
            try:
                month = parser.parse(date).strftime("%m")
            except ValueError:
                month = -1
            # year = parser.parse(date).strftime("%Y")
        else:
            dayOfWeek = ""
            day = -1
            month = -1
        time = source.cell_value(rowx = i, colx = 13)
        year = source.cell_value(rowx = i, colx = 2)
        if year == "":
            year = -1
        
        sql = "INSERT INTO time_dimension (time_id, day, month, year, day_of_week, time) VALUES (%s, %s, %s, %s, %s, %s)"
        val = i, day, month, year, dayOfWeek, time

        # wykonanie statementa i commit
        mycursor.execute(sql, val)
        mydb.commit()

    print(f"{records} records inserted")

def insertFactAttacks(records):
    for i in range(1, records):
        mType = source.cell_value(rowx = i, colx = 3)
        injury = source.cell_value(rowx = i, colx = 11)
        fatal = source.cell_value(rowx = i, colx = 12)

        sql = "INSERT INTO fact_attacks (case_id, type, injury, fatal, victim_id, time_id, shark_id, circumstances_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = i, mType, injury, fatal, i, i, i, i

        # wykonanie statementa i commit
        mycursor.execute(sql, val)
        mydb.commit()

    print(f"{records} records inserted")

if __name__ == '__main__':

    newRecords = countAttacks() - countRecords()

    if(newRecords):
        sharks = sharkDim.loadSharkList('sharks.txt')

        for i in range(1, newRecords):
            if source.cell_value(rowx = i, colx = 3) != 'Invalid' and source.cell_value(rowx = i, colx = 3) != '':
                    insertSharkDimension(i, sharks)
                    insertVictimDimension(i)
                    insertCircumstancesDimension(i)

        print(f"{newRecords} facts inserted")

    # insertSharkDimension()
    # insertTimeDimension()
    # insertCircumstancesDimension()
    # insertVictimDimension()
