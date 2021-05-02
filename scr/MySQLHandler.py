from mysql import connector
import os

class MySQLHandler:

    def __init__(self, host, user, password, database):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database

        self.__connection = None
        self.__cursor = None

        self.__createDataBaseIfNeeded()
        self.__createTableIfNeeded()

    def __createDataBaseIfNeeded(self):
        self.__connectWithoutDatabase()
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute("CREATE DATABASE IF NOT EXISTS BootProjects " +
                              "CHARACTER SET utf8 "+
                              "COLLATE utf8_hungarian_ci;")
        self.__connection.close()

    def __createTableIfNeeded(self):
        self.__connectWithDatabase()
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS BootSavedPaths ("+
                              "filename varchar(30),"+
                              "path varchar(100),"+
                              "ts datetime"+
                              ");")
        self.__connection.close()

    def __connectWithoutDatabase(self):
        self.__connection = connector.connect(
            host=self.__host,
            user=self.__user,
            password=self.__password,
        )

    def __connectWithDatabase(self):
        self.__connection = connector.connect(
            host=self.__host,
            user=self.__user,
            password=self.__password,
            database=self.__database
        )


    def addFilePath(self, path):
        fileName = path.split("/")[-1]

        self.__connectWithDatabase()
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute("INSERT INTO BootSavedPaths VALUES('"+
                                fileName + "', '"+
                                path +"', "
                                "NOW()"+
                              ")")
        self.__connection.commit()
        self.__connection.close()

    def deleteFilePath(self, path):
        self.__connectWithDatabase()
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute("DELETE FROM BootSavedPaths "+
                              "WHERE path='" + path + "';"
                              )
        self.__connection.commit()
        self.__connection.close()


    def __dropDataBaseTestOnly(self):
        self.__connectWithoutDatabase()
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute("DROP DATABASE BootProjects")
        self.__connection.close()

    def selectAllFromDataBase(self, limit):
        self.__connectWithDatabase()
        self.__cursor = self.__connection.cursor()
        sql = "SELECT filename, path FROM BootSavedPaths ORDER BY ts DESC"
        if limit !="0":
            sql+=" LIMIT "+limit
        self.__cursor.execute(sql)
        results = self.__cursor.fetchall()
        #print(results)
        self.__connection.close()
        return(results)

    def deleteAllWithLimit(self, limit):
        if limit !="0":
            self.__connectWithDatabase()
            self.__cursor = self.__connection.cursor()
            self.__cursor.execute("DELETE FROM BootSavedPaths "+
                                  "WHERE ts NOT IN (SELECT * FROM "+
                                  "(SELECT ts FROM BootSavedPaths ORDER BY ts DESC LIMIT "+limit+") as t)"
                                  )
            self.__connection.commit()
            self.__connection.close()
