import sqlite3
    
def _checkConnDec(func):
    def wrapper(self, *args, **kwargs):
        if not self._connection:
            if not self._database:
                raise NoDatabaseDefinedException
            else:
                self._connection = sqlite3.connect(self._database)
        return func(self, *args, **kwargs)
    return wrapper

class HistoryDBInterface:
    database = None
    def __enter__(self):
        if not HistoryDBInterface.database:
            raise NoDatabaseDefinedException
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self._connection.close()
        finally:
            self._connection = None
            
    def __init__(self):
        self._database = HistoryDBInterface.database
        self._connection = None
    

    def setDatabase(self, dbfile):
        HistoryDBInterface.database = dbfile
        self._database = dbfile
        self._connection = sqlite3.connect(self._database)

    @_checkConnDec
    def getRows(self, script, params = None):
        if params:
            return self._connection.execute(script, params)
        else:
            return self._connection.execute(script)

    @_checkConnDec
    def getOne(self, script, params = None):
        rows = self.getRows(script, params)
        return rows.fetchone()

    @_checkConnDec
    def upsert(self, script, params = None, commitNow = True):
        if params:
            self._connection.execute(script, params)
        else:
            self._connection.execute(script)
        if commitNow:
            self._connection.commit()

    @_checkConnDec
    def commit(self):
        self._connection.commit()
