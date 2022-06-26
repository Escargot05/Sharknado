import xlrd
import mysql.connector
import utils

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
    pass

def insertCircumstancesDimension():
    pass

def insertVictimDimension():
    pass

def insertFactAttacks():
    pass


if __name__ == '__main__':

    insertSharkDimension()

