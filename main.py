import xlrd
import mysql.connector
import utils
from dateutil import parser

ROWS = 6762 # tyle mamy rekordow w bazie

book = xlrd.open_workbook("GSAF5.xls")
source = book.sheet_by_index(0)

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "sharkdb"
)
mycursor = mydb.cursor()

def insertSharkDimension():

    for i in range(1, ROWS + 1):
    # wybór komórki
        species = source.cell_value(rowx = i, colx = 14)
        # size = "veri smol"
        size = utils.determineSize(utils.convertToNumber(species))

        sql = "INSERT INTO shark_dimension (shark_id, species, size) VALUES (%s, %s, %s)"
        val = i, species, size
        
        # wykonanie statementa i commit
        mycursor.execute(sql, val)
        mydb.commit()

    print(f"{ROWS} records inserted")


def insertTimeDimension():
    # pass
    for i in range(1, ROWS + 1):
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

    print(f"{ROWS} records inserted")

def insertCircumstancesDimension():
    # pass
    for i in range(1, ROWS + 1):
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

    print(f"{ROWS} records inserted")

def insertVictimDimension():
    # pass
    for i in range(1, ROWS + 1):
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

    print(f"{ROWS} records inserted")

def insertFactAttacks():
    # pass
    for i in range(1, ROWS + 1):
    # wybór komórki
        mType = source.cell_value(rowx = i, colx = 3)
        injury = source.cell_value(rowx = i, colx = 11)
        fatal = source.cell_value(rowx = i, colx = 12)

        sql = "INSERT INTO fact_attacks (case_id, type, injury, fatal, victim_id, time_id, shark_id, circumstances_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = i, mType, injury, fatal, i, i, i, i

        # wykonanie statementa i commit
        mycursor.execute(sql, val)
        mydb.commit()

    print(f"{ROWS} records inserted")

if __name__ == '__main__':

    # insertSharkDimension()
    # insertTimeDimension()
    # insertCircumstancesDimension()
    # insertVictimDimension()
    insertFactAttacks()
