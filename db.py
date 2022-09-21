# DB
def connect(hostName, userName, password, databaseName, table):
    db = mysql.connector.connect(host=hostName, user=userName, passwd=password, database=databaseName)
    cursor = db.cursor()