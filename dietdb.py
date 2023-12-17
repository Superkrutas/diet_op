import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '123',

)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE dietdb")

print("DONE!")