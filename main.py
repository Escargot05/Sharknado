import xlrd
import mysql.connector
import utils
from dateutil import parser

book = xlrd.open_workbook("GSAF5.xls")
source = book.sheet_by_index(0)

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "sharkdb"
)

mycursor = mydb.cursor()

def countRecords():
    mycursor.execute("SELECT COUNT(*) FROM fact_attacks")
    recordsNumnber = mycursor.fetchone()

    return int(recordsNumnber[0])

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
    species = utils.determineSpecies(speciesAndSize, sharkList)
    size = utils.determineSize(utils.convertToNumber(speciesAndSize))

    sql = "SELECT shark_id FROM shark_dimension WHERE size='" + str(size) + "' AND species='" + str(species) + "'"
    mycursor.execute(sql)
    sharkId = mycursor.fetchone()

    if not sharkId:
        sql = "SELECT COUNT(*) FROM shark_dimension"
        mycursor.execute(sql)
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

def insertCircumstancesDimension(records):
    # pass
    for i in range(1, records + 1):
    # wybór komórki
        country = source.cell_value(rowx = i, colx = 4)
        area = source.cell_value(rowx = i, colx = 5)
        location = source.cell_value(rowx = i, colx = 6)
        activity = source.cell_value(rowx = i, colx = 7)

        sql = "INSERT INTO circumstance_dimension (idcircumstances_id, activity, country, area, location) VALUES (%s, %s, %s, %s, %s)"
        val = i, activity, country, area, location

        # wykonanie statementa i commit
        mycursor.execute(sql, val)
        mydb.commit()

    print(f"{records} records inserted")

def insertVictimDimension(records):
    # pass
    for i in range(1, records + 1):
    # wybór komórki
        name = source.cell_value(rowx = i, colx = 8)
        sex = source.cell_value(rowx = i, colx = 9)
        age = source.cell_value(rowx = i, colx = 10)
        if type(age) != float:
            age = -1

        sql = "INSERT INTO victim_dimension (victim_id, name, sex, age) VALUES (%s, %s, %s, %s)"
        val = i, name, sex, age

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
        sharks = utils.loadSharks('sharks.txt')

        for i in range(1, newRecords):
            if(source.cell_value(rowx = i, colx = 3) == 'Unprovoked' or 
                source.cell_value(rowx = i, colx = 3) == 'Provoked' or
                source.cell_value(rowx = i, colx = 3) == 'Watercraft'):
                    insertSharkDimension(i, sharks)
                    # insertFactAttacks()

        print(f"{newRecords} facts inserted")

    # insertSharkDimension()
    # insertTimeDimension()
    # insertCircumstancesDimension()
    # insertVictimDimension()
