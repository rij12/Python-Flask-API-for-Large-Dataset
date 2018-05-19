import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT



def createDatabase(databaseName):

    conn = psycopg2.connect(dbname="postgres", user="postgres", password="", host="localhost")

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = conn.cursor()
    cur.execute("CREATE DATABASE {};".format(databaseName))
    conn.close()

def createTable(tableName, config):
    pass


createDatabase("hellworld")